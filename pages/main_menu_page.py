import tkinter as tk
from pages.page_tools.vertical_scrolled_frame import VerticalScrolledFrame
from pages.page_tools.ration import Ration

class MainMenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        db_rations = self.controller.ration_db.get_all_rations()

        title_label = tk.Label(self, text="Main Menu", font=self.controller.main_font)
        title_label.pack()

        ration_options = VerticalScrolledFrame(self)
        ration_options.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.extra_rations_space = tk.Frame(ration_options.interior)
        self.extra_rations_space.pack(side=tk.TOP)

        for db_ration in db_rations:
            ration = Ration.fromDbRation(db_ration)
            button = tk.Button(
                ration_options.interior, text=ration.name, font=self.controller.main_font,
                command=lambda ration=ration: self.controller.frames["RationPage"].display_page(ration)
            )
            button.pack(padx=10, pady=5, side=tk.TOP, fill=tk.X)

        button = tk.Button(
            self, text="Quit", font=self.controller.main_font, command=lambda: self.controller.show_frame("SplashPage")
        )
        button.pack(side=tk.BOTTOM, fill=tk.X)

    def add_incomplete_ration(self, ration):
        button_text = "Incomplete {} for {}".format(ration.name, ration.house)
        button = tk.Button(
            self.extra_rations_space, text=button_text, font=self.controller.main_font,
            bg="red", fg="white"
        )
        button.configure(command=lambda ration=ration, button=button: self.controller.frames["RationPage"].display_page(ration, button))
        button.pack(padx=10, pady=5, side=tk.TOP, fill=tk.X)