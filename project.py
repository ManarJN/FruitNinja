# Template for interactive animations with Tkinter
from Tkinter import *
import time
import random
import string

# This function is called when the user clicks the mouse
def mousePressed(event):
    pass

# This function is called when the user presses a key
def keyPressed(event):
    # event.char contains the character pressed on the keyboard
    # event.keysym contains the special key pressed on the keyboard
    delete = -1
    low = canvas.data.level * 5
    high = 5 + canvas.data.level * 5
    for i in range(len(canvas.data.x)):
        if event.char == canvas.data.t[i] :
            canvas.data.boomx=canvas.data.x[i]
            canvas.data.boomy=canvas.data.y[i]
            delete=i
            canvas.data.draw=True
            canvas.data.boom=5
            if canvas.data.fruits[i] == "special":
                canvas.data.points *= 2
            elif canvas.data.fruits[i] == "bomb":
                canvas.data.points/=2
            elif canvas.data.fruits[i]=="special2":
                for i in range(len(canvas.data.vy)):
                    canvas.data.vy[i]=2
            else:
                canvas.data.points +=10
            
                    
    if delete != -1 and (len(canvas.data.x))>0:
        del canvas.data.fruits[delete]
        del canvas.data.x[delete]
        del canvas.data.vx[delete]
        del canvas.data.vy[delete]
        del canvas.data.y[delete]
        del canvas.data.t[delete]
        canvas.data.fruits.append(random.choice(["apple","strawberry","orange",
                                                "banana","watermelon","pear",
                                                "bomb"]))
        canvas.data.x.append(random.randint(0,800))
        canvas.data.vx.append(5)
        canvas.data.vy.append(random.randint(low,high))
        canvas.data.y.append(700)
        a = canvas.data.letters[random.randint(0,len(canvas.data.letters)-1)]
        canvas.data.t.append(a)                                 
           
    redrawAll()

