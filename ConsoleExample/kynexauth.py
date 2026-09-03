"""
KynexAuth Python SDK
─────────────────────────────────────────────────────────────────────────────
High-security client-side authentication library for KynexAuth API.
Mirrors the official C# / C++ KynexAuth API specification.

Zero third-party dependencies required (pure standard library).
─────────────────────────────────────────────────────────────────────────────
"""

import sys
import os
import json
import time
import hashlib
import platform
import subprocess
import urllib.request
import urllib.error
import ssl
import ctypes
from datetime import datetime
from typing import List, Dict, Any


class Subscription:
    def __init__(self, name: str = "default", expiry: str = "Lifetime / Active"):
        self.name = name
        self.expiry = expiry


class UserData:
    def __init__(self):
        self.username: str = ""
        self.ip: str = ""
        self.hwid: str = ""
        self.createdate: str = ""
        self.lastlogin: str = ""
        self.area: str = ""
        self.rank: str = ""
        self.role: str = ""
        self.owner: str = ""
        self.subscriptions: List[Subscription] = []


class AppData:
    def __init__(self):
        self.numUsers: str = ""
        self.numOnlineUsers: str = ""
        self.numKeys: str = ""
        self.version: str = ""
        self.customerPanelLink: str = ""
        self.downloadLink: str = ""
        self.serverTime: str = ""


class ChannelStruct:
    def __init__(self, author: str = "", message: str = "", timestamp: str = ""):
        self.author = author
        self.message = message
        self.timestamp = timestamp


class ResponseData:
    def __init__(self):
        self.success: bool = False
        self.message: str = ""
        self.isPaid: bool = False
        self.channeldata: List[ChannelStruct] = []


