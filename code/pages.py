import tkinter as tk
from tkinter import ttk
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_components()

    def init_components(self):
        title_label = tk.Label(self, text="World Happiness Explorer", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=(20, 10))

        subtitle_label = tk.Label(self, text="Visualize and Analyze Happiness Trends Across the Globe",
                                  font=("Helvetica", 14))
        subtitle_label.pack(pady=10)

        explore_button = ttk.Button(self, text="Explore Now", command=self.controller.show_explore)
        explore_button.pack(pady=20)

        # Placeholder for world map image
        map_image = tk.Label(self, text="Placeholder for world map", bg="lightgray", width=400, height=200)
        map_image.pack(pady=20)


class ExplorePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.stats_text = None
        self.heatmap = None
        self.controller = controller
        self.init_components()

    def init_components(self):
        filters_frame = ttk.Frame(self)
        filters_frame.pack(pady=20)

        factor_label = ttk.Label(filters_frame, text="Select Economic Factor:")
        factor_label.grid(row=0, column=0, padx=5, pady=5)

        self.factor_combobox = ttk.Combobox(filters_frame)
        self.factor_combobox.grid(row=0, column=1, padx=5, pady=5)

        region_label = ttk.Label(filters_frame, text="Region:")
        region_label.grid(row=0, column=2, padx=5, pady=5)

        self.region_combobox = ttk.Combobox(filters_frame)
        self.region_combobox.grid(row=0, column=3, padx=5, pady=5)

        year_label = ttk.Label(filters_frame, text="Year:")
        year_label.grid(row=0, column=4, padx=5, pady=5)

        self.year_combobox = ttk.Combobox(filters_frame)
        self.year_combobox.grid(row=0, column=5, padx=5, pady=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        country_label = ttk.Label(button_frame, text="Country:")
        country_label.grid(row=0, column=0, padx=5, pady=5)

        country_entry = ttk.Entry(button_frame, state="disabled")  # Disable the country entry box
        country_entry.grid(row=0, column=1, padx=5, pady=5)

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_stats)
        clear_button.grid(row=0, column=2, padx=5, pady=5)

        self.stats_text = tk.Text(self, height=10, width=50)  # Initialize stats_text
        self.stats_text.pack()

        self.data = self.read_data()

        # Populate economic factor, region, and year comboboxes
        self.populate_filters()

        # Bind combobox selection events
        self.factor_combobox.bind("<<ComboboxSelected>>", self.update_stats)
        self.region_combobox.bind("<<ComboboxSelected>>", self.update_stats)
        self.year_combobox.bind("<<ComboboxSelected>>", self.update_stats)

    def read_data(self):
        data = []
        with open("WorldHappiness2015-2019.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data

    def populate_filters(self):
        factors = ["GDP", "Family", "Health", "Freedom", "Corruption", "Generosity"]
        regions = sorted(set(row["Region"] for row in self.data))
        years = sorted(set(row["Year"] for row in self.data))

        self.factor_combobox["values"] = factors
        self.region_combobox["values"] = regions
        self.year_combobox["values"] = years

    def update_stats(self, event=None):
        selected_factor = self.factor_combobox.get()
        selected_region = self.region_combobox.get()
        selected_year = self.year_combobox.get()

        filtered_data = [float(row[selected_factor]) for row in self.data if
                         row["Region"] == selected_region and row["Year"] == selected_year]

        if filtered_data:
            mean_value = np.mean(filtered_data)
            median_value = np.median(filtered_data)
            std_dev_value = np.std(filtered_data)

            stats_text = f"Summary Statistics for {selected_factor} in {selected_region} for the year {selected_year}:\n"
            stats_text += f"Mean: {mean_value:.2f}\n"
            stats_text += f"Median: {median_value:.2f}\n"
            stats_text += f"Standard Deviation: {std_dev_value:.2f}\n"

            self.stats_text.config(state="normal")
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, stats_text)
            self.stats_text.config(state="disabled")

            # Generate and show heatmap
            self.show_heatmap(selected_factor, selected_region, selected_year)

        else:
            self.clear_stats()  # Clear the stats text if no data found

    def show_heatmap(self, selected_factor, selected_region, selected_year):
        filtered_data = [row for row in self.data if
                         row["Region"] == selected_region and row["Year"] == selected_year]

        if filtered_data:
            # Convert to DataFrame
            df = pd.DataFrame(filtered_data)
            # Convert numeric columns to numeric type
            numerical_columns = ["Happiness_Score", selected_factor]
            df[numerical_columns] = df[numerical_columns].apply(pd.to_numeric, errors='coerce')
            # Drop NaN values
            df.dropna(subset=numerical_columns, inplace=True)

            sns.heatmap(df[numerical_columns].corr(), annot=True, cmap="YlGnBu")
            plt.title(f"Happiness Score vs {selected_factor} in {selected_region} ({selected_year})")
            plt.xlabel("Factors")
            plt.ylabel("Factors")
            plt.show()

    def clear_stats(self):
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.config(state="disabled")


class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_components()

    def init_components(self):
        about_label = tk.Label(self, text="About Page", font=("Helvetica", 16))
        about_label.pack(pady=20)
