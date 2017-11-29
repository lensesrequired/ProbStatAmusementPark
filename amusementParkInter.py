from Tkinter import *
import Tkconstants, tkFileDialog
import amusementParkMaths, amusementParkMisc
import os, random, math, copy
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

    Label(self, text = "At any point in the program you can type in your own random numbers").grid(row = 0, column = 1, columnspan = 8)
    Label(self, text = "and hit a recalculate button to use your own values").grid(row = 1, column = 1, columnspan = 8)
    #parameter controls
    self.setParameterControls()

    #a couple useful buttons...
    Arrivals = Button(self, text='Arrival of Cars!', command=self.next)
    Arrivals.grid(row = 6, column = 4, columnspan = 2)

  def setParameterControls(self):
    Label(self, text = "Set Parameters").grid(row = 2, column = 1, columnspan = 8)

    Label(self, text = "Possion/Exponential", width = 20).grid(row = 3, column = 1, columnspan = 2)
    Label(self, text = "Lambda").grid(row = 4, column = 1)
    self.lam = Entry(self, width = 5)
    self.lam.grid(row = 4, column = 2)
    self.lam.insert(0, "4")

    Label(self, text = "Cont. Uniform").grid(row = 3, column = 3, columnspan = 2)
    Label(self, text = "a").grid(row = 4, column = 3)
    self.a = Entry(self, width = 5)
    self.a.grid(row = 4, column = 4)
    self.a.insert(0, "30") 
    Label(self, text = "b").grid(row = 5, column = 3)
    self.b = Entry(self, width = 5)
    self.b.grid(row = 5, column = 4)
    self.b.insert(0, "90") 

    Label(self, text = "Normal", width = 10).grid(row = 3, column = 5, columnspan = 2)
    Label(self, text = "Mu").grid(row = 4, column = 5)
    self.mu = Entry(self, width = 5)
    self.mu.grid(row = 4, column = 6)
    self.mu.insert(0, "1") 
    Label(self, text = "Sigma").grid(row = 5, column = 5)
    self.sigma = Entry(self, width = 5)
    self.sigma.grid(row = 5, column = 6)
    self.sigma.insert(0, "0.3")

    Label(self, text = "Gamma", width = 15).grid(row = 3, column = 7, columnspan = 2)
    Label(self, text = "Theta").grid(row = 4, column = 7)
    self.theta = Entry(self, width = 5)
    self.theta.grid(row = 4, column = 8)
    self.theta.insert(0, "1")

  def next(self):
    AOCroot = Tk()
    AOCroot.resizable(width=False, height=False)
    AOCroot.geometry('{}x{}'.format(950, 275))    
    params = [0 for i in range(7)]
    params[LAM] = self.lam.get()
    params[A] = self.a.get()
    params[B] = self.b.get()
    params[MU] = self.mu.get()
    params[SIGMA] = self.sigma.get()
    params[THETA] = self.theta.get()
    ArrivalOfCars(AOCroot, params).grid()

  def animate(self):
    pass

