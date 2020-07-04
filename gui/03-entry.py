from tkinter import *

root = Tk()

e = Entry(root, width=50, borderwidth=5)
e.pack()
e.insert(0, "<Enter Your Name>")


def myClick():
    hello = f"Hello {e.get()}"
    myLabel = Label(root, text=hello)
    myLabel.pack()


myButton = Button(root, text="Click Me!", padx=50, pady=50, command=myClick, fg='yellow', bg='#113355')
myButton.pack()

root.mainloop()