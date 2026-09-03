"""
KynexAuth - Modern Python GUI Loader
─────────────────────────────────────────────────────────────────────────────
1:1 Pixel-Perfect Recreation of the official C# GunaUI2 GuiExample.
Matches all colors, borderless custom titlebar, draggable header, tabs,
inputs, animated toggle switches, sliders, and multi-tab MainForm.
─────────────────────────────────────────────────────────────────────────────
"""

import sys
import os
import time
import threading
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Callable
from kynexauth import api

# -------------------------------------------------------------
# CONFIGURE YOUR APP CREDENTIALS HERE
# -------------------------------------------------------------
kynexauthapp = api(
    name="YOUR_APP_NAME",       # Application Name from dashboard
    ownerid="YOUR_APP_KEY",     # Application Key (Owner ID)
    version="1.0",              # Application Version
    url="https://kynexauth.com/api/v1/client",
    debug=False                 # Set True to print raw HTTP requests/responses
)
KynexAuthApp = kynexauthapp

# -------------------------------------------------------------
# EXACT GUNAUI2 C# COLOR PALETTE
# -------------------------------------------------------------
COLOR_BG_DARK       = "#0B0E14"  # rgb(11, 14, 20)
COLOR_TOPBAR        = "#0E121C"  # rgb(14, 18, 28)
COLOR_CARD          = "#121622"  # rgb(18, 22, 34)
COLOR_CARD_BORDER   = "#2D374B"  # rgb(45, 55, 75)
COLOR_INPUT_BG      = "#121622"  # rgb(18, 22, 34)
COLOR_INPUT_BORDER  = "#2D374B"  # rgb(45, 55, 75)
COLOR_ACCENT_INDIGO = "#6366F1"  # rgb(99, 102, 241) - Guna2 Indigo
COLOR_ACCENT_HOVER  = "#818CF8"  # rgb(129, 140, 248)
COLOR_TAB_ACTIVE    = "#161B2A"  # rgb(22, 27, 42)

COLOR_TEXT_WHITE    = "#FFFFFF"
COLOR_TEXT_MUTED    = "#94A3B8"  # rgb(148, 163, 184)
COLOR_TEXT_PLACEHOLDER = "#64748B"  # rgb(100, 116, 139)
COLOR_SUCCESS_GREEN = "#10B981"
COLOR_ERROR_RED     = "#EF4444"


class DraggableWindow:
    """Helper to enable smooth window dragging from the custom top bar."""

    def __init__(self, window: tk.Toplevel or tk.Tk, drag_widget: tk.Widget):
        self.window = window
        self.drag_widget = drag_widget
        self._offset_x = 0
        self._offset_y = 0

        drag_widget.bind("<ButtonPress-1>", self._on_press)
        drag_widget.bind("<B1-Motion>", self._on_motion)

    def _on_press(self, event):
        self._offset_x = event.x_root - self.window.winfo_x()
        self._offset_y = event.y_root - self.window.winfo_y()

    def _on_motion(self, event):
        x = event.x_root - self._offset_x
        y = event.y_root - self._offset_y
        self.window.geometry(f"+{x}+{y}")


class GunaTextBox(tk.Frame):
    """Custom stylized text entry matching Guna2TextBox in C#."""

    def __init__(self, parent, placeholder: str = "", is_password: bool = False, **kwargs):
        super().__init__(parent, bg=COLOR_INPUT_BORDER, padx=1, pady=1, **kwargs)
        self.inner = tk.Frame(self, bg=COLOR_INPUT_BG, padx=14, pady=10)
        self.inner.pack(fill="both", expand=True)

        self.placeholder = placeholder
        self.is_password = is_password
        self._showing_placeholder = False

        self.entry = tk.Entry(
            self.inner,
            bg=COLOR_INPUT_BG,
            fg=COLOR_TEXT_WHITE,
            insertbackground=COLOR_TEXT_WHITE,
            relief="flat",
            font=("Segoe UI", 10),
        )
        self.entry.pack(fill="both", expand=True)

        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

        if placeholder:
            self._set_placeholder()

    def _set_placeholder(self):
        self._showing_placeholder = True
        self.entry.config(fg=COLOR_TEXT_PLACEHOLDER)
        if self.is_password:
            self.entry.config(show="")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)

    def _on_focus_in(self, event):
        self.config(bg=COLOR_ACCENT_INDIGO)
        if self._showing_placeholder:
            self._showing_placeholder = False
            self.entry.delete(0, tk.END)
            self.entry.config(fg=COLOR_TEXT_WHITE)
            if self.is_password:
                self.entry.config(show="●")

    def _on_focus_out(self, event):
        self.config(bg=COLOR_INPUT_BORDER)
        if not self.entry.get().strip():
            self._set_placeholder()

    def get(self) -> str:
        if self._showing_placeholder:
            return ""
        return self.entry.get().strip()

    def set(self, text: str):
        self._showing_placeholder = False
        self.entry.config(fg=COLOR_TEXT_WHITE)
        if self.is_password:
            self.entry.config(show="●")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)


