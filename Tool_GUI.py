

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import filedialog
from Properties import SearchAA
from SignalPeptides import SignalPeptide

def button_browse_callback():
    """ What to do when the Browse button is pressed """
    filename1 = filedialog.askopenfilename()
    entry.delete(0, END)
    entry.insert(0, filename1)

def button_browse_callback3():
    filename3 = filedialog.askopenfilename(initialfile="aaindex1.txt")
    entry3.delete(0, END)
    entry3.insert(0, filename3)

def button_browse_callback4():
    filename4 = filedialog.askopenfilename(initialfile="humansequencessp.txt")
    entry4.delete(0, END)
    entry4.insert(0, filename4)

def go_press():
    """ what to do when the "Go" button is pressed """
    input_file = entry.get()
    propertyid = entry2.get()
    propertyfile = entry3.get()
    backgroundfile= entry4.get()

    if input_file.rsplit(".")[-1] != "txt":
        return messagebox.showerror(title="Error", message="Filename must end in .txt")
    if input_file == '':
        return messagebox.showwarning('Warning',  'Empty Field')

    if backgroundfile.rsplit(".")[-1] != "txt":
        return messagebox.showerror(title="Error", message="Filename must end in .txt")
    if backgroundfile == '':
        return messagebox.showwarning('Warning',  'Empty Field')

    if propertyid == '':
        return messagebox.showwarning('Warning',  'Empty Field')

    if propertyfile == '':
        return messagebox.showwarning('Warning',  'Empty Field')

    if "aaindex1.txt" in propertyfile:
        SearchAA.AAindex_property(input_file, propertyfile, propertyid, backgroundfile)
    else:
        SearchAA.user_property(input_file, propertyfile, backgroundfile)

    SignalPeptide(input_file, backgroundfile)
    import time
    progress['value'] = 20
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 40
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 50
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 60
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 80
    root.update_idletasks()
    time.sleep(1)
    progress['value'] = 100
root = Tk()
root.title("Protein Property Calculator Tool")

frame = Frame(root)
progress = Progressbar(root, orient = HORIZONTAL,
              length = 100, mode = 'determinate')
frame1 = Frame(frame)

label = Label(frame1, text="FASTA file: ").grid(row=0, column=1)
statusText = StringVar()
entry = Entry(frame1, textvariable= statusText)
entry.grid(row=1, column=1)
button_browse = Button(frame1,
                       text="Browse",
                       command=button_browse_callback).grid(row=1,column=2)
frame1.pack(side= TOP)

Label(frame1, text= "Property ID:").grid(row=0,column=3)
v2 = StringVar()
entry2 = Entry(frame1, textvariable= v2)
entry2.grid(row=1, column=3,ipadx= 5)
frame1.pack(side= TOP)

Label(frame1, text= "Property File:").grid(row=3,column=1)
v3 = StringVar()
entry3 = Entry(frame1, textvariable= v3)
entry3.grid(row=4, column=1,ipadx= 5)
button_browse2 = Button(frame1,
                       text="Browse",
                       command=button_browse_callback3).grid(row=4,column=2)
frame1.pack(side= TOP)

Label(frame1, text= "Background File:").grid(row=3,column=3)
v4 = StringVar()
entry4 = Entry(frame1, textvariable= v4)
entry4.grid(row=4, column=3,ipadx= 5)
button_browse3 = Button(frame1,
                       text="Browse",
                       command=button_browse_callback4).grid(row=4,column=4)

frame1.pack(side= TOP)
Frame(frame,height=2, relief = GROOVE).pack(side = TOP, fill =
  BOTH, pady= 5)







frame.pack(side = TOP, padx = 10)
progress.pack(pady = 10)
button_go = Button(root,
                   text="Go",
                   comman=go_press).pack(side= TOP, pady= 5)

button_exit = Button(root,
                     text="Exit",
                     command=sys.exit).pack(side = BOTTOM, pady = 5)



mainloop()


