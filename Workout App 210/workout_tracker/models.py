from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Tuple, Optional
from tkinter import messagebox

@dataclass
class WorkoutSet:
    exercise: str
    reps: int
    weight: float

class User:
    def __init__(self, username: str, password_hash: str):
        self.username: str = username
        self.password_hash: str = password_hash
        self.workout_history: List[WorkoutSet] = []
        self.routines: Deque[List[Tuple[str, str]]] = deque()
        self.preferences: Dict[str, str] = {"unit": "lbs"}
        self.exercise_tree: Dict[str, List[str]] = defaultdict(list)
        self.progress_data: Dict[str, List[Tuple[int, float]]] = defaultdict(list)

    def add_set(self, exercise: str, reps: int, weight: float, muscle_group: Optional[str] = None):
        self.workout_history.append(WorkoutSet(exercise, reps, weight))
        seq = len(self.progress_data[exercise]) + 1
        self.progress_data[exercise].append((seq, weight))
        if muscle_group and exercise not in self.exercise_tree[muscle_group]:
            self.exercise_tree[muscle_group].append(exercise)

    def add_routine(self, exercises: List[Tuple[str, str]]):
        self.routines.append(exercises)

    def log_routine(self, app):
        from .ui.log_workout import LogWorkoutPage
        if not self.routines:
            messagebox.showerror("Error", "No routines available.")
            return
        routine = self.routines.popleft()
        app.show_frame(LogWorkoutPage)
        app.frames[LogWorkoutPage].start_routine(routine)