# The timer will execute periodically
def timerFired(previousTime):
    currentTime = time.time()
    #checks if the current time is the same as the time of the special fruit
    #that the special fruite will be drawn
    if canvas.data.specialTime==canvas.data.ss:
        canvas.data.special= True
    if canvas.data.specialTime2==canvas.data.ss:
        canvas.data.special2= True


    #makes sure that the bomb only appears for ten seconds
    if canvas.data.bombTime - 10 <= canvas.data.ss <= canvas.data.bombTime:
        canvas.data.bomb = True
    else:
        canvas.data.bomb = False

    #makes sure that the special fruit 3 appears for ten seconds
    if canvas.data.special3 == True and canvas.data.specialTime3 - 10 <= canvas.data.ss <= canvas.data.specialTime3:
        canvas.data.lines = True
    else:
        canvas.data.lines = False
        
    
    
    #Once the player collect maxPoints of level, he goes to the next level   
    if canvas.data.points >= canvas.data.maxPoints[canvas.data.level-1]:
        canvas.data.counterDelay-=2 #when countredelay is decresed by 5, the letters inside the fruite will change more quicly
        canvas.data.points = 0 #after the player reaches the next level, the score restarts
        canvas.data.level += 1 #level is increased by 1
        low = canvas.data.level * 5 #slowest speed a fruit can have at this level
        high = 5 + canvas.data.level * 5 #fastest speed a fruit can have at this level
        canvas.data.y=[700,700,700,700,700,700,700,700,700,700] #fruits start at the bottom of the screen (further than 600, the total height)
        #randomises the vertical speed of the fruit between the ranges of low and high defined above
        canvas.data.vy=[random.randint(low,high),
                    random.randint(low,high),
                    random.randint(low,high),
                    random.randint(low,high),
                    random.randint(low,high),
                    random.randint(low,high),
                    random.randint(low,high),
                    random.randint(low,high),
                    random.randint(low,high),
                    random.randint(low,high)]
        
    #dividing the current time which is sec by a number (canvas.data.counterDelay), would mean that this coundition will be true
    #only when it is divisable by counterDelay, in this manner if we assumed that canvas.data.counterDelay = 3, thus the function
    #will be excuted every three seconds (divisble by 3), thus the letter will change ever three seconds        
    if canvas.data.gameOver!=False:
        if canvas.data.ss % canvas.data.counterDelay == 0:
            for i in range(len(canvas.data.t)):
                if len(canvas.data.letters) == 0:
                    #randomises the letters that appear on the fruit
                    canvas.data.letters= list(string.ascii_lowercase)
                    random.shuffle(canvas.data.letters)
                    canvas.data.t[i]=random.choice(canvas.data.letters)
                else:
                    random.shuffle(canvas.data.letters)
                    canvas.data.t[i]=random.choice(canvas.data.letters)
    #at the end of the game the letters disappear
    else:
        for i in range(len(canvas.data.t)):
            canvas.data.t[i]=""
                
            
    # time passed since the last execution of the timer
    dt = currentTime - previousTime

    #ends the game when 60 seconds pass
    if currentTime - canvas.data.startTime > 60:
        canvas.data.gameOver= False

    #creates the explosion of the fruits when the correct letter is typed
    if canvas.data.gameOver == True:    
        if canvas.data.draw == True and canvas.data.boom<70:
                canvas.data.boom+=7               
        else:
            canvas.data.draw= False
            
        #creates the up and down movements of the new fruits that appear on the screen
        for i in range(len(canvas.data.y)):
            #when the fruits reach the top of the screen, they fall back down
            if canvas.data.y[i]<=100:
                canvas.data.vy[i]*=-1
                canvas.data.y[i]-=canvas.data.vy[i]
            else :
                canvas.data.y[i]-=canvas.data.vy[i]
            #when a fruit goes below 700 vertically, it comes back up    
            if canvas.data.y[i]> 700:
                canvas.data.vy[i]*=-1
                canvas.data.y[i]-=canvas.data.vy[i]
            else :
                canvas.data.y[i]-=canvas.data.vy[i]

            if canvas.data.r[i]==True:
                canvas.data.x[i]-=canvas.data.vx[i]
                #fixes the issue of fruits getting stuck on the corners of the screen
                if canvas.data.x[i]<= 0:
                    canvas.data.x[i]=50
                    canvas.data.r[i]=False
            else:
                canvas.data.x[i]+=canvas.data.vx[i]
                #fixes the issue of fruits getting stuck on the corners of the screen
                if canvas.data.x[i]>800:
                    canvas.data.x[i]= 750
                    canvas.data.r[i]=True
            
    # update the view
    redrawAll()
    # schedule the next call to timerFired
    canvas.after(40, timerFired, currentTime)
