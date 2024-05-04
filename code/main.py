from tkinter import Tk
from code.controller import Controller
from view import View

if __name__ == "__main__":
    root = Tk()
    controller = Controller()
    view = View(controller)
    controller.set_view(view)
    root.mainloop()
