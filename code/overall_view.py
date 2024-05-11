import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class OverallPage:
    """Page to display overall analysis of World Happiness data."""

    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.page = ttk.Frame(self.root)
        self.page.pack(fill="both", expand=True)

        self.load_data()
        self.create_widgets()

    def load_data(self):
        try:
            self.model.load_data()
            self.data = self.model.get_data()
        except FileNotFoundError:
            messagebox.showerror("Error", "CSV file not found.")
            self.data = None

    def create_widgets(self):
        if self.data is not None:
            # Choropleth Map
            map_frame = ttk.LabelFrame(self.page, text="Choropleth Map")
            map_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.show_choropleth_map(map_frame)

            # Scatter Plot
            scatter_frame = ttk.LabelFrame(self.page, text="Scatter Plot")
            scatter_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            self.show_scatter_plot(scatter_frame)

            # Pie Chart
            pie_frame = ttk.LabelFrame(self.page, text="Happiness Score by Region (All Years)")
            pie_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            self.show_pie_chart(pie_frame)

            # Bar Chart
            bar_frame = ttk.LabelFrame(self.page, text="Factors Contributing to Happiness Score")
            bar_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
            self.show_bar_chart(bar_frame)

            # Descriptive Statistics
            stats_frame = ttk.LabelFrame(self.page, text="Descriptive Statistics")
            stats_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            self.show_descriptive_statistics(stats_frame)

            # Correlation Coefficient
            coef_frame = ttk.LabelFrame(self.page, text="Correlation Coefficient")
            coef_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
            self.show_correlation_coefficient(coef_frame)

            # Configure grid weights to resize when the window expands
            for i in range(3):
                self.page.grid_rowconfigure(i, weight=1)
                self.page.grid_columnconfigure(i, weight=1)

        else:
            messagebox.showerror("Error", "Data not loaded.")

    def show_choropleth_map(self, parent_frame):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        # Calculate average happiness score by country
        avg_happiness = self.data.groupby('Country')['Happiness_Score'].mean()
        world = world.merge(avg_happiness, left_on='name', right_index=True, how='left')

        fig, ax = plt.subplots(figsize=(6, 5))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        world.plot(column="Happiness_Score", ax=ax, legend=True, cax=cax, cmap="YlGnBu",
                   legend_kwds={'label': "Happiness Score"})

        ax.set_title("Choropleth Map - Happiness Score of Each Country")

        # Display the map in the GUI
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_scatter_plot(self, parent_frame):
        factors = ["GDP", "Corruption", "Happiness_Score"]

        # Selecting random factors
        factor1, factor2 = np.random.choice(factors, 2, replace=False)

        # Scatter plot
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=self.data, x=factor1, y=factor2, hue="Region", ax=ax, legend='brief')
        ax.set_xlabel(factor1, fontsize=10)
        ax.set_ylabel(factor2, fontsize=10)
        ax.set_title(f"Scatter Plot: {factor1} vs {factor2}", fontsize=14)

        # Control legend size
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=handles, labels=labels, loc='upper right', fontsize=5)

        # Display the scatter plot in the GUI
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_pie_chart(self, parent_frame):
        # Pie chart
        fig, ax = plt.subplots(figsize=(8, 6))
        region_counts = self.data['Region'].value_counts()
        ax.pie(region_counts, labels=None, autopct='%1.1f%%', startangle=140)

        # Add color labels for regions
        colors = sns.color_palette("pastel", len(region_counts))
        ax.legend(region_counts.index, title="Region", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8,
                  facecolor='lightgrey')
        ax.set_title("Happiness Score by Region (All Years)")

        # Display the pie chart in the GUI
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_bar_chart(self, parent_frame):
        # Bar chart
        factors = ["GDP", "Family", "Health", "Freedom", "Corruption", "Generosity"]
        avg_factors = self.data[factors].mean()

        fig, ax = plt.subplots(figsize=(6, 4))
        avg_factors.plot(kind='bar', ax=ax)
        ax.set_title("Factors Contributing to Happiness Score")
        ax.set_ylabel("Average Score")

        # Display the bar chart in the GUI
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_descriptive_statistics(self, parent_frame):
        # Descriptive statistics
        stats_text = tk.Text(parent_frame, wrap="word", height=15, width=60, state="disabled")
        stats_text.pack(fill="both", expand=True)

        # Calculate descriptive statistics
        desc_stats = self.data.describe()

        # Insert statistics into the text widget
        stats_text.insert(tk.END, str(desc_stats))

    def show_correlation_coefficient(self, parent_frame):
        # Calculate correlation coefficients for numeric columns
        numeric_data = self.data.select_dtypes(include=np.number)
        corr_matrix = numeric_data.corr()

        # Display correlation coefficients in a text box
        coef_text = tk.Text(parent_frame, wrap="word", height=5, width=60, state="disabled")
        coef_text.pack(fill="both", expand=True)
        coef_text.insert(tk.END, "Correlation Coefficients:\n\n" + str(corr_matrix))
