"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         KYNEXAUTH SECURITY LOADER                            ║
║                      Premium Python Console Authentication                    ║
║                              v1.0 - Stylish Edition                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import threading
from typing import Optional
from kynexauth import api

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                         ANSI COLOR DEFINITIONS                            ║
# ╚════════════════════════════════════════════════════════════════════════════╝
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    DIM = '\033[2m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                         PREMIUM ASCII BANNER                              ║
# ╚════════════════════════════════════════════════════════════════════════════╝
PREMIUM_BANNER = rf"""{Colors.BRIGHT_CYAN}
  ██╗  ██╗██╗   ██╗███╗   ██╗███████╗██╗  ██╗ █████╗ ██╗   ██╗████████╗██╗  ██╗
  ██║ ██╔╝╚██╗ ██╔╝████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗██║   ██║╚══██╔══╝██║  ██║
  █████╔╝  ╚████╔╝ ██╔██╗ ██║█████╗   ╚███╔╝ ███████║██║   ██║   ██║   ███████║
  ██╔═██╗   ╚██╔╝  ██║╚██╗██║██╔══╝   ██╔██╗ ██╔══██║██║   ██║   ██║   ██╔══██║
  ██║  ██╗   ██║   ██║ ╚████║███████╗██╔╝ ██╗██║  ██║╚██████╔╝   ██║   ██║  ██║
  ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝

  {Colors.DIM}────────────────{Colors.END} {Colors.BOLD}{Colors.BRIGHT_GREEN}AUTHENTICATION & LICENSING ENGINE{Colors.END} {Colors.DIM}────────────────{Colors.END}
{Colors.END}"""

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                         CONFIGURATION SECTION                             ║
# ╚════════════════════════════════════════════════════════════════════════════╝
kynexauthapp = api(
    name="YOUR_APP_NAME",       # Application Name from dashboard
    ownerid="YOUR_APP_KEY",     # Application Key (Owner ID)
    version="1.0",              # Application Version
    url="https://kynexauth.com/api/v1/client",
    debug=False                 # Set True to print raw HTTP requests/responses
)
KynexAuthApp = kynexauthapp


def set_title(title: str):
    """Set terminal window title"""
    if os.name == "nt":
        os.system(f"title {title}")
    else:
        sys.stdout.write(f'\x1b]0;{title}\x07')


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_line(char: str = "─", length: int = 76):
    """Print decorative line"""
    print(f"  {Colors.DIM}{char * length}{Colors.END}")


def print_section(title: str):
    """Print styled section header"""
    print(f"\n  {Colors.BRIGHT_CYAN}┌───{Colors.END} {Colors.BOLD}{Colors.BRIGHT_GREEN}{title}{Colors.END} {Colors.BRIGHT_CYAN}{'─' * (66 - len(title))}┐{Colors.END}\n")


def print_info(message: str, icon: str = "ℹ"):
    """Print info message"""
    print(f"  {Colors.BRIGHT_CYAN}[{icon}]{Colors.END} {message}")


def print_success(message: str):
    """Print success message"""
    print(f"  {Colors.BRIGHT_GREEN}[✓]{Colors.END} {Colors.GREEN}{message}{Colors.END}")


def print_error(message: str):
    """Print error message"""
    print(f"  {Colors.RED}[✗]{Colors.END} {Colors.RED}{message}{Colors.END}")


def print_warning(message: str):
    """Print warning message"""
    print(f"  {Colors.BRIGHT_YELLOW}[!]{Colors.END} {Colors.BRIGHT_YELLOW}{message}{Colors.END}")


def print_input_prompt(text: str) -> str:
    """Print styled input prompt with clean colon separation so text never mixes"""
    return input(f"  {Colors.BRIGHT_CYAN}[›]{Colors.END} {Colors.BOLD}{text:<16}{Colors.END} {Colors.CYAN}:{Colors.END} ").strip()


