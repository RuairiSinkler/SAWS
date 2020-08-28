import time
import random
import re
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk

import exceptions as err

import excel.excel_management as ex

# class WarningPage(tk.Frame):

#     def __init__(self, parent, controller, name="WarningPage", temp=False):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_rowconfigure(3, weight=1)
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(2, weight=1)

#         self.name = name
#         self.active = False
#         self.temp = temp

#         self.message = tk.StringVar()
#         w = tk.Label(self, textvariable=self.message, font=self.controller.mainFont)
#         w.grid(row=1, column=1)
#         button = tk.Button(
#             self, text="Continue", font=self.controller.mainFont, command=lambda:w.textvariable.set("Poop")
#         )
#         button.grid(row=2, column=1, sticky="ew")

#     def display_page(self, warning, belowThis=None):
#         self.active = True
#         self.message.set(warning.message)
#         self.controller.show_frame(self.name, belowThis=belowThis)
    
#     def hide_page(self):
#         self.active = False
#         self.controller.hide_frame(self.name)
#         if self.temp:
#             del self.controller.frames[self.name]
#             self.controller.warning_frames.remove(self)
#             self.destroy()

# class Controller(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)

#         self.screen_width = self.winfo_screenwidth() // 2
#         self.screen_height = self.winfo_screenheight() // 2
#         self.geometry("{0}x{1}+0+0".format(self.screen_width, self.screen_height))

#         self.container = tk.Frame(self)
#         self.container.pack(side="top", fill="both", expand=True)
#         self.container.grid_rowconfigure(0, weight=1)
#         self.container.grid_rowconfigure(2, weight=1)
#         self.container.grid_columnconfigure(0, weight=1)
#         self.container.grid_columnconfigure(2, weight=1)

#         self.mainFont = Font(size=25)
#         self.textFont = Font(size=15)
#         self.option_add('*Dialog.msg.font', self.mainFont)
#         self.option_add("*TCombobox*Listbox*Font", self.mainFont)

#         self.frames = {}
#         self.warning_frames = []

#         page_name = "Base"
#         frame = tk.Frame(self.container)
#         self.frames[page_name] = frame

#         # put all of the pages in the same location;
#         # the one on the top of the stacking order
#         # will be the one that is visible.
#         #frame.grid(row=1, column=1, sticky="nsew")
#         frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)
#         label = tk.Label(frame, text="Base Level")
#         label.pack()

#         warning_frame = self.create_frame(WarningPage, self.container)
#         self.warning_frames.append(warning_frame)
        


#     def show_frame(self, page_name, aboveThis=None, belowThis=None):
#         '''Show a frame for the given page name'''
#         frame = self.frames[page_name]
#         if belowThis:
#             frame.lower(belowThis)
#         else:
#             frame.lift(aboveThis)
            

#     def hide_frame(self, page_name):
#         '''Hide a frame for the given page name'''
#         frame = self.frames[page_name]
#         frame.lower()

#     def display_warning(self, warning):
#         if self.frames["WarningPage"].active:
#             current_timestamp = time.time_ns()
#             page_name = "TempWarningPage.{}".format(current_timestamp)

#             frame = WarningPage(parent=self.container, controller=self, name=page_name, temp=True)
#             self.frames[page_name] = frame

#             # put all of the pages in the same location;
#             # the one on the top of the stacking order
#             # will be the one that is visible.
#             #frame.grid(row=1, column=1, sticky="nsew")
#             frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)

#             self.frames[page_name].display_page(warning, belowThis=self.warning_frames[-1])
#             self.warning_frames.append(frame)
#         else:
#             self.frames["WarningPage"].display_page(warning)
            

#     def create_frame(self, F, container, name=None, *args):
#         page_name = F.__name__
#         if name is not None:
#             page_name = name
#         frame = F(parent=container, controller=self, *args)
#         self.frames[page_name] = frame

#         # put all of the pages in the same location;
#         # the one on the top of the stacking order
#         # will be the one that is visible.
#         #frame.grid(row=1, column=1, sticky="nsew")
#         frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)
#         return frame
        
# root = Controller()
# root.display_warning(err.SAWSWarning("Warning 1"))
# root.display_warning(err.SAWSWarning("Warning 2"))
# root.display_warning(err.SAWSWarning("Warning 3"))
# root.display_warning(err.SAWSWarning("Warning 4"))
# root.mainloop()s

excel = ex.WorksheetManager("./", "rations")
excel.update_sheets("rations")
