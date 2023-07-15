import tkinter as tk
from tkinter import Canvas, filedialog, Text
from PIL import Image,ImageTk
import os

root=tk.Tk()
root.title("Age Detection")
root.iconbitmap(r'agedetection.ico')
root.configure()


apps=[]

if os.path.isfile('save.txt'):
    with open('save.txt','r') as f:
        tempApps=f.read()
        tempApps=tempApps.split(',')
        apps=[x for x in tempApps if x.strip()]

def addApp():
    


    for widget in frame.winfo_children():
        widget.destroy()

    filename=filedialog.askopenfilename(initialdir="/",title="Select File",
                                        filetypes=(("executables","*.exe"),("all files","*.*")))
    apps.append(filename)
    print(filename)
    for app in apps:
        label=tk.Label(frame,text=app)
        label.pack()
def runApps():
    for app in apps:
        os.startfile(app)


canvas = tk.Canvas(root,height=100,width=700)
canvas.pack()

instructions=tk.Label(root,text="DETECTING THE AGE OF A PERSON USING WEBCAM",font="Raleway")
instructions.pack()

logo=Image.open('logo.png')
logo=ImageTk.PhotoImage(logo)
logo_label=tk.Label(image=logo)
logo_label.image=logo
logo_label.pack()


frame=tk.Frame(root)
frame.place(relwidth=0.9)

openFile =tk.Button(root,text="Open",padx=10,
                    pady=5,fg="blue",bg="#00ffff",command=addApp)
openFile.pack()

runApps=tk.Button(root,text="Run",padx=10,
                   pady=5,fg="blue",bg="#00ffff",command=runApps)
runApps.pack()

for app in apps:
    label=tk.Label(frame,text=app)
    label.pack()

root.mainloop()

with open('save.txt','w') as f:
    for app in apps:
        f.write(app + ',')






