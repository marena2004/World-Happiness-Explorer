import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from model import Model  # Import the Model class


class StatPage:
    """Statistics page with summary statistics and histogram."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Statistics Page")
        self.create_widgets()

    def load_data(self):
        self.model = Model()
        try:
            self.model.load_data()
            self.data = self.model.get_data()
        except FileNotFoundError:
            messagebox.showerror("Error", "CSV file not found.")
            self.data = None

    def create_widgets(self):
        self.load_data()

        if self.data is not None:
            # Frame for selecting economic factor, region, and year
            selection_frame = ttk.Frame(self.root)
            selection_frame.pack(pady=10)

            # Select Economic Factor
            factor_label = ttk.Label(selection_frame, text="Select Economic Factor:")
            factor_label.grid(row=3, column=0, padx=5, pady=20)
            self.factor_var = tk.StringVar()
            factor_combobox = ttk.Combobox(selection_frame, textvariable=self.factor_var,
                                           values=["Happiness_Rank", "Happiness_Score", "GDP",
                                                   "Family", "Health", "Freedom",
                                                   "Corruption", "Generosity"])
            factor_combobox.grid(row=4, column=0, padx=5)

            # Select Region
            region_label = ttk.Label(selection_frame, text="Select Region:")
            region_label.grid(row=3, column=1, padx=5)
            self.region_var = tk.StringVar()
            region_combobox = ttk.Combobox(selection_frame, textvariable=self.region_var,
                                           values=["All"] + self.data["Region"].unique().tolist())
            region_combobox.grid(row=4, column=1, padx=5)

            # Select Year
            year_label = ttk.Label(selection_frame, text="Select Year:")
            year_label.grid(row=3, column=2, padx=5)
            self.year_var = tk.StringVar()
            year_combobox = ttk.Combobox(selection_frame, textvariable=self.year_var,
                                         values=["All"] + self.data["Year"].astype(str).unique().tolist())
            year_combobox.grid(row=4, column=2, padx=5)

            # Clear button
            clear_button = ttk.Button(selection_frame, text="Clear", command=self.clear)
            clear_button.grid(row=4, column=3, padx=5)

            # Show summary button
            summary_button = ttk.Button(selection_frame, text="Descriptive Statistics", command=self.show_summary)
            summary_button.grid(row=6, column=1, pady=40)

            # Show histogram button
            histogram_button = ttk.Button(selection_frame, text="Histogram", command=self.show_histogram)
            histogram_button.grid(row=6, column=2, pady=40)

            # Summary Box
            self.summary_box = tk.Text(self.root, height=10, width=50)
            self.summary_box.pack(side=tk.LEFT, padx=30, pady=40)

            # Histogram plot
            self.histogram_frame = ttk.Frame(self.root)
            self.histogram_frame.pack(side=tk.LEFT, padx=10)

    def show_summary(self):
        if self.data is None:
            return

        factor = self.factor_var.get()
        region = self.region_var.get()
        year = self.year_var.get()

        if year == "All":
            if region == "All":
                summary = self.data[factor].describe()
            else:
                summary = self.data[self.data["Region"] == region][factor].describe()
        else:
            if region == "All":
                summary = self.data[self.data["Year"] == int(year)][factor].describe()
            else:
                summary = self.data[(self.data["Year"] == int(year)) & (self.data["Region"] == region)][factor].describe()

        self.summary_box.delete(1.0, tk.END)
        self.summary_box.insert(tk.END, str(summary))

    def show_histogram(self):
        if self.data is None:
            return

        factor = self.factor_var.get()
        region = self.region_var.get()
        year = self.year_var.get()

        if year == "All":
            if region == "All":
                data_to_plot = self.data[factor]
            else:
                data_to_plot = self.data[self.data["Region"] == region][factor]
        else:
            if region == "All":
                data_to_plot = self.data[self.data["Year"] == int(year)][factor]
            else:
                data_to_plot = self.data[(self.data["Year"] == int(year)) & (self.data["Region"] == region)][factor]

        plt.hist(data_to_plot, bins=10)
        plt.xlabel(factor)
        plt.ylabel("Frequency")
        plt.title("Histogram")
        plt.show()

    def clear(self):
        if self.data is None:
            return

        self.factor_var.set("")
        self.region_var.set("")
        self.year_var.set("")

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    stat_page = StatPage()
    stat_page.run()
