

def mltply(a,b) :
    out = 0.0
    if a > b :
        for x in range(b): 
            out += a
        return out
    else :
        for x in range(a): 
            out += b
        return out

def sqr(a,b):
    out = a
    for x in range(b-1):
        out = mltply(out,a)
    return out

import colours

def Crmv(string):
    index = string.find("\033[")
    while index != -1 :
        # find end of thing
        end = index
        char = 0
        while char != "m" :
            char = string[end]
            end += 1
        string = string.replace(string[index:end],"")
        index = string.find("\033[")
    return string
