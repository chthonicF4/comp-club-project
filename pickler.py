import pickle
import time

def send(str,conn):
    msg = pickle.dumps(str)
    conn.send(msg)
    time.sleep(0.01)
    return msg

def recv(conn):
    Pmsg = conn.recv(1024)
    if Pmsg :
        msg = pickle.loads(Pmsg)
        return msg
    return None