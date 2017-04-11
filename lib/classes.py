from datetime import datetime

class Classes:
    def __init__(self, clsname, clstype, clstime, clsroom):
        self.raw_time = clstime # clstime will be a list
        self.room = clsroom
        self.name = clsname
        self.type = clstype

    def getRoom(self):
        return self.room

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def formatTime(self):
        """
        Formats the time into nice string to return
        """
        start = self.raw_time[0]
        end = self.raw_time[1]

        return self.convertTime(start) + " - " + self.convertTime(end)

    def convertTime(self, data):
        d = datetime.strptime(data, "%H:%M")
        return d.strftime("%I:%M")

    def getDict(self):
        """
        return dictionary format notation for jsonifying the object
        """
        return {
            "name": self.name,
            "type": self.type,
            "time": self.formatTime(),
            "room": self.room
        }
