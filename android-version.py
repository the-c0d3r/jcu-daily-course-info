# _*_ coding: utf-8 _*_
# !/usr/bin/env python

import re
import urllib
import sys
import datetime
import os

banner3 = """


   `7MMF' .g8\"\"\"bgd `7MMF'   `7MF'
     MM .dP'     `M   MM       M
     MM dM'       `   MM       M
     MM MM            MM       M
     MM MM.           MM       M
(O)  MM `Mb.     ,'   YM.     ,M
 Ymmm9    `\"bmmmd'     `bmmmmd\"'


"""


# Website used to generate banner => http://patorjk.com/software/taag/
# Banner1 font = Big Money-nw
# Banner2 font = AMC AAA01
# Banner3 font = Georgia11

display_banner = True
# Replace "True" with "False" if you want to disable banner
coursekeyfile = __file__.strip(os.path.basename(__file__))+"course.txt"

class course():

    def __init__(self, data=None):
        self.data = []
        if display_banner:
            print banner3
            # Options, banner1 or banner2 or banner3, whichever banner you like

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
                        self.data.append(code)

            if len(self.data) == 0:
                print("\n[+] No more classes today")
            else:
                self.pprint(self.data)
                print("\n[+] There are %d Classes" % len(self.data))

    def pprint(self, data):
        self.data = data
        rwidth = max([len(subj["Course"]) for subj in self.data]) + 4
        lwidth = max([len(subj.keys()) for subj in self.data]) + 5
        lineseparater = lwidth + rwidth

        rspace = max([len(subj["Course"]) for subj in self.data])
        lspace = max([len(subj.keys()) for subj in self.data])+2
        for course in self.data:
            # printed manually cuz the keys in the self.data dictionary is not sorted
            print "." * lineseparater
            print ("| {:%d} : {:%d} |" % (lspace, rspace)).format("Course", course["Course"])
            print ("| {:%d} : {:%d} |" % (lspace, rspace)).format("Type", course["Type"])
            print ("| {:%d} : {:%d} |" % (lspace, rspace)).format("Time", course["Time"])
            print ("| {:%d} : {:%d} |" % (lspace, rspace)).format("Room", course["Room"])
            print "." * lineseparater
            print ""

    def checkSubject(self, subj):
        print("[~] Getting webpage")
        page = self.getpage()
        pagedata = self.parse(page)
        print("\n[+] Subject : %s" % subj)
        data = []
        for code in pagedata:
            if subj.upper() in code["Course"]:
                data.append(code)

        if len(data) > 0:
            self.pprint(data)
            print("[+] Number of classes : %s" % len(data))
        else:
            print("[!] No information available for %s" % subj)

    def checkroom(self, room):
        print("[~] Getting webpage")
        page = self.getpage()
        # print page
        # date = self.getdate(page)
        # print("[+] Date : %s" % date)
        data = self.parse(page)

        print("\n[+] Room : %s" % room)
        numClasses = 0
        for code in data:
            if room == code["Room"]:
                numClasses += 1
                print("[{}] [{}] {}".format(code["Time"], code["Type"], code["Course"]))

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
        return [i for i in open(coursekeyfile).read().split('\n') if i != '']

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

        with open('course.txt', 'w') as cf:
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

    def convTime(self, data):
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
        osname = 'linux'
        os.system("clear")
        if len(sys.argv) == 1:
            app = course()
        elif len(sys.argv) == 2:
            app = course(str(sys.argv[1]).upper())

