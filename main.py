import re
import urllib
import sys
import datetime
import os

coursekey = ['LS0300', 'BU1805']

class course():

    def __init__(self):
        self.page = self.getpage()
        self.parse(self.page)


    def getpage(self):
        """
        Access the website
        returns the source code of the iFrame inside the webpage
        """
        print("[~] Getting webpage")
        try:
            return urllib.urlopen("http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInformation.aspx").readlines()
        except:
            print("[!] General Error")
            sys.exit()


    def parse(self, data):
        """
        Gets the input as list
        Returns the course info
        """
        print("[~] Parsing the Data")
        course_info = []
        filtered = []
        pat = re.compile(r'<td class="BTsubj">(.+)</td><td class="BTclass">(.+)</td><td class="BTtime">(.+)</td><td class="BTroom">(.+)</td></tr>')

        for i in data:
            if len(pat.findall(i)) != 0:
                filtered.append(pat.findall(i))
            else:
                pass

        for i in filtered:
            for a in coursekey:
                if a in i[0][0]:
                    print "Course : {}\nType : {}\nTime : {}\nRoom : {}".format(i[0][0],i[0][1],i[0][2],i[0][3])
        #[('BU1805 - Contemporary Business Communications', 'LA,B,C,D,E,F', '16:00 - 17:50', 'C4-14')]
        #print "BU1805" in filtered[5][0][0]


# 
    def convert_time(self,data):
        """
        Get input as string
        Convert it into 12 hour format if necessary
        """

        hour = data[:data.index(':')]
        minutes = data[data.index(':')+1:]

        if hour > 12:
            hour -= 12

        return str(hour,':',minutes)

if __name__ == '__main__':
    app = course()


"""
Check if the subject code is empty
    YES : Ask for it | NO : Pass
Check if the html file exists and date
    If exist and date inconsistent:
        get new page and save file
    Else:
        pass


Flow
1. Get file
2. Parse the file, get course information 
3. Print them

Modules

class course -> INIT -> getpage -> exists -> 

"""
