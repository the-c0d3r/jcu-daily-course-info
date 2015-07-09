import re
import urllib
import sys
import datetime
import os

coursekey = [i for i in open('course.txt').read().split('\n') if i != '']
# Reads the course.txt file and add it to coursekey if the data is not empty

banner1 = """
   $$$$$\  $$$$$$\  $$\   $$\ 
   \__$$ |$$  __$$\ $$ |  $$ |
      $$ |$$ /  \__|$$ |  $$ |
      $$ |$$ |      $$ |  $$ |
$$\   $$ |$$ |      $$ |  $$ |
$$ |  $$ |$$ |  $$\ $$ |  $$ |
\$$$$$$  |\$$$$$$  |\$$$$$$  |
 \______/  \______/  \______/ """

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

    def __init__(self):
        if display_banner:
            print banner2
            # Options, banner1 or banner2, whichever banner you like

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
        course_info = [] # to keep the course data inside as list which is stated by coursekey

        filtered = [] # to keep all the subject list

        pat = re.compile(r'<td class="BTsubj">(.+)</td><td class="BTclass">(.+)</td><td class="BTtime">(.+)</td><td class="BTroom">(.+)</td></tr>')

        for i in data:
        # Filter all the html code starting with <td class="BTsubj"
            if len(pat.findall(i)) != 0:
            # If the pattern is matched
                filtered.append(pat.findall(i))
                # The variable "i" is added to filtered list
            else: pass

        for i in filtered:
            for a in coursekey:
                if a in i[0][0]:
                    duration = self.convert_time(i[0][2][:5])+" ~ "+self.convert_time(i[0][2][8:])
                    # i[0][2][:5] is the start time and i[0][2][8:] is end time
                    # get those time strings and call convert_time to convert them into 12 hour format.
                    print("\nCourse : {}\nType : {}\nTime : {}\nRoom : {}\n".format(i[0][0],i[0][1],duration,i[0][3]))
                    # Printing the course information.


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
    app = course()