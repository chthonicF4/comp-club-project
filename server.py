import socket , lib.pickler as pickler , threading , lib.IP4hash as IP4hash , tkinter as tk , os
from lib.colours import c as colr , colrP , Crmv
from lib.personDrawer import *
from time import sleep
from datetime import datetime

# colour presets
C_input = colrP(fg="cyan",ut="bold")
C_wrng = colrP(fg="lightred",ut="bold")
C_out = colrP(fg="blue")
C_Imprtnt = colrP(fg="yellow",ut=["bold","underline"])

# constants and global variables

HOST = socket.gethostbyname(socket.gethostname())
PORT = 50505
WIDTH = 500
HEIGHT = 500
Shutdown = False
connections = []

# define and initiate logging functions

def log_init_() :
    # try make logs dir 
    try:
        os.mkdir("logs")
    except:
        pass
    count = 0
    date = datetime.now().strftime("%D").replace("/",".")

    # define function to make new log file so it can loop till it finds a valid name

    def make_file(count) : 
        file = f"logs/{date} ({count}).txt"
        try :
            temp = open(file,"x")
        except :
            return False
        temp.close()
        return file
    made = False
    while made == False :
        made = make_file(count)
        count += 1
    return made
    
def time() :
    # returns the current time
    return datetime.now().strftime("[%D %H:%M:%S]")

def log(str) : 
    # takes in a string , adds the time to it and saves it to the log file
    print(str)
    log = open(logFile,"a")
    log.write(f"\n{time()} {Crmv(str)}")
    log.close()

logFile = log_init_()

# define networking functions

def find(conn,connections):
    # finds a conn in a list and retrns the index
    for index , thing in enumerate(connections):
        if thing[0] == conn :
            return index 
    return None

def clientHandle(addr,conn):
    global connections
    log(f"server starting handle for {addr}")
    nickname = pickler.recv(conn)
    threading.current_thread().name = nickname[0]
    log(f"{addr} recved nickname '{nickname[0]}' , will now refer to thread as '{nickname[0]}'")
    log(f"{nickname[0]} : client chose colour '{nickname[1]}'")
    # send meta data
    pickler.send([(WIDTH,HEIGHT)],conn)
    # init conn data
    index = connections.index([conn])
    connections[index] = [conn,(WIDTH//2,HEIGHT//2),nickname]
    # network flags
    #
    # ccng : change in coords request
    # quit : tell client to exit
    # ccgd : coord change data from client
    # rcch : is a chat msg so needs to be brodcast
    # rqch : request chat msgs
    # ppdt : position data
    #
    # main loop
    while True :
        try:
            # get coord change 
            try :
                pickler.send(["ccng"],conn)
                change = pickler.recv(conn)
            except socket.error :
                break
            if change :
                if change[0] == "ccgd" :
                    if connections[index][0] != conn :
                        index = find(conn,connections)
                    current = connections[index][1]
                    connections[index][1] = (current[0] + change[1][0], current[1] + change[1][1])
                    pass
            # get queued chat msgs
            try : 
                pickler.send(["rqch"],conn)
                msgs = pickler.recv(conn)
            except socket.error :
                break
            if msgs :
                for msg in msgs[1] :
                    print(f"[{nickname[0]}] {msg}")
                    brodcast(f"[{nickname[0]}] {msg}")
            # send player postion data
            try: 
                data = []
                for client in connections:
                    try:
                        data.append((client[1],client[2]))
                    except:
                        pass
                pickler.send(["ppdt",data],conn)
            except socket.error :
                break
        except:
            break
        sleep(0.04)
        pass

    # exit protocol
    index = find(conn,connections)
    connections.pop(index)
    print(colr(f"{nickname[0]} has dissconected",cps=C_out))
    log(f"{threading.current_thread().name} has dissconected")
    return

def brodcast(msg):
    #  brodcasts a message to all conected clients
    log(f"brodcasting msg :{msg}")
    for conn in connections:
        pickler.send(msg,conn[0])
        sleep(0.08)

def networking():
    global connections
    name = (colr("server",cps=C_Imprtnt))
    with socket.socket(socket.AF_INET) as sock :
        sock.bind((HOST,PORT))
        log(f"{name} binded to {(HOST,PORT)}")
        log(f"{name} awaiting connections on {(HOST,PORT)}")
        print(colr(f"server code : {IP4hash.encode(HOST)}",cps=C_out))
        while Shutdown == False :
            sock.listen(1)
            conn,addr = sock.accept()
            if Shutdown == True :
                break
            log(colr(f"{name} accepted connection from {colr(addr,cps=C_input)}",cps=C_out))
            connections.append([conn])
            newThread  = threading.Thread(target=clientHandle,args=(addr,conn),name=f"{addr}")
            newThread.start()
        sock.close()
    return

# define graphics functions
def draw():
    prevpix = []
    while Shutdown == False :
        sleep(0.5)
        # delete old stuff
        for thing in prevpix :
            c.delete(thing)
        # draw new stuff
        for client in connections:
            try:
                prevpix.append(pixle(c,client[1],client[2][1]))
                prevpix.append(text(c,client[1],client[2][0]))
            except:
                pass


#  window setup

root = tk.Tk(className=" ROOM PEEK - Server")
root.geometry(f"{WIDTH}x{HEIGHT}")
c = tk.Canvas(width=WIDTH,height=HEIGHT,master=root,bg="grey")
c.pack()

def onClose() :
    global Shutdown
    print(colr("\nNow closing server",cps=C_wrng))
    log("server window closed, now closing server ")
    # shutdown threads
    print(colr("Shutting down threads",cps=C_out))
    Shutdown = True
    #stop listening
    try:
        with socket.socket(socket.AF_INET) as sock :
            sock.connect((HOST,PORT))
    except:
        pass
    #shutdown clients
    print(colr("Dissconecting clients",cps=C_out))
    brodcast(["quit"])
    #delete window
    print(colr("Destroying window",cps=C_out))
    root.destroy()
    #end main loop
    root.quit()
    log("server shutdown")

networkThread = threading.Thread(target=networking,args=())
networkThread.start()
drawingThread = threading.Thread(target=draw,args=())
drawingThread.start()


root.protocol("WM_DELETE_WINDOW", onClose)
root.mainloop()
print(colr("\nYou can now close this window",cps=C_Imprtnt))