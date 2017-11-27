from Tkinter import *
import Tkconstants, tkFileDialog
import amusementParkMaths, amusementParkMisc
import os, random, math
from shutil import copyfile

LAM = 0
A = 1
B = 2
MU = 3
SIGMA = 4
ALPHA = 5
THETA = 6

class AmusementPark(Frame):

  def __init__(self, root):
    global lam, a, b, mu, sigma, alpha, theta
    global seedBoxes

    Frame.__init__(self, root)


    #random number controls
    Label(self, text = "Random Seeds").grid(row = 1, column = 1)
    GenerateRand = Button(self, text='Generate', command=self.genRand)
    GenerateRand.grid(row=1, column = 2)
    self.seedBoxes = []
    for i in range(8):
      newBox = Entry(self)
      newBox.grid(row = 2 + i, column = 1, columnspan = 2)
      self.seedBoxes.append(newBox)
    Label(self, text = "Type in boxes to use your own values").grid(row = 10, column = 1, columnspan = 2)

    #parameter controls
    self.setParameterControls()

    #a couple useful buttons...
    Arrivals = Button(self, text='Arrival of Cars!', command=self.next)
    Arrivals.grid(row = 6, column = 4, columnspan = 2)
    
  def genRand(self):
    for i in range(8):
      newRand = random.random()
      self.seedBoxes[i].delete(0, END)
      self.seedBoxes[i].insert(0, str(newRand)) 

  def setParameterControls(self):
    Label(self, text = "Parameters").grid(row = 1, column = 3, columnspan = 8)

    Label(self, text = "Possion/Exponential", width = 20).grid(row = 2, column = 3, columnspan = 2)
    Label(self, text = "Lambda").grid(row = 3, column = 3)
    self.lam = Entry(self, width = 5)
    self.lam.grid(row = 3, column = 4)
    self.lam.insert(0, "4")

    Label(self, text = "Cont. Uniform").grid(row = 2, column = 5, columnspan = 2)
    Label(self, text = "a").grid(row = 3, column = 5)
    self.a = Entry(self, width = 5)
    self.a.grid(row = 3, column = 6)
    self.a.insert(0, "30") 
    Label(self, text = "b").grid(row = 4, column = 5)
    self.b = Entry(self, width = 5)
    self.b.grid(row = 4, column = 6)
    self.b.insert(0, "90") 

    Label(self, text = "Normal", width = 10).grid(row = 2, column = 7, columnspan = 2)
    Label(self, text = "Mu").grid(row = 3, column = 7)
    self.mu = Entry(self, width = 5)
    self.mu.grid(row = 3, column = 8)
    self.mu.insert(0, "1") 
    Label(self, text = "Sigma").grid(row = 4, column = 7)
    self.sigma = Entry(self, width = 5)
    self.sigma.grid(row = 4, column = 8)
    self.sigma.insert(0, "0.3")

    Label(self, text = "Gamma", width = 15).grid(row = 2, column = 9, columnspan = 2)
    Label(self, text = "Alpha").grid(row = 3, column = 9)
    self.alpha = Entry(self, width = 5)
    self.alpha.grid(row = 3, column = 10)
    self.alpha.insert(0, "tbd") 
    Label(self, text = "Theta").grid(row = 4, column = 9)
    self.theta = Entry(self, width = 5)
    self.theta.grid(row = 4, column = 10)
    self.theta.insert(0, "1")

  def next(self):
    AOCroot = Tk()
    AOCroot.resizable(width=False, height=False)
    AOCroot.geometry('{}x{}'.format(720, 275))    
    seeds = []
    for i in self.seedBoxes:
      seeds.append(float(i.get()))
    params = [0 for i in range(7)]
    params[LAM] = self.lam.get()
    params[A] = self.a.get()
    params[B] = self.b.get()
    params[MU] = self.mu.get()
    params[SIGMA] = self.sigma.get()
    params[ALPHA] = self.alpha.get()
    params[THETA] = self.theta.get()
    ArrivalOfCars(AOCroot, seeds, params).grid()

  def animate(self):
    pass

