# 🛡️ KynexAuth Python SDK & Example Projects

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://microsoft.com/windows)
[![GUI Ready](https://img.shields.io/badge/GUI-Modern%20Dark%20Theme%20(C%23%20Style)-purple.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Standard%20Library)-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Official, feature-complete Python implementation for the **[KynexAuth](https://kynexauth.com)** authentication and licensing API. 100% compatible with the C# / C++ specification.

---

## 📁 Repository Structure

```
Py Example/
├── 📁 ConsoleExample/
│   ├── kynexauth.py       # Core Python SDK Client Library (Zero third-party dependencies)
│   ├── main.py            # Cyberpunk-styled Console Loader application
│   ├── build_exe.bat      # 1-Click Standalone .EXE Compiler (PyInstaller)
│   └── requirements.txt   # Optional packaging dependencies
│
├── 📁 GuiExample/
│   ├── kynexauth.py       # Core Python SDK Client Library
│   ├── main.py            # 1:1 C# GunaUI2-styled Modern Dark GUI Loader & Dashboard
│   ├── build_exe.bat      # 1-Click Standalone .EXE Compiler (PyInstaller)
│   └── requirements.txt   # Optional packaging dependencies
│
└── 📄 README.md           # Setup & Integration Documentation
```

---

## 🔑 Step 1: Obtain Credentials from KynexAuth Dashboard

1. Sign in to your **[KynexAuth Developer Dashboard](https://kynexauth.com)**.
2. Navigate to the **Applications** page.
3. Retrieve your application credentials:
   * **Application Name** (e.g., `MyApplication`)
   * **Application Key / Owner ID** (e.g., `Z2zapMIjyB2nkw7ahr`)
   * **Application Version** (e.g., `1.0`)

---

## ⚙️ Step 2: Configure Credentials in Code

Open `ConsoleExample/main.py` or `GuiExample/main.py` and set your credentials:

```python
from kynexauth import api

# -------------------------------------------------------------
# CONFIGURE YOUR APPLICATION CREDENTIALS
# -------------------------------------------------------------
kynexauthapp = api(
    name="YOUR_APP_NAME",       # Application Name from dashboard
    ownerid="YOUR_APP_KEY",     # Application Key (Owner ID)
    version="1.0",              # Application Version
    url="https://kynexauth.com/api/v1/client",
    debug=False                 # Set True to enable debug HTTP logging
)
KynexAuthApp = kynexauthapp
```

---

## 🖥️ Running the Console Example

1. Open your terminal and navigate to the `ConsoleExample` directory:
   ```bash
   cd ConsoleExample
   ```
2. Run the loader:
   ```bash
   py main.py
   # or
   python main.py
   ```
3. **Features:**
   * Cyberpunk ANSI styling with rotating loading animations.
   * `[1] LOGIN` — Authenticate using username and password.
   * `[2] REGISTER` — Create a new account with a license key.
   * `[3] UPGRADE` — Extend an existing user's subscription.
   * `[4] LICENSE KEY ONLY` — Fast instant access via license key.
   * Automatic **Windows User SID** (`S-1-5-21-...`) hardware ID detection.
   * Background session watchdog monitoring.

---

## 🎨 Running the Modern Dark GUI Example

1. Open your terminal and navigate to the `GuiExample` directory:
   ```bash
   cd GuiExample
   ```
2. Run the GUI application:
   ```bash
   py main.py
   # or
   python main.py
   ```
3. **Features:**
   * Frameless custom title bar with minimize and close controls.
   * 3 Authentication Modes: `USER LOGIN`, `KEY LOGIN`, and `REGISTER`.
   * GunaUI2-inspired dark theme with responsive input focus indicators.
   * Full Protected Dashboard Window opened upon successful authentication.

---

## 📦 Compiling to Standalone Windows `.EXE`

To convert your Python scripts into standalone `.exe` binaries that run without Python installed on the client machine:

1. Double-click **`build_exe.bat`** in either the `ConsoleExample` or `GuiExample` folder.
2. The compilation will complete and output the single executable to the **`dist/`** directory:
   * **Console Binary:** `ConsoleExample/dist/KynexAuth_Console.exe`
   * **GUI Binary:** `GuiExample/dist/KynexAuth_GUI.exe`

Alternatively, build manually using PyInstaller:
```bash
# Console Loader:
py -m PyInstaller --console --onefile --clean --name="KynexAuth_Console" main.py

# GUI Loader:
py -m PyInstaller --noconsole --onefile --clean --name="KynexAuth_GUI" main.py
```

---

## 📚 Complete SDK API Reference

| Method | Description | Example Usage |
| :--- | :--- | :--- |
| `app.init()` | Initializes connection with server and retrieves session token. | `app.init()` |
| `app.login(username, password)` | Authenticates user credentials and binds HWID. | `app.login("john", "pass123")` |
| `app.register(username, password, key, email="")` | Creates new user account by redeeming license key. | `app.register("john", "pass123", "KEY-XXXX")` |
| `app.license(key)` | Authenticates using license key only. | `app.license("KEY-XXXX")` |
| `app.upgrade(username, key)` | Extends subscription duration for existing user. | `app.upgrade("john", "KEY-XXXX")` |
| `app.check()` | Verifies that session token is still valid. | `if not app.check(): sys.exit(1)` |
| `app.getvar(var_name)` | Fetches a secure server-side secret variable. | `secret = app.getvar("cheat_offset")` |
| `app.setvar(var_name, var_data)` | Sets a server-side variable. | `app.setvar("user_config", "data")` |
| `app.log(message)` | Sends a security or activity log directly to the dashboard. | `app.log("User initialized cheat")` |
| `app.ban(reason)` | Instantly bans the current user and HWID. | `app.ban("Memory tamper detected")` |
| `app.webhook(id, params)` | Executes a server-side webhook securely. | `app.webhook("12345", "arg=val")` |
| `app.chatget(channel)` | Fetches messages from a chat channel. | `msgs = app.chatget("general")` |
| `app.chatsend(message, channel)` | Sends a chat message to a channel. | `app.chatsend("Hello!", "general")` |
| `app.get_hwid()` | Returns the real Windows User SID (`S-1-5-...`). | `sid = app.get_hwid()` |
| `app.logout()` | Invalids and revokes the active session token. | `app.logout()` |

---

## 🔒 Implementing Your Protected Application Payload

Execute your protected code immediately after authentication validation:

```python
if KynexAuthApp.response.success:
    print("[+] Authentication Successful! Initializing protected payload...")
    
    # -------------------------------------------------------------
    # PLACE PROTECTED CODE / CHEAT MODULES HERE:
    # -------------------------------------------------------------
    # import protected_module
    # protected_module.run()
```

---

## 🛡️ Security Best Practices

1. **Obfuscation**: For commercial distribution, consider obfuscating compiled executables with tools such as PyArmor or VMProtect.
2. **HWID Binding**: Hardware IDs are automatically generated using native Win32 security APIs, matching the C# and C++ authentication security model.
3. **Session Heartbeat**: Keep the background session thread active to monitor real-time user bans and license revocations.
