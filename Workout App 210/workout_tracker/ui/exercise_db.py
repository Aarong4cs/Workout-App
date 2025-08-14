import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from .base import BasePage

class ExerciseDatabasePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        # Use GRID inside the content area
        self.content.grid_columnconfigure(0, weight=1, minsize=280)  # left: tree
        self.content.grid_columnconfigure(1, weight=2)  # right: plot
        self.content.grid_rowconfigure(0, weight=1)

        left = ttk.Labelframe(self.content, text="Exercise Database", padding=10, bootstyle=INFO)
        left.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        right = ttk.Labelframe(self.content, text="Progress", padding=10, bootstyle=WARNING)
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        # LEFT column (tree)
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(left, show="tree")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", self._on_item)

        # RIGHT column (plot area)
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(0, weight=1)

        self.graph_area = ttk.Frame(right)
        self.graph_area.grid(row=0, column=0, sticky="nsew")
        self.graph_area.pack_propagate(True)  # let canvas size naturally

        # Persistent figure/canvas; no manual set_size_inches (prevents distortion)
        self.fig, self.ax = plt.subplots(constrained_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_area)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def on_show(self):
        # Rebuild tree
        self.tree.delete(*self.tree.get_children())
        for mg, exercises in sorted(self.app.logged_in_user.exercise_tree.items()):
            parent = self.tree.insert("", "end", text=mg, open=True)
            for ex in sorted(exercises):
                self.tree.insert(parent, "end", text=ex)
        # Clear plot
        self.ax.clear()
        self.canvas.draw_idle()

    def _on_item(self, _e):
        sel = self.tree.focus()
        label = self.tree.item(sel)["text"]
        if label in self.app.logged_in_user.progress_data:
            self.ax.clear()
            x, y = zip(*self.app.logged_in_user.progress_data[label])
            min_w, max_w = min(y), max(y)
            unit = self.app.logged_in_user.preferences.get("unit", "lbs")

            self.ax.plot(x, y, marker="o")
            self.ax.set_ylim(min_w - 5, max_w + 5)
            self.ax.set_title(f"Progress for {label} (+{max_w - min_w} {unit})")
            self.ax.set_xlabel("Workout Session")
            self.ax.set_ylabel(f"Weight ({unit})")
            self.fig.tight_layout()
            self.canvas.draw_idle()
