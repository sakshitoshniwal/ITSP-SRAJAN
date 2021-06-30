from tkinter import*
import tkinter.ttk
from PIL import ImageTk, Image
import speech_recognition as sr
w = Tk()
w.title('VOICE TO BRAILLE CONVERTER ')
w.configure(background="black")
def stb():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            x = '{}'.format(text)
        except:
            print('SORRY')
    alphabraille = ['⠁', '⠃', '⠉', '⠙', '⠑', '⠋', '⠛', '⠓', '⠊', '⠚', '⠅', '⠇',
    '⠍', '⠝', '⠕', '⠏', '⠟', '⠗', '⠎', '⠞', '⠥', '⠧', '⠺', '⠭', '⠽', '⠵']
    numbraille = ['⠼⠁', '⠼⠃', '⠼⠉', '⠼⠙', '⠼⠑', '⠼⠋', '⠼⠛', '⠼⠓', '⠼⠊', '⠼⠚']
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    text = text.lower()
    b = " "
    for l in text:
        if l in alphabet:
            b += alphabraille[alphabet.index(l)]
        elif l in nums:
            b += numbraille[nums.index(l)]
        else:
            b += '  '
    label2 =Label(w, text = f'YOU SAID: {text}', bg = "black" , fg = "pink")
    label3=Label(w,text =  f'{b}',bg ="black" , fg = "pink")
    label2.grid(row = 5 , column = 2 , sticky = "NESW")
    label3.grid(row = 6 , column = 2, sticky = "NESW")

def gr():
    import cv2
    import numpy as np
    import math as m 
    import pyttsx3 as convert 

    cap = cv2.VideoCapture(0)

    while True:
            engine = convert.init()
            ret,frame = cap.read()

            kernel = np.ones((3,3),np.uint8)
            roi = frame[0:300,0:300]\

            #th = 0
            #max_val = 255

            cv2.rectangle(frame,(0,0),(300,300),(0,255,0))

            hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

            l_b = np.array([0,20,70])
            u_b = np.array([20,255,255])

            mask = cv2.inRange(hsv,l_b,u_b)
            #mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
            mask = cv2.dilate(mask,kernel,iterations=4)
            #ret, mask = cv2.threshold(mask, th , max_val,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
            #mask = cv2.filter2D(mask,-1,kernel)
            mask = cv2.GaussianBlur(mask,(5,5),cv2.BORDER_DEFAULT)
            #mask = cv2.morphologyEx(mask,cv2.MORPH_GRADIENT,kernel) JUST OUTLINE

            contours,hierachy= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #print(len(contours))

            ct = max(contours,key = lambda  x: cv2.contourArea(x))

            epsilon = 0.0005*cv2.arcLength(ct,True)      #can't find the use of 2(decreses noise said in video)
            approx = cv2.approxPolyDP(ct,epsilon,True)

            #cv2.drawContours(frame,cnt,-1,(0,255,0),3) draws contour in frame
            hull = cv2.convexHull(ct)
            
            areahull = cv2.contourArea(hull)
            areact = cv2.contourArea(ct)
            arearatio = (areahull - areact)*100/areact
            #print(arearatio)
            #print(areahull)

            hull = cv2.convexHull(approx,returnPoints=False)
            defects = cv2.convexityDefects(approx,hull)

            l = 0

            #print(defects.shape)
            for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(approx[s][0])
                    end = tuple(approx[e][0])
                    far = tuple(approx[f][0])
                    pt = (100,180)

                    a = m.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)
                    b = m.sqrt((start[0]-far[0])**2 + (start[1]-far[1])**2)
                    c = m.sqrt((far[0]-end[0])**2 + (far[1]-end[1])**2)

                    s = (a+b+c)/2

                    ar = m.sqrt(s*(s-a)*(s-b)*(s-c))

                    d = 2*ar/a #distance between point and convex hull

                    angle = m.acos((b**2 + c**2 - a**2)/(2*b*c))*57

                    if angle <= 90 and d>30:
                            cv2.circle(roi,far,3,[255,0,0], -1)
                            l = l+1

                    cv2.line(roi,start,end,[0,255,0],2)

            #mask2 = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
            #l_blue = np.array([94,80,2])
            #u_blue = np.array([126,255,255])
            #mask2 = cv2.inRange(mask2,l_blue,u_blue)

            #sakshi, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

            
            l = l + 1
            #print(l)

            string = str(l)

            font = cv2.	FONT_ITALIC
            if l==1:
                    if arearatio < 15:
                            if areahull <27000:
                                    if len(contours) == 1:
                                            cv2.putText(frame,'S',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                                            engine.say("s")
                                            engine.runAndWait()
                                    else:
                                            cv2.putText(frame,'O',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                                            engine.say("o")
                                            engine.runAndWait()


                            else:
                                    cv2.putText(frame,'B',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                                    engine.say("b")
                                    engine.runAndWait()

                    elif 15 < arearatio <27:
                            cv2.putText(frame,'I',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                            engine.say("i")
                            engine.runAndWait()

                    elif 27< arearatio < 40:
                            cv2.putText(frame,'Y',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                            engine.say("y")
                            engine.runAndWait()

                    else:
                            cv2.putText(frame,'T',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                            engine.say("t")
                            engine.runAndWait()

            elif l==3:
                    if arearatio < 35:
                            cv2.putText(frame,'W',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                            engine.say("w")
                            engine.runAndWait()

                    else:
                            cv2.putText(frame,'F',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                            engine.say("f")
                            engine.runAndWait()

            elif l==2:
                    if arearatio > 40:
                            cv2.putText(frame,'P',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                            engine.say("p")
                            engine.runAndWait()
                    else:
                            cv2.putText(frame,'V',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                            engine.say("v")
                            engine.runAndWait()

            elif l==4:
                    cv2.putText(frame,'4',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                    engine.say("four")
                    engine.runAndWait()

            elif l==5:
                    cv2.putText(frame,'5',(350,150),font,2,(0,0,255),2,cv2.LINE_AA)
                    engine.say("five")
                    engine.runAndWait()

            #print(frame.shape) == (480,640,3)
            cv2.imshow('frame',frame)
            cv2.imshow('mask',mask)
            #cv2.imshow('blue',mask2)

            if cv2.waitKey(5) & 0xFF == 27:
                    break

    cap.release()
    cv2.destroyAllWindows()


button = Button(w,text = "\n RECORD AUDIO \n",bg = "pink" , fg = "Black", command = stb)
button.grid(row = 3, column = 2, sticky = "NW")
pic = r"C:\Users\malani\Desktop\SRAJAN\newlogo.png"
img = Image.open(pic).resize((500, 500), Image.ANTIALIAS)
my_img = ImageTk.PhotoImage(img)
my_label = Label(image = my_img)
my_label.grid(row = 1, column = 2,sticky = "NESW")
ins = Label(w,text="CLICK THE BUTTON BELOW TO RECORD AUDIO AND ACTION", fg = "pink" , bg = "black")
ins.grid(row =2 ,column = 2)
button2 = Button(w, text = "\n RECORD ACTION \n" , bg = "pink" , fg = "Black" ,  command = gr )
button2.grid(row= 3, column = 2, sticky = "NE" )
