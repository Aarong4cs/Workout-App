import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .base import BasePage
from .log_workout import LogWorkoutPage
from .routine_builder import RoutineBuilderPage
from .exercise_db import ExerciseDatabasePage

class MainMenuPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        col = ttk.Frame(self.content)
        col.pack(fill=BOTH, expand=True)

        buttons = [
            ("Log Workout", lambda: app.show_frame(LogWorkoutPage), SUCCESS),
            ("Routine Builder", lambda: app.show_frame(RoutineBuilderPage), INFO),
            ("Log Saved Routine", lambda: app.logged_in_user.log_routine(app), PRIMARY),
            ("Database + Progress", lambda: app.show_frame(ExerciseDatabasePage), SECONDARY),
            ("Exit", app.destroy, DANGER),
        ]
        for text, cmd, style in buttons:
            ttk.Button(col, text=text, command=cmd, bootstyle=f"{style}-outline", width=28).pack(pady=8, ipady=6)

