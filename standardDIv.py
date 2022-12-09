numbs = []

def getNumbs():
    try :
        numb = float(input(">"))
    except:
        return
    numbs.append(numb)
    getNumbs()

getNumbs()

SumXsqrd = 0.0
BarXsqrd = 0.0
n = len(numbs)

for numb in numbs :
    SumXsqrd += numb**2
    BarXsqrd += numb

BarXsqrd = (BarXsqrd/n)**2

varience = (SumXsqrd/n) - BarXsqrd
print(f"BAR x^2 = {BarXsqrd:0}\nσ^2 = {varience}")


