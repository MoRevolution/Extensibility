from tkinter import *
from PIL import Image, ImageTk, ImageFilter
import time
import random
import math
import backend



class tapStrapGUI:
    indicatorClicked = None
    isClicked = True
    #Count and count blur used for calculating gaussian blur factor
    count = 0
    countBlur = 1
    deviceConnecteed = False
    #Global R, G, and B variables are used for calculating the RGB channels in feature three. See method: pilloChangeColor2 / pilloChangeColor2A
    #An int value of 10 indicates a normal value
    globalR = 10
    globalG = 10
    globalB = 10
    currentFeature = 0
    current_tap = 0
    global button1

    def __init__(self):
        global tap_instance
        tap_instance = tapStrapGUI.TapSDK()
        tap_instance.run()
        tap_instance.register_connection_events(self.on_connect)
        tap_instance.register_disconnection_events(self.on_disconnect)
        tap_instance.register_tap_events(self.on_tap_event)
        tap_instance.register_mouse_events(self.on_mouse_event)
        tap_instance.set_input_mode(self.TapInputMode("controller"))

        self.startWindow1()
        self.featuresFrame()
        self.mainFramemainCanvas()
        self.root.mainloop()

    
    def startWindow1(self):
        self.root = Tk()
        self.root.geometry("1000x600")
        self.root.title("TapStrap GUI")
        self.root.configure(bg = '#40495c' )
       # self.root.bind('<Motion>', self.eventListenerPosition)
    #Options frame
    def featuresFrame(self):
        self.frame1 = Frame(self.root, bg = '#0d0d0d')
        self.frame1.pack(side = LEFT)
        self.frame1.pack_propagate(False)
        self.frame1.configure(width = 175, height = 600)
        self.featureButtons()
    #Main Frame
    def mainFramemainCanvas(self):
        self.mainFrame = Frame(self.root, bg = '#40495c', highlightbackground = "blue",
        highlightthickness= 5)
        self.mainFrame.pack(side = LEFT)
        self.mainFrame.pack_propagate(False)
        self.mainFrame.configure(height = 600, width = 1000)
    #Side Bar feature buttons
    def featureButtons(self):
        
        self.labelb0 = Label(text = "")
        self.labelb0.config(bg = "#ffffff")
        self.labelb0.place(x = 0, y = (50), width = 175, height = 2)
        self.button1 = Button(self.frame1, text = "RGB Channels",
        font = ('Courier New', 13), fg= "White", bd = 0, bg = "#0d0d0d",
                command = lambda: self.selectIndicator(self.button1Indicator, self.button1))
        self.button1.place(x = 20, y = 100)
        self.button1Indicator = Label(self.frame1, text = '', bg = "#0d0d0d")
        self.button1Indicator.place(x = 15, y = 100, width = 5, height = 35)
        self.labelb1 = Label(text = "")
        self.labelb1.config(bg = "#ffffff")
        self.labelb1.place(x = 0, y = (175), width = 175, height = 2)
        

        self.button2 = Button(self.frame1, text = "Blur/Hue",
        font = ('Courier New', 13), fg= "White", bd = 0, bg = "#0d0d0d",
                command = lambda: self.selectIndicator(self.button2Indicator, self.button2))
        self.button2.place(x = 20, y = 225)
        self.button2Indicator = Label(self.frame1, text = '', bg = "#0d0d0d")
        self.button2Indicator.place(x = 15, y = 225, width = 5, height = 35)
        self.labelb2 = Label(text = "")
        self.labelb2.config(bg = "#ffffff")
        self.labelb2.place(x = 0, y = (300), width = 175, height = 2)
       
        self.button3 = Button(self.frame1, text = "Color Altering",
        font = ('Courier New', 13), fg= "White", bd = 0, bg = "#0d0d0d",
                command = lambda: self.selectIndicator(self.button3Indicator, self.button3))
        self.button3.place(x = 20, y = 350)
        self.button3Indicator = Label(self.frame1, text = '', bg = "#0d0d0d")
        self.button3Indicator.place(x = 15, y = 350, width = 5, height = 35)
        self.labelb3 = Label(text = "")
        self.labelb3.config(bg = "#ffffff")
        self.labelb3.place(x = 0, y = (425), width = 175, height = 2)


        self.button4 = Button(self.frame1, text = "Feature #4",
        font = ('Courier New', 15), fg= "White", bd = 0, bg = "#0d0d0d",
                command = lambda: self.selectIndicator(self.button4Indicator, self.button4))
        self.button4.place(x = 20, y = 475)
        self.button4Indicator = Label(self.frame1, text = '', bg = "#0d0d0d")
        self.button4Indicator.place(x = 15, y = 475, width = 5, height = 35)
        self.labelb4 = Label(text = "")
        self.labelb4.config(bg = "#ffffff")
        self.labelb4.place(x = 0, y = (550), width = 175, height = 2)
    #The button Variable here is actually a label. No I won't chage it EDIT: I changed it 
    def selectIndicator(self, indicator, button):
        if (self.isClicked == True):
            indicator.config(bg = "#ffffff")
            self.indicatorClicked = indicator
            self.isClicked = False
            self.stringVar1 = button.cget('text')
            self.text1 = self.button1.cget('text')
            self.text2 = self.button2.cget('text')
            self.text3 = self.button3.cget('text')
            #which window to trigger....
            match(self.stringVar1):
                case self.text1:
                    self.triggerFeat1(self.stringVar1);
                case self.text2:
                    self.triggerFeat2(self.stringVar1)
                case self.text3:
                    self.triggerFeat3(self.stringVar1)
                case _:
                    self.triggerFeat4(self.stringVar1)
        else:
            self.indicatorClicked.config(bg = '#0d0d0d')
            indicator.config(bg = "#ffffff")
            self.indicatorClicked = indicator
            self.stringVar1 = button.cget('text')
            self.destroyYourChildren(self.mainFrame)
            match(self.stringVar1):
                case self.text1:
                    self.triggerFeat1(self.stringVar1);
                case self.text2:
                    self.triggerFeat2(self.stringVar1)
                case self.text3:
                    self.triggerFeat3(self.stringVar1)
                case _:
                    self.triggerFeat4(self.stringVar1)

    def triggerFeat1(self, labelTxt):
         self.currentFeature = 1
         self.frameFF1 = Frame(self.mainFrame, height = 600,
         width = 1000, bg = "#40495c", highlightcolor = "blue",highlightbackground= "blue")
         self.frameFF1.pack()
         self.label1A= Label(self.frameFF1, text = labelTxt, bd = 5,
         font = ("Courier New", 18), relief = RAISED, bg = "#0d0d0d",
         fg = '#fff')
         self.label1A.grid(row = 0, column = 1,pady = 50)
         self.t1A = Text(self.frameFF1,  height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Blue")
         self.t1A.grid(row = 1, column = 0, padx = 25)
         self.t2A = Text(self.frameFF1,  height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Blue")
         self.t2A.grid(row = 1, column = 1, padx = 25)
         self.t3A = Text(self.frameFF1,  height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Blue")
         self.t3A.grid(row = 1, column = 2, padx = 25)
         self.mainCanvas = Canvas(self.mainFrame, height = 300,
         width = 400,bg = "black")
         self.mainCanvas.pack(pady = 50)
         self.backgroundImg = Image.open('finalGui\wheels2.png')
         self.tempImg = self.backgroundImg
         print(self.backgroundImg.mode)
         resized = self.backgroundImg.resize((200, 200), Image.LANCZOS)
         self.imageX = ImageTk.PhotoImage(resized)
         self.mainCanvas.create_image(213, 130, image= self.imageX)
         self.buttonTemp = Button(master = self.mainFrame, text = "CHANGE COLOR", command = lambda : self.pillowColorCommand(self.tempImg, self.mainCanvas))
         self.buttonTemp.place(x = 95, y = 400)


    def triggerFeat2(self, labelTxt):
         self.currentFeature = 2
         self.frameF2 = Frame(self.mainFrame, height = 600,
         width = 1000, bg = "#40495c")
         self.frameF2.pack()
         self.label2A = Label(self.frameF2, text = labelTxt, bd = 5,
         font = ("Courier New", 18), relief = RAISED, bg = "#0d0d0d",
         fg = '#fff')
         self.label2A.grid(row = 0, column = 1,pady = 50)
         self.t1A = Text(self.frameF2, height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Blue")
         self.t1A.grid(row = 1, column = 0, padx = 25)
         self.t2A = Text(self.frameF2, height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Blue")
         self.t2A.grid(row = 1, column = 1, padx = 25)
         self.t3A = Text(self.frameF2, height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Blue")
         self.t3A.grid(row = 1, column = 2, padx = 25)
         self.mainCanvas = Canvas(self.mainFrame, height = 300,
         width = 400,bg = "black")
         self.mainCanvas.pack(pady = 50)
         self.backgroundImg = Image.open('finalGui\elnatan.PNG')
         self.tempImg = self.backgroundImg
         print(self.backgroundImg.mode)
         resized = self.backgroundImg.resize((200, 200), Image.LANCZOS)
         self.imageX = ImageTk.PhotoImage(resized)
         self.mainCanvas.create_image(213, 130, image= self.imageX)
         self.buttonTemp = Button(master = self.mainFrame, text = "BLUR", command = lambda : self.pillowBlurCommand(resized, self.mainCanvas))
         self.buttonTemp.place(x = 85, y = 370)
         self.buttonTemp2 = Button(master = self.mainFrame, text = "CONTNUOUS BLUR", command = lambda : self.pillowContBlur(resized, self.mainCanvas))
         self.buttonTemp2.place(x = 85, y = 400)
         self.buttonTemp3 = Button(master = self.mainFrame, text = "New Window", command = lambda : self.openNewWindow(self.mainCanvas))
         self.buttonTemp3.place(x = 85, y = 430)
         self.buttonTemp4 = Button(master = self.mainFrame, text = "Change Hue?", command = lambda : self.pillowHueCommand(resized, self.mainCanvas))
         self.buttonTemp4.place(x = 85, y = 460)

    def triggerFeat3(self, labelTxt):
         self.currentFeature = 3
         self.frameF3 = Frame(self.mainFrame, height = 600,
         width = 1000, bg = "#40495c")
         self.frameF3.pack()
         self.label3A = Label(self.frameF3, text = labelTxt, bd = 5,
         font = ("Courier New", 18), relief = RAISED, bg = "#0d0d0d",
         fg = '#fff')
         self.backgroundImg = Image.open('finalGui\colorful.PNG')
         self.backgroundImg = self.backgroundImg.resize((400,220), Image.LANCZOS)
         self.imageJ = ImageTk.PhotoImage(self.backgroundImg)
         self.label3A.grid(row = 0, column = 1,pady = 50)
         self.t1A = Text(self.frameF3,  height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Red", font = ("Sans Serif", 15, "bold"))
         self.t1A.grid(row = 1, column = 0, padx = 25)
         self.t2A = Text(self.frameF3, height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Green", font = ("Sans Serif", 15, "bold"))
         self.t2A.grid(row = 1, column = 1, padx = 25)
         self.t3A = Text(self.frameF3, height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Blue", font = ("Sans Serif", 15, "bold"))
         self.t3A.grid(row = 1, column = 2, padx = 25)
         self.mainCanvas = Canvas(self.mainFrame, height = 300,
         width = 400,bg = "black")
         self.mainCanvas.pack(pady = 50)
         self.buttonTemp2 = Button(master = self.mainFrame, text = "Change Color", command = lambda : self.pillowChangeColor(self.backgroundImg, self.mainCanvas))
         self.buttonTemp2.place(x = 85, y = 510)
         self.buttonTemp3 = Button(master = self.mainFrame, text = "New Window", command = lambda : self.openNewWindow2(self.mainFrame))
         self.buttonTemp3.place(x = 85, y = 540)
         self.mainCanvas.create_image(202, 106, image= self.imageJ)
         self.buttonTemp4 = Button(master = self.mainFrame, text = "Change blue 2", command = lambda : self.pillowChangeColor2(self.backgroundImg, self.mainCanvas, "blue"))
         self.buttonTemp4.place(x = 85, y = 480)
         self.buttonTemp4 = Button(master = self.mainFrame, text = "Reverse blue 2", command = lambda : self.pillowChangeColor2A(self.backgroundImg, self.mainCanvas, "blue"))
         self.buttonTemp4.place(x = 85, y = 450)
         self.buttonTemp4 = Button(master = self.mainFrame, text = "Change red 2", command = lambda : self.pillowChangeColor2(self.backgroundImg, self.mainCanvas, "red"))
         self.buttonTemp4.place(x = 85, y = 420)
         self.buttonTemp4 = Button(master = self.mainFrame, text = "Reverse red 2", command = lambda : self.pillowChangeColor2A(self.backgroundImg, self.mainCanvas, "red"))
         self.buttonTemp4.place(x = 85, y = 390)
         self.buttonTemp4 = Button(master = self.mainFrame, text = "Change green 2", command = lambda : self.pillowChangeColor2(self.backgroundImg, self.mainCanvas, "green"))
         self.buttonTemp4.place(x = 85, y = 360)
         self.buttonTemp4 = Button(master = self.mainFrame, text = "Reverse green 2", command = lambda : self.pillowChangeColor2A(self.backgroundImg, self.mainCanvas, "green"))
         self.buttonTemp4.place(x = 85, y = 330)

    def triggerFeat4(self, labelTxt):
         self.currentFeature = 4
         self.frameF4 = Frame(self.mainFrame, height = 650,
         width = 1000, bg = "#40495c")
         self.frameF4.pack()
         self.label4A = Label(self.frameF4, text = labelTxt, bd = 5,
         font = ("Courier New", 18), relief = RAISED, bg = "#0d0d0d",
         fg = '#fff')
         self.label4A.grid(row = 0, column = 1,pady = 100)
         self.t1A = Text(self.frameF4,  height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Blue")
         self.t1A.grid(row = 1, column = 0, padx = 25)
         self.t2A = Text(self.frameF4, height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Blue")
         self.t2A.grid(row = 1, column = 1, padx = 25)
         self.t3A = Text(self.frameF4,  height = 5, width = 20, bd= 5, relief=SUNKEN, fg = "Blue")
         self.t3A.grid(row = 1, column = 2, padx = 25)

    def destroyYourChildren(self, frame):
        for frame in frame.winfo_children():
             frame.destroy()
    #Experimental feature to determine if device is connected or not
    def deviceConnecteed(self):
        if (self.deviceConnected == True):
            pass

    def changeInput(self):
        self.textbox1.config(text = f"Data point number {self.i}")
        self.root.update_idletasks()
        self.i += 1
    #AnRGB image contains 3 bands- ‘R’ (Red), ‘G’ (Green), and ‘B’ (Blue).
    #This method splits the RBG PNG into the 3 bands and displays them 
    #seperately 
    def pillowColorCommand(self, image, canvas):
        self.destroyYourChildren(canvas)
        arrVal = Image.Image.split(image)
        var1 = (self.count % 4)
        self.count +=1
        print(var1)
        match (var1):
            case (1):
                resozed= arrVal[2].resize((200,200), Image.LANCZOS)
                self.newImage = ImageTk.PhotoImage(resozed)
                self.mainCanvas.create_image(213, 130, image= self.newImage)
                newLabel = Label(master = canvas, bg = "#0bed07", width = 7, height = 13)
                newLabel.place(x = 30, y = 30)
            case (0):
                resozed= arrVal[1].resize((200,200), Image.LANCZOS)
                self.newImage = ImageTk.PhotoImage(resozed)
                self.mainCanvas.create_image(213, 130, image= self.newImage)
                newLabel = Label(master = canvas, bg = "Red", width = 7, height = 13)
                newLabel.place(x = 30, y = 30)
            case (2):
                resozed= arrVal[0].resize((200,200), Image.LANCZOS)
                self.newImage = ImageTk.PhotoImage(resozed)
                self.mainCanvas.create_image(213, 130, image= self.newImage)
                newLabel = Label(master = canvas, bg = "Blue", width = 7, height = 13)
                newLabel.place(x = 30, y = 30)
            case (3):
                resozed = image.resize((200,200), Image.LANCZOS)
                self.newImage = ImageTk.PhotoImage(resozed)
                self.mainCanvas.create_image(213, 130, image= self.newImage)
    #Debugger printing cursor location on parent widget.
    #Useful for finding borders of frames/canvas'and placing
    #widgets =)d - s21
    def eventListenerPosition(self, event):
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))
    #Button to blur discretely
    def pillowBlurCommand(self, image1, canvas):
        if (self.countBlur % 3 == 1):
            self.destroyYourChildren(canvas)
            self.newImage1 = ImageTk.PhotoImage(image1.filter(ImageFilter.GaussianBlur(4)))
            canvas.create_image(213, 130, image = self.newImage1)
            self.countBlur +=1
        elif(self.countBlur % 3 == 0 ):
            self.destroyYourChildren(canvas)
            self.newImage1 = ImageTk.PhotoImage(image1)
            canvas.create_image(213, 130, image = self.newImage1)
            self.countBlur +=1
        else:
            self.destroyYourChildren(canvas)
            self.newImage1 = ImageTk.PhotoImage(image1.filter(ImageFilter.GaussianBlur(13)))
            canvas.create_image(213, 130, image = self.newImage1)
            self.countBlur +=1
    
    def pillowContBlur(self, image1, canvas):
        #Increase Gaussian Blur
        for x in range(0, 50):
            self.newImage2 = ImageTk.PhotoImage(image1.filter(ImageFilter.GaussianBlur(x)))
            canvas.create_image(213, 130, image = self.newImage2)
            self.destroyYourChildren(canvas)
            canvas.update_idletasks()
            time.sleep(.03)
          #  print(x)
        #epic jumpsare
        #self.tempImg = image1.resize((400, 300), Image.LANCZOS)
        # self.newImage3 = ImageTk.PhotoImage(image1.filter((ImageFilter.FIND_EDGES)))
        # canvas.create_image(213, 130, image = self.newImage3)
        # canvas.update_idletasks()
        # time.sleep(.05)
        # canvas.delete("all")
        #Reduce Gaussian Blur
        for j in reversed(range(0,30)):
            self.newImage2 = ImageTk.PhotoImage(image1.filter(ImageFilter.GaussianBlur(j)))
            canvas.create_image(213, 130, image = self.newImage2)
            self.destroyYourChildren(canvas)
            canvas.update_idletasks()
            time.sleep(.03)
        #print(j)
    def pillowHueCommand(self, image1, canvas):
        #Change Hue of picture
        for x in range(0, 100):
            self.newImage2 = ImageTk.PhotoImage(image1.point(lambda p: p > x and 255))
            canvas.create_image(213, 130, image = self.newImage2)
            self.destroyYourChildren(canvas)
            canvas.update_idletasks()
            time.sleep(.05)
        #ADD FUNCTIONALITYYYY (this is for feature 2)
    def openNewWindow(self,pWindow):
        newWindow = Toplevel(pWindow)
        newWindow.title("New Window")
        newWindow.geometry("1400x800")
        Label(newWindow,
          text ="This is a new window").pack()
        #This is for feature 3
    def openNewWindow2(self,pWindow):
        newWindow = Toplevel(pWindow)
        newWindow.title("New Window")
        newWindow.geometry("1400x800")
        Label(newWindow,
          text ="This is a new window").pack()
        newCanvas = Canvas(newWindow, height = 800,
        width = 1400,bg = "black")
        newCanvas.pack()
    
    def pillowChangeColor(self, image1, canvas):
        for x in range(10):
            canvas.delete("all")
            arrImg = image1.split()
            colors = self.threeRandomInt()
            arrImg0 = arrImg[0].point(lambda i: i * colors[0])
            arrImg1 = arrImg[1].point(lambda i: i * colors[1])
            arrImg2 = arrImg[2].point(lambda i: i * colors[2])
            image4 = Image.merge("RGB", (arrImg0, arrImg1, arrImg2))
            image4 = image4.resize((400,220), Image.LANCZOS)
            self.image4 = ImageTk.PhotoImage(image4)
            canvas.create_image(202, 106, image = self.image4) 
            canvas.update_idletasks()
            time.sleep(.08)  

    def pillowChangeColor2(self, image1, canvas, color):
        match (color):
            case ("red"):
                for x in range(self.globalR, self.globalR + 5):
                    canvas.delete("all")
                    arrImg = image1.split()
                    arrImg0 = arrImg[0].point(lambda i: i * (x/10))
                    arrImg1 = arrImg[1].point(lambda i: i * (self.globalG / 10))
                    arrImg2 = arrImg[2].point(lambda i: i * (self.globalB/ 10))
                    image4 = Image.merge("RGB", (arrImg0, arrImg1, arrImg2))
                    image4 = image4.resize((400,220), Image.LANCZOS)
                    self.image4 = ImageTk.PhotoImage(image4)
                    canvas.create_image(202, 106, image = self.image4) 
                    canvas.update_idletasks()
                    time.sleep(.03)  
                    self.t1A.delete("1.0", "end")
                    self.t1A.insert(INSERT, self.globalR)
                    self.globalR +=1
                    
            case ("green"):
                for x in range(self.globalG, self.globalG + 5):
                    canvas.delete("all")
                    arrImg = image1.split()
                    arrImg0 = arrImg[0].point(lambda i: i * (self.globalR/ 10))
                    arrImg1 = arrImg[1].point(lambda i: i * (x/10))
                    arrImg2 = arrImg[2].point(lambda i: i * (self.globalB/ 10))
                    image4 = Image.merge("RGB", (arrImg0, arrImg1, arrImg2))
                    image4 = image4.resize((400,220), Image.LANCZOS)
                    self.image4 = ImageTk.PhotoImage(image4)
                    canvas.create_image(202, 106, image = self.image4) 
                    canvas.update_idletasks()
                    time.sleep(.03)
                    self.t2A.delete("1.0", "end")
                    self.t2A.insert(INSERT, self.globalG)
                    self.globalG +=1
            case _:  
                for x in range(self.globalB, self.globalB + 5):
                    canvas.delete("all")
                    arrImg = image1.split()
                    arrImg0 = arrImg[0].point(lambda i: i * (self.globalR/ 10))
                    arrImg1 = arrImg[1].point(lambda i: i * (self.globalG/ 10))
                    arrImg2 = arrImg[2].point(lambda i: i * (x/10))
                    image4 = Image.merge("RGB", (arrImg0, arrImg1, arrImg2))
                    image4 = image4.resize((400,220), Image.LANCZOS)
                    self.image4 = ImageTk.PhotoImage(image4)
                    canvas.create_image(202, 106, image = self.image4) 
                    canvas.update_idletasks()
                    time.sleep(.03)
                    self.t3A.delete("1.0", "end")
                    self.t3A.insert(INSERT, self.globalB)
                    self.globalB +=1
    #REVERSE color
    def pillowChangeColor2A(self, image1, canvas, color):
        match (color):
            case ("red"):
                print(self.globalR)
                for x in reversed(range(self.globalR - 5,self.globalR)):
                    print("MY LOOP IS WORKINGN")
                    canvas.delete("all")
                    arrImg = image1.split()
                    arrImg0 = arrImg[0].point(lambda i: i * (x/10))
                    arrImg1 = arrImg[1].point(lambda i: i * (self.globalG / 10))
                    arrImg2 = arrImg[2].point(lambda i: i * (self.globalB / 10))
                    image4 = Image.merge("RGB", (arrImg0, arrImg1, arrImg2))
                    image4 = image4.resize((400,220), Image.LANCZOS)
                    self.image4 = ImageTk.PhotoImage(image4)
                    canvas.create_image(202, 106, image = self.image4) 
                    canvas.update_idletasks()
                    time.sleep(.03)  
                    self.t1A.delete("1.0", "end")
                    self.t1A.insert(INSERT, self.globalR)
                    self.globalR -=1  
                    print(x)  

            case ("green"):
                for x in reversed(range(self.globalG - 5,self.globalG)):
                    canvas.delete("all")
                    arrImg = image1.split()
                    arrImg0 = arrImg[0].point(lambda i: i * (self.globalR / 10))
                    arrImg1 = arrImg[1].point(lambda i: i * (x/10))
                    arrImg2 = arrImg[2].point(lambda i: i * (self.globalB / 10))
                    image4 = Image.merge("RGB", (arrImg0, arrImg1, arrImg2))
                    image4 = image4.resize((400,220), Image.LANCZOS)
                    self.image4 = ImageTk.PhotoImage(image4)
                    canvas.create_image(202, 106, image = self.image4) 
                    canvas.update_idletasks()
                    time.sleep(.03)
                    self.t2A.delete("1.0", "end")
                    self.t2A.insert(INSERT, self.globalG)
                    self.globalG -=1

            case _:
                for x in reversed(range(self.globalB - 5,self.globalB)):
                    canvas.delete("all")
                    arrImg = image1.split()
                    arrImg0 = arrImg[0].point(lambda i: i * (self.globalR / 10))
                    arrImg1 = arrImg[1].point(lambda i: i * (self.globalG / 10))
                    arrImg2 = arrImg[2].point(lambda i: i * (x/10))
                    image4 = Image.merge("RGB", (arrImg0, arrImg1, arrImg2))
                    image4 = image4.resize((400,220), Image.LANCZOS)
                    self.image4 = ImageTk.PhotoImage(image4)
                    canvas.create_image(202, 106, image = self.image4) 
                    canvas.update_idletasks()
                    time.sleep(.03)  
                    self.t3A.delete("1.0", "end")
                    self.t3A.insert(INSERT, self.globalB)
                    self.globalB -=1
    #This is a helper function for changing the color to random 
    #in feature 3tiihieee
    def threeRandomInt(self):
        arr = [.3, .5, .7, .9, 1, 1.1, 1.2, 1.3, 1.4,1.3, 1.4, 1.6, 1.8]
        arrG = [.25, .3, .5, .7, .9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.9 ]
        r = random.choice(arr)
        g = random.choice(arrG)
        b = random.choice(arr)
        arrColor = [r, g, b]
        return arrColor

    from tapsdk import TapSDK, TapInputMode
    from Finger import Finger

    import keyboard
    import screen_brightness_control as sbc
    # from multiplePages import tapStrapGUI
   
    finger = Finger("Empty", "Put Hotkey Here", 0)
    tap_instance = []
    tap_identifiers = []
    fingerList = [Finger("Pointer", "ctrl", 2), Finger("Middle", "ctrl", 4), Finger("Ring", "ctrl", 8),Finger("Pinky", "ctrl", 16)]
    tap_status = False
    isActive = False
    current_tapcode = 0
    interval = 1
    direction = 0
    
    #Adds the connected Tap Strap to a list of connected taps and sets connection status to true
    def on_connect(self, identifier, name, fw):
        self.tap_status = True
        if identifier not in self.tap_identifiers:
            self.tap_identifiers.append(identifier)
        print("Connected taps:")
        for identifier in self.tap_identifiers:
            print(identifier)
    
    #Removes the connected Tap Strap from a list of connected taps and sets connection status to true
    def on_disconnect(self, identifier):
        self.tap_status = False
        print("Tap has disconnected")
        if identifier in self.tap_identifiers:
            self.tap_identifiers.remove(identifier)
        for identifier in self.tap_identifiers:
            print(identifier)
    
    #Detects a tap and gives the tapcode from the Tap Strap
    def on_tap_event(self, identifier, tapcode):
        # print(identifier, str(tapcode)) # For debugging to see what tapcode is being sent
        self.current_tapcode = tapcode
        self.activeStatus(tapcode)
        self.selectMode(tapcode)
        # self.selectMode(tapcode)

    #Detects mouse movement and gives the x and y coordinates
    def on_mouse_event(self, identifier, dx, dy, isMouse):
        if self.isActive:
            if isMouse:
                #print(str(dx), str(dy)) # For debugging to see what the mouse movement is
                if (int(dx) > 10):
                    self.sbc.set_brightness(75)
                elif (int(dx) < -10):
                    self.sbc.set_brightness(25)
            else:
                pass
                # print("Air: ", str(dx), str(dy))

    #Activates or deactivates the Tap Strap
    def activeStatus(self, tapcode):
        if int(self.current_tapcode) == 30:
            if tapStrapGUI.isActive:
                tapStrapGUI.isActive = False
                print("Tap is inactive")
            else:
                tapStrapGUI.isActive = True
                print("Tap is active")
    
    #Selects the mode of the Tap Strap using the given tapcode
    def selectMode(self, tapcode):
        if self.isActive:
            if int(self.current_tapcode) == 2:
                self.finger = self.fingerList[0]
                print("Pointer Finger Active")
                self.button1.invoke()
            elif int(self.current_tapcode) == 4:
                self.finger = self.fingerList[1]
                print("Middle Finger Active")
                self.button2.invoke()
            elif int(self.current_tapcode) == 8:
                self.finger = self.fingerList[2]
                print("Ring Finger Active")
                self.button3.invoke()
            elif int(self.current_tapcode) == 16:
                self.finger = self.fingerList[3]
                print("Pinky Finger Active")
                self.button4.invoke()
            elif int(self.current_tapcode) == 14:
                self.activateHotkey(self.finger.getHotKey())
                print("Hotkey Activated")

    #Changes the hotkey assigned to the finger 
    def setHotKey(self, hotkey):
        newKey = self.keyboard.record(until='\\')
        self.finger.changeHotKey(newKey)

    #Activates the hotkey of the current finger
    def activateHotkey(self, hotkey):
        self.keyboard.press_and_release(hotkey)
    
    #Changes the interval of adjustments when using the mouse mode
    def set_interval(self, interval):
        self.interval = interval
    





def main():
    tapStrapGUI()
        
if __name__ == "__main__":
    main()