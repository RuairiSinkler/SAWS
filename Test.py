import tkinter as tk
from tkinter import ttk

# class VerticalScrolledFrame(tk.Frame):
#     """A pure Tkinter scrollable frame that actually works!

#     * Use the 'interior' attribute to place widgets inside the scrollable frame
#     * Construct and pack/place/grid normally
#     * This frame only allows vertical scrolling
#     """
#     def __init__(self, parent, *args, **kw):
#         tk.Frame.__init__(self, parent, *args, **kw)

#         # create a canvas object and a vertical scrollbar for scrolling it
#         vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
#         vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
#         canvas = tk.Canvas(self, bd=0, highlightthickness=0,
#                         yscrollcommand=vscrollbar.set)
#         canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
#         vscrollbar.config(command=canvas.yview)
        
#         # reset the view
#         canvas.xview_moveto(0)
#         canvas.yview_moveto(0)
        
#         # create a frame inside the canvas which will be scrolled with it
#         self.interior = interior = tk.Frame(canvas)
#         interior_id = canvas.create_window(0, 0, window=self.interior,
#                                            anchor=tk.NW)
        
#         # track changes to the canvas and frame width and sync them,
#         # also updating the scrollbar
#         def _configure_interior(event):
#             # update the scrollbars to match the size of the inner frame
#             size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
#             canvas.config(scrollregion="0 0 %s %s" % size)
#             if interior.winfo_reqwidth() != canvas.winfo_width():
#                 # update the canvas's width to fit the inner frame
#                 canvas.config(width=interior.winfo_reqwidth())
        
#         interior.bind('<Configure>', _configure_interior)
        
#         def _configure_canvas(event):
#             if interior.winfo_reqwidth() != canvas.winfo_width():
#                 # update the inner frame's width to fill the canvas
#                 canvas.itemconfigure(interior_id, width=canvas.winfo_width())
#         canvas.bind('<Configure>', _configure_canvas)


# root = tk.Tk()
# root.title("Scrollable Frame Demo")
# root.configure(background="gray99")
# screen_width = root.winfo_screenwidth() // 2
# screen_height = root.winfo_screenheight() // 2
# root.geometry("{0}x{1}+0+0".format(screen_width, screen_height))

# ingredients = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

# main = tk.Frame(root)
# main.pack()
# footer = tk.Frame(root)
# footer.pack(side=tk.BOTTOM)

# button = tk.Button(
#     footer, text="Back"
# )

# button.pack(side=tk.LEFT)

# button = tk.Button(
#     footer, text="Run"
# )

# button.pack(side=tk.LEFT)

# main.destroy()
# main = tk.Frame(root)
# main.pack(fill=tk.BOTH, expand=tk.TRUE)

# name = "Ration Name"
# label = tk.Label(
#     main, text=name
# )
# label.pack()

# ingredients_list = VerticalScrolledFrame(main)
# ingredients_list.pack(fill=tk.BOTH, expand=tk.TRUE)
# for ingredient in ingredients:
#     label = tk.Label(
#         ingredients_list.interior, text="{}kg".format(ingredient)
#     )
#     label.pack()

# root.mainloop()