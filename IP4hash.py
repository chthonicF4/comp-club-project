from colours import c as colr , colrP
C_wrng = colrP(fg="lightred",ut="bold")
C_input = colrP(fg="cyan",ut="bold")

def decode(code):
    IPout = "10."
    PORTout = None
    temp = ""
    if len(code) >6:
        PORTout = int("0x" + code[6:],16)
        code = code[:6]
    for char in code :
        temp += char
        if len(temp) == 2 : 
            IPout += str(int("0x"+temp,16)) + "."
            temp = ""
    IPout = IPout[:-1]
    if PORTout :
        return (IPout,PORTout)
    return IPout

def encode(IP,**kwargs):
    port = kwargs.get("port",None)
    #convert IP to hex list
    IP = IP[3:]
    list = []
    temp  = "" 
    for char in IP :
        if char != "." :
            temp += (char)
            continue
        list.append(hex(int(temp)))
        temp = ""
    list.append(hex(int(temp)))
    # combine 
    out = ""
    for num in list:
        num = num.replace("0x","")
        if len(num) != 2 :
            num = "0" + num
        out += num
    return out

def getHost():
    try:
        HOST = decode(str(input(colr("HOST>> ",cps=C_input))))
    except:
        print(colr("Invalid Code, please enter a valid input",cps=C_wrng))
        HOST = getHost()
    return HOST