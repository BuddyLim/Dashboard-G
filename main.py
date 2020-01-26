from tkinter import filedialog, Label, Tk, Button, StringVar, Canvas, Scrollbar,Listbox, END, Frame, ttk, OptionMenu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
# from tkinter import *
from PIL import Image,ImageTk
import darknet_video as dv
import os

def file_prompt():
    # Creates a window to ask for video file
    # TODO: If no video, don't allow results 
    global file_Path

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

    # Scrollbar for the x number of warnings and display results
    frame.place(y = 60, relx = 0.5, rely = 0.5, anchor = "center")
    listbox.pack(side ="left" , fill="y")

    scrollbar.config(command = listbox.yview)
    scrollbar.pack(side = "right" , fill = "y")

    listbox.config(yscrollcommand = scrollbar.set)

    # Displays the time of the warning and the count 
    for count in warning_dict:
        time = warning_dict[count]/30
        listbox.insert(END, "Warning no: {} at time: {:.2f}s".format(count,time))

    backbutton.place(y= 180, relx = 0.5, rely = 0.5, anchor = "center")

    # Displays the warning count
    if(w_count == 0):
        w_display = Label(root, textvariable = var, relief = "flat", fg = "#08A4BD")
    else:
        w_display = Label(root, textvariable = var, relief = "flat", fg = "#B23A48")

    w_display.place(y = -60, relx = 0.5, rely = 0.5, anchor = "center")
    var.set("Number of warnings: " + str(w_count))
    
    elements.append(w_display)

    # TODO: Revise the number of warning threshold
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
        writeresults(warning_dict)
        warning_dict.clear()
        elements = root.winfo_children()
        root.after(100, displayresults)
        refreshed = True

def writeresults(warning_dict):

    global file_Path

    counter = 0
    import os,io,datetime,re
    from datetime import datetime

    # Get the current datetime today
    d = datetime.today()
    
    if(os.stat("test.txt").st_size == 0):
        with open("test.txt", "a+") as f:
            f.write(str(counter + 1) + ". " + str(d.strftime('%d-%m-%Y')) + " " + str(len(warning_dict))+"\n")
            # for count in warning_dict:
            #     time = warning_dict[count]/30
            #     f.write(str(counter + 1) + ". " + str(file_Path) + " Warning no: {} at time: {:.2f}s\n".format(count,time))
        f.close()

    else:
        with open("test.txt") as f:
            for line in f:
                pass
            last_line = line
            # strcounter = last_line.split('.')
            # counter = int(strcounter[0])
        f.close()

        strcounter = last_line.split('.')
        counter = int(strcounter[0])

        with open("test.txt", "a+") as f:
            # counter = int(last_line[0])
            f.write(str(counter + 1) + ". " + str(d.strftime('%d-%m-%Y')) + " " + str(len(warning_dict))+"\n")
        f.close()

def history():
    global dateselect, change

    addvideo.place_forget()
    badgesbutton.place_forget()
    quitexe.place_forget()
    
    plotwarning(0)

    if(change == False):
        dateselect.trace('w', rangechange)
        change = True

def rangechange(*args):

    print(dateselect.get())
    if "Week" in dateselect.get():
        plotwarning(0)
    elif "Month" in dateselect.get():
        plotwarning(1)
    elif "Year" in dateselect.get():
        plotwarning(2)

