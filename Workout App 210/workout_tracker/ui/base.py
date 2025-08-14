import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class BasePage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Header with theme switcher
        self.header = ttk.Frame(self)
        self.header.pack(fill=X)

        self.back_btn = ttk.Button(
            self.header,
            text="⬅ Back to Main Menu",
            command=lambda: app.show_frame(self._main_menu_cls()),
            bootstyle=SECONDARY,
        )
        self.back_btn.pack(side=LEFT, padx=10, pady=10)

        self.user_lbl = ttk.Label(self.header, text="", anchor=E)
        self.user_lbl.pack(side=RIGHT, padx=(6, 10), pady=10)

        # Theme dropdown
        dd_frame = ttk.Frame(self.header)
        dd_frame.pack(side=RIGHT, padx=10)
        ttk.Label(dd_frame, text="Theme:").pack(side=LEFT, padx=(0, 6))

        self.theme_var = tk.StringVar(value=app.style.theme.name)
        self.theme_dd = ttk.Combobox(
            dd_frame,
            textvariable=self.theme_var,
            values=sorted(app.style.theme_names()),
            width=16,
            state="readonly",
        )
        self.theme_dd.pack(side=LEFT)
        self.theme_dd.bind("<<ComboboxSelected>>", self._change_theme)

        ttk.Separator(self).pack(fill=X, pady=(0, 6))

        self.content = ttk.Frame(self, padding=10)
        self.content.pack(fill=BOTH, expand=True)

    def _main_menu_cls(self):
        from .main_menu import MainMenuPage
        return MainMenuPage

    def _change_theme(self, _e=None):
        new_theme = self.theme_var.get()
        try:
            self.app.style.theme_use(new_theme)
        except Exception as err:
            messagebox.showerror("Theme Error", str(err))

    def update_header(self):
        from .main_menu import MainMenuPage
        if isinstance(self, MainMenuPage):
            if self.back_btn.winfo_manager():
                self.back_btn.pack_forget()
        else:
            if not self.back_btn.winfo_manager():
                self.back_btn.pack(side=LEFT, padx=10, pady=10)
        if self.app.logged_in_user:
            self.user_lbl.config(text=f"Logged in as: {self.app.logged_in_user.username}")
        else:
            self.user_lbl.config(text="")

