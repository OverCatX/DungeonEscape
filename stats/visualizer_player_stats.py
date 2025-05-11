import sys
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import os
from math import pi

FILE_PATH = "stats/players.csv"

class PlayerStatVisualizer(tk.Tk):
    def __init__(self, player_name):
        super().__init__()
        self.title(f"{player_name}'s Stat Visualizer")
        self.geometry("800x600")

        if not os.path.exists(FILE_PATH):
            tk.messagebox.showerror("Missing File", f"{FILE_PATH} not found")
            self.destroy()
            return

        df = pd.read_csv(FILE_PATH)
        self.player_data = df[df["name"] == player_name]

        self.graph_var = tk.StringVar()
        self.graph_options = {
            "Bar Chart": self.plot_bar_chart,
        }

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self, text="Select Graph Type", font=("Arial", 14)).pack(pady=10)

        dropdown = ttk.Combobox(self, textvariable=self.graph_var, values=list(self.graph_options.keys()), state="readonly")
        dropdown.pack()
        dropdown.current(0)

        ttk.Button(self, text="Show Graph", command=self.render_graph).pack(pady=10)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    def render_graph(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig = plt.Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)

        func = self.graph_options.get(self.graph_var.get())
        if func:
            func(ax)
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_bar_chart(self, ax):
        cols = ["time_played", "enemies_defeated", "dash_used", "traps_triggered", "distance_traveled"]
        labels = ["Time", "Enemies", "Dash", "Traps", "Distance"]
        values = [self.player_data[col].values[0] for col in cols]
        ax.bar(labels, values, color="skyblue")
        ax.set_title("Average Stats (Bar Chart)")

    def plot_radar_chart(self, ax):
        cols = ["time_played", "enemies_defeated", "dash_used", "traps_triggered", "distance_traveled"]
        labels = ["Time", "Enemies", "Dash", "Traps", "Distance"]
        values = [self.player_data[col].values[0] for col in cols]
        values += values[:1]
        angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))]
        angles += angles[:1]

        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
        ax.plot(angles, values, linewidth=2, linestyle='solid')
        ax.fill(angles, values, 'skyblue', alpha=0.4)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_title("Radar Chart of Player Stats")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    app = PlayerStatVisualizer(name)
    app.mainloop()