class ArrivalOfCars(Frame):
  def __init__(self, root, p):
    self.params = p

    Frame.__init__(self, root)

    #Family number establishment
    Label(self, text = "Family #").grid(row = 1, column = 0)
    for i in range(8):
      Label(self, text = str(i + 1)).grid(row = 2 + i, column = 0)

    #Arrival Time calculations
    #random number controls
    Label(self, text = "Random Seeds").grid(row = 1, column = 1)
    self.seedBoxes = []
    self.seeds = []
    for i in range(8):
      newBox = Entry(self, width = 15)
      newBox.grid(row = 2 + i, column = 1)
      self.seedBoxes.append(newBox)
      self.seeds.append(random.random())
      self.seedBoxes[i].insert(0, str(self.seeds[i])) 

    dist = [-(1/float(self.params[LAM]))*math.log(1-seed) for seed in self.seeds]
    self.arrivalTimes = [sum(dist[:i+1]) for i in range(8)]
    Label(self, text = "Arrival Times (minutes)").grid(row = 1, column = 2)
    self.arrivalTimeBoxes = []
    for i, a in enumerate(self.arrivalTimes):
      newLabel = Label(self, text = str(a))
      newLabel.grid(row = 2 + i, column = 2)
      self.arrivalTimeBoxes.append(newLabel)

    #Service Time calculations
    randomNums = [random.random() for i in range(8)]
    self.randomNumBoxes = []
    Label(self, text = "Random Nums").grid(row = 1, column = 3)
    for i, r in enumerate(randomNums):
      newEntry = Entry(self, width = 15)
      newEntry.insert(0, str(r))
      newEntry.grid(row = 2 + i, column = 3)
      self.randomNumBoxes.append(newEntry)

    self.serviceBoxes = []
    self.serviceTimes = [float(self.params[A]) + (randomNums[i]*(float(self.params[B])-float(self.params[A]))) for i in range(8)]
    Label(self, text = "Service Times (seconds)").grid(row = 1, column = 4)
    for i, s in enumerate(self.serviceTimes):
      newEntry = Label(self, text = str(s))
      newEntry.grid(row = 2 + i, column = 4)
      self.serviceBoxes.append(newEntry)

    #Queue and Done time calculations
    self.queueBoxes = []
    queue1 = []
    queue2 = []
    Label(self, text = "Queue", width = 8).grid(row = 1, column = 5)

    self.doneTimes = []
    for i in range(0, 8):
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
        l = Label(self, text = "Left")
        l.grid(row = 2 + i, column = 5)
        self.queueBoxes.append(l)
      else:
        if(len(queue2) > 0):
          queue2.append(queue2[-1] +(float(self.serviceTimes[i])/60))
          self.doneTimes.append(queue2[-1] + (float(self.serviceTimes[i])/60))
        else:
          queue2.append(self.arrivalTimes[i] +(float(self.serviceTimes[i])/60))          
          self.doneTimes.append(self.arrivalTimes[i] + (float(self.serviceTimes[i])/60))
        l = Label(self, text = "Right")
        l.grid(row = 2 + i, column = 5)
        self.queueBoxes.append(l)

    self.doneBoxes = []
    Label(self, text = "Done Times (minutes)").grid(row = 1, column = 6)
    for i, d in enumerate(self.doneTimes):
      newL = Label(self, text = str(d))
      newL.grid(row = 2 + i, column = 6)
      self.doneBoxes.append(newL)


    #a couple useful buttons...
    RecalcArrival = Button(self, text='Recalculate Arrival times!', command=self.calcArrival)
    RecalcArrival.grid(row = 10, column = 2, columnspan = 1)
    RecalcService = Button(self, text='Recalculate service times!', command=self.calcService)
    RecalcService.grid(row = 10, column = 4, columnspan = 1)
    Entrance = Button(self, text='Move to Park Entrance!', command=self.next)
    Entrance.grid(row = 10, column = 3, columnspan = 1)

  def calcArrival(self):
    self.seeds = []
    for i in range(8):
      self.seeds.append(float(self.seedBoxes[i].get()))

    dist = [-(1/float(self.params[LAM]))*math.log(1-seed) for seed in self.seeds]
    self.arrivalTimes = [sum(dist[:i+1]) for i in range(8)]

    for i, a in enumerate(self.arrivalTimes):
      self.arrivalTimeBoxes[i].config(text = str(a))

    self.calcService()

  def calcService(self):
    randomNums = []
    for i, r in enumerate(self.randomNumBoxes):
      randomNums.append(float(r.get()))

    self.serviceTimes = [float(self.params[A]) + (randomNums[i]*(float(self.params[B])-float(self.params[A]))) for i in range(8)]
    for i, s in enumerate(self.serviceTimes):
      self.serviceBoxes[i].config(text = str(s))

    queue1 = []  #append done times to each queue
    queue2 = []

    self.doneTimes = []
    for i in range(0, 8):
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
        self.queueBoxes[i].config(text = "Left")
      else:
        if(len(queue2) > 0):
          queue2.append(queue2[-1] + (float(self.serviceTimes[i])/60))
          self.doneTimes.append(queue2[-1] + (float(self.serviceTimes[i])/60))
        else:
          queue2.append(self.arrivalTimes[i] +(float(self.serviceTimes[i])/60))          
          self.doneTimes.append(self.arrivalTimes[i] + (float(self.serviceTimes[i])/60))
        self.queueBoxes[i].config(text = "Right")

    for i, d in enumerate(self.doneTimes):
      self.doneBoxes[i].config(text = str(d))

  def next(self):
    PEroot = Tk()
    PEroot.resizable(width=True, height=False)
    PEroot.geometry('{}x{}'.format(720, 550))
    ParkEntrance(PEroot, self.arrivalTimes, self.serviceTimes, self.doneTimes, self.params).grid()