class ArrivalOfCars(Frame):
  global seeds
  global params
  global serviceTimes, serviceBoxes
  global doneBoxes, queueBoxes

  def __init__(self, root, s, p):
    self.seeds = s
    self.params = p

    Frame.__init__(self, root)

    #Arrival Time calculations
    dist = [-(1/float(self.params[LAM]))*math.log(1-seed) for seed in self.seeds]
    self.arrivalTimes = [sum(dist[:i+1]) for i in range(8)]
    Label(self, text = "Arrival Times (minutes)").grid(row = 1, column = 1)
    for i, a in enumerate(self.arrivalTimes):
      Label(self, text = str(a)).grid(row = 2 + i, column = 1)

    #Service Time calculations
    self.serviceBoxes = []
    self.serviceTimes = [random.randint(int(self.params[A]), int(self.params[B])) for i in range(8)]
    Label(self, text = "Service Times (seconds)").grid(row = 1, column = 2)
    for i, s in enumerate(self.serviceTimes):
      newEntry = Entry(self)
      newEntry.insert(0, str(s))
      newEntry.grid(row = 2 + i, column = 2)
      self.serviceBoxes.append(newEntry)

    #Queue and Done time calculations
    self.queueBoxes = []
    queue1 = [self.arrivalTimes[0] + (float(self.serviceTimes[0])/60)]
    queue2 = [self.arrivalTimes[1] + (float(self.serviceTimes[1])/60)]
    Label(self, text = "Queue").grid(row = 1, column = 3)
    l = Label(self, text = "1st")
    l.grid(row = 2, column = 3)
    self.queueBoxes.append(l)
    l = Label(self, text = "2nd")
    l.grid(row = 3, column = 3)
    self.queueBoxes.append(l)

    self.doneTimes = [self.arrivalTimes[0] + (float(self.serviceTimes[0])/60), self.arrivalTimes[1] + (float(self.serviceTimes[1])/60)]
    for i in range(2, 8):
      for c in queue1:
        if c < self.arrivalTimes[i]:
          queue1.remove(c)
        else:
          break
      for c in queue2:
        if c < self.arrivalTimes[i]:
          queue2.remove(c)
        else:
          break

      if(len(queue1) <= len(queue2)):
        if(len(queue1) > 0):
          queue1.append(queue1[-1] + (float(self.serviceTimes[i])/60))
          self.doneTimes.append(queue1[-1] + (float(self.serviceTimes[i])/60))
        else:
          queue1.append(self.arrivalTimes[i] +(float(self.serviceTimes[i])/60))          
          self.doneTimes.append(self.arrivalTimes[i] + (float(self.serviceTimes[i])/60))
        l = Label(self, text = "1st")
        l.grid(row = 2 + i, column = 3)
        self.queueBoxes.append(l)
      else:
        if(len(queue2) > 0):
          queue2.append(queue2[-1] +(float(self.serviceTimes[i])/60))
          self.doneTimes.append(queue2[-1] + (float(self.serviceTimes[i])/60))
        else:
          queue2.append(self.arrivalTimes[i] +(float(self.serviceTimes[i])/60))          
          self.doneTimes.append(self.arrivalTimes[i] + (float(self.serviceTimes[i])/60))
        l = Label(self, text = "2nd")
        l.grid(row = 2 + i, column = 3)
        self.queueBoxes.append(l)

    self.doneBoxes = []
    Label(self, text = "Done Times (minutes)").grid(row = 1, column = 4)
    for i, d in enumerate(self.doneTimes):
      newL = Label(self, text = str(d))
      newL.grid(row = 2 + i, column = 4)
      self.doneBoxes.append(newL)


    #a couple useful buttons...
    Recalc = Button(self, text='Recalculate with these service times!', command=self.calculate)
    Recalc.grid(row = 10, column = 2, columnspan = 1)
    Entrance = Button(self, text='Move to Park Entrance!', command=self.next)
    Entrance.grid(row = 10, column = 4, columnspan = 1)

  def calculate(self):
    self.serviceTimes = []
    for s in self.serviceBoxes:
      self.serviceTimes.append(int(s.get()))

    queue1 = [self.arrivalTimes[0] + (float(self.serviceTimes[0])/60)]  #append done times to each queue
    queue2 = [self.arrivalTimes[1] + (float(self.serviceTimes[1])/60)]

    self.doneTimes = [self.arrivalTimes[0] + (float(self.serviceTimes[0])/60), self.arrivalTimes[1] + (float(self.serviceTimes[1])/60)]
    for i in range(2, 8):
      for c in queue1:
        if c < self.arrivalTimes[i]:
          queue1.remove(c)
        else:
          break
      for c in queue2:
        if c < self.arrivalTimes[i]:
          queue2.remove(c)
        else:
          break

      if(len(queue1) <= len(queue2)):
        if(len(queue1) > 0):
          queue1.append(queue1[-1] + (float(self.serviceTimes[i])/60))
          self.doneTimes.append(queue1[-1] + (float(self.serviceTimes[i])/60))
        else:
          queue1.append(self.arrivalTimes[i] +(float(self.serviceTimes[i])/60))          
          self.doneTimes.append(self.arrivalTimes[i] + (float(self.serviceTimes[i])/60))
        self.queueBoxes[i].config(text = "1st")
      else:
        if(len(queue2) > 0):
          queue2.append(queue2[-1] + (float(self.serviceTimes[i])/60))
          self.doneTimes.append(queue2[-1] + (float(self.serviceTimes[i])/60))
        else:
          queue2.append(self.arrivalTimes[i] +(float(self.serviceTimes[i])/60))          
          self.doneTimes.append(self.arrivalTimes[i] + (float(self.serviceTimes[i])/60))
        self.queueBoxes[i].config(text = "2nd")

    for i, d in enumerate(self.doneTimes):
      self.doneBoxes[i].config(text = str(d))

  def next(self):
    PEroot = Tk()
    PEroot.resizable(width=False, height=False)
    PEroot.geometry('{}x{}'.format(720, 275))
    ParkEntrance(AOCroot, self.arrivalTimes, self.serviceTime, self.doneTimes, params).grid()

class ParkEntrance(Frame):
  global seeds
  global params
  global serviceTimes, serviceBoxes
  global doneBoxes, queueBoxes

  def __init__(self, root, a, s, d, p):
    self.startTimes = d
    self.params = p

    Frame.__init__(self, root)

if __name__=='__main__':
  root = Tk()
  root.resizable(width=False, height=False)
  root.geometry('{}x{}'.format(720, 275))
  AmusementPark(root).grid()
  root.mainloop()