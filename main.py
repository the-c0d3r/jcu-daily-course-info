#!/usr/bin/env python

import re
import urllib
import sys
import datetime
import os
import ast


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
   S&S  S&S     S&S       S&S  
   S&S  S&S     S&S       S&S  
   d*S  S*b     S*b       d*S  
  .S*S  S*S.    S*S.     .S*S  
sdSSS    SSSbs   SSSbs_sdSSS   
YSSY      YSSP    YSSP~YSSY    
"""

# Website used to generate banner => http://patorjk.com/software/taag/
# Banner1 font = Big Money-nw
# Banner2 font = AMC AAA01

display_banner = True
# Replace "True" with "False" if you want to disable banner

class course():

    def __init__(self, room=None):
        if display_banner:
            print banner2
            # Options, banner1 or banner2, whichever banner you like
        if room:
            self.checkroom(room)
        else:
            ckey = self.getcoursekey()
            # getcoursekey returns list, and save it as ckey
            print("[~] Getting webpage")
            self.page = self.getpage()
            # Get the webpage
            self.parse(self.page,ckey)
            # Parse and display the data scrapped. 

    def checkroom(self,room):
        print("[~] Getting webpage")
        
        page = self.getpage()
        #print page
        date = self.getdate(page)
        print("[+] Date : %s" % date)
        data = []
        classes = []
        print("[+] Getting information for room : %s" % room)
        pat = re.compile(r'.+<td class="BTsubj">(.+)</td><td class="BTclass">(.+)</td><td class="BTtime">(.+)</td><td class="BTroom">(.+)</td></tr>.+')
        for i in page:
            if len(pat.findall(i)) != 0:
                data.append(pat.findall(i))
            else: pass

        for i in data:
            if i[0][3] == room:
                i = i[0]
                duration = self.convert_time(i[2][0:4])+" ~ "+self.convert_time(i[2][8:])
                #class_data = i[0]+"\t"+i[1]+"\t"+duration+"\t"+i[3]
                class_data = "[{}] [{}] [{}] {}".format(i[3],duration,i[1],i[0])
                print class_data
                classes.append(class_data)

        #print classes
#             0                  1           2           3
#[('CP1404 - Programming I', 'LA', '09:00 - 11:50', 'C2-04')]
        

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
            os.system('echo > course.txt')

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
                key.append(code)
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

    def parse(self, data, key):
        """
        Gets the input as list
        Returns the course info
        """
        course_info = {} # to keep the course data inside as dictionary which is stated by coursekey

        filtered = [] # to keep all the subject list
        classes = 0 # Count of number of class today


        pat = re.compile(r'<td class="BTsubj">(.+)</td><td class="BTclass">(.+)</td><td class="BTtime">(.+)</td><td class="BTroom">(.+)</td></tr>')

        for i in data:
        # Filter all the html code starting with <td class="BTsubj"
            if len(pat.findall(i)) != 0:
            # If the pattern is matched
                filtered.append(pat.findall(i))
                # The variable "i" is added to filtered list
            else: pass

        for i in filtered:
            for a in key:
                if a in i[0][0]:
                    duration = self.convert_time(i[0][2][:5])+" ~ "+self.convert_time(i[0][2][8:])
                    # i[0][2][:5] is the start time and i[0][2][8:] is end time
                    # get those time strings and call convert_time to convert them into 12 hour format.
                    print("\nCourse : {}\nType : {}\nTime : {}\nRoom : {}\n".format(i[0][0],i[0][1],duration,i[0][3]))
                    classes += 1
                    #x = ast.literal_eval(str("{'Course':'%s','Type':'%s','Time':'%s','Room':'%s'}"%(i[0][0],i[0][1],duration,i[0][3])))
                    # Printing the course information.

        if not classes:
            print("[*] No More Class for today")
        elif classes:
            print ("[*] There are %d class(es) today" % classes)

        # Example response from Regular Expression, just for debugging purpose
        #[('BU1805 - Contemporary Business Communications', 'LA,B,C,D,E,F', '16:00 - 17:50', 'C4-14')]

    def convert_time(self,data):
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
    import sys
    if len(sys.argv) == 1:
        app = course()
    elif len(sys.argv) == 2:
        app = course(str(sys.argv[1]).upper())