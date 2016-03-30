#!/usr/bin/env python

import re
import urllib
import sys
import datetime
import os


banner1 = """
   $$$$$\  $$$$$$\  $$\   $$\
   \__$$ |$$  __$$\ $$ |  $$ |
      $$ |$$ /  \__|$$ |  $$ |
      $$ |$$ |      $$ |  $$ |
$$\   $$ |$$ |      $$ |  $$ |
$$ |  $$ |$$ |  $$\ $$ |  $$ |
\$$$$$$  |\$$$$$$  |\$$$$$$  |
 \______/  \______/  \______/
 """

banner2 = """
    .S    sSSs   .S       S.
   .SS   d%%SP  .SS       SS.
   S%S  d%S'    S%S       S%S
   S%S  S%S     S%S       S%S
   S&S  S&S     S&S       S&S
   S&S  S&S     S&S       S&S
   d*S  S*b     S*b       d*S
  .S*S  S*S.    S*S.     .S*S
sdSSS    SSSbs   SSSbsssdSSS
YSSY      YSSP    YSSP~YSSY
"""

# Website used to generate banner => http://patorjk.com/software/taag/
# Banner1 font = Big Money-nw
# Banner2 font = AMC AAA01

display_banner = True
# Replace "True" with "False" if you want to disable banner

class course():

    def __init__(self, data=None):
        if display_banner:
            print banner2
            # Options, banner1 or banner2, whichever banner you like

        # Checks if the input argument is room number or course code
        course_pattern = re.compile("(\w\w[\-]?\d\d\d\d)")
        room_pattern = re.compile("(\w\d[\-?]\d\d)")

        # if course code, search for course information
        # else if room number, search for room information
        if course_pattern.match(str(data)):
            self.checkSubject(data)
        elif room_pattern.match(str(data)):
            self.checkroom(data)

        else:
            ckey = self.getcoursekey()
            # getcoursekey returns list, and save it as ckey
            print("[~] Getting webpage")
            self.page = self.getpage()
            # Get the webpage
            data = self.parse(self.page)
            numClass = 0
            for subject in ckey:
                for code in data:
                    if subject in code["Course"]:
                        print("\n")
                        numClass += 1
                        for classes in code.keys():
                            print("{} : {}".format(classes,code[classes]))
            if numClass == 0:
                print("\n[+] No more classes today")
            elif numClass >=1 :
                print("\n[+] There are %s Classes" % numClass)

    def checkSubject(self,subj):
        print("[~] Getting webpage")
        page = self.getpage()
        data = self.parse(page)
        print("\n[+] Subject : %s" % subj)
        numClasses = 0

        for code in data:
            if subj in code["Course"]:
                numClasses += 1
                print("[{}] [{}] {}".format(code["Time"],code["Course"],code["Type"]))
        if numClasses > 0:
            print("[+] Number of classes : %s" % numClasses)
        else:
            print("[!] No information available for %s" % subj)

    def checkroom(self,room):
        print("[~] Getting webpage")

        page = self.getpage()
        #print page
        #date = self.getdate(page)
        #print("[+] Date : %s" % date)
        data = self.parse(page)

        print("\n[+] Room : %s" % room)
        numClasses = 0
        for code in data:
            if room == code["Room"]:
                numClasses += 1
                print("[{}] [{}] {}".format(code["Time"],code["Type"],code["Course"]))

        if numClasses == 0:
            print("\n[!] No info available right now. \n[!] Check back later")
        else:
            print("\n[+] Number of class : %s" % numClasses)

    def getcoursekey(self):
        """
        Read the course.txt and see if it is empty
        And prompt to enter course code if empty
        Returns coursekeys in list format
        """
        self.checkfile()
        # Check if the file exists first.
        try:
            if os.stat(str("%s/course.txt" % os.path.abspath('.'))).st_size <= 1:
            # Checking if the filesize is 0 byte
            # If it is empty/0 byte, ask for subject code.
                print("[!] Course.txt is empty")
                self.writecourse()
                return self.readcoursekey()
            else:
            # else means the file size is not 0 byte, which means the file is not empty
                return self.readcoursekey()

        except IOError:
            # This exception is to caught platform's file hierarchy
            # Example linux use '/'
            #         windows use '\'
            if os.stat(str("%s\course.txt" % os.path.abspath('.'))).st_size <= 1:
            # Checking if the filesize is 0 byte
            # If it is empty/0 byte, ask for subject code.
                print("[!] Course.txt is empty")
                self.writecourse()
                return self.readcoursekey()

            else:
            # else means the file size is not 0 byte, which means the file is not empty
                return self.readcoursekey()

    def checkfile(self):
        """
        Check if the course.txt file exists
        And create the file if necessary
        """
        try:
            f = open('course.txt').read()
        except IOError:
            if osname == 'windows':
                os.system('copy NUL course.txt')
            elif osname == 'linux':
                os.system('touch course.txt')

    def readcoursekey(self):
        """
        Read the course key from course.txt
        And return it as a list
        """
        return [i for i in open('course.txt').read().split('\n') if i != '']

    def writecourse(self):
        """
        Get the coursekey input from user
        And write it inside course.txt
        """
        key = []

        while True:
            code = raw_input("Enter course code : ")
            if code:
                key.append(code.upper())
            else:
                break
        with open('course.txt','w') as cf:
            for i in key:
                cf.write(i+'\n')

    def getpage(self):
        """
        Access the website
        returns the source code of the iFrame inside the webpage
        """
        try:
            return urllib.urlopen("http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInformation.aspx").readlines()
        except:
            print("[!] General Error, no internet connection?")
            sys.exit()

    def getdate(self,data):
        date_pattern = re.compile(r'<br>Date&nbsp;:&nbsp;<span id="lblDate">(.+)</span>')
        for i in data:
            if len(date_pattern.findall(i)) != 0:
                date = date_pattern.findall(i)
        return date[0]

    def parse(self, data):
        """
        Gets the input as list
        Returns the course info
        """
        page = urllib.urlopen("http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInformation.aspx").readlines()
        pat = re.compile(r'<td class="BTsubj">(.+)</td><td class="BTclass">(.+)</td><td class="BTtime">(.+)</td><td class="BTroom">(.+)</td></tr>')
        info = []
        print("[+] Processing webpage")
        for line in page:
            if len(pat.findall(line)) != 0:
                tempdata = pat.findall(line)[0]
                duration = self.convTime(tempdata[2][:5])+"~"+self.convTime(tempdata[2][8:])
                tempdict = {"Course": tempdata[0],
                            "Type"  : tempdata[1],
                            "Time"  : duration,
                            "Room"  : tempdata[3]}
                info.append(tempdict)
        return info

    def convTime(self,data):
        """
        Get input as string
        Convert it into 12 hour format if necessary
        And return it as string
        """

        hour = int(data[:data.index(':')])
        minutes = data[data.index(':')+1:]

        if hour > 12:
            hour -= 12

        return str(hour)+':'+str(minutes)

if __name__ == '__main__':
    try:
        import sys
        global osname
        osname = 'linux' if 'linux' in sys.platform else 'windows'

        import sys

        if len(sys.argv) == 1:
            app = course()
        elif len(sys.argv) == 2:
            app = course(str(sys.argv[1]).upper())
    except KeyboardInterrupt:
        print("\n[+] Ctrl + C detected!")
