import socket , pickler , threading , IP4hash
import tkinter as tk
from colours import c as colr
from colours import colrP

# colour presets
C_input = colrP(fg="cyan",ut="bold")
C_wrng = colrP(fg="lightred",ut="bold")
C_out = colrP(fg="blue")
C_Imprtnt = colrP(fg="yellow",ut=["bold","underline"])

def getHost():
    global HOST
    try:
        HOST = IP4hash.decode(str(input(colr("HOST>> ",cps=C_input))))
    except:
        print(colr("Invalid Code, please enter a valid input",cps=C_wrng))
        HOST = getHost()
    return HOST
HOST = getHost()
PORT = 50505
nickname = str(input(colr("name>> ",cps=C_input)))
WIDTH = 500
HEIGHT = 500
windoExsist = True
coordChange = [0,0]
chatQ = []

def networking() :
    global chatQ
    with socket.socket(socket.AF_INET) as sock :
        #attempt connection
        colours = ["red","orange","yellow","green","blue","purple","pink","black","white"]
        for index,colour in enumerate(colours) :
            print(f"[{index}] : '{colour}' ,",end="")
        print("")
        colour = colours[int(input(f"choose a colour (0-{len(colours)}) : "))]
        try :
            print(colr("\nattempting connection..",cps=C_out))
            sock.connect((HOST,PORT))
        except:
            print(colr("Failed connection, exiting",cps=C_wrng))  
            exit()
            return
        print(colr("Connection made to server",cps=C_out))  
        #------
        print(colr("talking to server..",cps=C_out))
        try:
            pickler.send([nickname,colour],sock)
            metaData = pickler.recv(sock)
        except:
            print(colr("No response from server, exiting",cps=C_wrng))  
            exit()
        
        global WIDTH , HEIGHT
        WIDTH , HEIGHT = metaData[0]
        global root
        root.geometry(f"{WIDTH}x{HEIGHT}")
        global coordChange
        print(colr("Starting main loop",cps=C_out))
        prevpx = []
        while windoExsist ==True :
            try:
                data = pickler.recv(sock)
            except socket.error :
                break
            if data :
                # when coord change is requested
                if data[0] == "ccng" :
                    pickler.send(["ccgd",coordChange],sock)
                    coordChange = [0,0]
                # when told to quit
                if data[0] == "quit" :
                    break
                #when recived chat msg
                if data[0] == "rcch" :
                    print(data[1])
                # when told to send queued chat msgs
                if data[0] == "rqch" :
                    pickler.send(["rcch",chatQ],sock)
                    chatQ = []
                #when recived player postitons
                if data[0] == "ppdt" :
                    print(data[1])
                    for pxl in prevpx :
                        Canvas.delete(pxl)
                    prevpx = []
                    #procces data
                    for client in data[1] :
                        prevpx.append(pixle(client[0],client[1][1])) 


            pass
        # exit protocol
        sock.close()
        print(colr("dissconected",cps=C_wrng))
    exit()
    return

def pixle(coords,colour):
    x , y = coords
    shape = Canvas.create_rectangle(x-1,y+2,x+1,y-1,fill=colour,outline=colour)
    return shape


networkThread = threading.Thread(target=networking,args=())
networkThread.start()
# key press functions

def onKeyPress(event):
    speed = 0.5
    if event.char == "w" :
        coordChange[1] += 0-speed
    elif event.char == "s" :
        coordChange[1] += speed
    elif event.char == "a" :
        coordChange[0] += 0-speed
    elif event.char == "d" :
        coordChange[0] += speed
    pass

# exit protocol
def exit():
    root.destroy()
    root.quit()

def onClose() :
    global windoExsist
    windoExsist = False
    exit()

# window init
root = tk.Tk(className=f" ROOM {PORT}")
root.geometry(f"{WIDTH}x{HEIGHT}")
Canvas = tk.Canvas(width=WIDTH,height=HEIGHT,bg="grey")
Canvas.pack()
root.bind("<Key>", onKeyPress)
windoExsist = True
root.protocol("WM_DELETE_WINDOW", onClose)
root.mainloop()
print(colr("You can now close this window",cps=C_Imprtnt))
