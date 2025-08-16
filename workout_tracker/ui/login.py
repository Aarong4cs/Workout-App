import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from tkinter import messagebox
from ..utils import hash_password
from .base import BasePage
from .main_menu import MainMenuPage

class LoginPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        form = ttk.Labelframe(self.content, text="Welcome", padding=20, bootstyle=INFO)
        form.pack(expand=True, ipadx=10, ipady=10)

        ttk.Label(form, text="Login", font="-size 18 -weight bold").pack(pady=(0, 15))
        ttk.Label(form, text="Username").pack(anchor=W)
        self.username = ttk.Entry(form)
        self.username.pack(ipady=6, pady=(0, 10), fill=X)
        ttk.Label(form, text="Password").pack(anchor=W)
        self.password = ttk.Entry(form, show="*")
        self.password.pack(ipady=6, pady=(0, 10), fill=X)

        ttk.Button(form, text="Login", command=self._login, bootstyle=SUCCESS).pack(fill=X, pady=6)
        ttk.Button(form, text="Register", command=self._register, bootstyle=PRIMARY).pack(fill=X, pady=6)

    def _login(self):
        u, p = self.username.get().strip(), self.password.get().strip()
        if u in self.app.users and self.app.users[u].password_hash == hash_password(p):
            self.app.logged_in_user = self.app.users[u]
            self.app.show_frame(MainMenuPage)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def _register(self):
        u, p = self.username.get().strip(), self.password.get().strip()
        if not u or not p:
            messagebox.showerror("Error", "Please enter a username and password.")
            return
        if u in self.app.users:
            messagebox.showerror("Error", "Username already exists.")
            return
        from ..models import User
        self.app.users[u] = User(u, hash_password(p))
        self.app.save_db()
        ToastNotification(title="Success", message="Registered successfully!", duration=2500, bootstyle=SUCCESS).show_toast()

