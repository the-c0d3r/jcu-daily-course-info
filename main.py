# _*_ coding: utf-8 _*_

import re
import urllib
import sys
import os
from lib.website import Website


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

banner3 = """


   `7MMF' .g8\"\"\"bgd `7MMF'   `7MF'
     MM .dP'     `M   MM       M
     MM dM'       `   MM       M
     MM MM            MM       M
     MM MM.           MM       M
(O)  MM `Mb.     ,'   YM.     ,M
 Ymmm9    `\"bmmmd'     `bmmmmd\"'


"""

banner4 = """
            »
            ╣
       ╖  ╣-Å.╣─,-
      ,╓Ñ╓╪╣╣╣╗╕Ü,-
     ,,╡╒╬ÅÅÅÅδ╣µ║,
╗╗╖      ,╓╗╗╦╖      ,╓╗╦
▒███▌▌▒▒▌███████▌▒▒▌▌███▌
`╙╙▀█████▀Γ``╙Ñ▀█████▀Γ``
                                   `7MMF' .g8\"\"\"bgd `7MMF'   `7MF'
▒▒▒▄╗,,,╓╗▒▒▒▒▒╗╖,,,╓╗▒▒▒            MM .dP'     `M   MM       M
▒███████████████████████▌            MM dM'       `   MM       M
    Ñ▀▀▀Γ`      Ñ▀▀▀Γ                MM MM            MM       M
 ,         ,,,         ,             MM MM.           MM       M
 ╚█▌▒▒▄▄▒▌█████▌▒▄▄▒▒▌█Σ        (O)  MM `Mb.     ,'   YM.     ,M
  ╙██████▌▀▀▀▀▀██████▌Γ          Ymmm9    `\"bmmmd'     `bmmmmd\"'
                                ██████████████████████████████████████
         ╓╗╣▄▄╗,
         `▀██▌▀Γ
                         """

# Website used to generate banner => http://patorjk.com/software/taag/
# Banner1 font = Big Money-nw
# Banner2 font = AMC AAA01
# Banner3 font = Georgia11

display_banner = True
# Replace "True" with "False" if you want to disable banner

class Record:
    """ A class to handle courses.txt file"""
    def __init__(self):
        """ if 'course.txt' doesn't exist, it'll ask the subject code and write to file """
        self.file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "course.txt"

        if os.path.exists(self.file_path):
            self.codes = self.read()
        else:
            self.write()

    def read(self):
        return [i.strip('\n') for i in open(self.file_path).readlines()]

    def write(self):
        self.codes = []
        with open(self.file_path, 'w') as cf:
            usrinput = input("Enter subject code : ")
            while usrinput != "":
                self.codes.append(usrinput.upper())
                usrinput = input("Enter subject code : ")
            cf.write([i+"\n" for i in self.codes])


def classPrinter(classObj):
    print("| Course : {}".format(classObj.name))
    print("| Type   : {}".format(classObj.type))
    print("| Time   : {}".format(classObj.formatTime()))
    print("| Room   : {}".format(classObj.room))
    print("\n")

def main(argument=None):
    if display_banner: print(banner4)
    courses = Record().codes
    print("[+] Processing Webpage\n")
    app = Website()
    if argument:
        # Checks if the input argument is room number or course code
        course_pattern = re.compile("(\w\w[\-]?\d\d\d\d)")
        room_pattern = re.compile("(\w\d[\-?]\d\d)")
        if course_pattern.match(str(argument)):
            result = app.getClassInfo(argument)
            if result:
                classPrinter(result)
            else:
                print("[-] There is no class information available")

        elif room_pattern.match(str(argument)):
            result = app.getRoomInfo(str(argument))
            if result:
                for i in result:
                    classPrinter(i)
            else:
                print("[-] No room information available")
    else:
        result = app.getClasses(courses)
        if len(result) == 0:
            print("[+] There seem to be no classes")
            exit()

        for i in result:
            classPrinter(i)



if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            main()
        elif len(sys.argv) == 2:
            main(str(sys.argv[1]).upper())
    except KeyboardInterrupt:
        print("\n[+] Ctrl + C detected!")
