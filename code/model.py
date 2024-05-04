class Model:
    def __init__(self):
        self.current_page = None

    def set_current_page(self, page):
        self.current_page = page

    def get_current_page(self):
        return self.current_page
