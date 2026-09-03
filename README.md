# 🛡️ KynexAuth Python SDK & GUI Integration Guide

[![Python](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://microsoft.com/windows)
[![GUI Ready](https://img.shields.io/badge/GUI-Modern%20Dark%20Theme%20(C%23%20Style)-purple.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Standard%20Library)-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Official, feature-complete Python implementation for the **KynexAuth API**, 100% compatible with the C# / C++ specification.

---

## 📁 Project Structure

```
Py Example/
├── 📁 ConsoleExample/
│   ├── kynexauth.py       # Core Python SDK Client Library (Zero third-party dependencies)
│   ├── main.py            # Cyberpunk-styled Console Loader application
│   ├── build_exe.bat      # 1-Click Standalone .EXE Compiler
│   └── requirements.txt   # Optional packaging dependencies
│
├── 📁 GuiExample/
│   ├── kynexauth.py       # Core Python SDK Client Library
│   ├── main.py            # 1:1 C# GunaUI2-styled Modern Dark GUI Loader & Dashboard
│   ├── build_exe.bat      # 1-Click Standalone .EXE Compiler
│   └── requirements.txt   # Optional packaging dependencies
│
└── 📄 README.md           # Complete integration & setup guide
```

---

## 🔑 Step 1: Get Your Credentials from KynexAuth Dashboard

1. Log in to your [KynexAuth Developer Dashboard](https://kynexauth.com/dashboard).
2. Go to your **Applications** tab.
3. Copy the following 3 values:
   * **Application Name** (e.g. `MyLoaderApp`)
   * **App Key / Owner ID** (e.g. `Z2zapMIjyB2nkw7ahr`)
   * **Application Version** (e.g. `1.0`)

---

## ⚙️ Step 2: Configure Your Credentials in Python

Open either `ConsoleExample/main.py` or `GuiExample/main.py` and replace lines 50–65 with your credentials:

```python
from kynexauth import api

# -------------------------------------------------------------
# CONFIGURE YOUR CREDENTIALS HERE
# -------------------------------------------------------------
kynexauthapp = api(
    name="YOUR_APP_NAME",       # Application Name from dashboard
    ownerid="YOUR_APP_KEY",     # Application Key (Owner ID)
    version="1.0",              # Application Version
    url="https://kynexauth.com/api/v1/client",
    debug=False                 # Set True to print raw HTTP requests/responses
)
KynexAuthApp = kynexauthapp
```

---

## 🖥️ Step 3: Run the Console Loader

1. Open your terminal inside the `ConsoleExample` directory:
   ```bash
   cd "C:\Users\Abdullah\Downloads\kynexauth\examples\cpp\Py Example\ConsoleExample"
   ```
2. Run the script:
   ```bash
   py main.py
   ```
3. **Features in Console Loader:**
   * Cyberpunk ANSI styling with smooth rotating loading spinner.
   * `[1] LOGIN` — Authenticate using username and password.
   * `[2] REGISTER` — Create a new account with a license key.
   * `[3] UPGRADE` — Extend an existing account subscription.
   * `[4] LICENSE KEY ONLY` — Instant fast authentication with key only.
   * Automatic **Windows User SID** (`S-1-5-21-...`) hardware ID detection.
   * Background session watchdog monitoring.

---

## 🎨 Step 4: Run the Modern Dark GUI Loader

1. Open your terminal inside the `GuiExample` directory:
   ```bash
   cd "C:\Users\Abdullah\Downloads\kynexauth\examples\cpp\Py Example\GuiExample"
   ```
2. Run the script:
   ```bash
   py main.py
   ```

---

## 📦 Step 5: 1-Click Compile to Standalone Windows `.EXE`

To convert your Python scripts into standalone Windows executables that run without needing Python installed on the client's PC:

1. Double-click **`build_exe.bat`** in either `ConsoleExample` or `GuiExample`.
2. The script will automatically package the loader.
3. Your compiled `.exe` will be located inside the **`dist/`** folder:
   * **Console EXE:** `ConsoleExample/dist/KynexAuth_Console.exe`
   * **GUI EXE:** `GuiExample/dist/KynexAuth_GUI.exe`

---

## 📚 Complete API Reference Cheat Sheet

| Method | Description | Example Usage |
| :--- | :--- | :--- |
| `app.init()` | Initializes connection with server and gets session token. | `app.init()` |
| `app.login(username, password)` | Authenticates user credentials and binds HWID. | `app.login("john", "pass123")` |
| `app.register(username, password, key, email="")` | Creates new user account by redeeming license key. | `app.register("john", "pass123", "KEY-XXXX")` |
| `app.license(key)` | Instant authentication with license key only. | `app.license("KEY-XXXX")` |
| `app.upgrade(username, key)` | Extends subscription duration for existing user. | `app.upgrade("john", "KEY-XXXX")` |
| `app.check()` | Verifies that session token is still valid. | `if not app.check(): sys.exit(1)` |
| `app.getvar(var_name)` | Fetches a secure server-side secret variable string. | `secret = app.getvar("cheat_offset")` |
| `app.setvar(var_name, var_data)` | Sets a server-side variable. | `app.setvar("user_config", "data")` |
| `app.log(message)` | Sends a security or activity log directly to the dashboard. | `app.log("User injected cheat")` |
| `app.ban(reason)` | Instantly bans the current user and HWID. | `app.ban("Tamper attempt detected")` |
| `app.webhook(id, params)` | Executes a server-side webhook securely. | `app.webhook("12345", "arg=val")` |
| `app.chatget(channel)` | Fetches messages from a chat channel. | `msgs = app.chatget("general")` |
| `app.chatsend(message, channel)` | Sends a chat message to a channel. | `app.chatsend("Hello!", "general")` |
| `app.get_hwid()` | Returns the real Windows User SID (`S-1-5-...`). | `sid = app.get_hwid()` |
| `app.logout()` | Invalids and revokes the active session token. | `app.logout()` |

---

## 🔒 Where to Place Your Protected Application Payload

Once authentication succeeds, execute your main game cheat, automation script, or tool payload:

```python
# Check authentication success
if KynexAuthApp.response.success:
    print("Authentication passed! Launching protected code...")
    
    # -------------------------------------------------------------
    # YOUR PROTECTED PAYLOAD STARTS HERE:
    # -------------------------------------------------------------
    # import my_cheat_module
    # my_cheat_module.start()
```

---

## 🛡️ Security & Best Practices

1. **Keep App Key Protected**: Obfuscate your compiled executable with tools like PyArmor or VMProtect if distributing to untrusted end-users.
2. **Dynamic HWID**: The Python SDK uses native Win32 `OpenProcessToken` and `ConvertSidToStringSidW` to ensure 100% compatibility with C# and C++ hardware binding.
3. **Session Watchdog**: Keep the background session thread running to detect if an administrator disables or bans the user from the web dashboard in real time.
