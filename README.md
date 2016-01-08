# JCU Daily Course info

**Contributors** : [the-c0d3r](https://github.com/the-c0d3r), [Hades.y2k](https://github.com/Hadesy2k)

This simple script is just for getting information on your course such as the time, class, and type of class such as lecture or Practical etc. The information is scrapped from publicly available source of [JCU website](http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInfoMain.aspx)

It will only display the course information if it is listed on this [JCU webpage](http://afm.jcu.edu.sg/JCU/InfoDisplay/DailyCourseInfoMain.aspx) and since it is daily time table, it will not display future or past day's time table and the courses which are not available on that day. 

####Why waste time to develope this [add suitable adjective here] ?
**Because** I have time to waste and I want to check information for my course only. I don't want to waste time looking at that messy JCU webpage for timetable.

Feature 
===

- Get your daily course information
- Get the classes that will or currently commencing at the room
- Get a list of class room which is not currently occupied, so you can go and do whatever


Usage
===

Run the program 
```sh
python main.py
```

Check the schedule of the room
```sh
python main.py c2-04
```
It will show all the classes that commence in the room "c2-04"

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
Example run with course code
```
LS0300
BU1805
```
![Imgur](http://i.imgur.com/ExJ70Xs.png)

![Imgur](http://i.imgur.com/6Hu2Gxa.png)
