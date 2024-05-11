import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StatPage:
    """Statistics page with summary statistics and histogram."""

    def __init__(self,root, model):
        self.root = root
        self.model = model
        self.page = ttk.Frame(self.root)
        # self.page.pack(fill="both", expand=True)
        self.load_data()
        # self.create_widgets()

        # Bind the configure event to the root window
        self.root.bind("<Configure>", self.on_resize)

    def load_data(self):
        self.model.load_data()
        self.data = self.model.get_data()

    def create_widgets(self):
        self.load_data()

        if self.data is not None:
            # Frame for selecting economic factor, region, and year
            selection_frame = ttk.Frame(self.root)
            selection_frame.pack(expand=True, fill='both', padx=10, pady=10)

            # Select Economic Factor
            factor_label = ttk.Label(selection_frame, text="Select Economic Factor:")
            factor_label.grid(row=0, column=0, padx=5, pady=5)
            self.factor_var = tk.StringVar()
            factor_combobox = ttk.Combobox(selection_frame, textvariable=self.factor_var,
                                           values=["Happiness_Rank", "Happiness_Score", "GDP",
                                                   "Family", "Health", "Freedom",
                                                   "Corruption", "Generosity"])
            factor_combobox.grid(row=1, column=0, padx=5, pady=5)

            # Select Region
            region_label = ttk.Label(selection_frame, text="Select Region:")
            region_label.grid(row=0, column=1, padx=5, pady=5)
            self.region_var = tk.StringVar()
            region_combobox = ttk.Combobox(selection_frame, textvariable=self.region_var,
                                           values=["All"] + self.data["Region"].unique().tolist())
            region_combobox.grid(row=1, column=1, padx=5, pady=5)

            # Select Year
            year_label = ttk.Label(selection_frame, text="Select Year:")
            year_label.grid(row=0, column=2, padx=5, pady=5)
            self.year_var = tk.StringVar()
            year_combobox = ttk.Combobox(selection_frame, textvariable=self.year_var,
                                         values=["All"] + self.data["Year"].astype(str).unique().tolist())
            year_combobox.grid(row=1, column=2, padx=5, pady=5)

            # Clear button
            clear_button = ttk.Button(selection_frame, text="Clear", command=self.clear)
            clear_button.grid(row=2, column=2, padx=5, pady=5)

            # Show summary button
            summary_button = ttk.Button(selection_frame, text="Descriptive Statistics", command=self.show_summary)
            summary_button.grid(row=2, column=0, columnspan=1, pady=10)

            # Show histogram button
            histogram_button = ttk.Button(selection_frame, text="Histogram", command=self.show_histogram)
            histogram_button.grid(row=2, column=1, columnspan=1, pady=10)

            # Summary Box
            self.summary_box = tk.Text(self.root, height=10, width=50, wrap='word')
            self.summary_box.pack(expand=True, fill='both', padx=10, pady=10)
            self.summary_box.configure(state='disabled', font=("Arial", 12))  # Make the text box read-only

            # Histogram canvas
            self.histogram_frame = ttk.Frame(self.root)
            self.histogram_frame.pack(expand=True, fill='both', padx=10, pady=10)
            self.figure, self.ax = plt.subplots(figsize=(5, 4))
            self.canvas = FigureCanvasTkAgg(self.figure, master=self.histogram_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(expand=True, fill='both')

    def show_summary(self):
        if self.data is None:
            return

        factor = self.factor_var.get()
        region = self.region_var.get()
        year = self.year_var.get()

        if factor == "" or region == "":
            messagebox.showwarning("Invalid Input", "Please select both an economic factor and a region.")
            return

        if year == "All":
            if region == "All":
                summary = self.data[factor].describe()
            else:
                summary = self.data[self.data["Region"] == region][factor].describe()
        else:
            try:
                year = int(year)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please select a valid year.")
                return

            if year not in self.data["Year"].unique():
                messagebox.showwarning("Invalid Input", "Year not found in data.")
                return

            if region == "All":
                summary = self.data[self.data["Year"] == year][factor].describe()
            else:
                summary = self.data[(self.data["Year"] == year) & (self.data["Region"] == region)][factor].describe()

        self.summary_box.configure(state='normal')
        self.summary_box.delete(1.0, tk.END)
        self.summary_box.insert(tk.END, str(summary))
        self.summary_box.configure(state='disabled')

    def show_histogram(self):
        if self.data is None:
            return

        factor = self.factor_var.get()
        region = self.region_var.get()
        year = self.year_var.get()

        if factor == "" or region == "":
            messagebox.showwarning("Invalid Input", "Please select both an economic factor and a region.")
            return

        if year == "All":
            if region == "All":
                data_to_plot = self.data[factor]
            else:
                data_to_plot = self.data[self.data["Region"] == region][factor]
        else:
            try:
                year = int(year)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please select a valid year.")
                return

            if year not in self.data["Year"].unique():
                messagebox.showwarning("Invalid Input", "Year not found in data.")
                return

            if region == "All":
                data_to_plot = self.data[self.data["Year"] == year][factor]
            else:
                data_to_plot = self.data[(self.data["Year"] == year) & (self.data["Region"] == region)][factor]

        self.ax.clear()
        self.ax.hist(data_to_plot, bins=10)
        self.ax.set_xlabel(factor)
        self.ax.set_ylabel("Frequency")
        self.ax.set_title("Histogram")
        self.canvas.draw()

    def clear(self):
        if self.data is None:
            return

        self.factor_var.set("")
        self.region_var.set("")
        self.year_var.set("")
        self.summary_box.configure(state='normal')
        self.summary_box.delete(1.0, tk.END)
        self.summary_box.configure(state='disabled')
        self.ax.clear()
        self.canvas.draw()

    def on_resize(self, event):
        """Adjust font size when the window is resized."""
        # Retrieve the new width of the window
        new_width = event.width
        # Calculate the new font size
        new_font_size = max(10, int(new_width / 100))
        # Configure the font size for the summary box
        self.summary_box.configure(font=("Arial", new_font_size))

        # Resize font in buttons and labels
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button) or isinstance(widget, ttk.Label) or isinstance(widget, ttk.Combobox):
                widget.configure(font=("Arial", new_font_size))

    def run(self):
        self.root.mainloop()

