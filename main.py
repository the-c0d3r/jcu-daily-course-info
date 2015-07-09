import re
import urllib
import sys
import date
import os
from bs4 import BeautifulSoup

coursekey = ['FS0203']

class course():

    def __init__(self):
        self.soup = BeautifulSoup(self.getpage())


    def getpage(self):
        """
        Access the website
        returns the source code of the iFrame inside the webpage
        """
        print("[~] Getting webpage")
        try:
            return urllib.urlopen("http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInformation.aspx")
        except:
            print("[!] General Error")
            sys.exit()


    def parse(self, data):
        """
        Gets the input as soup datatype or string
        Returns the course info
        """
        print("[~] Parsing the Data")
        course_info = []
        filtered = []
        for i in data:
            if i.startswith('<td class='):
                filtered.append(i)

        for i in coursekey:
            pass

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
