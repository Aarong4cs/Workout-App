import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from tkinter import messagebox
from .base import BasePage

class RoutineBuilderPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        left = ttk.Labelframe(self.content, text="Pick Exercises", padding=10, bootstyle=INFO)
        left.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        right = ttk.Labelframe(self.content, text="Routine", padding=10, bootstyle=PRIMARY)
        right.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(left, show="tree")
        self.tree.pack(fill=BOTH, expand=True)

        self.listbox = tk.Listbox(right, font=("Arial", 13))
        self.listbox.pack(fill=BOTH, expand=True)

        btns = ttk.Frame(right)
        btns.pack(fill=X, pady=8)
        ttk.Button(btns, text="Add ➕", command=self._add, bootstyle=SUCCESS).pack(side=LEFT, expand=True, fill=X, padx=4)
        ttk.Button(btns, text="Remove 🗑", command=self._remove, bootstyle=DANGER).pack(side=LEFT, expand=True, fill=X, padx=4)

        bottom = ttk.Frame(right)
        bottom.pack(fill=X, pady=6)
        ttk.Button(bottom, text="Save", command=self._save, bootstyle=PRIMARY).pack(side=LEFT, expand=True, fill=X, padx=4)
        ttk.Button(bottom, text="Start ▶", command=self._start_now, bootstyle=WARNING).pack(side=LEFT, expand=True, fill=X, padx=4)

    def on_show(self):
        self.tree.delete(*self.tree.get_children())
        for mg, exercises in sorted(self.app.logged_in_user.exercise_tree.items()):
            parent = self.tree.insert("", "end", text=mg, open=True)
            for ex in sorted(exercises):
                self.tree.insert(parent, "end", text=ex)

    def _add(self):
        sel = self.tree.focus()
        if not sel:
            return
        ex = self.tree.item(sel)["text"]
        parent = self.tree.parent(sel)
        if parent:
            mg = self.tree.item(parent)["text"]
            self.listbox.insert(tk.END, f"{ex} : {mg}")

    def _remove(self):
        idx = self.listbox.curselection()
        if idx:
            self.listbox.delete(idx[0])

    def _collect(self):
        return [(e.split(" : ")[0], e.split(" : ")[1]) for e in self.listbox.get(0, tk.END)]

    def _save(self):
        items = self._collect()
        if not items:
            messagebox.showerror("Error", "No exercises in routine.")
            return
        self.app.logged_in_user.add_routine(items)
        self.app.save_db()
        ToastNotification(title="Success", message="Routine saved!", duration=2000, bootstyle=SUCCESS).show_toast()

    def _start_now(self):
        items = self._collect()
        if not items:
            messagebox.showerror("Error", "No exercises in routine.")
            return
        from .log_workout import LogWorkoutPage
        self.app.show_frame(LogWorkoutPage)
        self.app.frames[LogWorkoutPage].start_routine(items)

