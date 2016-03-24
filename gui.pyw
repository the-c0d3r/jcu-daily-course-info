import re
import urllib
import sys
import datetime
import os
import Tkinter

class course:

    def __init__(self, room=None):
        if room:
            self.checkroom(room)
        else:
            ckey = self.getcoursekey()
            # getcoursekey returns list, and save it as ckey
            self.page = self.getpage()
            data = self.parse(self.page)
            numClass = 0
            self.classes = []
            for subject in ckey:
                for code in data:
                    if subject in code["Course"]:
                        numClass += 1
                        self.classes.append(code)

    def getcoursekey(self):
        self.checkfile()
        try:
            if os.stat(str("%s/course.txt" % os.path.abspath('.'))).st_size <= 1: 
                print("[!] Course.txt is empty")
                self.writecourse()
                return self.readcoursekey()
            else:
                return self.readcoursekey()
        except IOError:
            if os.stat(str("%s\course.txt" % os.path.abspath('.'))).st_size <= 1:
                print("[!] Course.txt is empty")
                self.writecourse()
                return self.readcoursekey()
            else:
                return self.readcoursekey()

    def checkfile(self):
        try:
            f = open('course.txt').read()
        except IOError:
            if osname == 'windows':
                os.system('copy NUL course.txt')
            elif osname == 'linux':
                os.system('touch course.txt')

    def readcoursekey(self):
        return [i for i in open('course.txt').read().split('\n') if i != '']

    def writecourse(self):
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
        page = urllib.urlopen("http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInformation.aspx").readlines()
        pat = re.compile(r'<td class="BTsubj">(.+)</td><td class="BTclass">(.+)</td><td class="BTtime">(.+)</td><td class="BTroom">(.+)</td></tr>')
        info = []
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
        hour = int(data[:data.index(':')])
        minutes = data[data.index(':')+1:]
        if hour > 12: hour -= 12
        return str(hour)+':'+str(minutes)


class GUI:
    def __init__(self):
        self.initUI()
        courses = course().classes
        
        for c in courses:
            Tkinter.Label(self.window,text=c).pack()

        self.window.mainloop()

    def initUI(self):
        width = 700
        height = 150

        self.window = Tkinter.Tk()
        self.window.focus_force()
        self.window.title("JCU Daily Course Info")
        self.window.maxsize(width,height)
        
        # Centers the window
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw-width)/2
        y = (sh-height)/2
        self.window.geometry('%dx%d+%d+%d' % (width,height,x,y))

if __name__ == "__main__":
    app = GUI()