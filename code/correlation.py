import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# todo
"Scatter Plot"
# can not choose year and region
# remove country box
# show coefficient value

"Matrix"
# cannot choose year
# back button

class CorrelationPage:
    """Page for correlation analysis."""

    def __init__(self, data):
        self.root = tk.Tk()
        self.root.title("Correlation Page")
        self.root.geometry("800x600")
        self.data = data
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for correlation page
        label = ttk.Label(self.root, text="Correlation Page")
        label.pack(pady=10)

        # Button to choose scatter plot
        scatter_button = ttk.Button(self.root, text="Scatter Plot", command=self.open_scatter_plot)
        scatter_button.pack()

        # Button to choose matrix heatmap
        heatmap_button = ttk.Button(self.root, text="Matrix Heatmap", command=self.open_heatmap)
        heatmap_button.pack()

    def open_scatter_plot(self):
        ScatterPlotPage(self.data)

    def open_heatmap(self):
        HeatmapPage(self.data)


class ScatterPlotPage:
    """Page to show scatter plot."""

    def __init__(self, data):
        self.data = data
        self.scatter_root = tk.Toplevel()
        self.scatter_root.title("Scatter Plot")
        self.scatter_root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for scatter plot page
        label = ttk.Label(self.scatter_root, text="Scatter Plot Page")
        label.pack(pady=10)

        # First row
        first_row_frame = ttk.Frame(self.scatter_root)
        first_row_frame.pack()

        year_label = ttk.Label(first_row_frame, text="Year:")
        year_label.grid(row=0, column=0)
        self.year_var = tk.StringVar()
        year_entry = ttk.Entry(first_row_frame, textvariable=self.year_var)
        year_entry.grid(row=0, column=1)

        region_label = ttk.Label(first_row_frame, text="Region:")
        region_label.grid(row=0, column=2)
        self.region_var = tk.StringVar()
        region_entry = ttk.Entry(first_row_frame, textvariable=self.region_var)
        region_entry.grid(row=0, column=3)

        country_label = ttk.Label(first_row_frame, text="Country:")
        country_label.grid(row=0, column=4)
        self.country_var = tk.StringVar()
        country_entry = ttk.Entry(first_row_frame, textvariable=self.country_var)
        country_entry.grid(row=0, column=5)

        # Second row
        second_row_frame = ttk.Frame(self.scatter_root)
        second_row_frame.pack()

        factor1_label = ttk.Label(second_row_frame, text="Factor 1:")
        factor1_label.grid(row=0, column=0)
        self.factor1_var = tk.StringVar()
        factor1_combobox = ttk.Combobox(second_row_frame, textvariable=self.factor1_var,
                                        values=["Happiness_Rank", "Happiness_Score", "GDP",
                                                "Family", "Health", "Freedom",
                                                "Corruption", "Generosity"])
        factor1_combobox.grid(row=0, column=1)

        factor2_label = ttk.Label(second_row_frame, text="Factor 2:")
        factor2_label.grid(row=0, column=2)
        self.factor2_var = tk.StringVar()
        factor2_combobox = ttk.Combobox(second_row_frame, textvariable=self.factor2_var,
                                        values=["Happiness_Rank", "Happiness_Score", "GDP",
                                                "Family", "Health", "Freedom",
                                                "Corruption", "Generosity"])
        factor2_combobox.grid(row=0, column=3)

        go_button = ttk.Button(second_row_frame, text="Go", command=self.show_scatter_plot)
        go_button.grid(row=0, column=4)

        clear_button = ttk.Button(second_row_frame, text="Clear", command=self.clear)
        clear_button.grid(row=0, column=5)

    def show_scatter_plot(self):
        year = self.year_var.get()
        region = self.region_var.get()
        country = self.country_var.get()
        factor1 = self.factor1_var.get()
        factor2 = self.factor2_var.get()

        data_to_plot = self.data.copy()

        if year:
            data_to_plot = data_to_plot[data_to_plot["Year"] == int(year)]
        if region:
            data_to_plot = data_to_plot[data_to_plot["Region"] == region]
        if country:
            data_to_plot = data_to_plot[data_to_plot["Country"] == country]

        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=data_to_plot, x=factor1, y=factor2)
        plt.xlabel(factor1)
        plt.ylabel(factor2)
        plt.title("Scatter Plot")
        plt.show()

    def clear(self):
        self.year_var.set("")
        self.region_var.set("")
        self.country_var.set("")
        self.factor1_var.set("")
        self.factor2_var.set("")


class HeatmapPage:
    """Page to show heatmap."""

    def __init__(self, data):
        self.data = data
        self.heatmap_root = tk.Toplevel()
        self.heatmap_root.title("Matrix Heatmap")
        self.heatmap_root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for heatmap page
        label = ttk.Label(self.heatmap_root, text="Matrix Heatmap Page")
        label.pack(pady=10)

        year_label = ttk.Label(self.heatmap_root, text="Year:")
        year_label.pack()
        self.year_var = tk.StringVar()
        year_entry = ttk.Entry(self.heatmap_root, textvariable=self.year_var)
        year_entry.pack()

        go_button = ttk.Button(self.heatmap_root, text="Go", command=self.show_heatmap)
        go_button.pack()

        clear_button = ttk.Button(self.heatmap_root, text="Clear", command=self.clear)
        clear_button.pack()

    def show_heatmap(self):
        year = self.year_var.get()

        if not year:
            messagebox.showwarning("Warning", "Please enter a year.")
            return

        data_to_plot = self.data[self.data["Year"] == int(year)].drop(columns=["Country", "Region", "Year"])

        plt.figure(figsize=(10, 8))
        sns.heatmap(data_to_plot.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Correlation Matrix Heatmap")
        plt.show()

    def clear(self):
        self.year_var.set("")


# Run the application
if __name__ == "__main__":
    # Sample CSV data
    data = pd.read_csv("WorldHappiness2015-2019.csv")

    correlation_page = CorrelationPage(data)
    correlation_page.root.mainloop()
