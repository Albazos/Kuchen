# pyright: reportGeneralClassIssues=false, reportAttributeAccessIssue=false
# type: ignore
#
# Standalone version — uses only Python standard library (no pip install needed).
# Replaces: requests, beautifulsoup4, lxml, python-dateutil, pandas, webdavclient3
#
import http.cookiejar
import urllib.request
import urllib.parse
import urllib.error
import ssl
import base64
import logging
import re
from logging.handlers import RotatingFileHandler
from html.parser import HTMLParser as _StdHTMLParser
import xml.etree.ElementTree as ET
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import StringIO, BytesIO
from datetime import datetime
import os
import json
from typing import TypedDict, Literal, Union, Optional, Dict


# ---------------------------------------------------------------------------
# Minimal HTML DOM (replaces BeautifulSoup + lxml)
# ---------------------------------------------------------------------------

class _HTMLNode:
    """Lightweight DOM node built by _HTMLTreeBuilder."""

    def __init__(self, tag=None, attrs=None, parent=None):
        self.tag = tag
        self.attrs = dict(attrs) if attrs else {}
        self.parent = parent
        self.children = []  # list[_HTMLNode | str]

    # --- text helpers ---
    @property
    def text(self):
        return self.get_text()

    def get_text(self, separator=""):
        parts = []
        self._collect_text(parts)
        return separator.join(parts)

    def _collect_text(self, parts):
        for child in self.children:
            if isinstance(child, str):
                parts.append(child)
            else:
                child._collect_text(parts)

    # --- child access ---
    @property
    def contents(self):
        return list(self.children)

    def __iter__(self):
        return iter(self.children)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.children[key]
        return self.attrs[key]

    def get(self, key, default=None):
        return self.attrs.get(key, default)

    # --- find / find_all ---
    def find(self, tag=None, attrs=None, **kwargs):
        attrs = dict(attrs) if attrs else {}
        if "id" in kwargs:
            attrs["id"] = kwargs.pop("id")
        if "class_" in kwargs:
            attrs["class"] = kwargs.pop("class_")
        results = self._find_all_impl(tag, attrs, limit=1)
        return results[0] if results else None

    def find_all(self, tag=None, attrs=None, **kwargs):
        attrs = dict(attrs) if attrs else {}
        if "id" in kwargs:
            attrs["id"] = kwargs.pop("id")
        if "class_" in kwargs:
            attrs["class"] = kwargs.pop("class_")
        return self._find_all_impl(tag, attrs)

    def _matches(self, tag, attrs):
        if tag and self.tag != tag:
            return False
        for k, v in attrs.items():
            node_val = self.attrs.get(k, "")
            if k == "class":
                if v not in node_val.split() and node_val != v:
                    return False
            else:
                if node_val != v:
                    return False
        return True

    def _find_all_impl(self, tag, attrs, limit=None):
        results = []
        for child in self.children:
            if isinstance(child, _HTMLNode):
                if child._matches(tag, attrs):
                    results.append(child)
                    if limit and len(results) >= limit:
                        return results
                remaining = (limit - len(results)) if limit else None
                results.extend(child._find_all_impl(tag, attrs, limit=remaining))
                if limit and len(results) >= limit:
                    return results
        return results

    # --- serialise back to HTML ---
    def __str__(self):
        return self._to_html()

    def _to_html(self):
        if self.tag is None:  # root wrapper
            return "".join(
                c._to_html() if isinstance(c, _HTMLNode) else c for c in self.children
            )
        attrs_str = ""
        for k, v in self.attrs.items():
            attrs_str += f' {k}="{v}"'
        inner = "".join(
            c._to_html() if isinstance(c, _HTMLNode) else c for c in self.children
        )
        _VOID = frozenset(
            ["area", "base", "br", "col", "embed", "hr", "img",
             "input", "link", "meta", "source", "track", "wbr"]
        )
        if self.tag in _VOID:
            return f"<{self.tag}{attrs_str}/>"
        return f"<{self.tag}{attrs_str}>{inner}</{self.tag}>"


class _HTMLTreeBuilder(_StdHTMLParser):
    """Feed HTML and produce an _HTMLNode tree."""

    _VOID = frozenset(
        ["area", "base", "br", "col", "embed", "hr", "img",
         "input", "link", "meta", "source", "track", "wbr"]
    )

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = _HTMLNode()
        self._stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = _HTMLNode(tag=tag, attrs=attrs, parent=self._stack[-1])
        self._stack[-1].children.append(node)
        if tag not in self._VOID:
            self._stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self._stack) - 1, 0, -1):
            if self._stack[i].tag == tag:
                self._stack = self._stack[: i]
                return

    def handle_data(self, data):
        self._stack[-1].children.append(data)


def _parse_html(html_string):
    """Parse *html_string* and return an _HTMLNode root (drop-in for BeautifulSoup)."""
    builder = _HTMLTreeBuilder()
    builder.feed(str(html_string))
    return builder.root


def _simple_xpath(node, xpath):
    """Navigate *node* tree with a *very* limited XPath subset.

    Supports paths like ``/html/body/div/div[2]/ul[1]``.
    Index is 1-based; omitting index means "first child of that tag".
    """
    parts = xpath.strip("/").split("/")
    current = [node]
    for part in parts:
        m = re.match(r"^(\w+)(?:\[(\d+)\])?$", part)
        if not m:
            return []
        tag = m.group(1)
        idx = int(m.group(2)) if m.group(2) else None
        next_nodes = []
        for n in current:
            children_of_tag = [
                c for c in n.children if isinstance(c, _HTMLNode) and c.tag == tag
            ]
            if idx is not None:
                if 0 < idx <= len(children_of_tag):
                    next_nodes.append(children_of_tag[idx - 1])
            elif children_of_tag:
                next_nodes.append(children_of_tag[0])
        current = next_nodes
    return current


# ---------------------------------------------------------------------------
# Minimal HTTP session (replaces requests.Session)
# ---------------------------------------------------------------------------

