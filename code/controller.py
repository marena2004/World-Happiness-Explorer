""" Module for Controller"""
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

        # Create frames
        self.options_frame = ttk.Frame(self.root)
        self.main_frame = ttk.Frame(self.root)

        # Styling
        self.options_frame.configure(width=630, height=50)
        self.main_frame.configure(padding=(10, 10, 10, 10))

        # Create navigation buttons
        self.create_navigation_buttons()

        # Organize widgets
        self.organize_widgets()

    def create_navigation_buttons(self):
        """Create navigation buttons."""
        self.buttons = []
        button_names = ["Overall", "Stat", "Correlation", "Trend", "Exit"]
        button_commands = [self.show_overall_page, self.show_statistics_page,
                           self.show_correlation_page, self.show_trend_page, self.exit_app]

        for name, command in zip(button_names, button_commands):
            button = ttk.Button(self.options_frame, text=name, command=command, style="NavigationButton.TButton")
            self.buttons.append(button)

        # Define custom style for buttons
        style = ttk.Style()
        style.configure("NavigationButton.TButton", font=('Arial', 13), foreground='black', background='#F8A030')

    def organize_widgets(self):
        """Organize widgets."""
        self.options_frame.pack(pady=5)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        for i, button in enumerate(self.buttons):
            button.pack(side="left", padx=5)

    def show_overall_page(self):
        """Show the overall analysis page."""
        self.clear_main_frame()
        overall_page = OverallPage(self.main_frame, self.model)
        overall_page.create_widgets()

    def show_correlation_page(self):
        """Show the correlation analysis page."""
        self.clear_main_frame()
        correlation_page = CorrelationPage(self.main_frame, self.model)
        correlation_page.create_widgets()

    def show_statistics_page(self):
        """Show the statistics page."""
        self.clear_main_frame()
        stat_page = StatPage(self.main_frame, self.model)
        stat_page.create_widgets()

    def show_trend_page(self):
        """Show the trend analysis page."""
        self.clear_main_frame()
        trend_page = TrendPage(self.main_frame, self.model)
        trend_page.create_widgets()

    def exit_app(self):
        """Exit the application."""
        self.root.destroy()

    def clear_main_frame(self):
        """Clear the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def run(self):
        """Run the application."""
        self.root.mainloop()


