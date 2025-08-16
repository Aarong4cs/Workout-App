import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .storage import Storage

import matplotlib

matplotlib.use("TkAgg")

from .ui.login import LoginPage
from .ui.main_menu import MainMenuPage
from .ui.log_workout import LogWorkoutPage
from .ui.routine_builder import RoutineBuilderPage
from .ui.exercise_db import ExerciseDatabasePage


class WorkoutTrackerApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("")

        width, height = 1150, 800
        self._center_window(width, height)
        self.minsize(width, height)
        self.resizable(False, False)

        self.users = {}
        self.logged_in_user = None
        self.storage = Storage(os.environ.get("WORKOUT_DB", "workout_db.json"))
        self.users = self.storage.ensure_db()

        self.container = ttk.Frame(self, padding=10)
        self.container.pack(fill=BOTH, expand=True)

        self.frames = {}
        for Page in (
            LoginPage,
            MainMenuPage,
            LogWorkoutPage,
            RoutineBuilderPage,
            ExerciseDatabasePage,
        ):
            page = Page(self.container, self)
            self.frames[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def _center_window(self, width: int, height: int):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = int((screen_w / 2) - (width / 2))
        y = int((screen_h / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_frame(self, page_cls):
        f = self.frames[page_cls]
        f.tkraise()
        if hasattr(f, "update_header"):
            f.update_header()
        if hasattr(f, "on_show"):
            f.on_show()

    def save_db(self):
        self.storage.save(self.users)

    def load_db(self):
        self.users = self.storage.load()