class _SimpleResponse:
    """Mimics the ``requests.Response`` interface used in this file."""

    def __init__(self, data: bytes, status_code: int, url: str, headers):
        self._data = data
        self.status_code = status_code
        self.url = url
        self.headers = headers

    @property
    def text(self):
        ct = ""
        if hasattr(self.headers, "get"):
            ct = self.headers.get("Content-Type", "") or ""
        charset = "utf-8"
        if "charset=" in ct:
            charset = ct.split("charset=")[-1].split(";")[0].strip()
        return self._data.decode(charset, errors="replace")

    @property
    def content(self):
        return self._data

    def json(self):
        return json.loads(self.text)


class _SimpleSession:
    """Drop-in for ``requests.Session`` – cookie-aware, redirect-following."""

    def __init__(self):
        self._jar = http.cookiejar.CookieJar()
        ctx = ssl.create_default_context()
        self._opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self._jar),
            urllib.request.HTTPSHandler(context=ctx),
        )

    # --- cookie access (self.cookies.get_dict()) ---
    @property
    def cookies(self):
        return self

    def get_dict(self):
        return {c.name: c.value for c in self._jar}

    # --- public API ---
    def get(self, url, headers=None, params=None, allow_redirects=True, cookies=None):
        if params:
            sep = "&" if "?" in url else "?"
            url = url + sep + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, method="GET")
        self._apply(req, headers, cookies, url)
        return self._execute(req, url)

    def post(self, url, headers=None, data=None, params=None, cookies=None, allow_redirects=True):
        if params:
            sep = "&" if "?" in url else "?"
            url = url + sep + urllib.parse.urlencode(params)
        body, ct = self._encode_data(data)
        req = urllib.request.Request(url, data=body, method="POST")
        if ct and not (headers and any(k.lower() == "content-type" for k in headers)):
            req.add_header("Content-Type", ct)
        self._apply(req, headers, cookies, url)
        return self._execute(req, url)

    # --- internals ---
    def _apply(self, req, headers, cookies, url):
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        if cookies:
            self._inject_cookies(url, cookies)

    def _execute(self, req, url):
        try:
            resp = self._opener.open(req)
            return _SimpleResponse(resp.read(), resp.status, resp.url, resp.headers)
        except urllib.error.HTTPError as e:
            data = e.read()
            return _SimpleResponse(data, e.code, url, e.headers)

    @staticmethod
    def _encode_data(data):
        if data is None:
            return None, None
        if isinstance(data, dict):
            parts = []
            for k, v in data.items():
                if isinstance(v, list):
                    for item in v:
                        parts.append((k, str(item)))
                elif v is not None:
                    parts.append((k, str(v)))
                else:
                    parts.append((k, ""))
            return urllib.parse.urlencode(parts).encode("utf-8"), "application/x-www-form-urlencoded"
        if isinstance(data, str):
            return data.encode("utf-8"), None
        if isinstance(data, bytes):
            return data, None
        return None, None

    def _inject_cookies(self, url, cookies):
        parsed = urllib.parse.urlparse(url)
        for name, value in cookies.items():
            c = http.cookiejar.Cookie(
                version=0, name=name, value=value,
                port=None, port_specified=False,
                domain=parsed.hostname, domain_specified=True,
                domain_initial_dot=False,
                path="/", path_specified=True,
                secure=parsed.scheme == "https",
                expires=None, discard=True,
                comment=None, comment_url=None,
                rest={"HttpOnly": None}, rfc2109=False,
            )
            self._jar.set_cookie(c)


# ---------------------------------------------------------------------------
# Flexible date parser (replaces python-dateutil)
# ---------------------------------------------------------------------------

_DATE_FMTS = [
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y %H:%M",
    "%d.%m.%Y",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%d/%m/%Y",
    "%m/%d/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M",
    "%m/%d/%Y",
]


def _parse_date(date_string, yearfirst=False):
    """Parse common date/datetime strings (replaces ``dateutil.parser.parse``)."""
    s = date_string.strip()
    # Normalise "T" separator variants
    s = s.replace("  ", " ")
    fmts = list(_DATE_FMTS)
    if yearfirst:
        # Put year-first formats at front (they already are, but ensure priority)
        pass
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    # Try Python's fromisoformat (handles many ISO-8601 variants in 3.11+)
    try:
        return datetime.fromisoformat(s)
    except (ValueError, AttributeError):
        pass
    raise ValueError(f"Unable to parse date string: {date_string!r}")


# ---------------------------------------------------------------------------
# Minimal WebDAV client (replaces webdavclient3)
# ---------------------------------------------------------------------------

class _SimpleWebDAVClient:
    """Very thin WebDAV wrapper – ``list``, ``download``, ``upload``, ``mkdir``."""

    def __init__(self, options):
        self._hostname = options.get("webdav_hostname", "").rstrip("/")
        self._login = options.get("webdav_login", "")
        self._password = options.get("webdav_password", "")
        self._auth = base64.b64encode(
            f"{self._login}:{self._password}".encode()
        ).decode()
        self._ctx = ssl.create_default_context()

    def _request(self, method, path, data=None, extra_headers=None):
        url = self._hostname + path
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Basic {self._auth}")
        if extra_headers:
            for k, v in extra_headers.items():
                req.add_header(k, v)
        handler = urllib.request.HTTPSHandler(context=self._ctx)
        opener = urllib.request.build_opener(handler)
        return opener.open(req)

    def list(self, path="/"):
        resp = self._request("PROPFIND", path, extra_headers={"Depth": "1"})
        tree = ET.parse(resp)
        root = tree.getroot()
        ns = {"d": "DAV:"}
        items = []
        for r in root.findall(".//d:response", ns):
            href = r.find("d:href", ns)
            if href is not None and href.text:
                items.append(urllib.parse.unquote(href.text))
        return items

    def download(self, remote_path, local_path):
        resp = self._request("GET", remote_path)
        with open(local_path, "wb") as f:
            f.write(resp.read())

    def upload(self, local_path, remote_path):
        with open(local_path, "rb") as f:
            data = f.read()
        self._request("PUT", remote_path, data=data)

    def mkdir(self, path):
        self._request("MKCOL", path)


# ---------------------------------------------------------------------------
# Type definitions (unchanged from original)
# ---------------------------------------------------------------------------

