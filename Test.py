import tkinter as tk
from tkinter import ttk

class ScrollableCanvas(tk.Canvas):

    def __init__(self, parent):
        # create a canvas object and a vertical scrollbar for scrolling it
        scrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        super().__init__(parent, bd=0, highlightthickness=0,
                           yscrollcommand=scrollbar.set)
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        scrollbar.config(command=self.yview)

        # reset the view
        self.xview_moveto(0)
        self.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(self)
        self.interior_id = self.create_window(0, 0, window=self.interior,
                                           anchor=tk.NW)

        self.interior.bind('<Configure>', self._configure_interior)

        self.bind('<Configure>', self._configure_canvas)
    
    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.winfo_width():
            # update the canvas's width to fit the inner frame
            self.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.winfo_width():
            # update the inner frame's width to fill the canvas
            self.itemconfigure(self.interior_id, width=self.winfo_width())

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        self.master = tk.Frame(self)
        self.master.pack()

        label = tk.Label(
            self.master, text="Ration Name",
        )
        label.pack()
        ingredients_list = tk.Frame(self.master)
        scrollable_canvas = ScrollableCanvas(ingredients_list)
        ingredients = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        for ingredient in ingredients:
            label = tk.Label(
                scrollable_canvas.interior, text="{}kg".format(ingredient[0])
            )
            label.pack()

        ingredients_list.pack()

        # # create a canvas object and a vertical scrollbar for scrolling it
        # vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        # vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        # canvas = tk.Canvas(self, bd=0, highlightthickness=0,
        #                 yscrollcommand=vscrollbar.set)
        # canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        # vscrollbar.config(command=canvas.yview)
        #
        # # reset the view
        # canvas.xview_moveto(0)
        # canvas.yview_moveto(0)
        #
        # # create a frame inside the canvas which will be scrolled with it
        # self.interior = interior = tk.Frame(canvas)
        # interior_id = canvas.create_window(0, 0, window=interior,
        #                                    anchor=tk.NW)
        #
        # # track changes to the canvas and frame width and sync them,
        # # also updating the scrollbar
        # def _configure_interior(event):
        #     # update the scrollbars to match the size of the inner frame
        #     size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
        #     canvas.config(scrollregion="0 0 %s %s" % size)
        #     if interior.winfo_reqwidth() != canvas.winfo_width():
        #         # update the canvas's width to fit the inner frame
        #         canvas.config(width=interior.winfo_reqwidth())
        #
        # interior.bind('<Configure>', _configure_interior)
        #
        # def _configure_canvas(event):
        #     if interior.winfo_reqwidth() != canvas.winfo_width():
        #         # update the inner frame's width to fill the canvas
        #         canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        # canvas.bind('<Configure>', _configure_canvas)


root = tk.Tk()
root.title("Scrollable Frame Demo")
root.configure(background="gray99")

scframe = VerticalScrolledFrame(root)
scframe.pack()

# lis = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
# for i, x in enumerate(lis):
#     btn = tk.Button(scframe.interior, height=1, width=20, relief=tk.FLAT,
#         bg="gray99", fg="purple3",
#         font="Dosis", text='Button ' + lis[i],
#         command=lambda i=i,x=x: openlink(i))
#     btn.pack(padx=10, pady=5, side=tk.TOP)
#
# def openlink(i):
#     print(lis[i])

root.mainloop()

# import RPi.GPIO as GPIO
# import time
# import tkinter as tk
#
# class WeightInput():
#
#     def __init__(self, weight_pin):
#         self.pin = weight_pin
#         GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#         # GPIO.add_event_detect(self.pin, GPIO.RISING, callback=lambda: print("button pressed"))
#         self.state = GPIO.input(self.pin)
#         self.check_input()
#
#     def check_input(self):
#         oldstate = self.state
#         newstate = GPIO.input(self.pin)
#         if oldstate != newstate:
#             self.state = newstate
#             if newstate == GPIO.LOW:
#                 print("button pressed")
#         time.sleep(0.2)
#         self.check_input()
#         # self.controller.after(200, self.check_input)
#
# def main():
#     try:
#         GPIO.setmode(GPIO.BCM)
#         input1 = WeightInput(19)
#         wait = input("Press enter to exit:")
#     except:
#         pass
#     finally:
#         GPIO.cleanup()
#
# if __name__ == "__main__":
#     try:
#         main()
#     except:
#         raise
