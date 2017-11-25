from Tkinter import *
import Tkconstants, tkFileDialog
import amusementParkMaths, amusementParkMisc
import os, random
from shutil import copyfile

class AmusementPark(Frame):
  
  def __init__(self, root):

    global listbox
    global AllTagList
    global seeds
    global seedBoxes
    
    Frame.__init__(self, root)

    #random number controls
    Label(self, text = "Random Seeds").grid(row = 1, column = 1)
    GenerateRand = Button(self, text='Generate', command=self.genRand)
    GenerateRand.grid(row=1, column = 2)
    seedBoxes = []
    for i in range(8):
      newBox = Entry(self)
      newBox.grid(row = 2 + i, column = 1, columnspan = 2)
      seedBoxes.append(newBox)
    Label(self, text = "Type in boxes to use your own values").grid(row = 10, column = 1, columnspan = 2)

  def genRand(self):
    seeds = []
    for i in range(8):
      newRand = random.random()
      seeds.append(newRand)
      seedBoxes[i].delete(0, END)
      seedBoxes[i].insert(0, str(newRand)) 


if __name__=='__main__':
  root = Tk()
  root.resizable(width=True, height=True)
  root.geometry('{}x{}'.format(500, 395))
  AmusementPark.folderpath = ''
  AmusementPark.newfolderpath = ''
  AmusementPark.AllTagList = []
  AmusementPark.photolist = []
  AmusementPark(root).grid()
  root.mainloop()