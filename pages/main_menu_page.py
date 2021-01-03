import tkinter as tk
import tkinter.font as tkfont

import pages.page_tools.font_manager as fm
from pages.page_tools.vertical_scrolled_frame import VerticalScrolledFrame
from pages.page_tools.ration import Ration

class MainMenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        db_rations = self.controller.ration_db.get_all_rations()

        title_label = tk.Label(self, text="Main Menu", font=self.controller.main_font)
        title_label.pack()

        self.buttons = []

        self.ration_options = VerticalScrolledFrame(self)
        self.ration_options.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.ration_options.interior.columnconfigure(0, weight=1)

        self.update_idletasks()
        print("---MAINMENU INIT---")
        for db_ration in db_rations:
            ration = Ration.from_db_ration(db_ration)
            # print(ration.__dict__)
            button_font = tkfont.Font(size=self.controller.main_font['size'])
            button = tk.Button(
                self.ration_options.interior, text=ration.name, font=button_font,
                command=lambda ration=Ration.copy(ration): self.controller.frames["RationPage"].display_page(ration)
            )
            self.buttons.append(button)
            button_row = len(self.buttons)
            button.grid(row=button_row, column=0, padx=10, pady=5, stick="nsew")
            self.ration_options.interior.grid_rowconfigure(button_row, weight=1, uniform="ration_buttons")
            fm.resize_font_width(button["text"], button_font, self.controller.screen_width, padding=50)
            self.controller.after(1000, lambda ration=ration: self.temp_loop_print(ration))

        button = tk.Button(
            self, text="Quit", font=self.controller.main_font, command=lambda: self.controller.show_frame("SplashPage")
        )
        button.pack(side=tk.BOTTOM, fill=tk.X)

    def add_incomplete_ration(self, ration):
        button_text = "Incomplete {} for {}".format(ration.name, ration.house)
        button_font = tkfont.Font(size=self.controller.main_font['size'])
        button = tk.Button(
            self.ration_options.interior, text=button_text, font=button_font,
            bg="red2", fg="white", activebackground="red", activeforeground="white"
        )
        button.configure(command=lambda ration=Ration.copy(ration), button=button: self.controller.frames["RationPage"].display_page(ration, button))
        self.buttons.insert(0, button)
        self.reset_buttons()
        fm.resize_font_width(button["text"], button_font, self.controller.screen_width, padding=50)

    def remove_button(self, button):
        button.grid_forget()
        self.buttons.remove(button)
        self.reset_buttons()

    def temp_loop_print(self, ration):
        print(ration.__dict__)
        self.controller.after(1000, lambda ration=ration: self.temp_loop_print(ration))

    def reset_buttons(self):
        for button in self.buttons:
            button.grid_forget()
        for i, button in enumerate(self.buttons):
            button.grid(row=i, column=0, padx=10, pady=5, stick="nsew")
            self.ration_options.interior.grid_rowconfigure(i, weight=1, uniform="ration_buttons")
        