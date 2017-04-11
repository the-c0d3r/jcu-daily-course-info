# JCU Daily Course info


This simple script is just for getting information on your course such as the time, class, and type of class such as lecture or Practical etc. The information is scrapped from publicly available source of [JCU website](http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInfoMain.aspx)

It will only display the course information if it is listed on this [JCU webpage](http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInfoMain.aspx) and since it is daily time table, it will not display future or past day's time table and the courses which are not available on that day. 

Feature 
===

- Get your daily course information
- Get the classes that will or currently commencing at the room
- Get the information for the class by subject code
- Get a list of class room which is not currently occupied.


Usage
===

```sh
python main.py
python main.py c2-04 
python main.py py5012
```


Get a list of free rooms
```sh
python getaroom.py
```


Options
===
1. The banner inside the program can be changed to banner1 or banner2
2. Entirely remove the banner by changing `display_banner = True` to `display_banner = False`
3. To get a simple command such as "jcu" you can add the following line to your `.bashrc` file, or `.profile` for mac. Change `path/to/jcu-daily-course-info` to the real path where you put the files. So after doing `source .bashrc` or `source .profile` you can just type "jcu" to execute the program. 

```sh
alias jcu="cd path/to/jcu-daily-course-info && python main.py && cd - > /dev/null"
```

Screenshot
=====

<img src="http://i.imgur.com/mcV5hhd.png" height="500" />
