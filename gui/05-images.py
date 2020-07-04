from tkinter import *
from PIL import ImageTk, Image
import sqlite3

root = Tk()
root.title("Images and Icons")
root.iconbitmap('images/sync.ico')
root.geometry("650x650")

img = Image.open('images/astro.jpg')
w, h = img.size
new_width = 400
new_height = round((new_width/w) * h)
img_tk = ImageTk.PhotoImage(Image.open('images/astro.jpg').resize((new_width, new_height)))
img_label = Label(root, image=img_tk, padx=10, pady=10)
img_label.pack()

root.mainloop()