#########################################################################
## This creates a basic GUI with the tkinter library. The user can
## input event information into the textboxes, then an events 
## logistics form will be generated and displayed.
##
## Pressing [GENERATE] will generate and display an ELF 
## through generator.py
#########################################################################

## Sources: 
## https://stackoverflow.com/questions/28467285/how-do-i-bind-the-escape-key-to-close-this-window
## https://riptutorial.com/tkinter/example/29713/grid--#:~:text=tkinter%20grid()&text=The%20grid()%20geometry%20manager,%2C%20row%20%2C%20rowspan%20and%20sticky%20.
## https://www.youtube.com/watch?v=_lSNIrR1nZU
## https://www.daniweb.com/programming/software-development/code/216550/tkinter-to-put-a-gif-image-on-a-canvas-python

# Import libraries, use tkinter for GUI
from tkinter import *
from PIL import ImageTk, Image # Used for resizing the image
import sys

#############
## Functions
#############

# Button to Generate and add animation:
def generate():
    ## TODO: Connect generator.py to be triggered by the button
    print("TODO: Connect generator.py to be triggered by the button")


# Below is code attempting to do an animation

    # frameCnt = 
    # frames = [PhotoImage(file='img/loadingbar.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

    # def update(ind):
    #     frame = frames[ind]
    #     ind += 1
    #     if ind == frameCnt:
    #         ind = 0
    #     label.configure(image=frame)
    #     window.after(100, update, ind)
    # label = Label(window)
    # label.grid(row=2, column=4, sticky=W)
    # window.after(0, update, 0)
    # canvas = Canvas(width = 300, height = 200, bg = '#1e374a')
    # # pack the canvas into a frame/form
    # canvas.grid(row=2, column=4, sticky=W)
    # # load the .gif image file
    # # put in your own gif file here, may need to add full path
    # # like 'C:/WINDOWS/Help/Tours/WindowsMediaPlayer/Img/mplogo.gif'
    # gif1 = PhotoImage(file = 'img/loadingbar.gif')
    # # put gif image on canvas
    # # pic's upper left corner (NW) on the canvas is at x=50 y=10
    # canvas.create_image(50, 10, image = gif1, anchor = NW)



#############
## Main
#############

def main():
    # Press ESC to quit
    def close(frame):
        window.withdraw() # if you want to bring it back
        sys.exit() # if you want to exit the entire thing
    
    # Adding a blank div
    def add_div(row_num, col_num=0):
        Label (window, text="___", bg="#1e374a", fg="#1e374a", font="Arial 3", justify=LEFT).grid(row=row_num, column=col_num, sticky=SW)

    # Adding a tex entry box
    def add_entry(row_num, col_num=1):
        textentry = Entry(window, width=25, bg='white', font="Arial 6")
        textentry.grid(row=row_num, column=col_num, padx=10)

    # Window setup
    window = Tk()
    window.title("Events Logistics Generator")
    window.configure(bg='#1e374a')
    window.geometry("800x740")
    window.tk.call('tk', 'scaling', 3)
    window.bind('<Escape>', close)
    # window.wm_attributes('-transparentcolor', 'grey') #window['bg'] #Transparent background...

    # ESC to Quit label
    Label (window, text="Press ESC to quit", bg="#1e374a", fg="white", font="Helvetica 4", justify=RIGHT).grid(row=0, column=4, pady=10, sticky=NE)

    # Title
    Label (window, text="Events Logistics Generator", bg="#1e374a", fg="white", font="Arial 8", justify=RIGHT).grid(row=0, column=1)


    # TBF Logo
    logoimg = Image.open('img/Berkeley_Forum_logo.png')
    logoimg = logoimg.resize((200, 200), Image.ANTIALIAS)
    logophoto = ImageTk.PhotoImage(logoimg)

    Label (window, image=logophoto, bg='#1e374a') .grid(row=0, column=0, sticky=W)

    # Adding text
    # Title
    Label (window, text="What is the title of the event?", bg="#1e374a", fg="white", font="Arial 6", justify=LEFT).grid(row=1, column=0, padx=10, sticky=SW)
    add_entry(1)

    text = Label (window, text="format: Alan Turing at the Berkeley Forum", bg="#1e374a", fg="white", font = "Arial 4 italic", justify=LEFT)
    text.grid(row=2, column=0, padx=10, sticky=NW)

    
    add_div(3)

    # Type
    Label (window, text="What type of event is it?", bg = "#1e374a", fg="white", font="Arial 6", justify=LEFT) .grid(row=4, column=0, padx=10, sticky=SW)
    add_entry(4)

    text = Label (window, text="format: single, multi", bg="#1e374a", fg="white", font = "Arial 4 italic", justify=LEFT)
    text.grid(row=5, column=0, padx=10, sticky=NW)

    add_div(6)

    # Day
    Label (window, text="What is the day of the event?", bg = "#1e374a", fg="white", font="Arial 6", justify=LEFT) .grid(row=7, column=0, padx=10, sticky=SW)
    add_entry(7)

    text = Label (window, text="format: Monday, Tuesday, etc.", bg="#1e374a", fg="white", font = "Arial 4 italic", justify=LEFT)
    text.grid(row=8, column=0, padx=10, sticky=NW)

    add_div(9)

    # Time
    Label (window, text="What is the time of the event?", bg = "#1e374a", fg="white", font="Arial 6", justify=LEFT) .grid(row=10, column=0, padx=10, sticky=SW)
    add_entry(10)

    text = Label (window, text="format: 5:00 PM, 6:30 PM, etc.", bg="#1e374a", fg="white", font = "Arial 4 italic", justify=LEFT)
    text.grid(row=11, column=0, padx=10, sticky=NW)

    add_div(12)
    
    # Member Exlusions
    Label (window, text="Are there any member exclusions?", bg = "#1e374a", fg="white", font="Arial 6", justify=LEFT) .grid(row=13, column=0, padx=10, sticky=SW)
    add_entry(13)

    text = Label (window, text="format: Alan Turing, Grace Hopper, etc.", bg="#1e374a", fg="white", font = "Arial 4 italic", justify=LEFT)
    text.grid(row=14, column=0, padx=10, sticky=NW)

    add_div(15)

    # Job Exlusions
    Label (window, text="Are there any job exclusions?", bg = "#1e374a", fg="white", font="Arial 6", justify=LEFT) .grid(row=16, column=0, padx=10, sticky=SW)
    add_entry(16)

    text = Label (window, text="format: Tech Oversight/Set Up, Photographer, etc.", bg="#1e374a", fg="white", font = "Arial 4 italic", justify=LEFT)
    text.grid(row=17, column=0, padx=10, sticky=NW)

    add_div(18)

    # Number of Schedules to be generated
    Label (window, text="Number of sample schedules created?", bg = "#1e374a", fg="white", font="Arial 6", justify=LEFT) .grid(row=19, column=0, padx=10, sticky=SW)
    add_entry(19)

    text = Label (window, text="recommended: 10000", bg="#1e374a", fg="white", font = "Arial 4 italic", justify=LEFT)
    text.grid(row=20, column=0, padx=10, sticky=NW)

    add_div(21,2)

    # submit button
    Button(window, text="GENERATE!", width=10, padx=10, font="Arial 6", command=generate) .grid(row=22, column=4, sticky=E)

    # run the main loop
    window.mainloop()

if __name__ == "__main__":
    main()