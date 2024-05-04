import tkinter as tk
from tkinter import ttk
from pages import HomePage, ExplorePage, AboutPage


class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("World Happiness Explorer")

        self.nav_bar = NavigationBar(self, self.controller)
        self.nav_bar.pack(side=tk.TOP, fill=tk.X)

        self.container = tk.Frame(self, width=800, height=600)  # Set fixed size for the container frame
        self.container.pack(fill=tk.BOTH, expand=True)

        self.pages = {}
        self.pages["Home"] = HomePage(self.container, self.controller)
        self.pages["Explore"] = ExplorePage(self.container, self.controller)
        self.pages["About"] = AboutPage(self.container, self.controller)

        self.show_home()

    def show_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            if self.controller.model.get_current_page():
                self.controller.model.get_current_page().place_forget()
            self.controller.model.set_current_page(page)
            page.place(relwidth=1, relheight=1)  # Set the page to fill the container

    def show_home(self):
        self.show_page("Home")

    def quit(self):
        self.destroy()


class NavigationBar(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.home_button = ttk.Button(self, text="Home", command=self.controller.show_home)
        self.home_button.pack(side=tk.LEFT, padx=10)

        self.explore_button = ttk.Button(self, text="Explore", command=self.controller.show_explore)
        self.explore_button.pack(side=tk.LEFT, padx=10)

        self.about_button = ttk.Button(self, text="About", command=self.controller.show_about)
        self.about_button.pack(side=tk.LEFT, padx=10)

        self.quit_button = ttk.Button(self, text="Quit", command=self.quit_application)
        self.quit_button.pack(side=tk.RIGHT, padx=10)

    def quit_application(self):
        self.controller.quit_application()