class ParkEntrance(Frame):
  global seeds
  global params
  global serviceTimes, serviceBoxes
  global doneBoxes, queueBoxes

  def __init__(self, root, a, s, d, p):
    self.startTimes = [(x, y+1) for y,x in enumerate(d)]
    self.startTimes.sort()
    self.params = p

    Frame.__init__(self, root)

    #Family numbers
    Label(self, text = "Family #").grid(row = 1, column = 0)
    for i in range(8):
      Label(self, text = str(self.startTimes[i][1])).grid(row = 2 + i, column = 0)

    #Generate and calculate movement time
    self.Ys = [random.random() for i in range(8)]
    self.YBoxes = []
    Label(self, text = "Random Nums").grid (row = 1, column = 1)
    for i, s in enumerate(self.Ys):
      newEntry = Entry(self, width = 15)
      newEntry.insert(0, str(s))
      newEntry.grid(row = 2 + i, column = 1)
      self.YBoxes.append(newEntry)

    self.Zs = []
    for i in range(0,8,2):
      self.Zs.append(math.sin(2*math.pi*self.Ys[i])*math.sqrt((-2)*math.log(self.Ys[i+1])))
      self.Zs.append(math.cos(2*math.pi*self.Ys[i])*math.sqrt((-2)*math.log(self.Ys[i+1])))

    self.Xs = [(float(self.params[SIGMA])*z) + float(self.params[MU]) if (float(self.params[SIGMA])*z) + float(self.params[MU]) > 0 else 0 for z in self.Zs]
    self.XBoxes = []
    Label(self, text = "Movement Times (min)").grid(row = 1, column = 2)
    for i, s in enumerate(self.Xs):
      newEntry = Label(self, text = str(s))
      newEntry.grid(row = 2 + i, column = 2)
      self.XBoxes.append(newEntry)

    #Display enter queue time
    self.queueEnterTimes = []
    self.queueEnterBoxes = []
    Label(self, text = "Enter Queue Time (min)").grid (row = 1, column = 3)
    for i, x in enumerate(self.Xs):
      newEntry = Label(self, text = str(x + self.startTimes[i][0]))
      newEntry.grid(row = 2 + i, column = 3)
      self.queueEnterBoxes.append(newEntry)
      self.queueEnterTimes.append((x + self.startTimes[i][0], self.startTimes[i][1]))

    self.queueEnterTimes.sort()

    #Family numbers
    Label(self, text = "Family #").grid(row = 1, column = 0)
    for i in range(8):
      Label(self, text = str(self.queueEnterTimes[i][1])).grid(row = 13 + i, column = 0)

    #Calculate and display family sizes
    self.randomNums = [random.random() for i in range(8)]
    self.randomNumBoxes = []
    Label(self, text = "Random Nums").grid(row = 12, column = 1)
    for i, s in enumerate(self.randomNums):
      newEntry = Entry(self, width = 15)
      newEntry.insert(0, str(s))
      newEntry.grid(row = 13 + i, column = 1)
      self.randomNumBoxes.append(newEntry)

    Label(self, text = "Family Size").grid (row = 12, column = 2)
    self.familySizes = []
    self.familySizeBoxes = []
    for i, r in enumerate(self.randomNums):
      if r < 0.1:
        self.familySizes.append((1, self.queueEnterTimes[i][1]))
        newEntry = Label(self, text = "1 person")
      elif r < 0.4:
        self.familySizes.append((2, self.queueEnterTimes[i][1]))
        newEntry = Label(self, text = "2 people")
      elif r < 0.8:
        self.familySizes.append((3, self.queueEnterTimes[i][1]))
        newEntry = Label(self, text = "3 people")
      else:
        self.familySizes.append((4, self.queueEnterTimes[i][1]))
        newEntry = Label(self, text = "4 people")
      newEntry.grid(row = 13 + i, column = 2)
      self.familySizeBoxes.append(newEntry)

    #Ticketbooth nonsense
    self.gamRandomBoxes = []
    Label(self, text = "Random Nums").grid(row = 12, column = 3, columnspan = 4)
    for i in range(32):
      newEntry = Entry(self, width = 15)
      newEntry.insert(0, str(random.random()))
      newEntry.grid(row = 13 + (i//4), column = 3 + (i%4))
      self.gamRandomBoxes.append(newEntry)

    #Helpful Buttons
    RecalcMovement = Button(self, text='Recalculate Move Times!', command=self.calcMove)
    RecalcMovement.grid(row = 10, column = 2, columnspan = 1)
    RecalcFamilies = Button(self, text='Recalculate Family Sizes!', command=self.calcSize)
    RecalcFamilies.grid(row = 21, column = 2, columnspan = 1)
  
  def calcMove(self):
    self.Ys = []
    for i, y in enumerate(self.YBoxes):
      self.Ys.append(float(y.get()))

    self.Zs = []
    for i in range(0,8,2):
      self.Zs.append(math.sin(2*math.pi*self.Ys[i])*math.sqrt((-2)*math.log(self.Ys[i+1])))
      self.Zs.append(math.cos(2*math.pi*self.Ys[i])*math.sqrt((-2)*math.log(self.Ys[i+1])))

    self.Xs = [(float(self.params[SIGMA])*z) + float(self.params[MU]) if (float(self.params[SIGMA])*z) + float(self.params[MU]) > 0 else 0 for z in self.Zs]
    for i, x in enumerate(self.XBoxes):
      x.config(text = str(self.Xs[i]))

    #Display enter queue time
    self.queueEnterTimes = []
    for i, t in enumerate(self.queueEnterBoxes):
      t.config(text = str(self.Xs[i] + self.startTimes[i][0]))
      self.queueEnterTimes.append((self.Xs[i] + self.startTimes[i][0], self.startTimes[i][1]))

  def calcSize(self):
    self.randomNums = []
    for r in self.randomNumBoxes:
     self.randomNums.append(float(r.get()))

    self.familySizes = []
    for i, r in enumerate(self.randomNumBoxes):
      if float(r.get()) < 0.1:
        self.familySizes.append((1, self.queueEnterTimes[i][1]))
        self.familySizeBoxes[i].config(text = "1 person")
      elif float(r.get()) < 0.4:
        self.familySizes.append((2, self.queueEnterTimes[i][1]))
        self.familySizeBoxes[i].config(text = "2 people")
      elif float(r.get()) < 0.8:
        self.familySizes.append((3, self.queueEnterTimes[i][1]))
        self.familySizeBoxes[i].config(text = "3 people")
      else:
        self.familySizes.append((4, self.queueEnterTimes[i][1]))
        self.familySizeBoxes[i].config(text = "4 people")

if __name__=='__main__':
  root = Tk()
  root.resizable(width=False, height=False)
  root.geometry('{}x{}'.format(490, 250))
  AmusementPark(root).grid()
  root.mainloop()