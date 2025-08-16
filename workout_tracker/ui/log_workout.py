import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from tkinter import messagebox
from .base import BasePage

class LogWorkoutPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._routine_queue = None

        form = ttk.Labelframe(self.content, text="Log Workout", padding=16, bootstyle=PRIMARY)
        form.pack(expand=True, fill=BOTH)

        self.exercise = tk.StringVar()
        self.mgroup = tk.StringVar()
        self.reps = tk.StringVar()
        self.weight = tk.StringVar()

        # Build fields; DO NOT reference logged_in_user here (may be None at startup)
        ttk.Label(form, text="Exercise").pack(anchor=W)
        ttk.Entry(form, textvariable=self.exercise).pack(fill=X, ipady=6, pady=(0, 10))

        ttk.Label(form, text="Muscle Group").pack(anchor=W)
        ttk.Entry(form, textvariable=self.mgroup).pack(fill=X, ipady=6, pady=(0, 10))

        ttk.Label(form, text="Reps").pack(anchor=W)
        ttk.Entry(form, textvariable=self.reps).pack(fill=X, ipady=6, pady=(0, 10))

        # Weight label stored to update later in on_show()
        self.weight_label = ttk.Label(form, text="Weight (lbs)")
        self.weight_label.pack(anchor=W)
        ttk.Entry(form, textvariable=self.weight).pack(fill=X, ipady=6, pady=(0, 10))

        ttk.Button(form, text="Save Set", command=self._save, bootstyle=SUCCESS).pack(fill=X, pady=8)
        self.hint = ttk.Label(form, text="", foreground="#666")
        self.hint.pack(pady=(6, 0))

    def on_show(self):
        # Update the weight label with the user's preferred unit once we're sure a user is logged in
        unit = "lbs"
        if self.app.logged_in_user and isinstance(self.app.logged_in_user.preferences, dict):
            unit = self.app.logged_in_user.preferences.get("unit", "lbs")
        self.weight_label.configure(text=f"Weight ({unit})")

    def start_routine(self, exercises):
        self._routine_queue = list(exercises)
        self._load_next()

    def _load_next(self):
        if not self._routine_queue:
            self.hint.config(text="Routine complete ✅")
            return
        ex, mg = self._routine_queue.pop(0)
        self.exercise.set(ex)
        self.mgroup.set(mg)
        self.reps.set("")
        self.weight.set("")
        self.hint.config(text=f"Logging routine… {len(self._routine_queue)} remaining.")

    def _save(self):
        try:
            ex = self.exercise.get().strip()
            mg = self.mgroup.get().strip()
            reps = int(self.reps.get().strip())
            wt = float(self.weight.get().strip())
            if not ex or not mg:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Invalid entry.")
            return
        self.app.logged_in_user.add_set(ex, reps, wt, mg)
        self.app.save_db()

        unit = self.app.logged_in_user.preferences.get("unit", "lbs")
        ToastNotification(title="Saved", message=f"{ex} — {reps} reps @ {wt} {unit}", duration=2200, bootstyle=SUCCESS).show_toast()

        if self._routine_queue:
            self._load_next()

