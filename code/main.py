from tkinter import Tk
from controller import Controller
from view import View

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    controller = Controller()
    view = View(controller)
    controller.set_view(view)
    root.mainloop()


