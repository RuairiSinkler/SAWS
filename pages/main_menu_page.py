import tkinter as tk
from pages.page_tools.vertical_scrolled_frame import VerticalScrolledFrame

class MainMenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        rations = self.controller.ration_db.get_all_rations()

        title_label = tk.Label(self, text="Main Menu", font=self.controller.main_font)
        title_label.pack()

        self.ration_options = VerticalScrolledFrame(self)
        self.ration_options.pack(fill=tk.BOTH, expand=tk.TRUE)

        for ration in rations:
            id = ration[0]
            name = ration[1]
            button = tk.Button(
                self.ration_options.interior, text=name, font=self.controller.main_font,
                command=lambda id=id: self.controller.frames["RationPage"].display_page(id)
            )
            button.pack(padx=10, pady=5, side=tk.TOP)

        button = tk.Button(
            self, text="Quit", font=self.controller.main_font, command=lambda: self.controller.show_frame("SplashPage")
        )
        button.pack(side=tk.BOTTOM, fill="x")

    def add_ration(self):
        ration = "hello"
        id = ration[0]
        name = ration[1]
        button = tk.Button(
            self.ration_options.interior, text=name, font=self.controller.main_font,
            command=lambda id=id: self.controller.frames["RationPage"].display_page(id)
        )
        button.pack(padx=10, pady=5, side=tk.TOP)