import tkinter as tk
from pages.page_tools.vertical_scrolled_frame import VerticalScrolledFrame

class MainMenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        rations = controller.ration_db.get_all_rations()

        title_label = tk.Label(self, text="Main Menu", font=controller.main_font)
        title_label.pack()

        ration_options = VerticalScrolledFrame(self)
        ration_options.pack(fill=tk.BOTH, expand=tk.TRUE)

        for ration in rations:
            id = ration[0]
            name = ration[1]
            button = tk.Button(
                ration_options.interior, text=name, font=controller.main_font,
                command=lambda id=id: controller.frames["RationPage"].display_page(id)
            )
            button.pack(padx=10, pady=5, side=tk.TOP)

        button = tk.Button(
            self, text="Quit", font=controller.main_font, command=lambda: controller.show_frame("SplashPage")
        )
        button.pack(side=tk.BOTTOM, fill="x")