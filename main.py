from tkinter import filedialog, Label, Tk, Button, StringVar
import darknet_video as dv
import os

def file_prompt():
    file_Path = filedialog.askopenfilename() #returns empty string if no video selected
    if(os.path.exists(file_Path)):
        dv.YOLO(file_Path)
        # print(file_Path)

def stop():
    root.destroy()

def badges():
    from darknet_video import w_count
    if(w_count >= 1):
        # w_display = Label(root, fg = "red")
        var.set("Number of warnings: " + str(w_count))
        # w_display.place(y = -20, relx = 0.5, rely = 0.5, anchor = "center")


root = Tk()
var = StringVar()
root.title("Lens G+")

addvideo = Button(root, text = "Add video", width=20, command = file_prompt)
addvideo.place(relx = 0.5, rely = 0.5, anchor = "center")

badgesbutton = Button(root, text = "Badges", width=20, command = badges)
badgesbutton.place(y = 40,relx = 0.5, rely = 0.5, anchor = "center")

quitexe = Button(root, text ="Quit", width = 20, command = stop)
quitexe.place(y= 80, relx = 0.5, rely = 0.5, anchor = "center")

w_display = Label(root,textvariable = var, relief = "raised", fg = "red")
w_display.place(y = -30, relx = 0.5, rely = 0.5, anchor = "center")

from darknet_video import w_count
if(w_count >= 1):
    # w_display = Label(root, fg = "red")
    var.set("Number of warnings: " + str(w_count))

root.geometry("250x250")
root.mainloop()
# root.mainloop()