class Recurring(TypedDict, total=False):
    intervalType: Literal["NO", "DAILY", "WEEKDAYS", "WEEKLY", "MONTHLY", "YEARLY"]
    interval: Literal[
        1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
        21,22,23,24,25,26,27,28,29,30,
    ]
    monthDayInMonth: Literal[
        1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
        21,22,23,24,25,26,27,28,29,30,31,
    ]
    monthlyIntervalType: Literal["BYMONTHDAY", "BYDAY"]
    monthInterval: Literal[1, 2, 3, 4, -1]
    monthDay: Literal["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
    recurrenceDays: list[Literal["MO", "TU", "WE", "TH", "FR", "SA", "SU"]]
    endType: Literal["NEVER", "COUNT", "UNTIL"]
    endInterval: Optional[int]
    untilDate: Optional[str]


class CustomDateTime(TypedDict):
    dateTime: str


class Interval(TypedDict):
    days: int
    hours: int
    minutes: int


class CustomInterval(TypedDict):
    interval: Interval
    before: bool


AlarmType = Union[
    Literal["0M", "5M", "15M", "30M", "1H", "2H", "12H", "1D", "2D", "7D"],
    Dict[str, CustomDateTime],
    Dict[str, CustomInterval],
]


# ---------------------------------------------------------------------------
# IServAPI
# ---------------------------------------------------------------------------

class IServAPI:

    # Technical

    def __init__(self, username, password, iserv_url):
        """
        Initializes the credentials and URLs needed for accessing the IServ system.

        :param username: str - The username for the IServ system.
        :param password: str - The password for the IServ system.
        :param iserv_url: str - The URL of the IServ system.
        :return: None
        """
        self.username = username
        self._password = password
        self.iserv_url = iserv_url
        self._session = None
        self._IServSAT = None
        self._IServSATId = None
        self._IServSession = None
        self.__DAVclient = None
        self.__login()

    @staticmethod
    def setup_logging(log_file="app.log"):
        """
        Set up a logger with a rotating file handler.
        """
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler = RotatingFileHandler(
            log_file, maxBytes=1024 * 1024, backupCount=5,
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logging.info("Logging setup successful!")

    def __get_cookies(self):
        # Create a temporary session to extract specific cookies
        session = _SimpleSession()

        login_url = f"https://{self.iserv_url}/iserv/auth/login"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }

        response = session.get(login_url, headers=headers)

        login_data = {"_username": self.username, "_password": self._password}
        response = session.post(login_url, headers=headers, data=login_data)

        home_url = f"https://{self.iserv_url}/iserv/auth/home"
        response = session.get(home_url, headers=headers)

        main_page_url = f"https://{self.iserv_url}/iserv/"
        response = session.get(main_page_url, headers=headers)
        response = session.get(main_page_url, headers=headers)

        cookies = session.cookies.get_dict()
        self._IServSAT = cookies.get("IServSAT")
        self._IServSATId = cookies.get("IServSATId")
        self._IServSession = cookies.get("IServSession")
        logging.info("Cookies extracted successfully!")
        return

    def __login(self):
        """
        Authenticates the user against the IServ server and initiates a session.
        """
        self._session = _SimpleSession()

        try:
            base_response = self._session.get(
                f"https://{self.iserv_url}/iserv/auth/login"
            )

            login_data = {"_username": self.username, "_password": self._password}
            login_response = self._session.post(base_response.url, data=login_data)

            if "Account existiert nicht!" in login_response.text:
                raise ValueError("Account does not exist!")

            if "Anmeldung fehlgeschlagen!" in login_response.text:
                raise ValueError("Login failed! Probably wrong password.")

        except (urllib.error.URLError, OSError) as e:
            raise ConnectionError(f"Error establishing connection: {e}")

        self.__get_cookies()

    # Own account

    def get_own_user_info(self):
        """
        Retrieves the user information from the server.

        Returns:
            dict: A dictionary containing the user information, including the following keys:
                - Groups (dict): A dictionary mapping group names to group URLs.
                - Roles (list): A list of role names.
                - Rights (list): A list of right names.
                - Public_info (dict): A dictionary containing the public information.
        """

        if not self._session:
            raise ValueError("Session is not initialized. Please log in first.")
        try:
            user_info_response = self._session.get(
                f"https://{self.iserv_url}/iserv/profile"
            )

        except Exception as e:
            logging.error(f"Error retrieving user information: {e}")
            raise ValueError("Error retrieving user information")
        user_info = {}
        try:
            personal_information_data_response = self._session.get(
                f"https://{self.iserv_url}/iserv/profile/public/edit#data"
            )
            personal_information_address_response = self._session.get(
                f"https://{self.iserv_url}/iserv/profile/public/edit#address"
            )
            personal_information_contact_response = self._session.get(
                f"https://{self.iserv_url}/iserv/profile/public/edit#contact"
            )
            personal_information_instant_response = self._session.get(
                f"https://{self.iserv_url}/iserv/profile/public/edit#instant"
            )
            personal_information_note_response = self._session.get(
                f"https://{self.iserv_url}/iserv/profile/public/edit#note"
            )
        except Exception as e:
            logging.error(f"Error retrieving user information: {e}")

        root = _parse_html(user_info_response.text)

        # Groups — find via limited XPath
        xpath_expr = "/html/body/div/div[2]/div[3]/div/div/div[2]/div/div/div/div/ul[1]"
        matching_elements = _simple_xpath(root, xpath_expr)

        groups_dict = {}
        for elem in matching_elements:
            a_tags = elem.find_all("a")
            for a_tag in a_tags:
                text = a_tag.get_text()
                href = a_tag["href"]
                groups_dict[text] = href

        logging.info("Got Groups")

        # Roles
        xpath_expr = "/html/body/div/div[2]/div[3]/div/div/div[2]/div/div/div/div/ul[2]"
        matching_elements = _simple_xpath(root, xpath_expr)

        roles_list = []
        for elem in matching_elements:
            li_tags = elem.find_all("li")
            for li_tag in li_tags:
                text = li_tag.get_text()
                roles_list.append(text)

        logging.info("Got Roles")

        # Rights
        xpath_expr = "/html/body/div/div[2]/div[3]/div/div/div[2]/div/div/div/div/ul[3]"
        matching_elements = _simple_xpath(root, xpath_expr)

        rights_list = []
        for elem in matching_elements:
            li_tags = elem.find_all("li")
            for li_tag in li_tags:
                text = li_tag.get_text()
                rights_list.append(text)

        logging.info("Got Rights")

        # Public information:
        public_info_json = {}

        soup = _parse_html(personal_information_data_response.text)

        ids_and_keys = [
            ("publiccontact_title", "title"),
            ("publiccontact_company", "company"),
            ("publiccontact_birthday", "birthday"),
            ("publiccontact_nickname", "nickname"),
            ("publiccontact_class", "class"),
        ]

        for id, key in ids_and_keys:
            try:
                value = soup.find("input", id=id)["value"]
                public_info_json[key] = value
            except (KeyError, TypeError):
                logging.warning(f"No data in {id}")
                public_info_json[key] = ""

        soup = _parse_html(personal_information_address_response.text)

        ids_and_keys = [
            ("publiccontact_street", "street"),
            ("publiccontact_zipcode", "zipcode"),
            ("publiccontact_city", "city"),
            ("publiccontact_country", "country"),
        ]

        for id, key in ids_and_keys:
            try:
                value = soup.find("input", id=id)["value"]
                public_info_json[key] = value
            except (KeyError, TypeError):
                logging.warning(f"No data in {id}")
                public_info_json[key] = ""

        soup = _parse_html(personal_information_instant_response.text)
        ids_and_keys = [
            ("publiccontact_icq", "icq"),
            ("publiccontact_jabber", "jabber"),
            ("publiccontact_msn", "msn"),
            ("publiccontact_skype", "skype"),
        ]

        for id, key in ids_and_keys:
            try:
                value = soup.find("input", id=id)["value"]
                public_info_json[key] = value
            except (KeyError, TypeError):
                logging.warning(f"No data in {id}")
                public_info_json[key] = ""

        soup = _parse_html(personal_information_note_response.text)
        ids_and_keys = [("publiccontact_note", "note")]

        for id, key in ids_and_keys:

            try:
                value = soup.find("textarea", id=id).get_text()

                public_info_json[key] = value
            except (KeyError, TypeError, AttributeError):
                logging.warning(f"No data in {id}")
                public_info_json[key] = ""

        soup = _parse_html(personal_information_contact_response.text)
        ids_and_keys = [
            ("publiccontact_phone", "phone"),
            ("publiccontact_mobilePhone", "mobilePhone"),
            ("publiccontact_fax", "fax"),
            ("publiccontact_mail", "mail"),
            ("publiccontact_homepage", "homepage"),
        ]

        for id, key in ids_and_keys:
            try:
                value = soup.find("input", id=id)["value"]
                public_info_json[key] = value
            except (KeyError, TypeError):
                logging.warning(f"No data in {id}")
                public_info_json[key] = ""

        soup = _parse_html(personal_information_contact_response.text)
        ids_and_keys = [("publiccontact__token", "_token")]

        for id, key in ids_and_keys:
            try:
                value = soup.find("input", id=id)["value"]
                public_info_json[key] = value
            except (KeyError, TypeError):
                logging.warning(f"No data in {id}")
                public_info_json[key] = ""

        logging.info("Got Public info")

        user_info["Groups"] = groups_dict
        user_info["Roles"] = roles_list
        user_info["Rights"] = rights_list
        user_info["Public_info"] = public_info_json
        return user_info

    def set_own_user_info(self, **settings):
        """
        Sets the user's own information with the provided settings.
        """

        if not self._session:
            raise ValueError("Session is not initialized. Please log in first.")
        try:

            def modify_data(userinfo, settings0):

                data = {
                    "publiccontact[title]": userinfo["Public_info"]["title"],
                    "publiccontact[company]": userinfo["Public_info"]["company"],
                    "publiccontact[birthday]": userinfo["Public_info"]["birthday"],
                    "publiccontact[nickname]": userinfo["Public_info"]["nickname"],
                    "publiccontact[class]": userinfo["Public_info"]["class"],
                    "publiccontact[street]": userinfo["Public_info"]["street"],
                    "publiccontact[zipcode]": userinfo["Public_info"]["zipcode"],
                    "publiccontact[city]": userinfo["Public_info"]["city"],
                    "publiccontact[country]": userinfo["Public_info"]["country"],
                    "publiccontact[phone]": userinfo["Public_info"]["phone"],
                    "publiccontact[mobilePhone]": userinfo["Public_info"][
                        "mobilePhone"
                    ],
                    "publiccontact[fax]": userinfo["Public_info"]["fax"],
                    "publiccontact[mail]": userinfo["Public_info"]["mail"],
                    "publiccontact[homepage]": userinfo["Public_info"]["homepage"],
                    "publiccontact[icq]": userinfo["Public_info"]["icq"],
                    "publiccontact[jabber]": userinfo["Public_info"]["jabber"],
                    "publiccontact[msn]": userinfo["Public_info"]["msn"],
                    "publiccontact[skype]": userinfo["Public_info"]["skype"],
                    "publiccontact[note]": userinfo["Public_info"]["note"],
                    "publiccontact[hidden]": "0",
                    "publiccontact[actions][submit]": "",
                    "publiccontact[_token]": urllib.parse.quote(
                        userinfo["Public_info"]["_token"]
                    ),
                }

                for key, value in settings.items():
                    if key == "title":
                        data["publiccontact[title]"] = value
                        logging.info("changed title to" + value)
                    elif key == "company":
                        data["publiccontact[company]"] = value
                        logging.info("changed company to" + value)
                    elif key == "birthday":
                        data["publiccontact[birthday]"] = value
                        logging.info("changed birthday to" + value)
                    elif key == "nickname":
                        data["publiccontact[nickname]"] = value
                        logging.info("changed nickname to" + value)
                    elif key == "_class":
                        data["publiccontact[class]"] = value
                        logging.info("changed class to" + value)
                    elif key == "street":
                        data["publiccontact[street]"] = value
                        logging.info("changed street to" + value)
                    elif key == "zipcode":
                        data["publiccontact[zipcode]"] = value
                        logging.info("changed zipcode to" + value)
                    elif key == "city":
                        data["publiccontact[city]"] = value
                        logging.info("changed city to" + value)
                    elif key == "country":
                        data["publiccontact[country]"] = value
                        logging.info("changed country to" + value)
                    elif key == "phone":
                        data["publiccontact[phone]"] = value
                        logging.info("changed phone to" + value)
                    elif key == "mobilePhone":
                        data["publiccontact[mobilePhone]"] = value
                        logging.info("changed mobilePhone to" + value)
                    elif key == "fax":
                        data["publiccontact[fax]"] = value
                        logging.info("changed fax to" + value)
                    elif key == "mail":
                        data["publiccontact[mail]"] = value
                        logging.info("changed mail to" + value)
                    elif key == "homepage":
                        data["publiccontact[homepage]"] = value
                        logging.info("changed homepage to" + value)
                    elif key == "icq":
                        data["publiccontact[icq]"] = value
                        logging.info("changed icq to" + value)
                    elif key == "jabber":
                        data["publiccontact[jabber]"] = value
                        logging.info("changed jabber to" + value)
                    elif key == "msn":
                        data["publiccontact[msn]"] = value
                        logging.info("changed msn to" + value)
                    elif key == "skype":
                        data["publiccontact[skype]"] = value
                        logging.info("changed skype to" + value)
                    elif key == "note":
                        data["publiccontact[note]"] = value
                        logging.info("changed note to" + value)

                return data

            userinfo = self.get_own_user_info()
            data = modify_data(userinfo, settings)

            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "max-age=0",
                "content-type": "application/x-www-form-urlencoded",
                "origin": "null",
                "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            }

            cookies = {
                "IServSAT": self._IServSAT,
                "IServSATId": self._IServSATId,
                "IServSession": self._IServSession,
            }
            response = self._session.post(
                f"https://{self.iserv_url}/iserv/profile/public/edit",
                headers=headers,
                cookies=cookies,
                data=data,
                allow_redirects=True,
            )
            logging.info("Public info changed successfully")
            return response.status_code
        except Exception as e:
            logging.error(f"Error setting user information: {e}")
            raise ValueError("Error setting user information")

    def get_notifications(self):
        """
        Retrieves notifications from the specified URL and returns them as a JSON object.
        """
        notifications = self._session.get(
            f"https://{self.iserv_url}/iserv/user/api/notifications"
        ).json()
        logging.info("Got Notifications")
        return notifications

    def get_badges(self):
        """
        Retrieves the badges from the IServ server.

        :return: A JSON object containing the badges.
        """
        badges = self._session.get(
            f"https://{self.iserv_url}/iserv/app/navigation/badges"
        ).json()
        logging.info("Got Badges")
        return badges

    def read_all_notifications(self):
        """
        Reads all notifications from the server.
        """
        notifications = self._session.post(
            f"https://{self.iserv_url}/iserv/notification/api/v1/notifications/readall",
            cookies={
                "IServSAT": self._IServSAT,
                "IServSATId": self._IServSATId,
                "IServSession": self._IServSession,
            },
        )
        logging.info("Read all notifications")
        return notifications

    def read_notification(self, notification_id: int):
        """
        Sends a POST request to the IServ notification API to mark a specific notification as read.
        """
        notification = self._session.post(
            f"https://{self.iserv_url}/iserv/notification/api/v1/notifications/{notification_id}/read",
            cookies={
                "IServSAT": self._IServSAT,
                "IServSATId": self._IServSATId,
                "IServSession": self._IServSession,
            },
        )
        logging.info("read notification " + notification_id)
        return notification

    def get_disk_space(self) -> dict:
        response = self._session.get(f"https://{self.iserv_url}/iserv/du/account")
        soup = _parse_html(response.text)
        disk_json = soup.find("script", id="user-diskusage-data").get_text()
        disk_json = json.loads(disk_json.strip("()"))
        return disk_json

    # Users

    def get_user_profile_picture(self, user, output_folder: str):
        """
        Retrieves the profile picture of a user and saves it to the specified output folder.
        """
        avatar = self._session.get(
            f"https://{self.iserv_url}/iserv/core/avatar/user/{user}"
        )

        file_path = output_folder.replace("\\", "/").removesuffix("/") + "/"

        if "<svg" in avatar.text:
            with open(file_path + user + ".svg", "w") as f:
                f.write(avatar.text)
        else:
            with open(file_path + user + ".webp", "wb") as f:
                f.write(avatar.content)

    def search_users(self, query):
        """
        Searches for users based on a query string and returns a list of dictionaries.
        """

        query = urllib.parse.quote(query)
        resonse = self._session.get(
            f"https://{self.iserv_url}/iserv/addressbook/public?filter%5Bsearch%5D={query}",
            allow_redirects=True,
        )
        soup = _parse_html(resonse.text)

        if "Too many results, please restrict filter criteria!" in resonse.text:
            logging.error("Too many results, please restrict filter criteria!")
            raise ValueError("Too many results, please restrict filter criteria!")

        if "Zu viele Treffer, bitte Filterkriterien einschränken!" in resonse.text:
            logging.error("Too many results, please restrict filter criteria!")
            raise ValueError("Too many results, please restrict filter criteria!")

        else:
            table = str(soup.find("table").contents[3])

            soup = _parse_html(table)

            rows = soup.find_all("tr")

            content_href_list = []

            for row in rows:
                a_tag = row.find("a")
                if a_tag:
                    content_href_dict = {
                        "name": a_tag.get_text(),
                        "user_url": a_tag.get("href"),
                    }
                    content_href_list.append(content_href_dict)
            logging.info("Searched users")
            return content_href_list

    def search_users_autocomplete(self, query, limit=50):
        """
        Perform autocomplete search for users based on the query and optional limit.
        """
        users = self._session.get(
            f"https://{self.iserv_url}/iserv/core/autocomplete/api?type=list,mail&query={query}&limit={str(limit)}"
        ).json()
        logging.info("Searched users (autocomplete)")
        return users

    def get_user_info(self, user):
        """
        A function to retrieve user information from a given URL and parse it into a dictionary.
        """
        response = self._session.get(
            f"https://{self.iserv_url}/iserv/addressbook/public/show/{user}"
        )
        soup = _parse_html(response.text)
        table = soup.find("table")

        try:
            # Manual HTML table parsing (replaces pd.read_html)
            rows = table.find_all("tr")
            data_dict = {}
            for row in rows:
                cells = row.find_all("td")
                if not cells:
                    cells = row.find_all("th")
                if len(cells) >= 2:
                    key = cells[0].get_text().strip()
                    val = cells[1].get_text().strip()
                    data_dict[key] = val
            logging.info("Got info of user " + user)
        except (ValueError, AttributeError):
            logging.error("No such user found!")
            raise ValueError("No such user found!")

        return data_dict

    # Email

    def get_emails(self, path="INBOX", length=50, start=0, order="date", dir="desc"):
        """
        Retrieves emails from a specified path with optional parameters for length, start, order, and direction.
        """
        emails = self._session.get(
            f"https://{self.iserv_url}/iserv/mail/api/message/list?path={path}&length={str(length)}&start={str(start)}&order%5Bcolumn%5D={order}&order%5Bdir%5D={dir}"
        ).json()
        logging.info("Got emails sccessfully!")
        return emails

    def get_email_info(self, path="INBOX", length=0, start=0, order="date", dir="desc"):
        """
        Retrieves email information from the specified path in the mailbox.
        """
        email_info = self._session.get(
            f"https://{self.iserv_url}/iserv/mail/api/message/list?path={path}&length={str(length)}&start={str(start)}&order%5Bcolumn%5D={order}&order%5Bdir%5D={dir}"
        ).json()
        logging.info("Got Email info!")
        return email_info

    def get_email_source(self, uid, path="INBOX"):
        """
        Retrieves the source code of an email message.
        """
        email_source = self._session.get(
            f"https://{self.iserv_url}/iserv/mail/show/source?path={path}&msg={str(uid)}"
        ).text
        logging.info("Got Email source")
        return email_source

    def get_mail_folders(self):
        """
        Retrieves the list of mail folders from the IServ API.
        """
        mail_folders = self._session.get(
            f"https://{self.iserv_url}/iserv/mail/api/folder/list"
        ).json()
        logging.info("Got Email Folders")
        return mail_folders

    def send_email(
        self,
        receiver_email: Union[str, list],
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        smtp_server: Optional[str] = None,
        smtps_port: int = 465,
        attachments: Optional[list] = None,
    ):
        """
        Sends an email with the given parameters.
        """

        if isinstance(receiver_email, str):
            receiver_email = [receiver_email]

        if attachments != None:
            if type(attachments) != list and attachments:
                logging.error("Attachments must be list!")
                raise TypeError("Attachments must be list!")

        if smtp_server == None:
            smtp_server = self.iserv_url

        message = MIMEMultipart()
        message["From"] = f"{self.username}@{self.iserv_url}"
        message["To"] = ", ".join(receiver_email)
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        if html_body:
            message.attach(MIMEText(html_body, "html"))

        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(attachment)}"',
                )
                message.attach(part)
                logging.debug(attachment)

        try:
            with smtplib.SMTP_SSL(smtp_server, smtps_port) as server_ssl:
                server_ssl.login(self.username, self._password)
                server_ssl.sendmail(
                    self.username + "@" + self.iserv_url,
                    receiver_email,
                    message.as_string(),
                )
                logging.info(
                    "Email sent successfully via SMTPS (port {}).".format(smtps_port)
                )

        except smtplib.SMTPException as e:
            logging.error("Failed to send email:", e)
            raise smtplib.SMTPException(e)

    # Calendar

    def get_upcoming_events(self):
        """
        Retrieves the upcoming events from the IServ calendar API.
        """
        events = self._session.get(
            f"https://{self.iserv_url}/iserv/calendar/api/upcoming"
        ).json()
        logging.info("Got upcomming events")
        return events

    def get_eventsources(self):
        """
        Retrieves the event sources from the calendar API.
        """
        eventsources = self._session.get(
            f"https://{self.iserv_url}/iserv/calendar/api/eventsources"
        ).json()
        logging.info("Got eventsources")
        return eventsources

    def get_events(self, start: str, end: str):
        """Returns all events from all eventsources (Calendars) as a JSON object

        Args:
            start (str): Start date
            end (str): End date

        Returns:
            JSON: A JSON object with the data
        """

        events = self._session.get(
            f"https://{self.iserv_url}/iserv/calendar/feed/calendar-multi",
            params={
                "start": _parse_date(start).strftime("%Y-%m-%d"),
                "end": _parse_date(end).strftime("%Y-%m-%d"),
            },
        ).json()

        logging.info("Got calendar events")
        logging.debug(f"Got Calendar events from {start} to {end}")
        return events

    def search_event(self, query: str, start: str, end: str):
        """Searches for events in all eventsources

        Args:
            query (str): The search term
            start (str): The start date. Time is also supported.
            end (str): The end date. Time is also supported.

        Returns:
            JSON: All found events
        """
        events = self._session.get(
            f"https://{self.iserv_url}/iserv/calendar/api/lookup_event",
            params={
                "summary": query,
                "start": _parse_date(start, yearfirst=True).isoformat(
                    timespec="microseconds"
                )[:-3]
                + "Z",
                "end": _parse_date(end, yearfirst=True).isoformat(
                    timespec="microseconds"
                )[:-3]
                + "Z",
            },
        )
        logging.info("Looked up calendar events")
        logging.debug(
            f"Looked up Calendar events with query {query} from {start} to {end}"
        )
        return events.json()

    def get_calendar_plugin_events(self, plugin: str, start: str, end: str):
        """Lists all events produced by a plugin.

        Args:
            plugin (str): The name of the plugin
            start (str): The start date of the results
            end (str): The end date of the results

        Returns:
            JSON: Events
        """
        events = self._session.get(
            f"https://{self.iserv_url}/iserv/calendar/feed/plugin",
            params={
                "plugin": plugin,
                "start": _parse_date(start).isoformat(),
                "end": _parse_date(end).isoformat(),
            },
        )
        logging.debug(f"Got {plugin} envents from {start} to {end}")
        logging.info("Got calendar plugin events")
        return events.json()

    def delete_event(
        self, uid: str, _hash: str, calendar: str, start: str, series: bool = False
    ):
        """Deletes a specified event or reocurring event series.

        Args:
            uid (str): uid of the event
            _hash (str): hash of the event
            calendar (str): calendar(_id) of the event
            start (str): The beginning date and time
            series (bool, optional): Delete reocurring events.

        Returns:
            JSON: Status
        """

        events = self._session.post(
            f"https://{self.iserv_url}/iserv/calendar/delete",
            params={
                "uid": uid,
                "hash": _hash,
                "cal": calendar,
                "start": _parse_date(start).strftime("%Y-%m-%dT%H:%M:%S%z"),
                "edit_series": "series" if series else "single",
            },
            cookies={
                "IServSAT": self._IServSAT,
                "IServSATId": self._IServSATId,
                "IServSession": self._IServSession,
            },
        )
        logging.debug(f"Deleted event {uid} with hash {_hash} in calendar {calendar}")
        logging.debug(f"Status code: {events.status_code}")
        logging.info("Event deleted")
        return events.json()

    def create_event(
        self,
        subject: str,
        calendar: str,
        start: str,
        end: str,
        category: str = "",
        location: str = "",
        alarms: list[AlarmType] = [],
        isAllDayLong: bool = False,
        description: str = "",
        participants: list = [],
        show_me_as: Literal["OPAQUE", "TRANSPARENT"] = "OPAQUE",
        privacy: Literal["PUBLIC", "CONFIDENTIAL", "PRIVATE"] = "PUBLIC",
        recurring: Recurring = {},
    ):
        """
        Create a new event in the IServ calendar.
        """

        token_request = self._session.get(
            f"https://{self.iserv_url}/iserv/calendar/create_simple",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "X-Requested-With": "XMLHttpRequest",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
            },
            cookies={
                "IServSAT": self._IServSAT,
                "IServSATId": self._IServSATId,
                "IServSession": self._IServSession,
            },
        )
        tokensoup = _parse_html(token_request.text)

        token = tokensoup.find("input", {"id": "eventForm__token"}).get("value")

        # Minimal data
        data = {
            "eventForm[uid]": "",
            "eventForm[etag]": "",
            "eventForm[hash]": "",
            "eventForm[calendarOrg]": "",
            "eventForm[startOrg]": "",
            "eventForm[action]": "create",
            "eventForm[seriesAction]": "",
            "eventForm[invited]": "",
            "eventForm[subscription]": "",
            "eventForm[subject]": subject,
            "eventForm[calendar]": calendar,
            "eventForm[category]": category,
            "eventForm[location]": location,
            "eventForm[startDate]": _parse_date(start).strftime("%d.%m.%Y"),
            "eventForm[startTime]": _parse_date(start).strftime("%H:%M"),
            "eventForm[endDate]": _parse_date(end).strftime("%d.%m.%Y"),
            "eventForm[endTime]": _parse_date(end).strftime("%H:%M"),
            "eventForm[description]": description,
            "eventForm[showMeAs]": show_me_as,
            "eventForm[privacy]": privacy,
            "eventForm[recurring][intervalType]": "NO",
            "eventForm[recurring][interval]": "1",
            "eventForm[recurring][recurrenceDays][]": "FR",
            "eventForm[recurring][monthlyIntervalType]": "BYMONTHDAY",
            "eventForm[recurring][monthDayInMonth]": "26",
            "eventForm[recurring][endType]": "NEVER",
            "eventForm[submit]": "",
            "eventForm[_token]": token,
        }

        if recurring != {}:
            if "intervalType" not in recurring:
                raise ValueError("intervalType must be present!")
            if (
                recurring["intervalType"] != "WEEKDAYS"
                and recurring["intervalType"] != "NO"
                and "interval" not in recurring
            ):
                raise ValueError("interval must be present!")

            if "interval" in recurring:
                if recurring["interval"] not in range(1, 31):
                    raise ValueError("Interval can only be between 1 and 30")
            if recurring["intervalType"] == "MONTHLY":
                if "monthlyIntervalType" not in recurring:
                    raise ValueError("monthlyIntervalType must be present!")
                if recurring["monthlyIntervalType"] == "BYDAY":
                    if "monthInterval" not in recurring:
                        raise ValueError("monthInterval must be present!")
                    if "monthDay" not in recurring:
                        raise ValueError("monthDay must be present!")
                if recurring["monthlyIntervalType"] == "BYMONTHDAY":
                    if "monthDayInMonth" not in recurring:
                        raise ValueError("monthDayInMonth must be present!")
            if recurring["intervalType"] == "WEEKLY":
                if "recurrenceDays" not in recurring:
                    raise ValueError("recurrenceDays must be present!")
            if recurring["intervalType"] != "NO":
                if "endType" not in recurring:
                    raise ValueError("endType must be present!")

                if recurring["endType"] == "COUNT":
                    if "endInterval" not in recurring:
                        raise ValueError("endInterval must be present!")

                if recurring["endType"] == "UNTIL":
                    if "untilDate" not in recurring:
                        raise ValueError("untilDate must be present!")
            try:
                data["eventForm[recurring][intervalType]"] = recurring["intervalType"]
            except KeyError:
                pass
            try:
                data["eventForm[recurring][interval]"] = recurring["interval"]
            except KeyError:
                pass
            try:
                data["eventForm[recurring][monthlyIntervalType]"] = recurring[
                    "monthlyIntervalType"
                ]
            except KeyError:
                pass
            try:
                data["eventForm[recurring][monthDayInMonth]"] = recurring[
                    "monthDayInMonth"
                ]
            except KeyError:
                pass
            try:
                data["eventForm[recurring][monthInterval]"] = recurring["monthInterval"]
            except KeyError:
                pass
            try:
                data["eventForm[recurring][monthDay]"] = recurring["monthDay"]
            except KeyError:
                pass
            try:
                data["eventForm[recurring][recurrenceDays][]"] = recurring[
                    "recurrenceDays"
                ]
            except KeyError:
                pass
            try:
                data["eventForm[recurring][endType]"] = recurring["endType"]
            except KeyError:
                pass
            try:
                data["eventForm[recurring][endInterval]"] = recurring["endInterval"]
            except KeyError:
                pass
            try:
                data["eventForm[recurring][untilDate]"] = recurring["untilDate"]
            except KeyError:
                pass

        # Very fun alarm parser
        if alarms != []:
            for i, alarm in enumerate(alarms):
                if isinstance(alarm, str):
                    if alarm not in [
                        "0M",
                        "5M",
                        "15M",
                        "30M",
                        "1H",
                        "2H",
                        "12H",
                        "1D",
                        "2D",
                        "7D",
                    ]:
                        raise ValueError(
                            "At least one timed alarm is not one of 0M,5M,15M,30M,1H,2H,12H,1D,2D or 7D."
                        )
                    else:
                        data[f"eventForm[alarms][{i}][trigger][type]"] = (
                            f"PT{alarm}"
                        )

                        data[f"eventForm[alarms][{i}][trigger][interval][days]"] = "0"
                        data[f"eventForm[alarms][{i}][trigger][interval][hours]"] = "0"
                        data[f"eventForm[alarms][{i}][trigger][interval][minutes]"] = (
                            "15"
                        )
                        data[f"eventForm[alarms][{i}][trigger][before]"] = "1"
                        data[f"eventForm[alarms][{i}][trigger][dateTime]"] = str(
                            _parse_date(start).strftime("%d.%m.%Y+00:00")
                        )

                if isinstance(alarm, dict):
                    if "custom_date_time" in alarm:
                        if "dateTime" not in alarm["custom_date_time"]:
                            raise ValueError(
                                "custom_date_time alarm dict is malformed."
                            )

                        data[f"eventForm[alarms][{i}][trigger][type]"] = (
                            "custom_date_time"
                        )
                        data[f"eventForm[alarms][{i}][trigger][interval][days]"] = "0"
                        data[f"eventForm[alarms][{i}][trigger][interval][hours]"] = "0"
                        data[f"eventForm[alarms][{i}][trigger][interval][minutes]"] = (
                            "15"
                        )
                        data[f"eventForm[alarms][{i}][trigger][before]"] = "1"
                        data[f"eventForm[alarms][{i}][trigger][dateTime]"] = (
                            str(
                                _parse_date(
                                    alarm["custom_date_time"]["dateTime"]
                                ).strftime("%d.%m.%Y %H:%M")
                            )
                        )

                    else:
                        ValueError("Alarm dict malformed! Missing: custom_date_time")

                    if "custom_interval" in alarm:
                        if "interval" in alarm["custom_interval"]:
                            if not all(
                                x in alarm["custom_interval"]["interval"]
                                for x in ["days", "hours", "minutes"]
                            ):
                                raise ValueError(
                                    "the `inteval` dict in `custom_interval` in alarms is malformed."
                                )

                        if "before" not in alarm["custom_interval"]:
                            raise ValueError("custom_interval needs a `before` key.")

                        data[f"eventForm[alarms][{i}][trigger][type]"] = (
                            "custom_interval"
                        )
                        data[f"eventForm[alarms][{i}][trigger][interval][days]"] = str(
                            alarm["custom_interval"]["interval"]["days"]
                        )
                        data[f"eventForm[alarms][{i}][trigger][interval][hours]"] = str(
                            alarm["custom_interval"]["interval"]["hours"]
                        )
                        data[f"eventForm[alarms][{i}][trigger][interval][minutes]"] = (
                            str(alarm["custom_interval"]["interval"]["minutes"])
                        )
                        data[f"eventForm[alarms][{i}][trigger][before]"] = (
                            "1" if alarm["custom_interval"]["before"] else "0"
                        )
                        data[f"eventForm[alarms][{i}][trigger][dateTime]"] = str(
                            _parse_date(start).strftime("%d.%m.%Y+00:00")
                        )
                    else:
                        ValueError("Alarm dict malformed! Missing: custom_interval")

        # Actually simple participant parser
        if participants != []:
            for i, participant in enumerate(participants):
                try:
                    participants[i] = self.search_users_autocomplete(participant, 1)[0][
                        "value"
                    ]
                except IndexError:
                    raise Exception(f"User `{participant}` not found!")

        data["eventForm[participants][]"] = participants

        response = self._session.post(
            f"https://{self.iserv_url}/iserv/calendar/create",
            data=data,
            cookies={
                "IServSAT": self._IServSAT,
                "IServSATId": self._IServSATId,
                "IServSession": self._IServSession,
            },
            params={
                "subject": subject,
                "calendar": calendar,
                "start": _parse_date(start).strftime("%d.%m.%Y"),
                "end": _parse_date(end).strftime("%d.%m.%Y"),
                "startTime": _parse_date(start).strftime("%H:%M"),
                "endTime": _parse_date(end).strftime("%H:%M"),
                "allDay": isAllDayLong,
            },
        )

        eventsoup = _parse_html(response.text)
        try:
            error = eventsoup.find("div", {"data-type": "error"})
            print(error.text)
        except AttributeError:
            pass

    # Misc

    def get_conference_health(self):
        """
        Get the health status of the conference API endpoint.
        """
        health = self._session.get(
            f"https://{self.iserv_url}/iserv/videoconference/api/health"
        ).json()
        logging.info("Got Conference Health")
        return health

    def file(self, davurl="default", username="default", password="default", path="/"):
        """
        Initializes a WebDAV client with the provided or default credentials and returns the client object.
        """
        try:
            davurl = "webdav." + self.iserv_url if davurl == "default" else davurl
            username = self.username if username == "default" else username
            password = self._password if password == "default" else password
            options = {
                "webdav_hostname": "https://" + davurl,
                "webdav_login": username,
                "webdav_password": password,
            }
            self.__DAVclient = _SimpleWebDAVClient(options)
            logging.info("Files initiated")
            return self.__DAVclient
        except Exception as e:
            logging.error("Exception at file (webdav): " + str(e))
            raise ValueError("Exception at file (webdav): " + str(e))

    def get_folder_size(self, path: str) -> dict:
        response = self._session.get(
            f"https://{self.iserv_url}/iserv/file/calc?path={path}"
        )
        return response.json()

    def get_groups(self) -> dict:

        groups = {}
        response = self._session.get(
            f"https://{self.iserv_url}/iserv/profile/grouprequest/add"
        )
        soup = _parse_html(response.text)
        select = soup.find(
            "select",
            class_="select2",
        )
        options = select.children
        for option in options:
            if isinstance(option, _HTMLNode) and option.tag == "option":
                groups[option.get_text()] = option.get("value", "")
        return groups
