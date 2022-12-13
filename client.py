# import custom modules from lib folder as well as other basic modules

import socket , lib.pickler as pickler , threading , lib.IP4hash as IP4hash , tkinter as tk
from lib.colours import c as colr , colrP
from lib.personDrawer import *

# colour presets

C_input = colrP(fg="cyan",ut="bold")
C_wrng = colrP(fg="lightred",ut="bold")
C_out = colrP(fg="blue")
C_Imprtnt = colrP(fg="yellow",ut=["bold","underline"])

# Global variables ----------

    #networking vars

HOST = IP4hash.getHost()
PORT = 50505
chatQ = []
nickname = str(input(colr("name>> ",cps=C_input)))

    #window vars

WIDTH = 500
HEIGHT = 500

windoExsist = True

    #client data

colours = ["red","orange","yellow","green","blue","purple","pink","black","white"]
for index,colour in enumerate(colours) :
    print(f"[{index}] : '{(colour)}'")
print("")
colour = colours[int(input(f"choose a colour (0-{len(colours)}) : "))]
coordChange = [0,0]

# --------------------------

#NETWORKING FUCTIONS

def networking() :
    #globals 
    global WIDTH , HEIGHT , root , coordChange , chatQ
    # start socket 
    with socket.socket(socket.AF_INET) as sock :

        #attempt connection

        try :
            print(colr("\nattempting connection..",cps=C_out))

            sock.connect((HOST,PORT)) # acctual bit of code connecting to the server
        
        except:
            # this will get trigered if the connection fails
            print(colr("Failed connection, exiting",cps=C_wrng))  
            exit()
            return
        print(colr("Connection made to server",cps=C_out))  
        
        # when connection has been made
        
        print(colr("talking to server..",cps=C_out))

        # try and send metadata (client nicname and what colour they chose)
        # then recive meta data from server about config (window size)
        try:
            pickler.send([nickname,colour],sock)
            metaData = pickler.recv(sock)
        except:
            # if server dosent respond exit 
            print(colr("No response from server, exiting",cps=C_wrng))  
            exit()

        # set window dimention vars to recived data and then set the size

        WIDTH , HEIGHT = metaData[0]
        root.geometry(f"{WIDTH}x{HEIGHT}")

        # start the mainloop of message reciving and sending
        print(colr("Starting main loop",cps=C_out))
        prevpx = []

        while windoExsist ==True :
            # try and recive messages from server
            try:
                data = pickler.recv(sock)
            except socket.error :
                # if get a dissconect error , exit loop
                break
            
            # ---- NETWORK FLAGS -------
            #
            # coord change 
            #   ccng : server is requesting the change in coords
            #   ccgd : tells server the message is the coord change data
            # 
            # chat 
            #   rcch : is a chat msg so needs to be brodcast
            #   rqch : request chat msgs
            #
            # misc
            #   quit : tells client to exit the connection
            #   ppdt : position data
            #             
            
            #if data is recived 

            if data :

                # when coord change is requested
                if data[0] == "ccng" :
                    # send over the coord change and clear it
                    pickler.send(["ccgd",coordChange],sock)
                    coordChange = [0,0]
                
                # when told to quit , just quit yk?
                elif data[0] == "quit" :
                    break
                    
                #when recived chat msg
                elif data[0] == "rcch" :
                    # print out the chat msg
                    print(data[1])

                # when told to send queued chat msgs
                elif data[0] == "rqch" :
                    # send over the chat queue
                    pickler.send(["rcch",chatQ],sock)
                    chatQ = []

                #when recived clients postitons , draw the clients
                elif data[0] == "ppdt" :
                    # delete previous clients
                    for pxl in prevpx :
                        Canvas.delete(pxl)
                    prevpx = []
                    # draw the new clients 
                    for client in data[1] :
                        prevpx.append(pixle(Canvas,client[0],client[1][1])) 
                        prevpx.append(text(Canvas,client[0],client[1][0]))


        # when the mainloop is broken close the connection 
        sock.close()
        print(colr("dissconected",cps=C_wrng))

    # call the exit function
    exit()

    # end thread
    return

def chat():
    # takes in chat mesages to be sent and adds them to the chat queue
    while windoExsist == True :
        msg = str(input(">>"))
        chatQ.append(msg)

# key press functions

def onKeyPress(event):
    # monitors keys that are pressed and alters the coordChange var acordingly
    speed = 2
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
    # closes the window and sets the windowExsist var to False
    
    windoExsist = False
    
    try:
        # closes window
        root.destroy()
        #ends the window mainloop
        root.quit()
    except :
        pass

#THREADS

networkThread = threading.Thread(target=networking,args=())
networkThread.start()
chatThread = threading.Thread(target=chat)
#chatThread.start()

# window init

    # root setup

root = tk.Tk(className=f" ROOM {PORT}")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.bind("<Key>", onKeyPress)
root.protocol("WM_DELETE_WINDOW", exit)

    # canvas setup

Canvas = tk.Canvas(width=WIDTH,height=HEIGHT,bg="grey")
Canvas.pack()

    # set window exist to TRUE

windoExsist = True

    # start window mainloop

root.mainloop()

# when window mainloop is exited

print(colr("You can now close this window",cps=C_Imprtnt))
