import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt

root = tk.Tk()
root.title("Contacts DataBase")
root.iconbitmap('images/sync.ico')
root.geometry("600x90")


def graph():
    house_prices = np.random.normal(200000, 25000, 5000)
    plt.hist(house_prices, 200)
    plt.show()


my_button = ttk.Button(root, text="Graph It!", command=graph)
my_button.pack()

root.mainloop()
