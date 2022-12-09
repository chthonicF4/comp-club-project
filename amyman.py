import math

BASES = { 
    130:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/¬`!£$%^&*()_-+={[}]:;@'~#<,>.?|αβγδεζηθικλμνξοπρςστυφχψωΓΔΘΛΞΠΣΦΨΩ",
    64:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
    16:"0123456789abcdef",
    10:"0123456789",
    2:"01",
    3:"012",
    4:"0123",
    5:"01234",
    36:"0123456789abcdefghijklmnopqrstuvwxyz",
    32:"0123456789abcdefghijklmnopqrstuv",
    30:"0123456789abdcefghijklmnopqrst"
}
def IntToBase(int,base):
    int2= int
    out = ""
    numberOfChar = math.ceil(math.log(int,base))
    for power in range(numberOfChar-1,-1,-1):
        powerValue = math.floor(int/(base**power))
        out += (BASES[base][powerValue])
        int += 0 - powerValue*(base**power)
    for x in out :
        if x != "0" :
            break
        out = out[1:]
    perc = 100 - (len(out)*1000//len(str(int2))*1000)//10000
    print(out,f"\n{perc}% reduction")
    return out

def BaseToInt(str,base):
    power = len(str) - 1 
    out = 0
    for char in str :
        out += (BASES[base].index(char))*(base**power)
        power += 0-1
    print(out)
    return out

base = 30
num = BaseToInt("111",base)
