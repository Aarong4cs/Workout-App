import json, os, random
from collections import defaultdict
from typing import Dict
from .models import User
from .utils import hash_password

DEFAULT_DB_FILE = "workout_db.json"

class Storage:
    def __init__(self, db_file: str = DEFAULT_DB_FILE):
        self.db_file = db_file

    def save(self, users: Dict[str, User]):
        data = {
            u: {
                "password_hash": usr.password_hash,
                "workout_history": [(ws.exercise, ws.reps, ws.weight) for ws in usr.workout_history],
                "routines": list(usr.routines),
                "preferences": usr.preferences,
                "progress_data": dict(usr.progress_data),
                "exercise_tree": dict(usr.exercise_tree),
            }
            for u, usr in users.items()
        }
        with open(self.db_file, "w") as f:
            json.dump(data, f)

    def load(self) -> Dict[str, User]:
        with open(self.db_file, "r") as f:
            data = json.load(f)
        users: Dict[str, User] = {}
        for username, info in data.items():
            user = User(username, info["password_hash"])
            # rebuild workout history and progress
            for ex, reps, wt in info.get("workout_history", []):
                user.add_set(ex, reps, wt)
            # restore other fields
            from collections import deque
            user.routines = deque(info.get("routines", []))
            user.preferences = info.get("preferences", {"unit": "lbs"})
            user.progress_data = defaultdict(list, {k: v for k, v in info.get("progress_data", {}).items()})
            user.exercise_tree = defaultdict(list, {k: v for k, v in info.get("exercise_tree", {}).items()})
            users[username] = user
        return users

    def ensure_db(self) -> Dict[str, User]:
        if not os.path.exists(self.db_file):
            return self._create_preset()
        return self.load()

    # --- preset/demo data ---
    def _create_preset(self) -> Dict[str, User]:
        preset = {
            "Chest": ["Bench Press", "Incline Dumbbell Press", "Push Up", "Chest Fly"],
            "Back": ["Pull Up", "Barbell Row", "Lat Pulldown", "Deadlift"],
            "Legs": ["Squat", "Leg Press", "Lunge", "Leg Curl"],
            "Shoulders": ["Overhead Press", "Lateral Raise", "Front Raise"],
            "Arms": ["Bicep Curl", "Tricep Pushdown", "Hammer Curl", "Skull Crusher"],
            "Core": ["Plank", "Crunch", "Russian Twist", "Leg Raise"],
        }
        type_map = {
            "Bench Press": "compound",
            "Incline Dumbbell Press": "accessory",
            "Push Up": "bodyweight",
            "Chest Fly": "accessory",
            "Pull Up": "bodyweight",
            "Barbell Row": "compound",
            "Lat Pulldown": "machine",
            "Deadlift": "compound",
            "Squat": "compound",
            "Leg Press": "machine",
            "Lunge": "accessory",
            "Leg Curl": "machine",
            "Overhead Press": "compound",
            "Lateral Raise": "accessory",
            "Front Raise": "accessory",
            "Bicep Curl": "accessory",
            "Tricep Pushdown": "machine",
            "Hammer Curl": "accessory",
            "Skull Crusher": "accessory",
            "Plank": "bodyweight",
            "Crunch": "bodyweight",
            "Russian Twist": "bodyweight",
            "Leg Raise": "bodyweight",
        }
        def gen_progress(ex_type):
            sessions = random.randint(4, 6)
            start = {
                "compound": random.randint(85, 185),
                "accessory": random.randint(10, 35),
                "bodyweight": 0,
                "machine": random.randint(40, 100),
            }[ex_type]
            wts = []
            reps = []
            for i in range(sessions):
                if ex_type == "compound":
                    change = random.choice([5, 5, 10, 15])
                elif ex_type == "accessory":
                    change = random.choice([0, 2.5, 5])
                elif ex_type == "machine":
                    change = random.choice([5, 10, 15, 20])
                else:  # bodyweight
                    change = random.choice([0, 5, 10])
                weight = start + change * i
                if i == random.randint(1, sessions - 2):
                    weight -= random.choice([0, 5])
                wts.append(weight)
                reps.append(random.choice([6, 8, 10, 12]))
            return list(zip(reps, wts))

        demo = User("demo", hash_password("demo"))
        demo.preferences["unit"] = "lbs"
        from collections import defaultdict as _dd
        demo.exercise_tree = _dd(list, {k: list(v) for k, v in preset.items()})
        for mg, exs in preset.items():
            for ex in exs:
                ex_type = type_map[ex]
                for r, w in gen_progress(ex_type):
                    demo.add_set(ex, r, float(w), mg)
        demo.add_routine([
            ("Squat", "Legs"),
            ("Bench Press", "Chest"),
            ("Barbell Row", "Back"),
            ("Overhead Press", "Shoulders"),
            ("Bicep Curl", "Arms"),
            ("Tricep Pushdown", "Arms"),
        ])
        users = {"demo": demo}
        self.save(users)
        return users

