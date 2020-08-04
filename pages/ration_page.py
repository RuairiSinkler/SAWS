import tkinter as tk
from pages.page_tools.vertical_scrolled_frame import VerticalScrolledFrame

class RationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.main = tk.Frame(self)
        self.main.pack()
        self.footer = tk.Frame(self)
        self.footer.pack(side=tk.BOTTOM)

        self.controller = controller

        self.ration_id = None
        self.name = None

        button = tk.Button(
            self.footer, text="Back", font=self.controller.mainFont,
            command=lambda: self.controller.show_frame("MainMenuPage")
        )

        button.pack(side=tk.LEFT)

        button = tk.Button(
            self.footer, text="Run", font=self.controller.mainFont,
            command=lambda: self.controller.frames["RunPage"].display_page(self.ration_id)
        )

        button.pack(side=tk.LEFT)

    def display_page(self, ration_id):

        self.main.destroy()
        self.main = tk.Frame(self)
        self.main.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.ration_id = ration_id

        self.name = self.controller.ration_db.get_ration(self.ration_id)[1]
        ingredients = self.controller.ration_db.get_ration_ingredients(ration_id)
        label = tk.Label(
            self.main, text=self.name, font=self.controller.mainFont
        )
        label.pack()

        ingredients_list = VerticalScrolledFrame(self.main)
        ingredients_list.pack(fill=tk.BOTH, expand=tk.TRUE)
        for ingredient in ingredients:
            label = tk.Label(
                ingredients_list.interior, text="{}, {}kg".format(ingredient[0], str(ingredient[1])), font=self.controller.mainFont
            )
            label.pack()

        self.controller.show_frame("RationPage")