class GunaToggle(tk.Canvas):
    """Custom toggle switch matching Guna2ToggleSwitch in C#."""

    def __init__(self, parent, width=44, height=22, default=False, command: Optional[Callable] = None, **kwargs):
        super().__init__(parent, width=width, height=height, bg=COLOR_CARD, highlightthickness=0, cursor="hand2", **kwargs)
        self.w = width
        self.h = height
        self.command = command
        self.state = default
        self.bind("<Button-1>", self._on_click)
        self._draw()

    def _draw(self):
        self.delete("all")
        r = self.h / 2
        bg_color = COLOR_ACCENT_INDIGO if self.state else "#2D374B"
        
        # Rounded pill track
        self.create_arc((0, 0, self.h, self.h), start=90, extent=180, fill=bg_color, outline=bg_color)
        self.create_arc((self.w - self.h, 0, self.w, self.h), start=270, extent=180, fill=bg_color, outline=bg_color)
        self.create_rectangle((r, 0, self.w - r, self.h), fill=bg_color, outline=bg_color)

        # Thumb Circle
        pad = 3
        dia = self.h - (pad * 2)
        cx = (self.w - r) if self.state else r
        self.create_oval(
            cx - (dia / 2),
            pad,
            cx + (dia / 2),
            pad + dia,
            fill="#FFFFFF",
            outline="#FFFFFF",
        )

    def _on_click(self, event):
        self.state = not self.state
        self._draw()
        if self.command:
            self.command(self.state)

    def get(self) -> bool:
        return self.state


