import random
import math
def main():
    ylist = [random.random() for i in range(8)]                              #8 random numbers each between 0 and 1
    x = [-(1/3)*math.log(1-y) for y in ylist]                                #Exponential distribution on how long it takes to get to the coaster
    arrivalTimes = []
    famSize1 = [2, 3, 3, 1, 4, 2, 3, 4]                                      #test family sizes; this copy will be for the families we are waiting to arrive at the line for the coaster
    famSize3 = famSize1[:]                                                   #this copy is for printing purposes only
    allPeople = sum(famSize1)                                                #remember the total number of people coaster is expecting
    lastFamSize = famSize1[-1]                                               #remember how many people are in the last family coaster is expecting


    for i in range(len(famSize1)):                                           #this code loads arrival times assuming that there was one ticket booth, so this will need to be changed because we work with 2 ticket booths
        for t in range(famSize1[i]):
            arrivalTimes.append(sum(x[:i+1]))                                #add the arrival times for each family member from each family

    famSize1 = [1]*allPeople                                                 #this is for the number of people we are expecting to come to the coaster that have not arrived yet
    famSize2 = [1]*allPeople                                                 #this is for removing 4 people at a time from the line
    totalPeople = allPeople                                                  #get copy of total number of people for remembering how many people have rode the coaster

    waitTime = [0] * allPeople                                               #give each person their own wait times
    serviceTime = [0] * allPeople                                            #give each person their own service times
    time = arrivalTimes[0]                                                   #start time going at arrival of first family
    numQ = 1                                                                 #start with at least one person in the line
    famSize1[0] = 0                                                          #mark the first individual as having arrived
    doneTime = []                                                            #have a list to record done times of each individual
    index = 0                                                                #start of index in list of individuals that will/are being served 
    loadTime = 0                                                             #how long it takes to load and begin the next ride
    endIndex = 1                                                             #end index in list of individuals that will/are being served


    while(totalPeople > 0):
        if(numQ <= 4 and len(famSize2) <= lastFamSize  and totalPeople <= 4): #if we are on the last family
           totalPeople = 0                                                    #load them up and finish
           numQ = 0
           y = random.random()
           loadTime = (26*y+1)**(1/3)                                         #calculate time to load on individuals
           for i in range(index, endIndex):
               serviceTime[i] += 2 + loadTime                                 #add the service time for the last individuals
               doneTime.append(time + 2 + loadTime)                           #add the final done times
        
        else:
            if(numQ < 4 and len(famSize2) > 0):                               #if there is not enough people to ride the coaster
                time += arrivalTimes[endIndex] - arrivalTimes[endIndex-1]     #wait for the next individual
                for i in range(index, endIndex):
                    waitTime[i] += arrivalTimes[endIndex]-arrivalTimes[endIndex-1]
                endIndex += 1
                numQ += 1                                                     #add them to the line
                famSize1[nonZero(famSize1)] = 0                               #mark that individual as having arrived
                
            elif(numQ >= 4 or len(famSize2) == 0):
                y = random.random()
                loadTime = (26*y+1)**(1/3)                                    #calculate time it takes to unload and load ride and start it
                for i in range(len(arrivalTimes)):                            #add every individual that enters line during the ride
                    if(time <= arrivalTimes[i] and arrivalTimes[i] <= time + 2 + loadTime and famSize1[i] > 0):
                        numQ+=1
                        waitTime[i] += (time + 2 + loadTime) - arrivalTimes[i] #calculate their respective wait times while the coaster is going
                        famSize1[i] = 0                                        #mark each individual that arrives as having arrived
                    elif i >= endIndex and famSize1[i] == 0:                  #if the person has arrived and their not riding the coaster
                        waitTime[i] += 2 + loadTime                           #add the time to load the coaster and ride it as wait time for that person
                time += 2 + loadTime                                          #add load and ride time to the total time
                
                for i in range(index, endIndex):                              #for each person that is being served
                    serviceTime[i] += 2 + loadTime                            #add the time to load and ride the coaster to their service times
                numQ -= 4                                                     #subtract 4 people from the line
                totalPeople -= 4                                              #subtract 4 people from the total people we know need to ride
                sub = 4
                while(sub > 0 and len(famSize2) > 0):
                    if(famSize2[0] <= sub): 
                        sub -= 1                                              #load them onto the coaster
                        famSize2.pop(0)                                       #remove them from our line copy
                        doneTime.append(time)                                 #record their time it took them to ride the coaster
                index = allPeople - len(famSize2)                             #get index of next individual that will be served
                endIndex =index + first4(famSize2)+1                          #begin from start index and find how many families will be served in next ride
                if(endIndex > allPeople):                                     #cap endIndex at the total number of people in the park
                    endIndex = allPeople


    #the rest of this (besides the helper functions) is just for checking the math that's been done
    for i in range(allPeople):
        if(doneTime[i] != arrivalTimes[i] + serviceTime[i] + waitTime[i]):
            print(doneTime[i] - (arrivalTimes[i] + serviceTime[i] + waitTime[i])) #done time should equal how long it took an individual to arrive, wait for the coaster, and load and ride the coaster
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
