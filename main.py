from tkinter import filedialog, Label, Tk, Button, StringVar, Canvas, Scrollbar,Listbox, END, Frame
from PIL import Image,ImageTk
import darknet_video as dv
import os

def file_prompt():
    # Creates a window to ask for video file
    # TODO: If no video, don't allow results 
    file_Path = filedialog.askopenfilename() #returns empty string if no video selected
    if(os.path.exists(file_Path)):
        dv.YOLO(file_Path)

    # Hides the button
    addvideo.place_forget()
    badgesbutton.place_forget()
    quitexe.place_forget()

    displayresults()

def displayresults():
    global elements, refreshed

    from darknet_video import w_count, warning_dict
    from tkinter import ttk

    frame.place(y = 60, relx = 0.5, rely = 0.5, anchor = "center")
    listbox.pack(side ="left" , fill="y")

    scrollbar.config(command = listbox.yview)
    scrollbar.pack(side = "right" , fill = "y")

    listbox.config(yscrollcommand = scrollbar.set)

    for count in warning_dict:
        time = warning_dict[count]/30
        listbox.insert(END, "Warning no: {} at time: {:.2f}s".format(count,time))

    warning_dict.clear()

    backbutton.place(y= 180, relx = 0.5, rely = 0.5, anchor = "center")

    # Displays the warning count
    if(w_count == 0):
        w_display = Label(root, textvariable = var, relief = "flat", fg = "green")
    else:
        w_display = Label(root, textvariable = var, relief = "flat", fg = "red")

    w_display.place(y = -60, relx = 0.5, rely = 0.5, anchor = "center")
    var.set("Number of warnings: " + str(w_count))
    
    elements.append(w_display)

    # Displays the badges relative to the warning count
    if(w_count <= 5):
        bronzelabel.place(x = -90, y = -120, relx = 0.5, rely = 0.5, anchor = "center")
        silverlabel.place(x = 0, y = -120, relx = 0.5, rely = 0.5, anchor = "center")
        goldlabel.place(x = 90, y = -120, relx = 0.5, rely = 0.5, anchor = "center")

    elif(w_count <= 10):
        bronzelabel.place(x = -45, y = -120, relx = 0.5, rely = 0.5, anchor = "center")
        silverlabel.place(x = 45, y = -120, relx = 0.5, rely = 0.5, anchor = "center")

    elif(w_count <= 15):
        bronzelabel.place(x = 0, y = -120, relx = 0.5, rely = 0.5, anchor = "center")

    elif(w_count <=20):
        pass
    
    # Updating the window so that the warning count updates
    # Not including it will not update the results in the window 
    # Check to prevent constant update to elements list
    if(refreshed == False):
        elements = root.winfo_children()
        root.after(100,displayresults)
        refreshed = True

def back():
    global elements,refreshed

    refreshed = False

    for i,e in enumerate(elements):
        e.pack_forget()
        e.place_forget()

    del elements[:]

    initwindow()

def stop():
    root.destroy()

def badges():
    #TODO: Add list of previous badges in previous videos
    addvideo.place_forget()
    badgesbutton.place_forget()
    quitexe.place_forget()

def initwindow():
    addvideo.place(relx = 0.5, rely = 0.5, anchor = "center")
    badgesbutton.place(y = 40, relx = 0.5, rely = 0.5, anchor = "center")
    quitexe.place(y= 80, relx = 0.5, rely = 0.5, anchor = "center")

# Window properties 
root = Tk()
root.title("Lens G+")

# Warning counter string variable
var = StringVar()

# Bool to force tkinter to create scroll once
refreshed = False

# List to add elements in a window to clear after Back
elements = []

# Declaring images using PIL and tkinter
bronzeimg = Image.open("bronzestar.png")
bronzeimg = bronzeimg.resize((105,105))
bronze = ImageTk.PhotoImage(bronzeimg)
bronzelabel = Label(image = bronze) 
bronzelabel.image = bronze # IMPORTANT: Keeps a reference of the image in the memory
bronzelabel.place_forget()

silverimg = Image.open("silverstar.png")
silverimg = silverimg.resize((75,75))
silver = ImageTk.PhotoImage(silverimg)
silverlabel = Label(image = silver)
silverlabel.image = silver # IMPORTANT: Keeps a reference of the image in the memory
silverlabel.place_forget()

goldimg = Image.open("goldstar.png")
goldimg = goldimg.resize((100,100))
gold = ImageTk.PhotoImage(goldimg)
goldlabel = Label(image = gold)
goldlabel.image = gold # IMPORTANT: Keeps a reference of the image in the memory
goldlabel.place_forget()

# Declaring buttons to add into the video
addvideo = Button(root, text = "Add video", width=20, command = file_prompt)
badgesbutton = Button(root, text = "Badges", width=20, command = badges)
quitexe = Button(root, text ="Quit", width = 20, command = stop)
backbutton = Button(root, text = "Back", width=20, command = back)

# Getting the screen resolution and calculating the position to place
window_width = 416
window_height = 416
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
xcoord = int((screen_width/2) - (window_width/2))
ycoord = int((screen_height/2) - (window_height/2))

# Place the window in the middle of the screen
root.geometry("{}x{}+{}+{}".format(window_width,window_height,xcoord,ycoord))

#Creating 
frame = Frame(root)
scrollbar = Scrollbar(frame)
listbox = Listbox(frame, width = 50, height = 10)

def main():
    initwindow()

if __name__ == "__main__":
    main()
    root.update()
    root.mainloop()



