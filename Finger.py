class Finger:
    name = ""
    hotKey = ""
    finger = 0
    def __init__(self, name, hotKey, finger):
        self.name = name
        self.hotKey = hotKey
        self.finger = finger

    def changeName(self, name):
        self.name = name

    def changeHotKey(self, hotKey):
        self.hotKey = hotKey
    
    def changeFinger(self, finger):
        self.finger = finger
    
    def getName(self):
        return self.name
    
    def getHotKey(self):
        return self.hotKey

    def getFinger(self):
        return self.finger