from Tkinter import *
import Tkconstants, tkFileDialog
import amusementParkMaths, amusementParkMisc
import os, random
from shutil import copyfile

class AmusementPark(Frame):
  
  def __init__(self, root):

    global seeds, seedBoxes

    global lam, a, b, mu, sigma, alpha, theta
    
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

    #parameter controls
    Label(self, text = "Parameters").grid(row = 1, column = 3, columnspan = 8)

    Label(self, text = "Possion/Exponential", width = 20).grid(row = 2, column = 3, columnspan = 2)
    Label(self, text = "Lambda").grid(row = 3, column = 3)
    lam = Entry(self, width = 5)
    lam.grid(row = 3, column = 4)
    lam.insert(0, "4") 

    Label(self, text = "Cont. Uniform").grid(row = 2, column = 5, columnspan = 2)
    Label(self, text = "a").grid(row = 3, column = 5)
    a = Entry(self, width = 5)
    a.grid(row = 3, column = 6)
    a.insert(0, "30") 
    Label(self, text = "b").grid(row = 4, column = 5)
    b = Entry(self, width = 5)
    b.grid(row = 4, column = 6)
    b.insert(0, "90") 

    Label(self, text = "Normal", width = 10).grid(row = 2, column = 7, columnspan = 2)
    Label(self, text = "Mu").grid(row = 3, column = 7)
    mu = Entry(self, width = 5)
    mu.grid(row = 3, column = 8)
    mu.insert(0, "1") 
    Label(self, text = "Sigma").grid(row = 4, column = 7)
    sigma = Entry(self, width = 5)
    sigma.grid(row = 4, column = 8)
    sigma.insert(0, "0.3")

    Label(self, text = "Gamma", width = 15).grid(row = 2, column = 9, columnspan = 2)
    Label(self, text = "Alpha").grid(row = 3, column = 9)
    alpha = Entry(self, width = 5)
    alpha.grid(row = 3, column = 10)
    alpha.insert(0, "tbd") 
    Label(self, text = "Theta").grid(row = 4, column = 9)
    theta = Entry(self, width = 5)
    theta.grid(row = 4, column = 10)
    theta.insert(0, "1")
  def genRand(self):
    seeds = []
    for i in range(8):
      newRand = random.random()
      seeds.append(newRand)
      seedBoxes[i].delete(0, END)
      seedBoxes[i].insert(0, str(newRand)) 


if __name__=='__main__':
  root = Tk()
  root.resizable(width=False, height=False)
  root.geometry('{}x{}'.format(1000, 800))
  AmusementPark.folderpath = ''
  AmusementPark.newfolderpath = ''
  AmusementPark.AllTagList = []
  AmusementPark.photolist = []
  AmusementPark(root).grid()
  root.mainloop()