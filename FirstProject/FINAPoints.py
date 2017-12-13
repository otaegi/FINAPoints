'''
FINA Swimming point system. To compare times across different events and genders
Author: motaegi
Recommended enhancements: include yard events, include short course events
Exception handling needs to be improved, corner case error when entering incorrect inputs
USAGE:
Follow prompts to choose female/male events
Length of event in meters
Stroke
And enter the individual time.
You can enter multiple times in sequence for the same event.
Use "gender" to change genders
Use "change" to change the event within the same gender. i.e: from 50 free to 200 breaststroke
Use "end" to end the script.
Limitations: yards and short course not supported. Collaboration welcomed to add those features.
'''
import sys

def getGenderFile():
    wrDict={} # Dictionary containing World Records
    gender = input("Enter event gender. i.e: m/f:")
    
    try:
        if(gender == "f"):
            file = open("WorldRecordsFemale.txt", "r") 
        elif(gender =="m"):
            file = open("WorldRecordsMale.txt", "r") 
        else: 
            print("Invalid gender input")
            getGenderFile()
    except:
        print("WR source file contains invalid characters")
        sys.exit()    
    
    try:
        for line in file:
            listedline = line.split() 
            if len(listedline) < 5: 
                wrDict[listedline[0] + listedline[1] + " " + listedline[2]] =  listedline[3]
            else: # for IM event
                if (listedline[3] == "relay"): # differentiate freestyle from IM relay
                    wrDict[listedline[0]  +  listedline[1] + " " + listedline[2]] =  listedline[4]
                else:
                    wrDict[listedline[0]  +  listedline[1] + " " + listedline[3]] =  listedline[4]
    except:
        print("WR source file contains invalid characters")
        sys.exit()   
    finally:
        file.seek(0)
    return wrDict
    
    #convert ",",";" and ":" to "." if input is entered in m:s.ms or m:s:ms format
def cleanInput(i):
    i = i.replace(":", ".").replace(",", ".").replace(";", ".").replace("/", ".")
    return i


def convertTime(t): # transform the time into ss.msms format
    timeList=[]
    for i in t.split('.'):
        try:
            timeList.append(int(i))
        except:
            print("Time Input Incorrect format")
            sys.exit()    
    if(len(timeList)==2): # if minutes are not provided
        timeList.insert(0, 0)       
    if(len(timeList)!=3):
        print("Time Input Incorrect format")
        requestTime()
    t = timeList[0]*60 + timeList[1] + timeList[2]/100
    return(t)

def requestEventInput():
    distance = input('Enter event distance in meters. i.e: 50/100/200/400/800/1500: ')
    stroke = input('Enter stroke. i.e:fr/br/ba/bu/im/re/mre:')   
    return distance, stroke

def requestTime(key, worldRecord):  
    individualTimeinMinutes = input('Enter event time in m.s.ms format: ')
    if(individualTimeinMinutes == "change"): # to reset event
        return "change"
    if(individualTimeinMinutes == "gender"): # to reset gender
        return "gender"
    elif(individualTimeinMinutes == "end"):
        return False  
    else:
        individualTime =  convertTime(cleanInput(individualTimeinMinutes))
        print("FINA points for " + key + ": " + calculateFina(individualTime,worldRecord))
        return True

def composeKey(distance,stroke):
    key = distance + "m "
    if(stroke =="fr"):
        key += "freestyle"
    elif(stroke =="br"):
        key += "breaststroke"
    elif(stroke =="ba"): 
        key += "backstroke"
    elif(stroke =="bu"):
        key += "butterfly"
    elif(stroke =="im"):
        key += "medley"
    elif(stroke =="re"):
        key = "4x" + key + "freestyle"
    elif(stroke == "mre"):
        key = "4x" + key + "medley"
    else:
        print("Stroke Input Incorrect format")
        setEvent()     
    print(key)
    return str(key)

def extractWR(key):
    try:
        worldRecordinMinutes = wrDict[key]
    except:
        print("Incorrect combination of length and stroke entered")
        setEvent()
    return convertTime(cleanInput(worldRecordinMinutes))

def calculateFina(individualTime,worldRecord):           
    #Apply FINA formula
    points= 1000*(worldRecord/individualTime)**3
    #truncate float into integer
    return str(int(points))

def setEvent():
    distance, stroke = requestEventInput()
    key = composeKey(distance,stroke)
    return key

wrDict= getGenderFile()
key = setEvent()
worldRecord = extractWR(key)

qt = True
while(qt): #run continuous, "change" to set new event, "end" to exit.
    if(qt == "change" or qt == "gender"):
        if (qt == "gender"):
            wrDict = getGenderFile()
        key = setEvent()
        worldRecord = extractWR(key)
    qt = requestTime(key, worldRecord)


    
    
    
