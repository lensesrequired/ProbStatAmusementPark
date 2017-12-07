from Tkinter import *
import Tkconstants, tkFileDialog
#import amusementParkMaths, amusementParkMisc
import os, random, math, copy
from shutil import copyfile

LAM = 0
A = 1
B = 2
MU = 3
SIGMA = 4
ALPHA = 5
THETA = 6
EXPTHETA = 7

class AmusementPark(Frame):

  def __init__(self, root):
    global lam, a, b, mu, sigma, alpha, theta
    global seedBoxes

    Frame.__init__(self, root)

    Label(self, text = "At any point in the program you can type in your own random numbers").grid(row = 0, column = 1, columnspan = 10)
    Label(self, text = "and hit a recalculate button to use your own values").grid(row = 1, column = 1, columnspan = 10)
    #parameter controls
    self.setParameterControls()

    #a couple useful buttons...
    Arrivals = Button(self, text='Arrival of Cars!', command=self.next)
    Arrivals.grid(row = 6, column = 5, columnspan = 2)

  def setParameterControls(self):
    Label(self, text = "Set Parameters").grid(row = 2, column = 1, columnspan = 10)

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

    Label(self, text = "Exponential", width = 15).grid(row = 3, column = 9, columnspan = 2)
    Label(self, text = "Theta").grid(row = 4, column = 9)
    self.exptheta = Entry(self, width = 5)
    self.exptheta.grid(row = 4, column = 10)
    self.exptheta.insert(0, "3")

  def next(self):
    AOCroot = Tk()
    AOCroot.resizable(width=True, height=True)
    AOCroot.geometry('{}x{}'.format(1270, 290))    
    params = [0 for i in range(8)]
    params[LAM] = self.lam.get()
    params[A] = self.a.get()
    params[B] = self.b.get()
    params[MU] = self.mu.get()
    params[SIGMA] = self.sigma.get()
    params[THETA] = self.theta.get()
    params[EXPTHETA] = self.exptheta.get()
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
    self.serviceTimes = [(float(self.params[A])/60) + (randomNums[i]*((float(self.params[B])/60)-(float(self.params[A])/60))) for i in range(8)]
    Label(self, text = "Service Times (minutes)").grid(row = 1, column = 4)
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
          self.doneTimes.append(max(queue1[-1], self.arrivalTimes[i]) +(float(self.serviceTimes[i])))
          queue1.append(max(queue1[-1], self.arrivalTimes[i]) +(float(self.serviceTimes[i])))
        else:
          queue1.append(self.arrivalTimes[i] +(float(self.serviceTimes[i])))          
          self.doneTimes.append(self.arrivalTimes[i] + (float(self.serviceTimes[i])))
        l = Label(self, text = "Left")
        l.grid(row = 2 + i, column = 5)
        self.queueBoxes.append(l)
      else:
        if(len(queue2) > 0):
          self.doneTimes.append(max(queue2[-1], self.arrivalTimes[i]) +(float(self.serviceTimes[i])))
          queue2.append(max(queue2[-1], self.arrivalTimes[i]) +(float(self.serviceTimes[i])))
        else:
          queue2.append(self.arrivalTimes[i] +(float(self.serviceTimes[i])))          
          self.doneTimes.append(self.arrivalTimes[i] + (float(self.serviceTimes[i])))
        l = Label(self, text = "Right")
        l.grid(row = 2 + i, column = 5)
        self.queueBoxes.append(l)

    self.doneBoxes = []
    Label(self, text = "Done Times (minutes)").grid(row = 1, column = 6)
    for i, d in enumerate(self.doneTimes):
      newL = Label(self, text = str(d))
      newL.grid(row = 2 + i, column = 6)
      self.doneBoxes.append(newL)

    self.waitTimes = []
    self.waitBoxes = []
    Label(self, text = "Wait Times (minutes)").grid(row = 1, column = 7)
    for i in range(len(self.doneTimes)):
      self.waitTimes.append(self.doneTimes[i] - (self.serviceTimes[i]+self.arrivalTimes[i]))
      newL = Label(self, text = str(self.doneTimes[i] - (self.serviceTimes[i]+self.arrivalTimes[i])))
      newL.grid(row = 2 + i, column = 7)
      self.waitBoxes.append(newL)

    waitTimeAvg = sum(self.waitTimes)/len(self.waitTimes)
    self.waitAvgLbl = Label(self, text = "Average Wait Time (minutes):\n" + str(waitTimeAvg))
    self.waitAvgLbl.grid(row = 10, column = 7)

    qLenAvg = sum(self.waitTimes)/(2*self.doneTimes[-1])
    self.qLenLbl = Label(self, text = "Average Queue\nLength: " + str(qLenAvg))
    self.qLenLbl.grid(row = 10, column = 5)


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

    self.serviceTimes = [float(self.params[A])/60 + (randomNums[i]*(float(self.params[B])/60-(float(self.params[A])/60))) for i in range(8)]
    for i, s in enumerate(self.serviceTimes):
      self.serviceBoxes[i].config(text = str(s))

    queue1 = []  #append done times to each queue
    queue2 = []

    self.doneTimes = []
    self.waitTimes = []
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
          self.doneTimes.append(max(queue1[-1], self.arrivalTimes[i]) + (float(self.serviceTimes[i])))
          queue1.append(max(queue1[-1], self.arrivalTimes[i]) + (float(self.serviceTimes[i])))
        else:
          self.doneTimes.append(self.arrivalTimes[i] + (float(self.serviceTimes[i])))
          queue1.append(self.arrivalTimes[i] +(float(self.serviceTimes[i])))          
        self.queueBoxes[i].config(text = "Left")
      else:
        if(len(queue2) > 0):
          queue2.append(max(queue2[-1], self.arrivalTimes[i]) + (float(self.serviceTimes[i])))
          self.doneTimes.append(max(queue2[-1], self.arrivalTimes[i]) + (float(self.serviceTimes[i])))
        else:
          queue2.append(self.arrivalTimes[i] +(float(self.serviceTimes[i])))          
          self.doneTimes.append(self.arrivalTimes[i] + (float(self.serviceTimes[i])))
        self.queueBoxes[i].config(text = "Right")

    for i, d in enumerate(self.doneTimes):
      self.doneBoxes[i].config(text = str(d))
      self.waitBoxes[i].config(text = str(d - self.arrivalTimes[i]-self.serviceTimes[i]))
      self.waitTimes.append(d - self.arrivalTimes[i]-self.serviceTimes[i])

    waitTimeAvg = sum(self.waitTimes)/len(self.waitTimes)
    self.waitAvgLbl.config(text = "Average Wait Time (minutes):\n" + str(waitTimeAvg))

    qLenAvg = sum(self.waitTimes)/(2*self.doneTimes[-1])
    self.qLenLbl.config(text = "Average Queue\nLength: " + str(qLenAvg))  

  def next(self):
    PEroot = Tk()
    PEroot.resizable(width=True, height=True)
    PEroot.geometry('{}x{}'.format(1310, 580))
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

    #Family numbers
    Label(self, text = "Family #").grid(row = 1, column = 0)
    for i in range(8):
      Label(self, text = str(self.startTimes[i][1])).grid(row = 13 + i, column = 0)

    #Calculate and display family sizes
    self.randomNums = [random.random() for i in range(8)]
    self.randomNumBoxes = []
    Label(self, text = "Random Nums").grid(row = 1, column = 4)
    for i, s in enumerate(self.randomNums):
      newEntry = Entry(self, width = 15)
      newEntry.insert(0, str(s))
      newEntry.grid(row = 2 + i, column = 4)
      self.randomNumBoxes.append(newEntry)

    Label(self, text = "Family Size").grid (row = 1, column = 5)
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
      newEntry.grid(row = 2 + i, column = 5)
      self.familySizeBoxes.append(newEntry)

    #Ticketbooth nonsense
    self.gamRandomBoxes = []
    Label(self, text = "Random Nums").grid(row = 12, column = 1, columnspan = 4)
    for i in range(32):
      newEntry = Entry(self, width = 15)
      newEntry.insert(0, str(random.random()))
      newEntry.grid(row = 13 + (i//4), column = 1 + (i%4))
      self.gamRandomBoxes.append(newEntry)

    serviceTimes = []
    for i in range(len(self.familySizes)):
      service = 0
      for j in range(self.familySizes[i][0]):
        service += -float(self.params[THETA])*math.log(1-float(self.gamRandomBoxes[4*i + j].get()))
      serviceTimes.append((service, self.familySizes[i][1]))

    self.sortedServiceTimes = []
    for i in range(8):
      for j in range(8):
        if self.queueEnterTimes[i][1] == serviceTimes[j][1]:
          self.sortedServiceTimes.append(serviceTimes[j])
    self.waitTimes = []

    booth1 = []
    booth2 = []
    self.doneTimes = []
    self.boothDir = []
    time = 0
    #sort these the other way for the loop
    #then sort them back for display
    for i in range(8):
      if len(booth1) == 0:
        booth1.append(float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
        self.doneTimes.append(float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
        self.waitTimes.append(0)

        newDir = Label(self, text = "Left")
        self.boothDir.append(newDir)
        newDir.grid(row = 13+i, column = 5)
        
      elif len(booth2) == 0:
        booth2.append(float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
        self.doneTimes.append(float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
        self.waitTimes.append(0)

        newDir = Label(self, text = "Right")
        self.boothDir.append(newDir)
        newDir.grid(row = 13+i, column = 5)

      else:
        if self.queueEnterTimes[i][0] >= booth1[0]:
          self.waitTimes.append(0)
          booth1.pop(0)
          booth1.append(self.waitTimes[-1] + float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
          self.doneTimes.append(self.waitTimes[-1] + float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])

          newDir = Label(self, text = "Left")
          self.boothDir.append(newDir)
          newDir.grid(row = 13+i, column = 5)

        elif self.queueEnterTimes[i][0] >= booth2[0]:
          self.waitTimes.append(0)
          booth2.pop(0)
          booth2.append(self.waitTimes[-1] + float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
          self.doneTimes.append(self.waitTimes[-1] + float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])

          newDir = Label(self, text = "Right")
          self.boothDir.append(newDir)
          newDir.grid(row = 13+i, column = 5)

        elif min(booth1[0], booth2[0]) == booth1[0]:
          self.waitTimes.append(booth1[0] - self.queueEnterTimes[i][0])
          booth1.pop(0)
          booth1.append(self.waitTimes[-1] + self.queueEnterTimes[i][0] + self.sortedServiceTimes[i][0])
          self.doneTimes.append(self.waitTimes[-1] + self.queueEnterTimes[i][0] + self.sortedServiceTimes[i][0])

          newDir = Label(self, text = "Left")
          self.boothDir.append(newDir)
          newDir.grid(row = 13+i, column = 5)

        elif min(booth1[0], booth2[0]) == booth2[0]:
          self.waitTimes.append(booth2[0] - self.queueEnterTimes[i][0])
          booth2.pop(0)
          booth2.append(self.waitTimes[-1] + self.queueEnterTimes[i][0] + self.sortedServiceTimes[i][0])
          self.doneTimes.append(self.waitTimes[-1] + self.queueEnterTimes[i][0] + self.sortedServiceTimes[i][0])

          newDir = Label(self, text = "Right")
          self.boothDir.append(newDir)
          newDir.grid(row = 13+i, column = 5)
          
    self.doneBoxes = []
    self.waitBoxes = []
    self.serviceBoxes = []
    Label(self, text = "Booth").grid(row = 12, column = 5)
    Label(self, text = "Service Times (minutes)").grid(row = 12, column = 6)
    Label(self, text = "Wait Times (minutes)").grid(row = 12, column = 8)
    Label(self, text = "Done Times (minutes)").grid(row = 12, column = 7)
    for i in range(8):
      newService = Label(self, text = str(self.sortedServiceTimes[i][0]))
      newService.grid(row = 13+i, column = 6)
      self.serviceBoxes.append(newService)

      newWait = Label(self, text = str(self.waitTimes[i]))
      newWait.grid(row = 13+i, column = 8)
      self.waitBoxes.append(newWait)

      newDone = Label(self, text = str(self.doneTimes[i]))
      newDone.grid(row = 13+i, column = 7)
      self.doneBoxes.append(newDone)

    self.avgWaitTime = sum(self.waitTimes)/len(self.waitTimes)
    self.avgWaitLbl = Label(self, text = "Average Wait Time\n (minutes): " + str(self.avgWaitTime))
    self.avgWaitLbl.grid(row = 21, column = 8)

    self.avgQLen = sum(self.waitTimes)/max(self.doneTimes)
    self.avgQLbl = Label(self, text = "Average Queue Length:\n" + str(self.avgQLen))
    self.avgQLbl.grid(row = 10, column = 3)

    #Helpful Buttons
    RecalcMovement = Button(self, text='Recalculate Move Times!', command=self.calcMove)
    RecalcMovement.grid(row = 10, column = 2, columnspan = 1)
    RecalcFamilies = Button(self, text='Recalculate Family Sizes!', command=self.calcSize)
    RecalcFamilies.grid(row = 10, column = 4, columnspan = 2)
    RecalcService = Button(self, text='Recalculate Service Times!', command=self.calcService)
    RecalcService.grid(row = 21, column = 6, columnspan = 1)

    Next = Button(self, text='Move to DEATHCOASTER!', command=self.next)
    Next.grid(row = 5, column = 6, columnspan = 2)
  
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

    self.calcSize()
    self.calcService()

  def calcService(self):
    self.calcMove()
    self.calcSize()

    serviceTimes = []
    for i in range(len(self.familySizes)):
      service = 0
      for j in range(self.familySizes[i][0]):
        service += -float(self.params[THETA])*math.log(1-float(self.gamRandomBoxes[4*i + j].get()))
      serviceTimes.append((service, self.familySizes[i][1]))

    self.sortedServiceTimes = []
    for i in range(8):
      for j in range(8):
        if self.queueEnterTimes[i][1] == serviceTimes[j][1]:
          self.sortedServiceTimes.append(serviceTimes[j])
    self.waitTimes = []

    booth1 = []
    booth2 = []
    self.doneTimes = []
    #self.boothDir = []
    time = 0
    #sort these the other way for the loop
    #then sort them back for display
    for i in range(8):
      if len(booth1) == 0:
        booth1.append(float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
        self.doneTimes.append(float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
        self.waitTimes.append(0)

        self.boothDir[i].config(text = "Left")

        #newDir = Label(self, text = "Left")
        #self.boothDir.append(newDir)
        #newDir.grid(row = 2+i, column = 4)
        
      elif len(booth2) == 0:
        booth2.append(float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
        self.doneTimes.append(float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
        self.waitTimes.append(0)

        self.boothDir[i].config(text = "Right")

        #newDir = Label(self, text = "Right")
        #self.boothDir.append(newDir)
        #newDir.grid(row = 2+i, column = 4)

      else:
        if self.queueEnterTimes[i][0] >= booth1[0]:
          self.waitTimes.append(0)
          booth1.pop(0)
          booth1.append(self.waitTimes[-1] + float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
          self.doneTimes.append(self.waitTimes[-1] + float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])

          self.boothDir[i].config(text = "Left")

          #newDir = Label(self, text = "Left")
          #self.boothDir.append(newDir)
          #newDir.grid(row = 2+i, column = 4)

        elif self.queueEnterTimes[i][0] >= booth2[0]:
          self.waitTimes.append(0)
          booth2.pop(0)
          booth2.append(self.waitTimes[-1] + float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])
          self.doneTimes.append(self.waitTimes[-1] + float(self.queueEnterTimes[i][0]) + self.sortedServiceTimes[i][0])

          self.boothDir[i].config(text = "Right")
          #newDir = Label(self, text = "Right")
          #self.boothDir.append(newDir)
          #newDir.grid(row = 2+i, column = 4)

        elif min(booth1[0], booth2[0]) == booth1[0]:
          self.waitTimes.append(booth1[0] - self.queueEnterTimes[i][0])
          booth1.pop(0)
          booth1.append(self.waitTimes[-1] + self.queueEnterTimes[i][0] + self.sortedServiceTimes[i][0])
          self.doneTimes.append(self.waitTimes[-1] + self.queueEnterTimes[i][0] + self.sortedServiceTimes[i][0])

          self.boothDir[i].config(text = "Left")

          #newDir = Label(self, text = "Left")
          #self.boothDir.append(newDir)
          #newDir.grid(row = 2+i, column = 4)

        elif min(booth1[0], booth2[0]) == booth2[0]:
          self.waitTimes.append(booth2[0] - self.queueEnterTimes[i][0])
          booth2.pop(0)
          booth2.append(self.waitTimes[-1] + self.queueEnterTimes[i][0] + self.sortedServiceTimes[i][0])
          self.doneTimes.append(self.waitTimes[-1] + self.queueEnterTimes[i][0] + self.sortedServiceTimes[i][0])

          self.boothDir[i].config(text = "Right")

          #newDir = Label(self, text = "Right")
          #self.boothDir.append(newDir)
          #newDir.grid(row = 2+i, column = 4)
          
    #self.doneBoxes = []
    #self.waitBoxes = []
    #self.serviceBoxes = []
    #Label(self, text = "Booth").grid(row = 1, column = 4)
    #Label(self, text = "Service Times (minutes)").grid(row = 1, column = 5)
    #Label(self, text = "Wait Times (minutes)").grid(row = 1, column = 7)
    #Label(self, text = "Done Times (minutes)").grid(row = 1, column = 6)
    for i in range(8):
      self.serviceBoxes[i].config(text = self.sortedServiceTimes[i][0])
      #newService = Label(self, text = str(self.sortedServiceTimes[i][0]))
      #newService.grid(row = 2+i, column = 5)
      #self.serviceBoxes.append(newService)

      self.waitBoxes[i].config(text = str(self.waitTimes[i]))
      #newWait = Label(self, text = str(self.waitTimes[i]))
      #newWait.grid(row = 2+i, column = 7)
      #self.waitBoxes.append(newWait)

      self.doneBoxes[i].config(text = str(self.doneTimes[i]))
      #newDone = Label(self, text = str(self.doneTimes[i]))
      #newDone.grid(row = 2+i, column = 6)
      #self.doneBoxes.append(newDone)

    self.avgWaitTime = sum(self.waitTimes)/len(self.waitTimes)
    self.avgWaitLbl.config(text = "Average Wait Time\n (minutes): " + str(self.avgWaitTime)) #Label(self, text = "Average Wait Time\n (minutes): " + str(self.avgWaitTime))
    #self.avgWaitLbl.grid(row = 10, column = 7)

    self.avgQLen = sum(self.waitTimes)/max(self.doneTimes)
    self.avgQLbl.config(text = "Average Queue Length:\n" + str(self.avgQLen)) #Label(self, text = "Average Queue Length:\n" + str(self.avgQLen))
    #self.avgQLbl.grid(row = 10, column = 3)
      
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

    self.calcMove()
    self.calcService()

  def next(self):
    doneTimeList = []
    famSizeList = []
    famNumList = []
    for i in range(8):
      doneTimeList.append(float(self.doneBoxes[i]["text"]))
      famSizeList.append(self.familySizes[i][0])
      famNumList.append(self.startTimes[i][1])

      #print("family " + str(self.startTimes[i][1]) + " of size " + str(self.familySizes[i][0]) + " finished at " + self.doneBoxes[i]["text"])
    
    RCroot = Tk()
    RCroot.resizable(width=True, height=True)
    RCroot.geometry('{}x{}'.format(1250, max(25*sum(famSizeList), 300)))
    RollerCoaster(RCroot, doneTimeList, famSizeList, famNumList, self.params).grid()

class RollerCoaster(Frame):
  global seeds
  global params
  global serviceTimes, serviceBoxes
  global doneBoxes, queueBoxes
  global allPeople, totalPeople
  global famSize1, famSize2, lastFamSize
  global numLoads
  global startTimes
  global arrivalTimes, arrivalBoxes
  global famAll, origFamAll, famNums
  global randomTravels, randomLoads
  global travelTimes, travelBoxes
  global loadTimes, loadBoxes
  global waitTimes, waitBoxes
  global doneTimes, doneBoxes
  global avgWaitTime, waitLbl
  global avgQLen, qLenLbl
  global famNumLbls
  global recalcArriveBtn, recalcServeBtn
  global randomCall
  

  def __init__(self, root, d, f, n, p):
      Frame.__init__(self, root)

      #lots of initialization
      self.params = p[:]
      self.famAll = []
      self.startTimes = []
      self.famSize1 = []
      self.famSize2 = []
      self.randomTravels = []
      self.randomLoads = []
      self.famNums = []
      self.serviceTimes = []
      self.serviceBoxes = []
      self.travelTimes = []
      self.travelBoxes = []
      self.arrivalTimes = []
      self.arrivalBoxes = []
      self.loadTimes = []
      self.loadBoxes = []
      self.waitTimes = []
      self.waitBoxes = []
      self.doneTimes = []
      self.doneBoxes = []
      self.famNumLbls = []
      randListTravel = [random.random() for i in range(8)]
      self.randomCall = randListTravel[:]
      self.travelTimes = [-(1/float(self.params[EXPTHETA]))*math.log(1-float(y)) for y in randListTravel]
      self.allPeople = sum(f)
      self.totalPeople = sum(f)
      numIndividList = []
      mylist = ["First", "Second", "Third", "Fourth"] #["1st", "2nd", "3rd", "4th"]

      #calculate the queue arrival times
      for i in range(8):
          self.arrivalTimes.append(d[i] + self.travelTimes[i])

      #sort the information by the arrival time
      for i in range(8):
          self.famAll.append((self.arrivalTimes[i], n[i], f[i], d[i]))
      self.famAll.sort()
      self.origFamAll = self.famAll[:]

      self.arrivalTimes = []
      for i in range(8):
          self.arrivalTimes.append(self.famAll[i][0])

      #get 2 copies of the family size list, record the family number in the same index
      #record each individual's start time (they left with their family so it will be the
      #same as their fellow family members)
      for i in range(len(self.famAll)):
          self.famSize1.append(self.famAll[i][2])
          self.famSize2.append(self.famAll[i][2])
          self.famNums.append(self.famAll[i][1])
          for j in range(self.famSize1[i]):
              self.startTimes.append(self.famAll[i][3])
      
      #get a copy of the last family's size
      self.lastFamSize = self.famSize1[-1]

      #remember how many times the coaster will need to run to serve each person
      if self.allPeople % 4 == 0:
          self.numLoads = self.allPeople/4
      else:
          self.numLoads = self.allPeople/4 + 1

      #remember each individual and their place in their family
      for i in range(len(self.famSize1)):
          for j in range(self.famSize1[i]):
              numIndividList.append((self.famNums[i], mylist[j]))
      

      #MYLES, this is where you start putting the controls on the form

      #top row labels
      Label(self, text = "Family #, person").grid(row = 1, column = 1)
      Label(self, text = "Random Seeds").grid(row = 1, column = 2)
      Label(self, text = "Movement Times (min)").grid(row = 1, column = 3)
      Label(self, text = "Enter Queue Time (min)").grid(row = 1, column = 4)
      Label(self, text = "Random Seeds").grid(row = 1, column = 5)
      Label(self, text = "Service Times (min)").grid(row = 1, column = 6)
      Label(self, text = "Done Times (min)").grid(row = 1, column = 7)
      Label(self, text = "Wait Times (min)").grid(row = 1, column = 8)

      #bottom row buttons
      self.recalArriveBtn = Button(self, text = "Recalculate Arrival times!", command = lambda: self.calcMove(True))
      self.recalServeBtn = Button(self, text = "Recalculate Service times!", command = lambda: self.calcService(True))

      self.recalArriveBtn.grid(row = 2 + self.allPeople, column = 2)
      self.recalServeBtn.grid(row = 2 + self.allPeople, column = 5)
      

      #label each individual's family number and where they are in the family
      for i in range(self.allPeople):
          newLbl = Label(self, text = "Family " + str(numIndividList[i][0]) + ", " + numIndividList[i][1], anchor = "w")
          newLbl.grid(row = 2 + i, column = 1, sticky = "w")
          self.famNumLbls.append(newLbl)

      noModRide = self.allPeople

      #set up random number entry boxes for movement and being loaded onto the coaster
      create = True
      for i in range(8):
          newEntry = Entry(self, width = 15)
          newEntry.grid(row = 2 + sum(self.famSize1[:i]), column = 2, rowspan = self.famSize1[i], sticky = "news")
          newEntry.insert(0, str(randListTravel[i]))
          self.randomTravels.append(newEntry)

          if noModRide > 0:
            newEntry = Entry(self, width = 15)
            if create == True and noModRide != 0:
                if noModRide >= 4:
                    newEntry.grid(row = 2 + i * 4, column = 5, rowspan = 4, sticky = "news")
                else:
                  if noModRide != 0:
                    if noModRide < 1:
                      #noModRide += 4
                      create = False
                    newEntry.grid(row = 2 + i * 4, column = 5, rowspan = noModRide, sticky = "news")
                    
                noModRide -= 4
                newEntry.insert(0, random.random())
                self.randomLoads.append(newEntry)
          


      self.calcMove(False)

  def calcMove(self, buttonPush):
      if buttonPush == False:
          self.arrivalBoxes = []
          for i in range(8):
              for j in range(self.famSize1[i]):
                  newLbl = Label(self, text = str(self.travelTimes[i]))
                  newLbl.grid(row = 2 + sum(self.famSize1[:i]) + j, column = 3)
                  self.travelBoxes.append(newLbl)

                  newLbl = Label(self, text = str(self.arrivalTimes[i]))
                  newLbl.grid(row = 2 + sum(self.famSize1[:i]) + j, column = 4)
                  self.arrivalBoxes.append(newLbl)
          self.calcService(False)

      else:
          mylist = ["First", "Second", "Third", "Fourth"] #["1st", "2nd", "3rd", "4th"]
          randListTravel = [float(y.get()) for y in self.randomTravels]
##          go = False
##          for i in range(len(self.randomCall)):
##            if self.randomCall[i] != randListTravel[i] and abs(self.randomCall[i] - randListTravel[i]) > 0.00000000001:
##              go = True
##          if go == True:
          self.travelTimes = [-(1/float(self.params[EXPTHETA]))*math.log(1-float(y)) for y in randListTravel]
          self.arrivalTimes = []

          # for i in range(8):
          #     print(self.origFamAll[i][1])
          #     print(self.travelTimes[i])
          #     print(self.origFamAll[i][3])
          #     print(self.travelTimes[i] + self.origFamAll[i][3])

          for i in range(8):
            self.arrivalTimes.append(self.origFamAll[i][3] + self.travelTimes[i])

##          famAll = []
##          for i in range(8): #sort by arrival times the arrival times, family booth leave times, family numbers, family sizes, random number for travel, and travel time
##              famAll.append((self.arrivalTimes[i], self.origFamAll[i][1], self.origFamAll[i][2], self.origFamAll[i][3]))#, self.travelTimes[i]))
##          self.famAll = famAll[:]
##          self.famAll.sort()
##
##          self.arrivalTimes = []
##          self.travelTimes = [-(1/float(self.params[THETA]))*math.log(1-float(y)) for y in randListTravel]
##          for i in range(8):
##              self.arrivalTimes.append(self.famAll[i][0])
##              self.travelTimes.append(self.famAll[i][4])
##
##          self.famSize1 = []
##          self.famSize2 = []
##          self.famNums = []
##          self.startTimes = []
##          randTravel = []
##          for i in range(len(self.famAll)):
##              #print(self.famAll[i][3])
##              self.famSize1.append(self.famAll[i][2])
##              self.famSize2.append(self.famAll[i][2])
##              self.famNums.append(self.famAll[i][1])
##              for j in range(self.famSize1[i]):
##                  self.startTimes.append(self.famAll[i][3])
          
##          #get a copy of the last family's size
##          self.lastFamSize = self.famSize1[-1]
##
##          #remember how many times the coaster will need to run to serve each person
##          if self.allPeople % 4 == 0:
##              self.numLoads = self.allPeople/4
##          else:
##              self.numLoads = self.allPeople/4 + 1

##          numIndividList = []
##          #remember each individual and their place in their family
##          for i in range(len(self.famSize1)):
##              for j in range(self.famSize1[i]):
##                  numIndividList.append((self.famNums[i], mylist[j]))
##          
##          for i in range(self.allPeople):
##              self.famNumLbls[i].config(text = "Family " +  str(numIndividList[i][0]) + ", " + numIndividList[i][1])

          #set up random number entry boxes for movement and being loaded onto the coaster
##          for i in range(8):
##              #self.randomTravels[i].delete(0, 'end')
##              #self.randomTravels[i].insert(0, str(randListTravel[i]))
##              self.randomTravels[i].grid(row = 2 + sum(self.famSize1[:i]), column = 2, rowspan = self.famSize1[i], sticky = "news")
          

          for i in range(8):
              for j in range(self.famSize1[i]):
                  self.travelBoxes[sum(self.famSize1[:i]) + j].config(text = str(self.travelTimes[i]))
                  self.arrivalBoxes[sum(self.famSize1[:i]) + j].config(text = str(self.arrivalTimes[i]))
          self.calcService(True)

  def calcService(self, buttonPush):
      if buttonPush == False:
          self.loadTimes = [(26*float(y.get())+1)**(float(1)/3) for y in self.randomLoads]
          noModRide = self.allPeople
          self.loadBoxes = []
          for i in range(self.numLoads):
            newLbl = 0
            if noModRide >= 4:
              for j in range(4):
                newLbl = Label(self, text = str(self.loadTimes[i] + 2))
                newLbl.grid(row = 2 + i * 4 + j, column = 6)
                self.loadBoxes.append(newLbl)
            else:
              if noModRide < 1:
                noModRide += 4
              for j in range(noModRide):
                newLbl = Label(self, text = str(self.loadTimes[i] + 2))
                newLbl.grid(row = 2 + i * 4 + j, column = 6)
                self.loadBoxes.append(newLbl)
            noModRide -= 4
          self.calcDone(False)
      else:
        self.loadTimes = [(26*float(y.get())+1)**(float(1)/3) for y in self.randomLoads]
        noModRide = self.allPeople
        for i in range(self.numLoads):
          newLbl = 0
          if noModRide >= 4:
            for j in range(4):
              self.loadBoxes[i * 4 + j].config(text = str(self.loadTimes[i] + 2))
          else:
            if noModRide < 1:
              noModRide += 4
              for j in range(noModRide):
                self.loadBoxes[i * 4 + j].config(text = str(self.loadTimes[i] + 2))
          noModRide -= 4
        self.calcDone(True)
          
  def calcDone(self, buttonPush):
      #create local copies of everything to avoid those globals from being changed
      famSize3 = self.famSize1[:]
      allPeople = self.allPeople
      lastFamSize = self.lastFamSize
      arrivalTimes = [float(x["text"]) for x in self.arrivalBoxes]
      famSize1 = [1]*allPeople
      famSize2 = [1]*allPeople
      totalPeople = self.totalPeople
      waitTime = [0]*allPeople
      serviceTime = [float(x["text"]) for x in self.loadBoxes]
      late = 0
      i = 0
      while i < len(serviceTime):
          if late == serviceTime[i]:
              serviceTime.remove(late)
              i-=1
          else:
              late = serviceTime[i]
          i+=1
      time = arrivalTimes[0]
      numQ = 1
      famSize1[0] = 0
      doneTime = [0]*allPeople
      index = 1
      rideAndLoadTime = 0
      endIndex = 1
      serviceIndex = 0

      
      if buttonPush == False:
        for i in range(4):
          doneTime[i] = arrivalTimes[3] + serviceTime[serviceIndex]

        serviceIndex += 1

        if allPeople % 4 == 0:
          for i in range(7, allPeople, 4):
            doneTime[i] = max((max(doneTime) + serviceTime[serviceIndex]), arrivalTimes[i] + serviceTime[serviceIndex])
            doneTime[i-1] = doneTime[i]
            doneTime[i-2] = doneTime[i]
            doneTime[i-3] = doneTime[i]

            serviceIndex += 1
        if allPeople % 4 != 0:
          try:
            for i in range(7, allPeople, 4):
              doneTime[i] = max((max(doneTime) + serviceTime[serviceIndex]), arrivalTimes[i] + serviceTime[serviceIndex])
              doneTime[i-1] = doneTime[i]
              doneTime[i-2] = doneTime[i]
              doneTime[i-3] = doneTime[i]

              serviceIndex += 1
          except IndexError:
            pass
          index = self.Zero(doneTime)
          time = max((max(doneTime) + serviceTime[serviceIndex]), arrivalTimes[-1] + serviceTime[serviceIndex])
          for i in range(index, allPeople):
            doneTime[i] = time


        for i in range(allPeople):
          waitTime[i] = doneTime[i] - float(self.loadBoxes[i]["text"]) - arrivalTimes[i]
        self.doneTimes = doneTime[:]
        self.waitTimes = waitTime[:]
        self.doneBoxes = []
        self.waitBoxes = []

        for i in range(self.allPeople):
            newLbl = Label(self, text = str(doneTime[i]))
            newLbl.grid(row = 2 + i, column = 7)
            self.doneBoxes.append(newLbl)

            newLbl = Label(self, text = str(waitTime[i]))
            newLbl.grid(row = 2 + i, column = 8)
            self.waitBoxes.append(newLbl)

        self.avgWaitTime = sum(waitTime)/self.allPeople
        self.avgQLen = sum(waitTime)/ max(doneTime)

        self.waitLbl = Label(self, text = "Average Wait Time (min):\n" + str(self.avgWaitTime))
        self.qLenLbl = Label(self, text = "Average Queue Length:\n" + str(self.avgQLen))

        self.waitLbl.grid(row = 2 + self.allPeople, column = 8)
        self.qLenLbl.grid(row = 2 + self.allPeople, column = 7)
      else:
        ppleList = []
        for i in range(allPeople):
          ppleList.append((arrivalTimes[i], i))
        ppleList.sort()
        arrivalTimes2 = []
        for i in range(allPeople):
          arrivalTimes2.append(ppleList[i][0])
        serve = []


        for i in range(4):
          doneTime[i] = arrivalTimes2[3] + serviceTime[serviceIndex]
          serve.append(serviceTime[serviceIndex])

        serviceIndex += 1

        if allPeople % 4 == 0:
          for i in range(7, allPeople, 4):
            doneTime[i] = max((max(doneTime) + serviceTime[serviceIndex]), arrivalTimes2[i] + serviceTime[serviceIndex])
            doneTime[i-1] = doneTime[i]
            doneTime[i-2] = doneTime[i]
            doneTime[i-3] = doneTime[i]
            serve.append(serviceTime[serviceIndex])
            serve.append(serviceTime[serviceIndex])
            serve.append(serviceTime[serviceIndex])
            serve.append(serviceTime[serviceIndex])

            serviceIndex += 1
        if allPeople % 4 != 0:
          try:
            for i in range(7, allPeople, 4):
              doneTime[i] = max((max(doneTime) + serviceTime[serviceIndex]), arrivalTimes2[i] + serviceTime[serviceIndex])
              doneTime[i-1] = doneTime[i]
              doneTime[i-2] = doneTime[i]
              doneTime[i-3] = doneTime[i]
              serve.append(serviceTime[serviceIndex])
              serve.append(serviceTime[serviceIndex])
              serve.append(serviceTime[serviceIndex])
              serve.append(serviceTime[serviceIndex])

              serviceIndex += 1
          except IndexError:
            pass
          index = self.Zero(doneTime)
          
          time = max((max(doneTime) + serviceTime[serviceIndex]), arrivalTimes2[-1] + serviceTime[serviceIndex])
          for i in range(index, allPeople):
            doneTime[i] = time
            serve.append(serviceTime[serviceIndex])
        ppleList2 = []
        for i in range(allPeople):
          ppleList2.append((ppleList[i][1], doneTime[i], serve[i]))
        ppleList2.sort()
        doneTime2 = []
        serve2 = []
        for i in range(allPeople):
          doneTime2.append(ppleList2[i][1])
          serve2.append(ppleList2[i][2])
        for i in range(allPeople):
          waitTime[i] = doneTime2[i] - serve2[i] - arrivalTimes[i]
##        famNum = []
##        famSizes = []
##        individList = []
##        for i in range(8):
##          famNum.append(self.origFamAll[i][1])
##          famSizes.append(self.origFamAll[i][2])
##        for i in range(8):
##          for j in range(famSizes[i]):
##            individList.append(arrivalTimes[sum(famSizes[:i]+j)], famNum[i]
        self.avgWaitTime = sum(waitTime)/self.allPeople
        self.avgQLen = sum(waitTime)/ max(doneTime2)
        for i in range(self.allPeople):
            self.doneBoxes[i].config(text = str(doneTime2[i]))
            self.waitBoxes[i].config(text = str(waitTime[i]))
            self.loadBoxes[i].config(text = str(serve2[i]))
        self.waitLbl.config(text = "Average Wait Time (min):\n" + str(self.avgWaitTime))
        self.qLenLbl.config(text = "Average Queue Length:\n" + str(self.avgQLen))

  def nonZero(self, mylist):
      for i in range(len(mylist)):
          if mylist[i] > 0:
              return i
      return 100
  def Zero(self, mylist):
    for i in range(len(mylist)):
      if mylist[i] == 0:
        return i
    return -1

  def first4(self, mylist):
      index = 0
      j = 4
      list2 = mylist[:]
      while(j > 0):
          try:
              if list2[index] < j:
                  j -= list2[index]
                  index += 1
              elif list2[index] >= j:
                  j -= list2[index]
          except IndexError:
              return index
      return index

if __name__=='__main__':
  root = Tk()
  root.resizable(width=True, height=True)
  root.geometry('{}x{}'.format(700, 250))
  AmusementPark(root).grid()
  root.mainloop()
