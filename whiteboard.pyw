import math, random, tkinter as tk, sys, functools, math, re
from tkinter import *
from tkinter import ttk
# A simple drawing tool in python!

# general utility variables & constants
COLORS = [["Red", "Blue", "Green", "Black"],["Orange", "Yellow", "Grey", "LightGrey"],["DarkGrey", "aqua", "olive", "brown"],["purple", "lightgreen", "skyblue", "pink"]]
isDrawing = False
myColor = "blue"
myWidth = 2
textvar = None
myTool = ""
prec = 100
x, y = [0, 0], [0,0]
req = 0 # keeps track of click actions for line tool
last_x, last_y=None,None
def setcolor(col):
    global myColor
    myColor = col
def pixelBrush(event, board):
    x1,y1=(event.x-1),(event.y-1)
    x2,y2=(event.x+1),(event.y+1)
    board.create_oval(x1,y1,x2,y2,fill=myColor,outline=myColor, width=myWidth)
def regBrush(event, board):
    global last_x, last_y
    global myWidth
    if isDrawing:
        x=event.x
        y=event.y
        board.create_line((last_x, last_y, x, y), fill=myColor, width=myWidth)
        last_x, last_y = x, y
def line(board):
    global myWidth, myColor, req, x, y
    board.create_line((x[0],y[0],x[1],y[1]), fill=myColor, width=myWidth)
def startReg(event):
    global isDrawing
    isDrawing = True
    global last_x, last_y
    last_x, last_y = event.x, event.y
def stopReg(event):
    global isDrawing
    isDrawing = False
def fill(b):
    b.configure(background=myColor)
def clear():
    return
def pencil(event):
    global myColor, myWidth
    x = event.x
    y = event.y
    canvas = event.widget
    for i in range(prec): # 100 is precision
        random_x,random_y = getSmear(x,y)
        canvas.create_line(random_x,random_y,random_x+1,random_y+1,fill=myColor)
def brush(event):
    global myColor, myWidth
    x = event.x
    y = event.y
    canvas = event.widget
    for i in range(prec): # 100 is precision
        random_x,random_y = getSmear1(x,y)
        canvas.create_line(random_x,random_y,random_x+1,random_y+1,fill=myColor)
def getSmear(x, y):
    global myWidth
    a = 2 * math.pi * random.random() # random angle measure
    r = random_radius= myWidth*math.sqrt(random.random())
    random_x = r*math.cos(a)+x
    random_y = r*math.sin(a)+y
    return random_x,random_y

def getSmear1(x, y):
    global myWidth
    a = 2 * math.pi * random.random() # random angle measure
    r = random_radius= myWidth*math.sqrt(random.random())
    random_x = r*math.cos(a)+x
    random_y = r*math.tan(a)+y
    return random_x,random_y
def initBrush(b, board):
    if b == 4:
        board.bind('<B1-Motion>', lambda event, arg=board: pixelBrush(event, board))
    if b == 1 or b == 5:
        global myColor
        if b == 5:
            myColor = 'white'
        board.bind("<Button-1>", startReg)
        board.bind("<ButtonRelease-1>", stopReg)
        board.bind("<B1-Motion>", lambda event, arg=board: regBrush(event, board))
    if b==2:
        board.bind('<B1-Motion>', pencil)
    if b==3:
        board.bind('<B1-Motion>', brush)
    if b==6:
        board.bind('<Button-1>', lambda event, arg=board: getcrds(event, board))
        board.bind('<Button-3>', lambda event, arg=board: getcrds(event, board))
def getcrds(event, board):
    global x, y, req
    if event.num == 1:
        x[0],y[0]=event.x,event.y
    else:
        x[1],y[1]=event.x,event.y
    req+=1
    if req == 2:
        req = 0
        line(board)
def init():
    root = Tk()
    root.title("Whiteboard")
    root.state('zoomed')
    initMenu(root)
    toolbar = Frame(root, width=200, height=750, background="aqua")
    board = Canvas(root, cursor="hand2", borderwidth=1, background="white")
    board.place(x=220, y=0, width=1500, height=1000)
    # have bind be an event of the button click
    toolbar.place(x=0, y=0)
    Label(toolbar,text="Select Color", font=("Arial", 20), foreground="olive", background="aqua").place(x=30, y=0)
    Label(toolbar,text="Select Tool", font=("Arial", 20), foreground="olive", background="aqua").place(x=30, y=250)
    Label(toolbar,text="Thickness", font=("Arial", 20), foreground="olive", background="aqua").place(x=30, y=500)
    b = ttk.Combobox(state="readonly",values=["1px","2px","5px","10px","15px","20px","30px","40px","50px","100px"])
    b.place(x=30, y=550)
    b.bind('<<ComboboxSelected>>',lambda event, arg=b: modif(event, b))    
    Button(toolbar, text="Marker", command=lambda:initBrush(1, board)).place(x=0, y=290, width=100)
    Button(toolbar, text="Spray", command=lambda:initBrush(2, board)).place(x=100, y=290, width=100)
    Button(toolbar, text="Fill", command=lambda:initBrush(3, board)).place(x=0, y=330, width=100)
    Button(toolbar, text="Brush", command=lambda:initBrush(4, board)).place(x=100, y=330, width=100)
    Button(toolbar, text="Eraser", command=lambda:initBrush(5, board)).place(x=0, y=370, width=100)
    Button(toolbar, text="Line", command=lambda:initBrush(6, board)).place(x=100, y=370, width=100)
    buttons = {}
    for i in range(1,5):
        for j in range(1, 5):
            Button(toolbar, background=getc(i, j), command=functools.partial(setcolor, col=COLORS[i-1][j-1])).place(x=35 * j, y = 35 * (i), width=30, height=30)
    Entry(toolbar) # custom rgb code
    root.mainloop()
def modif(event, b):
    global myWidth
    myWidth = b.get()
    if myWidth.endswith('px'):
        myWidth = int(myWidth[:-2])

def getc(i, j):
    return COLORS[i-1][j-1]
def q(root):
    root.destroy()
    sys.exit()
def togglebg():
    return
def initMenu(root):
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    optmenu = Menu(menubar, tearoff=0)
    helpmenu = Menu(menubar, tearoff=0)
    abmenu = Menu(menubar, tearoff=0)

    filemenu.add_command(label="Save Drawing")
    filemenu.add_command(label="Upload Image")



    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=lambda:q(root))


    optmenu.add_command(label="Clear")
    abmenu.add_command(label="About")


    helpmenu.add_command(label="How To Use")



    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Edit", menu=optmenu)
    menubar.add_cascade(label="Help", menu=helpmenu)
    menubar.add_cascade(label="About", menu=abmenu)
    root.config(menu=menubar)


if __name__ == '__main__':
    init()