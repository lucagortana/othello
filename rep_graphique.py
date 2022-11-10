from tkinter import *
from PIL import ImageTk, Image
import os

try: 
    othellier = Image.open("othellier.PNG")
    pion_blanc = Image.open("pion_blanc.png")
    pion_noir = Image.open("pion_noir.png")
    
except IOError:
    pass

width_b, height_b = pion_blanc.size
xp, yp = width_b//10, height_b//10
pion_blanc = pion_blanc.resize((xp, yp))
pion_noir = pion_noir.resize((xp, yp))

def rep_graph(oth):
    for i in range(oth.shape[0]):
        for j in range(oth.shape[1]):
            if int(oth[i, j]) == 1:
                othellier.paste(pion_noir, (35+xp*i, 33+yp*j))
            if int(oth[i, j]) == 2:
                othellier.paste(pion_blanc, (35+xp*i, 33+yp*j)) 
    othellier.show()

root = Tk()
img = ImageTk.PhotoImage(rep_graph(othellier))
panel = Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()