class api:
    def __init__(
        self,
        name: str,
        ownerid: str,
        version: str,
        url: str = "https://kynexauth.com/api/v1/client",
        seed: str = "",
        debug: bool = False,
    ):
        self.name = name
        self.ownerid = ownerid
        self.version = version
        self.url = url.rstrip("/")
        self.seed = seed
        self.debug = debug

        self.sessionid: str = ""
        self.initialized: bool = False

        self.user_data = UserData()
        self.app_data = AppData()
        self.response = ResponseData()
        self._hwid_cache: str = ""

    def init(self) -> bool:
        payload = {
            "name": self.name,
            "appKey": self.ownerid,
            "version": self.version,
            "hash": self.get_checksum(),
        }

        res_str = self._req("/init", payload)
        try:
            data = json.loads(res_str)
            self.response.success = bool(data.get("success", False))
            self.response.message = str(data.get("message", ""))

            if self.response.success:
                self.initialized = True
                self.sessionid = str(data.get("sessionToken", ""))
                app_info = data.get("appInfo", {})
                if isinstance(app_info, dict):
                    self.app_data.version = str(app_info.get("version", self.version))
                    if "name" in app_info and not self.name:
                        self.name = str(app_info["name"])

            if "downloadLink" in data:
                self.app_data.downloadLink = str(data.get("downloadLink", ""))

            return self.response.success
        except Exception as e:
            self.response.success = False
            self.response.message = f"Failed to parse init response: {e}"
            return False

    def login(self, username: str, password: str, code: str = "") -> bool:
        self._check_init()
        payload = {
            "username": username,
            "password": password,
            "hwid": self.get_hwid(),
            "sessionToken": self.sessionid,
        }
        res_str = self._req("/login", payload)
        return self._parse_login_response(res_str, username, "login")

    def register(self, username: str, password: str, key: str, email: str = "") -> bool:
        self._check_init()
        payload = {
            "username": username,
            "password": password,
            "licenseKey": key,
            "email": email,
            "hwid": self.get_hwid(),
            "sessionToken": self.sessionid,
        }
        res_str = self._req("/register", payload)
        return self._parse_login_response(res_str, username, "register")

    def regstr(self, username: str, password: str, key: str, email: str = "") -> bool:
        return self.register(username, password, key, email)

    def license(self, key: str, code: str = "") -> bool:
        self._check_init()
        payload = {
            "licenseKey": key,
            "hwid": self.get_hwid(),
            "sessionToken": self.sessionid,
        }
        res_str = self._req("/license", payload)
        return self._parse_login_response(res_str, f"Key_{key[:6]}", "license")

    def upgrade(self, username: str, key: str) -> bool:
        self._check_init()
        payload = {
            "username": username,
            "licenseKey": key,
            "sessionToken": self.sessionid,
        }
        res_str = self._req("/upgrade", payload)
        try:
            data = json.loads(res_str)
            self.response.success = bool(data.get("success", False))
            self.response.message = str(data.get("message", ""))
            return self.response.success
        except Exception:
            return False

    def check(self, check_paid: bool = False) -> bool:
        payload = {"sessionToken": self.sessionid}
        res_str = self._req("/check", payload)
        try:
            data = json.loads(res_str)
            self.response.success = bool(data.get("success", False))
            self.response.message = str(data.get("message", ""))
            return self.response.success
        except Exception:
            self.response.success = False
            return False

    def log(self, message: str) -> bool:
        payload = {
            "sessionToken": self.sessionid,
            "message": message,
        }
        self._req("/log", payload)
        return True

    def ban(self, reason: str = "") -> bool:
        payload = {
            "sessionToken": self.sessionid,
            "reason": reason,
            "username": self.user_data.username,
        }
        res_str = self._req("/ban", payload)
        try:
            data = json.loads(res_str)
            self.response.success = bool(data.get("success", False))
            self.response.message = str(data.get("message", ""))
            return self.response.success
        except Exception:
            return False

    def getvar(self, var_name: str) -> str:
        payload = {
            "sessionToken": self.sessionid,
            "varName": var_name,
        }
        res_str = self._req("/var", payload)
        try:
            data = json.loads(res_str)
            if data.get("success"):
                return str(data.get("data", ""))
        except Exception:
            pass
        return ""

    def setvar(self, var_name: str, var_data: str) -> bool:
        payload = {
            "sessionToken": self.sessionid,
            "varName": var_name,
            "varData": var_data,
        }
        res_str = self._req("/var", payload)
        try:
            data = json.loads(res_str)
            return bool(data.get("success", False))
        except Exception:
            return False

    def webhook(self, webhook_id: str, params_val: str) -> str:
        payload = {
            "sessionToken": self.sessionid,
            "webhookId": webhook_id,
            "params": params_val,
        }
        res_str = self._req("/webhook", payload)
        try:
            data = json.loads(res_str)
            if data.get("success"):
                return str(data.get("data", ""))
        except Exception:
            pass
        return ""

    def chatget(self, channel: str) -> List[ChannelStruct]:
        payload = {
            "sessionToken": self.sessionid,
            "channel": channel,
        }
        res_str = self._req("/chat", payload)
        self.response.channeldata.clear()
        try:
            data = json.loads(res_str)
            self.response.success = bool(data.get("success", False))
            self.response.message = str(data.get("message", ""))
            messages = data.get("messages", [])
            for msg in messages:
                if isinstance(msg, dict):
                    self.response.channeldata.append(
                        ChannelStruct(
                            author=str(msg.get("author", "")),
                            message=str(msg.get("message", "")),
                            timestamp=str(msg.get("timestamp", "")),
                        )
                    )
        except Exception:
            pass
        return self.response.channeldata

    def chatsend(self, message: str, channel: str) -> bool:
        payload = {
            "sessionToken": self.sessionid,
            "message": message,
            "channel": channel,
        }
        res_str = self._req("/chat", payload)
        try:
            data = json.loads(res_str)
            return bool(data.get("success", False))
        except Exception:
            return False

    def logout(self) -> None:
        if self.sessionid:
            payload = {"sessionToken": self.sessionid}
            self._req("/logout", payload)
            self.sessionid = ""
            self.initialized = False

    def get_hwid(self) -> str:
        if self._hwid_cache:
            return self._hwid_cache

        hwid = ""
        try:
            if platform.system() == "Windows":
                try:
                    from ctypes import wintypes
                    advapi32 = ctypes.windll.advapi32
                    kernel32 = ctypes.windll.kernel32

                    TOKEN_QUERY = 0x0008
                    TokenUser = 1

                    h_token = wintypes.HANDLE()
                    if advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), TOKEN_QUERY, ctypes.byref(h_token)):
                        size = wintypes.DWORD(0)
                        advapi32.GetTokenInformation(h_token, TokenUser, None, 0, ctypes.byref(size))
                        if size.value > 0:
                            buf = ctypes.create_string_buffer(size.value)
                            if advapi32.GetTokenInformation(h_token, TokenUser, buf, size.value, ctypes.byref(size)):
                                p_sid = ctypes.c_void_p.from_buffer(buf)
                                sid_ptr = ctypes.c_void_p(p_sid.value)
                                p_string_sid = wintypes.LPWSTR()
                                if advapi32.ConvertSidToStringSidW(sid_ptr, ctypes.byref(p_string_sid)):
                                    hwid = str(p_string_sid.value).strip()
                                    kernel32.LocalFree(p_string_sid)
                        kernel32.CloseHandle(h_token)
                except Exception:
                    pass

                if not hwid or not hwid.startswith("S-1-"):
                    try:
                        out = subprocess.check_output("whoami /user", shell=True, stderr=subprocess.DEVNULL).decode()
                        lines = [l.strip() for l in out.strip().splitlines() if l.strip()]
                        if lines:
                            for part in lines[-1].split():
                                if part.startswith("S-1-"):
                                    hwid = part.strip()
                                    break
                    except Exception:
                        pass
        except Exception:
            pass

        if not hwid:
            import uuid
            hwid = hashlib.sha256(f"{uuid.getnode()}-{platform.node()}".encode()).hexdigest().upper()

        self._hwid_cache = hwid
        return self._hwid_cache

    def get_checksum(self) -> str:
        try:
            filepath = sys.argv[0] if sys.argv else __file__
            if os.path.exists(filepath):
                hasher = hashlib.md5()
                with open(filepath, "rb") as f:
                    while chunk := f.read(65536):
                        hasher.update(chunk)
                return hasher.hexdigest()
        except Exception:
            pass
        return "UNKNOWN_HASH"

    def _check_init(self) -> None:
        if not self.initialized:
            print("\n[!] KynexAuth Error: You must run init() first!", file=sys.stderr)
            sys.exit(1)

    def _format_time(self, timestamp: Any) -> str:
        if not timestamp:
            return "N/A"
        try:
            ts_int = int(timestamp)
            return datetime.fromtimestamp(ts_int).strftime("%a %m/%d/%y %H:%M:%S")
        except Exception:
            return str(timestamp)

    def _parse_login_response(self, res_str: str, username: str, action_name: str) -> bool:
        try:
            data = json.loads(res_str)
            self.response.success = bool(data.get("success", False))
            self.response.message = str(data.get("message", ""))

            if self.response.success:
                self.initialized = True
                if "sessionToken" in data:
                    self.sessionid = str(data["sessionToken"])

                app_info = data.get("appInfo", {})
                if isinstance(app_info, dict) and "downloadLink" in app_info:
                    self.app_data.downloadLink = str(app_info["downloadLink"])

                self.user_data.username = username
                self.user_data.hwid = self.get_hwid()

                if "serverTime" in data:
                    self.app_data.serverTime = str(data["serverTime"])

                user_info = data.get("userInfo", {})
                if isinstance(user_info, dict):
                    if "createdAt" in user_info:
                        self.user_data.createdate = self._format_time(user_info["createdAt"])

                    self.user_data.ip = str(user_info.get("ip", ""))
                    if not self.user_data.ip:
                        try:
                            req = urllib.request.Request("https://api.ipify.org", headers={"User-Agent": "Mozilla/5.0"})
                            with urllib.request.urlopen(req, timeout=2) as r:
                                self.user_data.ip = r.read().decode().strip()
                        except Exception:
                            self.user_data.ip = "127.0.0.1"

                    if "lastlogin" in user_info:
                        self.user_data.lastlogin = self._format_time(user_info["lastlogin"])
                    else:
                        self.user_data.lastlogin = "Just Now"

                    self.user_data.subscriptions.clear()
                    expiry_val = user_info.get("expiresAt", "0")
                    if expiry_val and expiry_val != "0":
                        formatted_expiry = self._format_time(expiry_val)
                    else:
                        formatted_expiry = "Lifetime / Active"

                    self.user_data.subscriptions.append(
                        Subscription(name="default", expiry=formatted_expiry)
                    )

            return self.response.success
        except Exception as e:
            self.response.success = False
            self.response.message = f"Failed to parse {action_name} response: {e}"
            return False

    def _req(self, endpoint: str, json_data: Dict[str, Any]) -> str:
        url = f"{self.url}{endpoint}"
        body_bytes = json.dumps(json_data).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "X-App-Name": self.name,
            "X-Owner-ID": self.ownerid,
            "User-Agent": f"KynexAuth-PythonSDK/{self.version}",
        }

        if self.debug:
            print(f"\n[DEBUG] POST {url}")
            print(f"[DEBUG] Body: {json.dumps(json_data, indent=2)}")

        req = urllib.request.Request(url, data=body_bytes, headers=headers, method="POST")

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                res_body = response.read().decode("utf-8")
                if self.debug:
                    print(f"[DEBUG] Response: {res_body}\n")
                return res_body
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            if self.debug:
                print(f"[DEBUG] HTTP Error {e.code}: {err_body}\n")
            return err_body
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Network Exception: {e}\n")
            return json.dumps({"success": False, "message": f"Connection error: {e}"})