def plotwarning(daterange):
    from pandas import DataFrame
    import matplotlib
    from collections import OrderedDict
    from datetime import datetime, timedelta
    from file_read_backwards import FileReadBackwards

    global elements, ranges, backbutton

    date_warning = OrderedDict()

    counter = 0
    recent = 0
    second_recent = 0
    messagedisplay = StringVar()
    datemessage = StringVar()

    if(daterange == 0):
        delta = timedelta(days=7)
    elif(daterange == 1):
        delta = timedelta(days = 30)
    elif(daterange == 2):
        delta = timedelta(days = 365)

    with FileReadBackwards("test.txt", encoding = "utf-8") as f:
        for line in f:
            text = line.split(" ")
            strdate = text[1]
            date = datetime.strptime(strdate, '%d-%m-%Y')
            if((datetime.today() - date) <= delta):
                # Equivalent to C# ? operator 
                # date_warning[date] = int(date_warning[date]) + int(text[2]) if (date in date_warning) else date_warning[date] = int(text[2])
                if(date in date_warning):
                    date_warning[date] = int(date_warning[date]) + int(text[2])
                else:
                    date_warning[date] = int(text[2])
                if(counter !=2):
                    if(counter == 0):
                        recent = date_warning[date]
                        recentdate = date.strftime('%d-%m-%Y')
                        counter+=1
                    elif(counter == 1):
                        second_recent = date_warning[date]
                        secondrecent_date = date.strftime('%d-%m-%Y')
                        counter+=1
            else:
                break
    
    if(recent <= second_recent):
        messagedisplay.set("Your recent driving performance has increased")
        messagelabel = Label(root, textvariable = messagedisplay, relief = "flat", fg = "#08A4BD")

        datemessage.set("From {} to {} ".format(secondrecent_date,recentdate))
        datelabel = Label(root, textvariable = datemessage, relief = "flat")
    else:
        messagedisplay.set("Your recent driving performance has decreased")
        messagelabel = Label(root, textvariable = messagedisplay, relief = "flat", fg = "#B23A48")

        datemessage.set("From {} to {} ".format(secondrecent_date,recentdate))
        datelabel = Label(root, textvariable = datemessage, relief = "flat")

    datelabel.place(y = 165, relx = 0.5, rely = 0.5, anchor = "center")
    messagelabel.place(y = 185, relx = 0.5, rely = 0.5, anchor = "center")
    # Converting dict to list so that dataframe is able to construct
    df = DataFrame(list(date_warning.items()), columns = ['Date','Warning Count'])
    df.set_index('Date', inplace=True)
    matplotlib.rc('xtick',labelsize = 9.5)
    # Fig size is measured by inches DPI acts like a "magnifying glass"
    figure = plt.Figure(figsize=(6,6), dpi = 60)
    figure.patch.set_facecolor('#F0F0F0')
    # Position of subplot relative to other plots
    ax = figure.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure,root)
    chart_type.get_tk_widget().place(y = -20, relx = 0.5, rely = 0.5, anchor='center')
    
    # Calling line plot with y axes legend shown
    df.plot(kind = 'line',legend = True, ax = ax)
    
    backbutton.place(x = 80, y = 30, anchor = 'center')
    ranges.place(x = 340, y = 30, anchor = "center")

    Label.lift(ranges)
    Label.lift(backbutton)

    elements = root.winfo_children()
    elements.append(ranges)
    elements.append(backbutton)

def initwindow():
    addvideo.place(relx = 0.5, rely = 0.5, anchor = "center")
    badgesbutton.place(y = 40, relx = 0.5, rely = 0.5, anchor = "center")
    quitexe.place(y= 80, relx = 0.5, rely = 0.5, anchor = "center")

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
    
# Window properties 
root = Tk()
root.title("Lens G+")

# Warning counter string variable
var = StringVar()
dateselect = StringVar()

# Bool to force tkinter to create scroll once
refreshed = False
change = False

# List to add elements in a window to clear after Back
elements = []

rangelist = ["Previous Week","Previous Month", "Previous Year"]

dateselect = StringVar(root)
dateselect.set(rangelist[0]) # Default choice

ranges = OptionMenu(root, dateselect, *rangelist)
# ranges.config(height = 1)
file_Path = ""
# figure = plt.Figure(figsize=(6,6), dpi = 60)
# chart_type = FigureCanvasTkAgg(figure, root)

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
addvideo = Button(root, text = "Add video", width= 20, command = file_prompt)
badgesbutton = Button(root, text = "History", width= 20, command = history)
quitexe = Button(root, text ="Quit", width = 20, command = stop)
backbutton = Button(root, text = "Back", width= 15, height = 1, command = back)

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