class MainForm(tk.Toplevel):
    """1:1 Recreation of C# MainForm (Protected Application Dashboard)."""

    def __init__(self, login_form: tk.Tk):
        super().__init__(login_form)
        self.login_form = login_form
        self.title("KynexAuth Dashboard")
        self.geometry("720x500")
        self.resizable(False, False)
        self.overrideredirect(True)  # Frameless like C# Guna2 Form
        self.configure(bg=COLOR_BG_DARK)

        # 1px border around whole window for sleek high-end look
        self.config(highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)

        # Center on screen
        self.update_idletasks()
        w = 720
        h = 500
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        self._build_ui()
        self._start_watchdog()

    def _build_ui(self):
        # 1. Custom Top Bar (46px, Draggable)
        top_bar = tk.Frame(self, bg=COLOR_TOPBAR, height=46)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)

        DraggableWindow(self, top_bar)

        lbl_title = tk.Label(
            top_bar,
            text="KYNEXAUTH DASHBOARD v1.0",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT_WHITE,
            bg=COLOR_TOPBAR,
        )
        lbl_title.pack(side="left", padx=18)
        DraggableWindow(self, lbl_title)

        # Window Controls
        btn_close = tk.Button(
            top_bar,
            text="✕",
            font=("Segoe UI", 10),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_TOPBAR,
            activebackground=COLOR_ERROR_RED,
            activeforeground=COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            width=4,
            cursor="hand2",
            command=self.on_close,
        )
        btn_close.pack(side="right", fill="y")

        btn_min = tk.Button(
            top_bar,
            text="—",
            font=("Segoe UI", 10),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_TOPBAR,
            activebackground=COLOR_CARD,
            activeforeground=COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            width=4,
            cursor="hand2",
            command=self.iconify,
        )
        btn_min.pack(side="right", fill="y")

        # 2. Main Body (Sidebar + Content Panel)
        body = tk.Frame(self, bg=COLOR_BG_DARK)
        body.pack(fill="both", expand=True)

        # Sidebar Panel (170px width, #0E121C)
        sidebar = tk.Frame(body, bg=COLOR_TOPBAR, width=170)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self.current_nav = "AIMBOT"
        self.nav_buttons = {}

        nav_items = [
            ("AIMBOT", "🎯  Aimbot"),
            ("SNIPER", "🔭  Sniper"),
            ("MISC", "⚙️  Misc"),
            ("SETTING", "👤  Profile"),
        ]

        for key, text in nav_items:
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Segoe UI", 10, "bold"),
                fg=COLOR_TEXT_WHITE if key == "AIMBOT" else COLOR_TEXT_MUTED,
                bg=COLOR_TAB_ACTIVE if key == "AIMBOT" else COLOR_TOPBAR,
                activebackground=COLOR_TAB_ACTIVE,
                activeforeground=COLOR_TEXT_WHITE,
                relief="flat",
                bd=0,
                anchor="w",
                padx=20,
                pady=14,
                cursor="hand2",
                command=lambda k=key: self.show_tab(k),
            )
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        btn_logout = tk.Button(
            sidebar,
            text="🚪  Logout",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_ERROR_RED,
            bg=COLOR_TOPBAR,
            activebackground=COLOR_ERROR_RED,
            activeforeground=COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            anchor="w",
            padx=20,
            pady=14,
            cursor="hand2",
            command=self.on_close,
        )
        btn_logout.pack(side="bottom", fill="x")

        # Content Area
        self.content_area = tk.Frame(body, bg=COLOR_BG_DARK, padx=22, pady=20)
        self.content_area.pack(side="right", fill="both", expand=True)

        self.tabs = {}
        self.tabs["AIMBOT"] = self._build_aimbot_tab()
        self.tabs["SNIPER"] = self._build_sniper_tab()
        self.tabs["MISC"] = self._build_misc_tab()
        self.tabs["SETTING"] = self._build_setting_tab()

        self.show_tab("AIMBOT")

    def show_tab(self, tab_key: str):
        self.current_nav = tab_key

        for k, btn in self.nav_buttons.items():
            if k == tab_key:
                btn.config(bg=COLOR_TAB_ACTIVE, fg=COLOR_TEXT_WHITE)
            else:
                btn.config(bg=COLOR_TOPBAR, fg=COLOR_TEXT_MUTED)

        for k, tab_frame in self.tabs.items():
            if k == tab_key:
                tab_frame.pack(fill="both", expand=True)
            else:
                tab_frame.pack_forget()

    def _build_aimbot_tab(self) -> tk.Frame:
        pnl = tk.Frame(self.content_area, bg=COLOR_BG_DARK)

        tk.Label(
            pnl,
            text="AIMBOT CONFIGURATION",
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_TEXT_WHITE,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w", pady=(0, 14))

        card = tk.Frame(pnl, bg=COLOR_CARD, padx=18, pady=18, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True)

        toggles = [
            ("Enable Memory Aimbot", True),
            ("Draw Field of View Circle", True),
            ("Silent Aim (Memory Bypass)", False),
        ]
        for text, default in toggles:
            row = tk.Frame(card, bg=COLOR_CARD)
            row.pack(fill="x", pady=7)
            tk.Label(row, text=text, font=("Segoe UI", 10), fg=COLOR_TEXT_WHITE, bg=COLOR_CARD).pack(side="left")
            GunaToggle(row, default=default).pack(side="right")

        # FOV Slider
        row_fov = tk.Frame(card, bg=COLOR_CARD)
        row_fov.pack(fill="x", pady=(12, 0))
        tk.Label(row_fov, text="Aimbot FOV Range (30 - 360°)", font=("Segoe UI", 9), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(side="left")
        lbl_fov_val = tk.Label(row_fov, text="120°", font=("Segoe UI", 9, "bold"), fg=COLOR_ACCENT_INDIGO, bg=COLOR_CARD)
        lbl_fov_val.pack(side="right")

        s_fov = tk.Scale(
            card, from_=30, to_=360, orient="horizontal", bg=COLOR_CARD, fg=COLOR_TEXT_WHITE,
            troughcolor=COLOR_BG_DARK, highlightthickness=0, activebackground=COLOR_ACCENT_INDIGO,
            command=lambda v: lbl_fov_val.config(text=f"{v}°"),
        )
        s_fov.set(120)
        s_fov.pack(fill="x", pady=(0, 8))

        # Smooth Slider
        row_smooth = tk.Frame(card, bg=COLOR_CARD)
        row_smooth.pack(fill="x", pady=(6, 0))
        tk.Label(row_smooth, text="Smooth Aim Speed (1 - 30)", font=("Segoe UI", 9), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(side="left")
        lbl_smooth_val = tk.Label(row_smooth, text="12", font=("Segoe UI", 9, "bold"), fg=COLOR_ACCENT_INDIGO, bg=COLOR_CARD)
        lbl_smooth_val.pack(side="right")

        s_smooth = tk.Scale(
            card, from_=1, to_=30, orient="horizontal", bg=COLOR_CARD, fg=COLOR_TEXT_WHITE,
            troughcolor=COLOR_BG_DARK, highlightthickness=0, activebackground=COLOR_ACCENT_INDIGO,
            command=lambda v: lbl_smooth_val.config(text=f"{v}"),
        )
        s_smooth.set(12)
        s_smooth.pack(fill="x", pady=(0, 6))

        return pnl

    def _build_sniper_tab(self) -> tk.Frame:
        pnl = tk.Frame(self.content_area, bg=COLOR_BG_DARK)

        tk.Label(
            pnl,
            text="SNIPER ASSIST MODULES",
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_TEXT_WHITE,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w", pady=(0, 14))

        card = tk.Frame(pnl, bg=COLOR_CARD, padx=18, pady=18, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True)

        toggles = [
            ("Fast Scope Auto-Trigger", True),
            ("Quick Weapon Switch on Fire", False),
            ("Bullet Velocity Prediction", True),
        ]
        for text, default in toggles:
            row = tk.Frame(card, bg=COLOR_CARD)
            row.pack(fill="x", pady=8)
            tk.Label(row, text=text, font=("Segoe UI", 10), fg=COLOR_TEXT_WHITE, bg=COLOR_CARD).pack(side="left")
            GunaToggle(row, default=default).pack(side="right")

        return pnl

    def _build_misc_tab(self) -> tk.Frame:
        pnl = tk.Frame(self.content_area, bg=COLOR_BG_DARK)

        tk.Label(
            pnl,
            text="MISCELLANEOUS SETTINGS",
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_TEXT_WHITE,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w", pady=(0, 14))

        card = tk.Frame(pnl, bg=COLOR_CARD, padx=18, pady=18, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True)

        toggles = [
            ("Automatic Bunny Hop", False),
            ("Stream-Proof / OBS Bypass Mode", True),
            ("Show Watermark Overlay", True),
        ]
        for text, default in toggles:
            row = tk.Frame(card, bg=COLOR_CARD)
            row.pack(fill="x", pady=8)
            tk.Label(row, text=text, font=("Segoe UI", 10), fg=COLOR_TEXT_WHITE, bg=COLOR_CARD).pack(side="left")
            GunaToggle(row, default=default).pack(side="right")

        return pnl

    def _build_setting_tab(self) -> tk.Frame:
        pnl = tk.Frame(self.content_area, bg=COLOR_BG_DARK)

        tk.Label(
            pnl,
            text="ACCOUNT PROFILE & HARDWARE INFO",
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_TEXT_WHITE,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w", pady=(0, 14))

        card = tk.Frame(pnl, bg=COLOR_CARD, padx=18, pady=18, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True)

        user = KynexAuthApp.user_data
        expiry_text = user.subscriptions[0].expiry if user.subscriptions else "Lifetime / Active"

        rows = [
            ("Username", user.username or "N/A"),
            ("Subscription Expiry", expiry_text, COLOR_SUCCESS_GREEN),
            ("Protected HWID", user.hwid or "N/A"),
            ("IP Address", user.ip or "127.0.0.1"),
            ("Last Login", user.lastlogin or "Just Now"),
            ("Created Date", user.createdate or "N/A"),
        ]

        for item in rows:
            lbl = item[0]
            val = item[1]
            col = item[2] if len(item) > 2 else COLOR_TEXT_WHITE

            r = tk.Frame(card, bg=COLOR_CARD)
            r.pack(fill="x", pady=5)
            tk.Label(r, text=lbl, font=("Segoe UI", 9), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(side="left")
            tk.Label(r, text=val, font=("Segoe UI", 9, "bold"), fg=col, bg=COLOR_CARD).pack(side="right")

        return pnl

    def _start_watchdog(self):
        def watch():
            while True:
                time.sleep(30)
                if not KynexAuthApp.check():
                    self.after(0, self.on_close)
                    break
        threading.Thread(target=watch, daemon=True).start()

    def on_close(self):
        KynexAuthApp.logout()
        self.destroy()
        self.login_form.destroy()
        sys.exit(0)


class LoginForm(tk.Tk):
    """1:1 Exact Recreation of C# GunaUI2 LoginForm."""

    def __init__(self):
        super().__init__()
        self.title("KynexAuth Loader")
        self.geometry("420x440")
        self.resizable(False, False)
        self.overrideredirect(True)  # Frameless like C# Guna2 Form
        self.configure(bg=COLOR_BG_DARK)

        # 1px border around whole window for sleek outline
        self.config(highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)

        # Center on screen
        self.update_idletasks()
        w = 420
        h = 440
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.current_mode = "USER"
        self._build_ui()
        self._init_connection()

    def _build_ui(self):
        # 1. Top Panel (46px height, Dark, Draggable)
        top_panel = tk.Frame(self, bg=COLOR_TOPBAR, height=46)
        top_panel.pack(fill="x", side="top")
        top_panel.pack_propagate(False)

        DraggableWindow(self, top_panel)

        lbl_title = tk.Label(
            top_panel,
            text="KYNEXAUTH LOADER v1.0",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT_WHITE,
            bg=COLOR_TOPBAR,
        )
        lbl_title.pack(side="left", padx=16)
        DraggableWindow(self, lbl_title)

        btn_close = tk.Button(
            top_panel,
            text="✕",
            font=("Segoe UI", 10),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_TOPBAR,
            activebackground=COLOR_ERROR_RED,
            activeforeground=COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            width=4,
            cursor="hand2",
            command=self.destroy,
        )
        btn_close.pack(side="right", fill="y")

        btn_min = tk.Button(
            top_panel,
            text="—",
            font=("Segoe UI", 10),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_TOPBAR,
            activebackground=COLOR_CARD,
            activeforeground=COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            width=4,
            cursor="hand2",
            command=self.iconify,
        )
        btn_min.pack(side="right", fill="y")

        # 2. Main Container Panel
        container = tk.Frame(self, bg=COLOR_BG_DARK, padx=28, pady=16)
        container.pack(fill="both", expand=True)

        # Tab Navigation Header (Exact C# button style)
        tab_bar = tk.Frame(container, bg=COLOR_BG_DARK)
        tab_bar.pack(fill="x", pady=(0, 16))

        self.btn_tab_user = tk.Button(
            tab_bar,
            text="USER LOGIN",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXT_WHITE,
            bg=COLOR_TAB_ACTIVE,
            activebackground=COLOR_TAB_ACTIVE,
            activeforeground=COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            pady=7,
            cursor="hand2",
            command=lambda: self.switch_mode("USER"),
        )
        self.btn_tab_user.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_tab_key = tk.Button(
            tab_bar,
            text="KEY LOGIN",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG_DARK,
            activebackground=COLOR_BG_DARK,
            activeforeground=COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            pady=7,
            cursor="hand2",
            command=lambda: self.switch_mode("KEY"),
        )
        self.btn_tab_key.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_tab_reg = tk.Button(
            tab_bar,
            text="REGISTER",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG_DARK,
            activebackground=COLOR_BG_DARK,
            activeforeground=COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            pady=7,
            cursor="hand2",
            command=lambda: self.switch_mode("REGISTER"),
        )
        self.btn_tab_reg.pack(side="left", expand=True, fill="x", padx=2)

        # Form Inputs Frame
        self.form_box = tk.Frame(container, bg=COLOR_BG_DARK)
        self.form_box.pack(fill="both", expand=True)

        self.txt_username = GunaTextBox(self.form_box, placeholder="Username")
        self.txt_password = GunaTextBox(self.form_box, placeholder="Password", is_password=True)
        self.txt_license  = GunaTextBox(self.form_box, placeholder="License Key")
        self.txt_email    = GunaTextBox(self.form_box, placeholder="Email Address (Optional)")

        # Action Button (Guna2 Indigo Button)
        self.btn_action = tk.Button(
            container,
            text="LOGIN",
            font=("Segoe UI", 11, "bold"),
            fg=COLOR_TEXT_WHITE,
            bg=COLOR_ACCENT_INDIGO,
            activebackground=COLOR_ACCENT_HOVER,
            activeforeground=COLOR_TEXT_WHITE,
            relief="flat",
            bd=0,
            pady=11,
            cursor="hand2",
            command=self._on_action_click,
        )
        self.btn_action.pack(fill="x", pady=(12, 8))

        # Status Label
        self.lbl_status = tk.Label(
            container,
            text="Ready. Please enter your credentials.",
            font=("Segoe UI", 9),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG_DARK,
            wraplength=350,
        )
        self.lbl_status.pack(fill="x", pady=(0, 4))

        self.switch_mode("USER")

    def switch_mode(self, mode: str):
        self.current_mode = mode

        tabs = [
            ("USER", self.btn_tab_user),
            ("KEY", self.btn_tab_key),
            ("REGISTER", self.btn_tab_reg),
        ]
        for name, btn in tabs:
            if name == mode:
                btn.config(bg=COLOR_TAB_ACTIVE, fg=COLOR_TEXT_WHITE)
            else:
                btn.config(bg=COLOR_BG_DARK, fg=COLOR_TEXT_MUTED)

        self.txt_username.pack_forget()
        self.txt_password.pack_forget()
        self.txt_license.pack_forget()
        self.txt_email.pack_forget()

        if mode == "USER":
            self.txt_username.pack(fill="x", pady=6)
            self.txt_password.pack(fill="x", pady=6)
            self.btn_action.config(text="LOGIN")
            self.geometry("420x420")

        elif mode == "KEY":
            self.txt_license.pack(fill="x", pady=12)
            self.btn_action.config(text="LICENSE LOGIN")
            self.geometry("420x360")

        elif mode == "REGISTER":
            self.txt_username.pack(fill="x", pady=4)
            self.txt_password.pack(fill="x", pady=4)
            self.txt_license.pack(fill="x", pady=4)
            self.txt_email.pack(fill="x", pady=4)
            self.btn_action.config(text="REGISTER")
            self.geometry("420x510")

    def set_status(self, text: str, color: str = COLOR_TEXT_MUTED):
        self.lbl_status.config(text=text, fg=color)

    def _init_connection(self):
        def worker():
            self.set_status("Connecting to KynexAuth server...", COLOR_TEXT_MUTED)
            if KynexAuthApp.init():
                self.set_status("Connected. Ready to authenticate.", COLOR_SUCCESS_GREEN)
            else:
                self.set_status(KynexAuthApp.response.message, COLOR_ERROR_RED)

        threading.Thread(target=worker, daemon=True).start()

    def _on_action_click(self):
        if not KynexAuthApp.initialized:
            self.set_status("Connecting... Please wait.", COLOR_TEXT_MUTED)
            self._init_connection()
            return

        self.btn_action.config(state="disabled")
        self.set_status("Authenticating...", COLOR_TEXT_MUTED)

        def worker():
            success = False
            mode = self.current_mode

            if mode == "USER":
                u = self.txt_username.get()
                p = self.txt_password.get()
                if not u or not p:
                    self.after(0, lambda: self._on_result(False, "Please enter username and password."))
                    return
                success = KynexAuthApp.login(u, p)

            elif mode == "KEY":
                k = self.txt_license.get()
                if not k:
                    self.after(0, lambda: self._on_result(False, "Please enter your license key."))
                    return
                success = KynexAuthApp.license(k)

            elif mode == "REGISTER":
                u = self.txt_username.get()
                p = self.txt_password.get()
                k = self.txt_license.get()
                e = self.txt_email.get()
                if not u or not p or not k:
                    self.after(0, lambda: self._on_result(False, "All fields except email are required."))
                    return
                success = KynexAuthApp.register(u, p, k, e)

            msg = KynexAuthApp.response.message or ("Success!" if success else "Authentication failed.")
            self.after(0, lambda: self._on_result(success, msg))

        threading.Thread(target=worker, daemon=True).start()

    def _on_result(self, success: bool, msg: str):
        self.btn_action.config(state="normal")
        if success:
            self.set_status(f"✓ {msg}", COLOR_SUCCESS_GREEN)
            self.withdraw()  # Hide login form
            MainForm(self)   # Open C# style MainForm
        else:
            self.set_status(f"✗ {msg}", COLOR_ERROR_RED)


if __name__ == "__main__":
    app = LoginForm()
    app.mainloop()