def background():
        canvas.create_rectangle(800,600,0,0,fill="#715A3B")
        #inner vertical lines
        for i in range(170,315,5):
            canvas.create_line(i,400-6,i,0,fill="#624724",width=2.5)
        for i in range(170,315,5):
            canvas.create_line(i,400+6,i,600,fill="#624724",width=2.5)
        for i in range(0,155,5):
            canvas.create_line(i,200+6,i,600,fill="#624724",width=2.5)
        for i in range(0,155,5):
            canvas.create_line(i,200-6,i,0,fill="#624724",width=2.5)
        for i in range(330,475,5):
            canvas.create_line(i,600,i,0,fill="#624724",width=2.5)
        for i in range(490,635,5):
            canvas.create_line(i,600,i,0,fill="#624724",width=2.5)
        for i in range(650,800,5):
            canvas.create_line(i,300+6,i,600,fill="#624724",width=2.5)
        for i in range(650,800,5):
            canvas.create_line(i,300-6,i,0,fill="#624724",width=2.5)
        
        if canvas.data.gameOver!=False:
            canvas.create_text(400,130,text="FRUIT NINJA",font=("Helvetica",90),fill="#715A3B",state=DISABLED)
        else:
            canvas.create_text(400,130,text="FRUIT NINJA",font=("Helvetica",90),fill="darkgreen",state=DISABLED)
        #vertical lines
        canvas.create_line(160,0,160,600,fill="#624724",width=12)
        canvas.create_line(160,0,160,600,fill="#46390E",width=4)
        canvas.create_line(160*2,0,160*2,600,fill="#624724",width=12)
        canvas.create_line(160*2,0,160*2,600,fill="#46390E",width=4)
        canvas.create_line(160*3,0,160*3,600,fill="#624724",width=12)
        canvas.create_line(160*3,0,160*3,600,fill="#46390E",width=4)
        canvas.create_line(160*4,0,4*160,600,fill="#624724",width=12)
        canvas.create_line(160*4,0,160*4,600,fill="#46390E",width=4)
        canvas.create_line(160*5,0,160*5,600,fill="#624724",width=12)
        canvas.create_line(160*5,0,160*5,600,fill="#46390E",width=4)
        #horizontal lines
        canvas.create_line(0,200,158,200,fill="#624724",width=12)
        canvas.create_line(0,200,160,200,fill="#46390E",width=4)
        canvas.create_line(164,400,158*2,400,fill="#624724",width=12)
        canvas.create_line(160,400,160*2,400,fill="#46390E",width=4)
        canvas.create_line(161*4,300,159*5,300,fill="#624724",width=12)
        canvas.create_line(160*4,300,160*5,300,fill="#46390E",width=4)
        #first 6 circles
        canvas.create_oval(36,200-25,44,200-15,fill="#554724",outline="")
        canvas.create_oval(76,200-25,84,200-15,fill="#46390E",outline="")
        canvas.create_oval(116,200-25,124,200-15,fill="#554724",outline="")
        canvas.create_oval(36,200+25,44,200+15,fill="#46390E",outline="")
        canvas.create_oval(76,200+25,84,200+15,fill="#46390E",outline="")
        canvas.create_oval(116,200+25,124,200+15,fill="#554724",outline="")
        #second 6 circles
        canvas.create_oval(200-4,400-25,200+4,400-15,fill="#46390E",outline="")
        canvas.create_oval(240-4,400-25,240+4,400-15,fill="#554724",outline="")
        canvas.create_oval(280-4,400-25,280+4,400-15,fill="#554724",outline="")
        canvas.create_oval(200-4,400+25,200+4,400+15,fill="#46390E",outline="")
        canvas.create_oval(240-4,400+25,240+4,400+15,fill="#554724",outline="")
        canvas.create_oval(280-4,400+25,280+4,400+15,fill="#46390E",outline="")
        #third 6 circles
        canvas.create_oval(760-4,300-25,760+4,300-15,fill="#46390E",outline="")
        canvas.create_oval(680-4,300-25,680+4,300-15,fill="#46390E",outline="")
        canvas.create_oval(720-4,300-25,720+4,300-15,fill="#554724",outline="")
        canvas.create_oval(720-4,300+25,720+4,300+15,fill="#46390E",outline="")
        canvas.create_oval(680-4,300+25,680+4,300+15,fill="#554724",outline="")
        canvas.create_oval(760-4,300+25,760+4,300+15,fill="#46390E",outline="")


