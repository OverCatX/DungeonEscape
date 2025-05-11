import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

FILE_PATH = "stats/session_log.csv"

class GraphViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dungeon Escape: Data Visualizer")
        self.geometry("800x600")
        self.df = self.load_data()

        self.graph_var = tk.StringVar()
        self.graph_options = {
            "Histogram: Time Played": self.plot_histogram,
            "Pie Chart: Character Used": self.plot_pie,
            "Scatter: Enemies vs Survival": self.plot_scatter,
            "Bar: Avg Dash by Character": self.plot_bar,
            "Line: Distance Traveled": self.plot_line,
        }

        self.setup_widgets()

    def load_data(self):
        if not os.path.exists(FILE_PATH):
            messagebox.showerror("File Not Found", f"Cannot find {FILE_PATH}")
            self.destroy()
            return None
        return pd.read_csv(FILE_PATH)

    def setup_widgets(self):
        ttk.Label(self, text="Select Graph to Display", font=("Arial", 14)).pack(pady=10)

        dropdown = ttk.Combobox(self, textvariable=self.graph_var, values=list(self.graph_options.keys()), state="readonly")
        dropdown.pack()
        dropdown.current(0)

        ttk.Button(self, text="Show Graph", command=self.render_graph).pack(pady=10)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    def render_graph(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig = plt.Figure(figsize=(7, 5), dpi=100)
        ax = fig.add_subplot(111)

        plot_func = self.graph_options.get(self.graph_var.get())
        if plot_func:
            plot_func(ax)
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_histogram(self, ax):
        ax.hist(self.df["time_played"], bins=10, color='skyblue', edgecolor='black')
        ax.set_title("Time Played Histogram")
        ax.set_xlabel("Time Played (seconds)")
        ax.set_ylabel("Sessions")

    def plot_pie(self, ax):
        counts = self.df["character"].value_counts()
        ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=140)
        ax.set_title("Character Usage")

    def plot_scatter(self, ax):
        ax.scatter(self.df["enemies_defeated"], self.df["survived"], color='orange', alpha=0.6)
        ax.set_title("Enemies Defeated vs Survival")
        ax.set_xlabel("Enemies Defeated")
        ax.set_ylabel("Survived (0=No, 1=Yes)")
        ax.grid(True)

    def plot_bar(self, ax):
        avg_dash = self.df.groupby("character")["dash_used"].mean()
        avg_dash.plot(kind='bar', ax=ax, color='teal')
        ax.set_title("Avg Dash by Character")
        ax.set_ylabel("Dash Count")

    def plot_line(self, ax):
        ax.plot(self.df["distance_traveled"], marker='o')
        ax.set_title("Distance Traveled Over Sessions")
        ax.set_ylabel("Distance")
        ax.set_xlabel("Session")
        ax.grid(True)

if __name__ == "__main__":
    app = GraphViewer()
    app.mainloop()