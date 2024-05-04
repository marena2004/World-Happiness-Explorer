from model import Model


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = None

    def set_view(self, view):
        self.view = view

    def show_home(self):
        self.view.show_page("Home")

    def show_explore(self):
        self.view.show_page("Explore")

    def show_about(self):
        self.view.show_page("About")

    def quit_application(self):
        self.view.quit()