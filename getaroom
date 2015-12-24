#!/usr/bin/env python

""" 
Co-Author = Hades.y2k
github profile = https://github.com/Hadesy2k
"""

import re
import urllib
import time

def getaroom():
    print("[+] Searching A Free Room, just for you :P")
    page = getpage()
    data = parse(page)
    
    freeRooms = []
    freeRooms = [{"A2-04":"19:00 - 20:00"}, {"B3-02":"18:00 - 20:00"}]
    for i in data:
        if freeroom(i["Time"]):
            room = {i["Room"]:i["Time"]}
            freeRooms.append(room)
            
    if freeRooms:
        print("\n[+] %s Free Rooms found! :)" % len(freeRooms))
        for i in freeRooms:
            startingtime = i[i.keys()[0]]
            hour = startingtime[:startingtime.index(':')]
            minute = startingtime[:5][3:]
            classtime = convTime(hour+":"+minute)
            
            print("[=] Room : %s, Class start at : %s" % (i.keys(),classtime))
    else:
        print("[!] No Free Room for you :(")
            

def freeroom(data):
    ''' example input : 15:30 '''
    ''' example output : True || False '''
    
    hour = int(time.strftime("%H"))
    minute = int(time.strftime("%M"))
    if minute >= 30:
        hour += 1
    
    diff = int(data[:2]) - hour
    if diff > 0.5:
        return True
    else:
        return False


def getpage():
    try:
        return urllib.urlopen("http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInformation.aspx").readlines()
    except:
        print("[!] General Error, no internet connection?")
        exit()


def parse(data):
    page = urllib.urlopen("http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInformation.aspx").readlines()
    pat = re.compile(r'<td class="BTsubj">(.+)</td><td class="BTclass">(.+)</td><td class="BTtime">(.+)</td><td class="BTroom">(.+)</td></tr>')
    info = []
    print("[+] Processing webpage")
    for line in page:
        if len(pat.findall(line)) != 0:
            tempdata = pat.findall(line)[0]
            #duration = self.convTime(tempdata[2][:5])+"~"+self.convTime(tempdata[2][8:])
            duration = tempdata[2]
            tempdict = {"Course": tempdata[0],
                        "Type"  : tempdata[1],
                        "Time"  : duration,
                        "Room"  : tempdata[3]}
            info.append(tempdict)
    return info

def convTime(data):
    period = "AM"
    
    hour = int(data[:data.index(':')])
    minutes = data[data.index(':')+1:]
    if hour > 12:
        hour -= 12
        period = "PM"
    return str(hour)+':'+str(minutes)+" "+ period


if __name__ == '__main__':
    try:
        getaroom()
    except KeyboardInterrupt:
        print("\n[+] Ctrl + C detected!")
