import random
import math
def main():
    ylist = [random.random() for i in range(8)]                              #8 random numbers each between 0 and 1
    x = [-(1/3)*math.log(1-y) for y in ylist]                                #Exponential distribution on how long it takes to get to the coaster
    arrivalTimes = []
    famSize1 = [2, 3, 3, 1, 4, 2, 3, 4]                                            #test family sizes; this copy will be for the families we are waiting to arrive at the line for the coaster
    famSize3 = famSize1[:]
    allPeople = sum(famSize1)
    lastFamSize = famSize1[-1]


    for i in range(len(famSize1)):                                          #this code loads arrival times assuming that there was one ticket booth, so this will need to be changed because we work with 2 ticket booths
        for t in range(famSize1[i]):
            arrivalTimes.append(sum(x[:i+1]))                                #sum arrival times to include the one we are one to append the total time since the first family arrived

    famSize1 = [1]*allPeople
    famSize2 = [1]*allPeople                                                   #this is for removing 4 people at a time from the line
    #print(len(famSize1))
    totalPeople = allPeople

    waitTime = [0] * allPeople                                                       #give them each their own wait times
    serviceTime = [0] * allPeople                                                    #give them each their own service times
    time = arrivalTimes[0]                                                   #start time going at arrival of first family
    numQ = famSize1[0]                                                       #remember the number of people in the line
    famSize1[0] = 0                                                          #have the copy of families we are waiting to arrive fam
    doneTime = []                                                            #have a list to record done times
    index = 0                                                                #start of index in list families that will/are being served 
    loadTime = 0                                                             #how long it takes to load and begin the next ride
    endIndex = 1                                                             #end index in list of families that will/are being served


    while(totalPeople > 0):
        if(numQ <= 4 and len(famSize2) <= lastFamSize  and totalPeople <= 4):            #if we are on the last family
           #print(len(doneTime))
           totalPeople = 0                                                    #load them up and finish
           #print(numQ)
           #print(len(doneTime))
           numQ = 0
           y = random.random()
           loadTime = (26*y+1)**(1/3)
           for i in range(index, endIndex):
               serviceTime[i] += 2 + loadTime
               doneTime.append(time + 2 + loadTime)
        
        else:
            if(numQ < 4 and len(famSize2) > 0):                               #if there is not enough people to ride the coaster
                time += arrivalTimes[endIndex] - arrivalTimes[endIndex-1]     #wait for the next family
                for i in range(index, endIndex):
                    waitTime[i] += arrivalTimes[endIndex]-arrivalTimes[endIndex-1]
                endIndex += 1
                numQ += 1                           #add them to the line
                famSize1[nonZero(famSize1)] = 0                               #set the first family number equal to 0
                
            elif(numQ >= 4 or len(famSize2) == 0):
                y = random.random()
                loadTime = (26*y+1)**(1/3)                                    #calculate time it takes to unload and load ride and start it
                for i in range(len(arrivalTimes)):                            #add every family that enters line load and ride time
                    #print(str(i) + " " + str(time <= arrivalTimes[i] and arrivalTimes[i] <= time + 2 + loadTime and famSize1[i] > 0))
                    #print(i, time, arrivalTimes[i], time+2+loadTime)
                    if(time <= arrivalTimes[i] and arrivalTimes[i] <= time + 2 + loadTime and famSize1[i] > 0):
                        #print(str(i) + " just arrived")
                        numQ+=1
                        #print(str(i) + " just arrived")
                        #print(numQ)
                        waitTime[i] += (time + 2 + loadTime) - arrivalTimes[i]
                        famSize1[i] = 0
                    elif i >= endIndex and famSize1[i] == 0:
                        waitTime[i] += 2 + loadTime
                #print(numQ)   
                time += 2 + loadTime                                          #add load and ride time to the total time
                
                for i in range(index, endIndex):
                    serviceTime[i] += 2 + loadTime
                #print(2+loadTime)
                #print(serviceTime)
                #print(numQ)
                numQ -= 4                                                     #subtract 4 people from the line
                totalPeople -= 4                                              #subtract 4 people from the total people we know need to ride
                sub = 4
                #print("here")
                while(sub > 0 and len(famSize2) > 0):
                    if(famSize2[0] <= sub):                                   #if the remaining family can fit on the coaster with room to spare or fill it up
                        sub -= 1                                    #load them onto the coaster
                        famSize2.pop(0)                                       #remove them from our line copy
                        doneTime.append(time)                                 #record their time it took them to ride the coaster
                 #       print(doneTime)
                 #       print(len(doneTime))
                    else:                                                     #if the remaining family can't all get on together
                        famSize2[0] = famSize2[0] - sub                       #put on those that can fit on the coaster
                        sub = 0
                index = allPeople - len(famSize2)                                     #get index of next family that will be served
                endIndex =index + first4(famSize2)+1                          #begin from start index and find how many families will be served in next ride
                #print(len(famSize2))
                #print(famSize2)
                #print(numQ)
                #print(numQ)
                if(endIndex > allPeople):
                    endIndex = allPeople
    for i in range(allPeople):
        #print(len(doneTime))
        #print(len(arrivalTimes))
        #print(len(serviceTime))
        #print(len(waitTime))
        if(doneTime[i] != arrivalTimes[i] + serviceTime[i] + waitTime[i]):
            print(doneTime[i] - (arrivalTimes[i] + serviceTime[i] + waitTime[i]))
    outfile = open("notes.txt", "w")
    print("family sizes", file = outfile)
    print(famSize3, file = outfile)
    print("ylist", file = outfile)
    print(ylist,file = outfile )
    print("x", file = outfile)
    print(x,file = outfile)
    print("arrival list", file = outfile)
    print(arrivalTimes,file = outfile)
    print("service times", file = outfile)
    print(serviceTime,file = outfile)
    print("done times", file = outfile)
    print(doneTime,file = outfile)
    print("wait times", file = outfile)
    print(waitTime,file = outfile)
    outfile.close()


def nonZero(mylist):
    for i in range(len(mylist)):
        if mylist[i] > 0:
            return i
    return 100

def first4(mylist):
    index = 0
    j = 4
    list2 = mylist[:]
    while(j > 0):
        try:
            if list2[index] < j:
                j-=list2[index]
                index+=1
            elif list2[index] >= j:
                j-=list2[index]
        except IndexError:
            return index
    return index
