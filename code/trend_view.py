import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from model import Model
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TrendPage:
    """Page to display trend analysis throughout the years."""

    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.page = ttk.Frame(self.root)
        self.page.pack(fill="both", expand=True)

        self.factors = ["Happiness_Rank", "Happiness_Score", "GDP", "Family", "Health", "Freedom", "Corruption", "Generosity"]
        self.load_data()
        self.create_widgets()

    def load_data(self):
        try:
            self.model.load_data()
            self.data = self.model.get_data()
            self.data = self.data.dropna(subset=['Region'])  # Drop rows with NaN in Region column
        except FileNotFoundError:
            messagebox.showerror("Error", "CSV file not found.")
            self.data = None

    def create_widgets(self):
        if self.data is not None:
            # Factor selection
            factor_label = ttk.Label(self.page, text="Select Factors:")
            factor_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            self.factor_listbox = tk.Listbox(self.page, selectmode="multiple", exportselection=0, height=5)
            self.factor_listbox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            for factor in self.factors:
                self.factor_listbox.insert(tk.END, factor)

            # Region selection
            region_label = ttk.Label(self.page, text="Select Region:")
            region_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
            self.region_var = tk.StringVar()
            self.region_listbox = tk.Listbox(self.page, listvariable=self.region_var, selectmode="multiple", exportselection=0, height=5)
            self.region_listbox.grid(row=0, column=3, padx=10, pady=5, sticky="w")

            for region in self.data["Region"].unique().tolist():
                self.region_listbox.insert(tk.END, region)

            # Go button for trend plot
            go_button = ttk.Button(self.page, text="Go", command=self.show_trend_plot)
            go_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

            # Clear button for trend plot
            clear_button = ttk.Button(self.page, text="Clear", command=self.clear_trend_plot)
            clear_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

            # Trend graph frame
            self.trend_frame = ttk.LabelFrame(self.page, text="Trend Analysis")
            self.trend_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        else:
            messagebox.showerror("Error", "Data not loaded.")

    def show_trend_plot(self):
        if self.data is None:
            return

        selected_factors = [self.factor_listbox.get(idx) for idx in self.factor_listbox.curselection()]
        if not selected_factors:
            messagebox.showwarning("Warning", "Please select at least one factor.")
            return

        selected_regions = self.region_listbox.curselection()
        if not selected_regions:
            selected_regions = self.data["Region"].unique().tolist()
        else:
            selected_regions = [self.region_listbox.get(region) for region in selected_regions]

        fig, ax = plt.subplots(figsize=(6, 4))

        # Color dictionary for factors
        factor_colors = {
            "Happiness_Rank": "blue",
            "Happiness_Score": "green",
            "GDP": "orange",
            "Family": "red",
            "Health": "purple",
            "Freedom": "brown",
            "Corruption": "cyan",
            "Generosity": "magenta"
        }

        for factor in selected_factors:
            for region in selected_regions:
                data_filtered = self.data[(self.data["Region"] == region)]
                ax.plot(data_filtered["Year"], data_filtered[factor], marker='o', label=f"{region}: {factor}",
                        color=factor_colors[factor])

        ax.set_xlabel("Year")
        ax.set_ylabel("Value")
        ax.set_title("Trend Analysis")
        ax.legend()
        ax.grid(True)

        # Set x-axis ticks to only whole years
        plt.xticks(range(2015, 2020))

        # Display the trend plot in the GUI
        canvas = FigureCanvasTkAgg(fig, master=self.trend_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def clear_trend_plot(self):
        self.factor_listbox.selection_clear(0, tk.END)
        self.region_listbox.selection_clear(0, tk.END)
        self.trend_frame.destroy()
        self.trend_frame = ttk.LabelFrame(self.page, text="Trend Analysis")
        self.trend_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


