import tkinter as tk
# from tkinter import ttk 


# class ToggledFrame(tk.Frame):

    # def __init__(self, parent, text="", *args, **options):
    #     tk.Frame.__init__(self, parent, *args, **options)

#         self.show = tk.IntVar()
#         self.show.set(0)

#         self.title_frame = ttk.Frame(self)
#         self.title_frame.pack(fill="x", expand=1)

#         ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

#         self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
#                                             variable=self.show, style='Toolbutton')
#         self.toggle_button.pack(side="left")

#         self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)

#     def toggle(self):
#         if bool(self.show.get()):
#             self.sub_frame.pack(fill="x", expand=1)
#             self.toggle_button.configure(text='-')
#         else:
#             self.sub_frame.forget()
#             self.toggle_button.configure(text='+')


# if __name__ == "__main__":
#     root = tk.Tk()

#     t = ToggledFrame(root, text='Rotate', relief="raised", borderwidth=1)
#     t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

#     ttk.Label(t.sub_frame, text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
#     ttk.Entry(t.sub_frame).pack(side="left")

#     t2 = ToggledFrame(root, text='Resize', relief="raised", borderwidth=1)
#     t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

#     for i in range(10):
#         ttk.Label(t2.sub_frame, text='Test' + str(i)).pack()

#     t3 = ToggledFrame(root, text='Fooo', relief="raised", borderwidth=1)
#     t3.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

#     for i in range(10):
#         ttk.Label(t3.sub_frame, text='Bar' + str(i)).pack()

#     root.geometry("416x416")
#     root.mainloop()

# parent = tk.Tk()
# canvas = tk.Canvas(parent)
# scroll_y = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)

# frame = tk.Frame(canvas)
# # group of widgets
# for i in range(20):
#     tk.Label(frame, text='label %i' % i).pack()
# # put the frame in the canvas
# canvas.create_window(0, 0, anchor='nw', window=frame)
# # make sure everything is displayed before configuring the scrollregion
# canvas.update_idletasks()

# canvas.configure(scrollregion=canvas.bbox('all'), 
#                  yscrollcommand=scroll_y.set)
                 
# canvas.pack(fill='both', expand=True, side='left')
# scroll_y.pack(fill='y', side='right')

# class MenuButtons:
#     def __init__(self, parent, text = "", *args, **options):
#         tk.Frame.__init__(self, parent, text = "", *args, **options):


import tkinter as tk

def on_enter(e):
    myButton = tk.Button(root,text="Click Me", default = 'active')
    # myButton['background'] = 'green'

def on_leave(e):
    myButton['background'] = 'SystemButtonFace'

root = tk.Tk()
myButton = tk.Button(root,text="Click Me")
myButton.grid()


myButton.bind("<Enter>", on_enter)
myButton.bind("<Leave>", on_leave)

root.mainloop()