def loading_animation(message: str, duration: float = 3):
    """Animated loading sequence"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start = time.time()
    
    while time.time() - start < duration:
        for frame in frames:
            print(f"\r {Colors.BRIGHT_CYAN}{frame}{Colors.END} {message}", end="", flush=True)
            time.sleep(0.1)
    print(f"\r {Colors.BRIGHT_GREEN}✓{Colors.END} {message}" + " " * 20)


def print_user_data(app: api):
    """Display user data in stylish format"""
    user = app.user_data
    
    print_section("USER PROFILE INFORMATION")
    
    # User data table
    user_info = [
        ("Username", user.username),
        ("IP Address", user.ip),
        ("Hardware ID", user.hwid),
        ("Created At", user.createdate),
        ("Last Login", user.lastlogin),
    ]
    
    for label, value in user_info:
        print(f" {Colors.BRIGHT_CYAN}├─{Colors.END} {Colors.BOLD}{label:<16}{Colors.END} {Colors.GREEN}::{Colors.END} {Colors.DIM}{value}{Colors.END}")
    
    # Subscription info
    print_section("SUBSCRIPTION STATUS")
    
    if user.subscriptions:
        for idx, sub in enumerate(user.subscriptions, 1):
            status = f"{Colors.BRIGHT_GREEN}[ACTIVE]{Colors.END}"
            print(f" {Colors.BRIGHT_CYAN}├─{Colors.END} Plan #{idx}: {Colors.BOLD}{sub.name}{Colors.END}")
            print(f" {Colors.BRIGHT_CYAN}│  └─{Colors.END} Status: {status} | Expiry: {Colors.YELLOW}{sub.expiry}{Colors.END}")
    else:
        print(f" {Colors.BRIGHT_CYAN}├─{Colors.END} {Colors.GREEN}Premium Plan{Colors.END} {Colors.BRIGHT_GREEN}[LIFETIME]{Colors.END}")


def print_menu():
    """Print stylish main menu"""
    print_section("AUTHENTICATION OPTIONS")
    
    options = [
        ("1", "LOGIN", "Access with Username & Password"),
        ("2", "REGISTER", "Create account with License Key"),
        ("3", "UPGRADE", "Extend account using License Key"),
        ("4", "LICENSE", "Fast instant access via License Key"),
    ]
    
    for idx, (num, title, desc) in enumerate(options):
        connector = "├─" if idx < len(options) - 1 else "└─"
        print(f" {Colors.BRIGHT_CYAN}{connector}{Colors.END} {Colors.BOLD}[{num}]{Colors.END} {Colors.BRIGHT_GREEN}{title:<15}{Colors.END} {Colors.DIM}| {desc}{Colors.END}")
    print()


def session_checker():
    """Background thread to keep verifying session integrity"""
    while True:
        time.sleep(30)
        if not KynexAuthApp.check():
            print_error("Session expired or invalidated by server. Exiting...")
            os._exit(1)


def handle_login():
    """Handle login flow"""
    print_section("USER LOGIN")
    username = print_input_prompt("Username")
    password = print_input_prompt("Password")
    
    loading_animation("Verifying credentials", 2)
    KynexAuthApp.login(username, password)


def handle_register():
    """Handle registration flow"""
    print_section("NEW ACCOUNT REGISTRATION")
    username = print_input_prompt("Username")
    password = print_input_prompt("Password")
    key = print_input_prompt("License Key")
    email = print_input_prompt("Email [Optional]")
    
    loading_animation("Creating new account", 2)
    KynexAuthApp.register(username, password, key, email)


def handle_upgrade():
    """Handle upgrade flow"""
    print_section("ACCOUNT UPGRADE")
    username = print_input_prompt("Username")
    key = print_input_prompt("License Key")
    
    loading_animation("Processing upgrade", 2)
    KynexAuthApp.upgrade(username, key)


def handle_license():
    """Handle license key only flow"""
    print_section("LICENSE KEY VERIFICATION")
    key = print_input_prompt("License Key")
    
    loading_animation("Verifying license key", 2)
    KynexAuthApp.license(key)


def main():
    """Main application entry point"""
    clear_screen()
    set_title(f"KynexAuth - {time.strftime('%b %d %Y %H:%M:%S')}")
    
    print(PREMIUM_BANNER)
    
    print_info("Connecting to secure authentication server...", ">>")
    loading_animation("Establishing secure connection", 2.5)
    
    # Initialize API Session
    if not KynexAuthApp.init():
        print_error(f"Initialization Failed: {KynexAuthApp.response.message}")
        
        if KynexAuthApp.app_data.downloadLink:
            print_warning(f"Update available: {KynexAuthApp.app_data.downloadLink}")
        
        time.sleep(3)
        sys.exit(1)
    
    print_success("Connected and session secured!\n")
    
    # Display menu
    print_menu()
    
    choice = print_input_prompt("Select option (1-4)").strip()
    
    # Route to appropriate handler
    handlers = {
        "1": handle_login,
        "2": handle_register,
        "3": handle_upgrade,
        "4": handle_license,
    }
    
    if choice not in handlers:
        print_error("Invalid selection! Please choose 1, 2, 3, or 4.")
        time.sleep(2)
        sys.exit(1)
    
    handlers[choice]()
    
    # Handle authentication result
    if not KynexAuthApp.response.success:
        print_error(f"Authentication Failed: {KynexAuthApp.response.message}")
        time.sleep(4)
        sys.exit(1)
    
    print_success(f"Authentication Successful: {KynexAuthApp.response.message}")
    
    # Display user data
    print_user_data(KynexAuthApp)
    
    # Start background session monitor
    session_thread = threading.Thread(target=session_checker, daemon=True)
    session_thread.start()
    
    # Application payload section
    print_line("═", 80)
    print(f"{Colors.BOLD}{Colors.BRIGHT_GREEN}")
    print(" ┌──────────────────────────────────────────────────────────────────────┐")
    print(" │  WELCOME TO PROTECTED APPLICATION PAYLOAD                           │")
    print(" │  You can now execute your main application / script here!           │")
    print(" │                                                                      │")
    print(" │  :: All security validations passed                                 │")
    print(" │  :: Session monitoring active                                       │")
    print(" │  :: Ready for execution                                             │")
    print(" └──────────────────────────────────────────────────────────────────────┘")
    print(f"{Colors.END}")
    print_line("═", 80)
    print()
    
    input(f" {Colors.BRIGHT_CYAN}[>>>]{Colors.END} {Colors.BOLD}Press ENTER to exit...{Colors.END}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!!] Program terminated by user.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)