import urllib
import re
#  import requests
from classes import Classes


class Website:
    def __init__(self):
        self.url = "http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInformation.aspx"
        self.page = self.getPage()
        self.classes = []

        self.parse()

    def getPage(self):
        try:
            return urllib.urlopen(self.url).readlines()
        except IOError:
            print("[!] Unable to connect to JCU")
            exit()

    def parse(self):
        pattern = re.compile(r'<td class="BTsubj">(.+)</td><td class="BTclass">(.+)</td><td class="BTtime">(.+)</td><td class="BTroom">(.+)</td></tr>')
        # be wary of using regular expression to parse html
        # refer to this link -> https://stackoverflow.com/a/1732454/1509809
        # but hey it works right now, i don't want to waste time experimenting tags and children with beautifulsoup
        for line in self.page:
            if len(pattern.findall(line)) != 0:
                rawdata = pattern.findall(line)[0]

                clsname = rawdata[0]
                clstype = rawdata[1]
                clstime = [rawdata[2][:5], rawdata[2][8:]] # a list with starting and ending time
                clsroom = rawdata[3]

                tempcls = Classes(clsname, clstype, clstime, clsroom)

                self.classes.append(tempcls)

    def getClassInfo(self, subjCode):
        """
        Filter the class using subject code and return class object
        """
        for cls in self.classes:
            if subjCode in cls.name:
                return cls
        return None

    def getClasses(self, codes):
        """
        Get all the classes from the provided code list
        """
        result = []
        for subjCode in codes:
            temp = self.getClassInfo(subjCode.upper())
            if temp:
                result.append(temp)
        return result

    def getRoomInfo(self, roomNumber):
        """
        returns a list of classes held at the roomNumber)
        """
        result = []
        for cls in self.classes:
            if cls.room.lower() == roomNumber.lower():
                result.append(cls)
        return result