# Redraws the view
def redrawAll():
    canvas.delete(ALL) # clean up the view
    currentTime = time.time()
    canvas.data.sec=currentTime-canvas.data.startTime
    canvas.data.minute=0
    canvas.data.ss=60 - int(canvas.data.sec % 60)

    background()
     
    if canvas.data.gameOver!=False:
        canvas.create_text(20,20,text= str(canvas.data.minute) +" : "+str(canvas.data.ss),
                          fill="white",font=("Helvetica",30),
                          anchor=NW)
    else:
        canvas.create_text(20,20,text= "0: 00",fill="white",font=("Helvetica",30),anchor=NW)

    if canvas.data.gameOver!=False:
        for i in range(len(canvas.data.x)):
            if canvas.data.fruits[i]=="apple":  
                canvas.create_oval(canvas.data.x[i]-30,canvas.data.y[i]-30,canvas.data.x[i]+30,canvas.data.y[i]+40,fill="lightgreen",outline="")
                canvas.create_oval(canvas.data.x[i]-10,canvas.data.y[i]-30,canvas.data.x[i]+50,canvas.data.y[i]+40,fill="lightgreen",outline="")
                canvas.create_arc(canvas.data.x[i],canvas.data.y[i]-30,canvas.data.x[i]+15,canvas.data.y[i]-50,fill="#8A5D2C",outline="",start=120,extent=180)
                canvas.create_arc(canvas.data.x[i]-20,canvas.data.y[i]+20,canvas.data.x[i],canvas.data.y[i]-20,style=PIESLICE,fill="white",outline="",start=90)
                canvas.create_text(canvas.data.x[i]+10,canvas.data.y[i]+8,text=str(canvas.data.t[i]),font=("Helvetica",36))

            if canvas.data.fruits[i]=="strawberry":
                canvas.create_arc(canvas.data.x[i]-60,canvas.data.y[i]-60,canvas.data.x[i]+55,canvas.data.y[i]+120,fill="red",outline="",style=PIESLICE,start=45)
                canvas.create_oval(canvas.data.x[i]-20,canvas.data.y[i]-30,canvas.data.x[i]-30,canvas.data.y[i]-40,fill="yellow",outline="")
                canvas.create_oval(canvas.data.x[i]-5,canvas.data.y[i]-30,canvas.data.x[i]-15,canvas.data.y[i]-40,fill="yellow",outline="")
                canvas.create_oval(canvas.data.x[i]+10,canvas.data.y[i]-30,canvas.data.x[i],canvas.data.y[i]-40,fill="yellow",outline="")
                canvas.create_oval(canvas.data.x[i]+25,canvas.data.y[i]-30,canvas.data.x[i]+15,canvas.data.y[i]-40,fill="yellow",outline="")
                canvas.create_oval(canvas.data.x[i]-5,canvas.data.y[i]-45,canvas.data.x[i]-15,canvas.data.y[i]-55,fill="yellow",outline="")
                canvas.create_oval(canvas.data.x[i]+10,canvas.data.y[i]-45,canvas.data.x[i],canvas.data.y[i]-55,fill="yellow",outline="")
                canvas.create_rectangle(canvas.data.x[i],canvas.data.y[i]-60,canvas.data.x[i]-5,canvas.data.y[i]-75,fill="#8A5D2C",outline="")
                canvas.create_arc(canvas.data.x[i]-15,canvas.data.y[i]-60,canvas.data.x[i],canvas.data.y[i]-80,fill="darkgreen",outline="",start=120,extent=180)
                canvas.create_text(canvas.data.x[i]-2,canvas.data.y[i]-7,text=str(canvas.data.t[i]),font=("Helvetica",36))

            if canvas.data.fruits[i]=="orange":
                canvas.create_oval(canvas.data.x[i]-35,canvas.data.y[i]-35,canvas.data.x[i]+35,canvas.data.y[i]+35,fill="orange",outline="")
                canvas.create_arc(canvas.data.x[i]-27,canvas.data.y[i]+20,canvas.data.x[i]-5,canvas.data.y[i]-22,style=PIESLICE,fill="yellow",outline="",start=90)
                canvas.create_text(canvas.data.x[i]+3,canvas.data.y[i]+3,text=str(canvas.data.t[i]),font=("Helvetica",36))
                canvas.create_arc(canvas.data.x[i]-10,canvas.data.y[i]-35,canvas.data.x[i]+5,canvas.data.y[i]-55,fill="darkgreen",outline="",start=120,extent=180)

            if canvas.data.fruits[i]=="banana":
                canvas.create_arc(canvas.data.x[i]-80,canvas.data.y[i]-20,canvas.data.x[i]+120,canvas.data.y[i]+20,fill="yellow",outline="",style=CHORD,extent=200,start=130)
                canvas.create_text(canvas.data.x[i],canvas.data.y[i],text=str(canvas.data.t[i]),font=("Helvetica",36))
                canvas.create_rectangle(canvas.data.x[i]-54,canvas.data.y[i],canvas.data.x[i]-44,canvas.data.y[i]-20,fill="yellow",outline="")

            if canvas.data.fruits[i]=="watermelon":
                canvas.create_oval(canvas.data.x[i]-70,canvas.data.y[i]-40,canvas.data.x[i]+70,canvas.data.y[i]+40,fill="lightgreen",outline="darkgreen",width=3)
                canvas.create_arc(canvas.data.x[i]-61,canvas.data.y[i],canvas.data.x[i]+60,canvas.data.y[i]+30,fill="darkgreen",outline="#7FC567",style=CHORD,start=180,extent=180,width=2)
                canvas.create_arc(canvas.data.x[i]-60,canvas.data.y[i]-30,canvas.data.x[i]+61,canvas.data.y[i],fill="darkgreen",outline="#7FC567",style=CHORD,extent=180,width=2)
                canvas.create_rectangle(canvas.data.x[i]-67,canvas.data.y[i]-8,canvas.data.x[i]+67,canvas.data.y[i]+8,fill="#7FC567",outline="")
                canvas.create_rectangle(canvas.data.x[i]-65,canvas.data.y[i]-6,canvas.data.x[i]-15,canvas.data.y[i]+6,fill="darkgreen",outline="")
                canvas.create_rectangle(canvas.data.x[i]+15,canvas.data.y[i]-6,canvas.data.x[i]+65,canvas.data.y[i]+6,fill="darkgreen",outline="")
                canvas.create_text(canvas.data.x[i],canvas.data.y[i]+3,text=str(canvas.data.t[i]),font=("Helvetica",36))

            if canvas.data.fruits[i]=="pear":
                canvas.create_rectangle(canvas.data.x[i]-23,canvas.data.y[i],canvas.data.x[i]-17,canvas.data.y[i]-75,fill="#8A5D2C",outline="")
                canvas.create_oval(canvas.data.x[i]-55,canvas.data.y[i]-30,canvas.data.x[i],canvas.data.y[i]+30,fill="#E5C945",outline="")
                canvas.create_oval(canvas.data.x[i]-40,canvas.data.y[i]-30,canvas.data.x[i]+15,canvas.data.y[i]+30,fill="#E5C945",outline="")
                canvas.create_oval(canvas.data.x[i]-40,canvas.data.y[i],canvas.data.x[i],canvas.data.y[i]-60,fill="#E5C945",outline="")
                canvas.create_arc(canvas.data.x[i]-32,canvas.data.y[i]-10,canvas.data.x[i]-15,canvas.data.y[i]-50,fill="white",outline="",start=90,style=PIESLICE)
                canvas.create_text(canvas.data.x[i]-20,canvas.data.y[i],text=str(canvas.data.t[i]),font=("Helvetica",36))

            if canvas.data.fruits[i]=="bomb" and canvas.data.bomb == True:
                canvas.create_oval(canvas.data.x[i]-35,canvas.data.y[i]+35,canvas.data.x[i]+35,canvas.data.y[i]-35,fill="black")
                canvas.create_rectangle(canvas.data.x[i]-3,canvas.data.y[i]-43,canvas.data.x[i]+3,canvas.data.y[i],fill="black")
                canvas.create_arc(canvas.data.x[i],canvas.data.y[i]-43,canvas.data.x[i]+20,canvas.data.y[i]-57,style=ARC,fill="yellow",width=2,start=180,outline="yellow",extent=-150)
                canvas.create_oval(canvas.data.x[i]+15,canvas.data.y[i]-60,canvas.data.x[i]+20,canvas.data.y[i]-50,fill="orange",outline="")
                canvas.create_arc(canvas.data.x[i]-27,canvas.data.y[i]+20,canvas.data.x[i]-10,canvas.data.y[i]-22,style=PIESLICE,fill="white",outline="",start=90)
                canvas.create_text(canvas.data.x[i]+3,canvas.data.y[i]+3,text=str(canvas.data.t[i]),font=("Helvetica",36),fill="white")
            
            if canvas.data.fruits[i]=="special" and canvas.data.special==True :
                canvas.create_oval(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#FF00FF",outline="")
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#00FFFF",style=CHORD,start=45,outline="",extent=270)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="green",style=CHORD,start=67.5,outline="",extent=225)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="yellow",style=CHORD,start=90,outline="",extent=180)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="orange",style=CHORD,start=110.5,outline="",extent=137)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="red",style=CHORD,start=135,outline="",extent=90)
                canvas.create_text(canvas.data.x[i],canvas.data.y[i],text=str(canvas.data.t[i]),font=("Helvetica",36))

            if canvas.data.fruits[i]=="special2" and canvas.data.special2==True :
                canvas.create_oval(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#FF0000",outline="")
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#FF4200",style=CHORD,start=45,outline="",extent=270)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#FF6B00",style=CHORD,start=67.5,outline="",extent=225)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#FF9A00",style=CHORD,start=90,outline="",extent=180)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#FFB800",style=CHORD,start=110.5,outline="",extent=137)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#FFDB00",style=CHORD,start=135,outline="",extent=90)
                canvas.create_text(canvas.data.x[i],canvas.data.y[i],text=str(canvas.data.t[i]),font=("Helvetica",36))

            if canvas.data.fruits[i]=="special3" and canvas.data.special3==True :
                canvas.create_oval(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#000000",outline="")
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#414144",style=CHORD,start=45,outline="",extent=270)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#626061",style=CHORD,start=67.5,outline="",extent=225)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#797978",style=CHORD,start=90,outline="",extent=180)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#999A99",style=CHORD,start=110.5,outline="",extent=137)
                canvas.create_arc(canvas.data.x[i]-40,canvas.data.y[i]-40,canvas.data.x[i]+40,canvas.data.y[i]+40,fill="#BDBCBB",style=CHORD,start=135,outline="",extent=90)
                canvas.create_text(canvas.data.x[i],canvas.data.y[i],text=str(canvas.data.t[i]),font=("Helvetica",36))
    else:
        canvas.create_oval(114-30,500-30,114+30,500+40,fill="lightgreen",outline="")
        canvas.create_oval(114-10,500-30,114+50,500+40,fill="lightgreen",outline="")
        canvas.create_arc(114,500-30,114+15,500-50,fill="#8A5D2C",outline="",start=120,extent=180)
        canvas.create_arc(114-20,500+20,114,500-20,style=PIESLICE,fill="white",outline="",start=90)
        canvas.create_arc(213-60,500-60,213+55,500+120,fill="red",outline="",style=PIESLICE,start=45)
        canvas.create_oval(213-20,500-30,213-30,500-40,fill="yellow",outline="")
        canvas.create_oval(213-5,500-30,213-15,500-40,fill="yellow",outline="")
        canvas.create_oval(213+10,500-30,213,500-40,fill="yellow",outline="")
        canvas.create_oval(213+25,500-30,213+15,500-40,fill="yellow",outline="")
        canvas.create_oval(213-5,500-45,213-15,500-55,fill="yellow",outline="")
        canvas.create_oval(213+10,500-45,213,500-55,fill="yellow",outline="")
        canvas.create_rectangle(213,500-60,213-5,500-75,fill="#8A5D2C",outline="")
        canvas.create_arc(213-15,500-60,213,500-80,fill="darkgreen",outline="",start=120,extent=180)
        canvas.create_oval(294-35,500-35,294+35,500+35,fill="orange",outline="")
        canvas.create_arc(294-27,500+20,294-5,500-22,style=PIESLICE,fill="yellow",outline="",start=90)
        canvas.create_arc(294-10,500-35,294+5,500-55,fill="darkgreen",outline="",start=120,extent=180)
        canvas.create_arc(408-80,500-20,408+120,500+20,fill="yellow",outline="",style=CHORD,extent=200,start=130)
        canvas.create_rectangle(408-54,500,408-44,500-20,fill="yellow",outline="")
        canvas.create_oval(553-70,500-40,553+70,500+40,fill="lightgreen",outline="darkgreen",width=3)
        canvas.create_arc(553-61,500,553+60,500+30,fill="darkgreen",outline="#7FC567",style=CHORD,start=180,extent=180,width=2)
        canvas.create_arc(553-60,500-30,553+61,500,fill="darkgreen",outline="#7FC567",style=CHORD,extent=180,width=2)
        canvas.create_rectangle(553-67,500-8,553+67,500+8,fill="#7FC567",outline="")
        canvas.create_rectangle(553-65,500-6,553-15,500+6,fill="darkgreen",outline="")
        canvas.create_rectangle(553+15,500-6,553+65,500+6,fill="darkgreen",outline="")
        canvas.create_rectangle(685-23,500,685-17,500-75,fill="#8A5D2C",outline="")
        canvas.create_oval(685-55,500-30,685,500+30,fill="#E5C945",outline="")
        canvas.create_oval(685-40,500-30,685+15,500+30,fill="#E5C945",outline="")
        canvas.create_oval(685-40,500,685,500-60,fill="#E5C945",outline="")
        canvas.create_arc(685-32,500-10,685-15,500-50,fill="white",outline="",start=90,style=PIESLICE)
        
    if canvas.data.draw== True:
        canvas.create_oval(canvas.data.boomx+canvas.data.boom,
                            canvas.data.boomy+canvas.data.boom,
                            canvas.data.boomx-canvas.data.boom,
                            canvas.data.boomy-canvas.data.boom,fill="white")
    canvas.create_text(750,20,text="Score = "+ str(canvas.data.points),font=("Helvetica",25), anchor=NE, fill="white")
    canvas.create_text(750,50,text="Points for Level "+str(canvas.data.level+1)+"="+str(canvas.data.maxPoints[canvas.data.level-1]), anchor=NE, fill="white",font=("Helvetica",25))


    if canvas.data.gameOver==False:
        canvas.create_text(400,220,text="Game Over",font=("Helvetica",50),fill="white")
        canvas.create_text(400,300,text="YOU REACHED LEVEL "+str(canvas.data.level)+"!!!",font=("Helvetica",60),fill="white")

    if canvas.data.lines == True:
        for i in range(20):
            canvas.create_line(0,30*i,800,30*i,fill="white",width=3)

# Creates the initial state of the model
# Put all the state variables inside canvas.data
def init():
    
    canvas.data.fruits=["apple","strawberry",
                        "orange","banana",
                        "watermelon","pear",
                        "bomb","special","special2","special3"] 
    #x-coordinates
    canvas.data.x=[random.randint(0,800),
                   random.randint(0,800),
                   random.randint(0,800),
                   random.randint(0,800),
                   random.randint(0,800),
                   random.randint(0,800),
                   random.randint(0,800),
                   random.randint(0,800),
                   random.randint(0,800),
                   random.randint(0,800)]
    
    #y-coordinates
    canvas.data.y=[700,700,700,700,700,700,700,700,700,700]
    #y-velocity coordinates
    canvas.data.vy=[random.randint(5,10),
                    random.randint(5,10),
                    random.randint(5,10),
                    random.randint(5,10),
                    random.randint(5,10),
                    random.randint(5,10),
                    random.randint(5,10),
                    random.randint(5,10),
                    random.randint(5,10),
                    random.randint(5,10)]
    #x-velocity coordinates
    canvas.data.vx=[5,5,5,5,5,5,5,5,5,5]
    #letters
    
    canvas.data.letters= list(string.ascii_lowercase)

    canvas.data.t=[] 
    for i in range(len(canvas.data.x)):
        random.shuffle(canvas.data.letters)
        canvas.data.t.append(random.choice(canvas.data.letters))
        #del canvas.data.letters[0]
    
    canvas.data.r=[]
    canvas.data.boom=5
    canvas.data.draw= None
    canvas.data.startTime=time.time()
    canvas.data.gameOver= True
    canvas.data.sec=0
    canvas.data.minute=1
    canvas.data.ss=0
    canvas.data.counter=5
    canvas.data.points=0
    canvas.data.counterDelay = 10
    canvas.data.maxPoints=[200,175,150,125,100,75,50,25]
    canvas.data.level = 1
    canvas.data.start=0
    canvas.data.special=False
    canvas.data.special2=False
    canvas.data.special3=False
    canvas.data.bomb=False
    canvas.data.bombTime= random.randint(0,60)
    canvas.data.specialTime=random.randint(0,60)
    canvas.data.specialTime2=random.randint(0,60)
    canvas.data.specialTime3=random.randint(0,60)
    canvas.data.lines = False
    
    

    pass

def run():
    # create root and canvas
    global canvas
    root = Tk()
    canvas = Canvas(root, width=800, height=600, bg="white")
#    canvas2 = Canvas(root, width=800, height=300, bg="blue")
    canvas.pack()
#    canvas2.pack()
    # store canvas in root and canvas itself
    root.canvas = canvas.canvas = canvas
 #   root.canvas2 = canvas2.canvas2 = canvas2
    # set up a structure to store the model
    class MyModel: pass
    canvas.data = MyModel()
#    canvas2.data= MyModel()
    init()
    
    for i in range(len(canvas.data.x)):
        if canvas.data.x[i]>=400:
            canvas.data.r.append(True)
        else:
            canvas.data.r.append(False)
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    # start the timer
    timerFired(time.time())
    # start the main loop
    root.mainloop()

run()

