import socket , os , threading , pickler , IP4hash
from datetime import datetime
import tkinter as tk
from time import sleep
from colours import c as colr
from colours import colrP

# colour presets
C_input = colrP(fg="cyan",ut="bold")
C_wrng = colrP(fg="lightred",ut="bold")
C_out = colrP(fg="blue")
C_Imprtnt = colrP(fg="yellow",ut=["bold","underline"])


HOST = socket.gethostbyname(socket.gethostname())
PORT = 50505
WIDTH = 500
HEIGHT = 500
Shutdown = False

def log_init_() :
    try:
        os.mkdir("logs")
    except:
        pass
    count = 0
    date = datetime.now().strftime("%D").replace("/",".")
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
    return datetime.now().strftime("[%D %H:%M:%S]")

def log(str) : 
    log = open(logFile,"a")
    log.write(f"\n{time()} {str}")
    log.close()

logFile = log_init_()

connections = []

def find(conn,connections):
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
    connections[index] = [conn,(0,0),nickname]
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
                    print(f"[{nickname}] {msg}")
                    brodcast(f"[{nickname}] {msg}")
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
        sleep(0.08)
        pass

    # exit protocol
    index = find(conn,connections)
    connections.pop(index)
    print(colr(f"{nickname} has dissconected",cps=C_out))
    log(f"{threading.current_thread().name} has dissconected")
    return

def brodcast(msg):
    log(f"brodcasting msg :{msg}")
    for conn in connections:
        pickler.send(msg,conn[0])
        sleep(0.08)

def draw():
    prevpix = []
    while Shutdown == False :
        sleep(0.5)
        # delete old stuff
        for thing in prevpix :
            c.delete(thing)
        # draw new stuff
        for client in connections:
            prevpix.append(pixle(client[1],client[2][1]))
            pass

def pixle(coords,colour):
    x , y = coords
    shape = c.create_rectangle(x-1,y+2,x+1,y-1,fill=colour,outline=colour)
    return shape

def networking():
    global connections
    name = (colr("server",cps=C_Imprtnt))
    with socket.socket(socket.AF_INET) as sock :
        sock.bind((HOST,PORT))
        log(f"server binded to {(HOST,PORT)}")
        print(f"{name} binded to {(HOST,PORT)}")
        log(f"server awaiting connections on {(HOST,PORT)}")
        print(f"{name} awaiting connections on {(HOST,PORT)}")
        print(colr(f"server code : {IP4hash.encode(HOST)}",cps=C_out))
        while Shutdown == False :
            sock.listen(1)
            conn,addr = sock.accept()
            if Shutdown == True :
                break
            log(f"server accepted connection from {addr}")
            print(colr(f"{name} accepted connection from {colr(addr,cps=C_input)}",cps=C_out))
            connections.append([conn])
            newThread  = threading.Thread(target=clientHandle,args=(addr,conn),name=f"{addr}")
            newThread.start()
        sock.close()
    return
                
# window init

root = tk.Tk(className=" ROOM PEEK - Server")
root.geometry(f"{WIDTH}x{HEIGHT}")
c = tk.Canvas(width=WIDTH,height=HEIGHT,master=root,bg="grey")
c.pack()

networkThread = threading.Thread(target=networking,args=())
networkThread.start()
drawingThread = threading.Thread(target=draw,args=())
drawingThread.start()

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

root.protocol("WM_DELETE_WINDOW", onClose)
root.mainloop()
print(colr("\nYou can now close this window",cps=C_Imprtnt))