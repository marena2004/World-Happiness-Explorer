import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from model import Model
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import linregress

class CorrelationPage:
    """Page to display scatter plot and correlation matrix."""
    def __init__(self,root, model):
        self.root = root
        self.model = model
        self.page = ttk.Frame(self.root)
        # self.page.pack(fill="both", expand=True)
        self.load_data()
        # self.create_widgets()


    def load_data(self):
        self.model.load_data()
        self.data = self.model.get_data()

    def create_widgets(self):
        self.load_data()

        if self.data is not None:
            # Scatter plot section
            scatter_frame = ttk.LabelFrame(self.root, text="Scatter Plot")
            scatter_frame.pack(side="left", fill="both", expand=True)

            scatter_frame.rowconfigure(0, weight=1)
            scatter_frame.columnconfigure(0, weight=1)
            scatter_frame.columnconfigure(1, weight=1)
            scatter_frame.columnconfigure(2, weight=1)
            scatter_frame.columnconfigure(3, weight=1)

            # Year selection
            year_label = ttk.Label(scatter_frame, text="Select Year:")
            year_label.grid(row=0, column=0, padx=5, pady=5)
            self.year_var = tk.StringVar()
            year_combobox = ttk.Combobox(scatter_frame, textvariable=self.year_var,
                                         values=["All"] + self.data["Year"].astype(str).unique().tolist())
            year_combobox.grid(row=0, column=1, padx=5, pady=5)

            # Region selection
            region_label = ttk.Label(scatter_frame, text="Select Region:")
            region_label.grid(row=0, column=2, padx=5, pady=5)
            self.region_var = tk.StringVar()
            self.region_listbox = tk.Listbox(scatter_frame, listvariable=self.region_var, selectmode="multiple", exportselection=0)
            self.region_listbox.grid(row=0, column=3, padx=5, pady=5)

            for region in ["All"] + self.data["Region"].unique().tolist():
                self.region_listbox.insert(tk.END, region)

            # Factor 1 selection
            factor1_label = ttk.Label(scatter_frame, text="Select Factor 1:")
            factor1_label.grid(row=1, column=0, padx=5, pady=5)
            self.factor1_var = tk.StringVar()
            factor1_combobox = ttk.Combobox(scatter_frame, textvariable=self.factor1_var,
                                            values=["Happiness_Rank", "Happiness_Score", "GDP",
                                                    "Family", "Health", "Freedom",
                                                    "Corruption", "Generosity"])
            factor1_combobox.grid(row=1, column=1, padx=5, pady=5)

            # Factor 2 selection
            factor2_label = ttk.Label(scatter_frame, text="Select Factor 2:")
            factor2_label.grid(row=2, column=0, padx=5, pady=5)
            self.factor2_var = tk.StringVar()
            factor2_combobox = ttk.Combobox(scatter_frame, textvariable=self.factor2_var,
                                            values=["Happiness_Rank", "Happiness_Score", "GDP",
                                                    "Family", "Health", "Freedom",
                                                    "Corruption", "Generosity"])
            factor2_combobox.grid(row=2, column=1, padx=5, pady=5)

            # Go button for scatter plot
            scatter_go_button = ttk.Button(scatter_frame, text="Go", command=self.show_scatter_plot)
            scatter_go_button.grid(row=2, column=2, padx=5, pady=10)

            # Clear button for scatter plot
            scatter_clear_button = ttk.Button(scatter_frame, text="Clear", command=self.clear_scatter)
            scatter_clear_button.grid(row=2, column=3, padx=5, pady=10)

            # Correlation matrix section
            matrix_frame = ttk.LabelFrame(self.root, text="Correlation Matrix")
            matrix_frame.pack(side="right", fill="both", expand=True)

            matrix_frame.rowconfigure(0, weight=1)
            matrix_frame.columnconfigure(0, weight=1)
            matrix_frame.columnconfigure(1, weight=1)

            # Year selection for matrix
            matrix_year_label = ttk.Label(matrix_frame, text="Select Year:")
            matrix_year_label.grid(row=1, column=0, padx=5, pady=5)  # Adjusted row to 0
            self.matrix_year_var = tk.StringVar()
            matrix_year_combobox = ttk.Combobox(matrix_frame, textvariable=self.matrix_year_var,
                                                values=["All"] + self.data["Year"].astype(str).unique().tolist())
            matrix_year_combobox.grid(row=1, column=1, padx=5, pady=5)  # Adjusted row to 0

            # Go button for matrix
            matrix_go_button = ttk.Button(matrix_frame, text="Go", command=self.show_correlation_matrix)
            matrix_go_button.grid(row=1, column=2, padx=5, pady=10)

            # Clear button for matrix
            matrix_clear_button = ttk.Button(matrix_frame, text="Clear", command=self.clear_matrix)
            matrix_clear_button.grid(row=1, column=3, padx=5, pady=10)

            # Graph frame for scatter plot
            scatter_graph_frame = ttk.Frame(scatter_frame)
            scatter_graph_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

            self.scatter_figure, self.scatter_ax = plt.subplots(figsize=(5, 4))
            self.scatter_canvas = FigureCanvasTkAgg(self.scatter_figure, master=scatter_graph_frame)
            self.scatter_canvas.get_tk_widget().pack(fill="both", expand=True)

            # Coefficient text box for scatter plot
            self.scatter_coefficient_text = tk.Text(scatter_frame, height=2, width=30)
            self.scatter_coefficient_text.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
            self.scatter_coefficient_text.config(state='disabled')

            # Graph frame for matrix
            matrix_graph_frame = ttk.Frame(matrix_frame)
            matrix_graph_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

            self.matrix_figure, self.matrix_ax = plt.subplots(figsize=(5, 4))
            self.matrix_canvas = FigureCanvasTkAgg(self.matrix_figure, master=matrix_graph_frame)
            self.matrix_canvas.get_tk_widget().pack(fill="both", expand=True)

            # Coefficient text box for matrix
            self.matrix_coefficient_text = tk.Text(matrix_frame, height=10, width=150)
            self.matrix_coefficient_text.grid(row=3, column=0, columnspan=1, padx=5, pady=5)
            self.matrix_coefficient_text.config(state='disabled')

    def show_scatter_plot(self):
        if self.data is None:
            return

        year = self.year_var.get()
        region = self.region_var.get()
        factor1 = self.factor1_var.get()
        factor2 = self.factor2_var.get()

        if year == "All":
            data_to_plot = self.data
        else:
            year = int(year)
            data_to_plot = self.data[self.data["Year"] == year]

        if region != "All":
            regions = self.region_listbox.curselection()
            selected_regions = [self.region_listbox.get(region) for region in regions]
            data_to_plot = data_to_plot[data_to_plot["Region"].isin(selected_regions)]

        self.scatter_ax.clear()
        sns.scatterplot(data=data_to_plot, x=factor1, y=factor2, hue="Region", ax=self.scatter_ax)

        # Add linear regression line
        slope, intercept, _, _, _ = linregress(data_to_plot[factor1], data_to_plot[factor2])
        x_vals = np.array(self.scatter_ax.get_xlim())
        y_vals = intercept + slope * x_vals
        self.scatter_ax.plot(x_vals, y_vals, color='red', linestyle='--', linewidth=2)

        self.scatter_ax.set_xlabel(factor1)
        self.scatter_ax.set_ylabel(factor2)
        self.scatter_ax.set_title(f"Scatter Plot: {factor1} vs {factor2}")

        # Calculate correlation coefficients
        corr_coef = np.corrcoef(data_to_plot[factor1], data_to_plot[factor2])
        self.scatter_coefficient_text.config(state="normal")
        self.scatter_coefficient_text.delete("1.0", tk.END)
        self.scatter_coefficient_text.insert(tk.END, f"Correlation Coefficient:\n{corr_coef[0, 1]:.2f}")
        self.scatter_coefficient_text.config(state="disabled")

        self.scatter_canvas.draw()

    def clear_scatter(self):
        self.year_var.set("")
        self.region_listbox.selection_clear(0, tk.END)
        self.factor1_var.set("")
        self.factor2_var.set("")
        self.scatter_ax.clear()
        self.scatter_canvas.draw()
        self.scatter_coefficient_text.config(state="normal")
        self.scatter_coefficient_text.delete("1.0", tk.END)
        self.scatter_coefficient_text.config(state="disabled")

    def show_correlation_matrix(self):
        if self.data is None:
            return

        year = self.matrix_year_var.get()

        if year == "All":
            data_to_plot = self.data
        else:
            data_to_plot = self.data[self.data["Year"] == int(year)]

        self.matrix_ax.clear()
        numeric_data = data_to_plot.select_dtypes(include=np.number)
        corr_matrix = numeric_data.corr()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", square=True, ax=self.matrix_ax)
        self.matrix_ax.set_title("Correlation Matrix")

        self.matrix_canvas.draw()

        self.matrix_coefficient_text.config(state="normal")
        self.matrix_coefficient_text.delete("1.0", tk.END)
        self.matrix_coefficient_text.insert(tk.END, "Correlation Coefficients:\n" + str(corr_matrix))
        self.matrix_coefficient_text.config(state="disabled")

    def clear_matrix(self):
        self.matrix_year_var.set("")
        self.matrix_ax.clear()
        self.matrix_canvas.draw()
        self.matrix_coefficient_text.config(state="normal")
        self.matrix_coefficient_text.delete("1.0", tk.END)
        self.matrix_coefficient_text.config(state="disabled")

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    correlation_page = CorrelationPage()
    correlation_page.run()