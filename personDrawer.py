

def pixle(Canvas,coords,colour):
    x , y = coords
    shape = Canvas.create_rectangle(x-2,y+4,x+2,y-4,fill=colour,outline=colour)
    return shape

def text(Canvas,coords,text) :
    x,y = coords
    widgit = Canvas.create_text(x,y-8,text=text,fill="black",font=("arial",7))
    return widgit
