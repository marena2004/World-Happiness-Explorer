import tkinter as tk
from tkinter import ttk
from model import Model
from overall_view import OverallPage
from correlation_view import CorrelationPage
from stat_view import StatPage
from trend_view import TrendPage


class Controller:
    """Controller class to manage navigation and interaction between model and views."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("World Happiness Explorer")
        self.model = Model()
        self.create_home_page()

    def create_home_page(self):
        """Create the home page with navigation buttons."""
        home_frame = ttk.Frame(self.root)
        home_frame.pack(padx=10, pady=10)

        # Navigation buttons
        overall_button = ttk.Button(home_frame, text="Overall Analysis", command=self.show_overall_page)
        overall_button.grid(row=0, column=0, padx=10, pady=5)

        correlation_button = ttk.Button(home_frame, text="Correlation Analysis", command=self.show_correlation_page)
        correlation_button.grid(row=0, column=1, padx=10, pady=5)

        statistics_button = ttk.Button(home_frame, text="Statistics", command=self.show_statistics_page)
        statistics_button.grid(row=0, column=2, padx=10, pady=5)

        trend_button = ttk.Button(home_frame, text="Trend Analysis", command=self.show_trend_page)
        trend_button.grid(row=0, column=3, padx=10, pady=5)

        # Exit button
        exit_button = ttk.Button(home_frame, text="Exit", command=self.root.quit)
        exit_button.grid(row=0, column=4, padx=10, pady=5)

    def show_overall_page(self):
        """Show the overall analysis page."""
        overall_page = OverallPage(self.root, self.model)
        overall_page.create_widgets()

    def show_correlation_page(self):
        """Show the correlation analysis page."""
        correlation_page = CorrelationPage(self.root, self.model)
        correlation_page.create_widgets()

    def show_statistics_page(self):
        """Show the statistics page."""
        stat_page = StatPage(self.root, self.model)
        stat_page.create_widgets()

    def show_trend_page(self):
        """Show the trend analysis page."""
        trend_page = TrendPage(self.root, self.model)
        trend_page.create_widgets()

    def run(self):
        """Run the application."""
        self.root.mainloop()


