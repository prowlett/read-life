from tkinter import * 
from tkinter.ttk import *
from random import randint
from time import sleep
from math import floor

# sleeptime = 0.1 # seconds between steps
sleeptime = 0.5

# Set up a big enough window and a canvas within this that we can draw on
window = Tk()
window.geometry('1650x1000')
window.title("Cellular Automata")
window.columnconfigure(0, weight=4)
window.columnconfigure(1, weight=1)

# main canvas to put automata on
canvas = Canvas(window, width=1400, height=1000, bg='white')
canvas.grid(column=0, row=0)

# menu frame
frame = Frame(window, width=10, height=1000)

menu_frame = Frame(frame)
menu_frame['borderwidth'] = 5
menu_frame['relief'] = 'groove'

size_frame = Frame(frame)
size_frame['borderwidth'] = 5
size_frame['relief'] = 'groove'
Label(size_frame, text='Rows:', width=15, anchor="e").grid(column=0, row=0)
Label(size_frame, text='Columns:', width=15, anchor="e").grid(column=0, row=1)
Label(size_frame, text='Cell size:', width=15, anchor="e").grid(column=0, row=2)
rows_entry = Entry(size_frame, width=5)
rows_entry.grid(column=1, row=0)
cols_entry = Entry(size_frame, width=5)
cols_entry.grid(column=1, row=1)
cell_size_entry = Entry(size_frame, width=5)
cell_size_entry.grid(column=1, row=2)
size_frame.grid(column=1, row=0)

rules_frame = Frame(menu_frame)
Label(rules_frame, text='Loneliness l=', width=15, anchor="e").grid(column=0, row=0)
Label(rules_frame, text='Overcrowding o=', width=15, anchor="e").grid(column=0, row=1)
Label(rules_frame, text='Empty between e1=', width=15, anchor="e").grid(column=0, row=2)
Label(rules_frame, text='to e2=', width=15, anchor="e").grid(column=0, row=3)
l = Entry(rules_frame, width=5) # dies by loneliness
l.grid(column=1, row=0)
o = Entry(rules_frame, width=5) # dies by overpopulation
o.grid(column=1, row=1)
e1 = Entry(rules_frame, width=5) # reproduction range start
e1.grid(column=1, row=2)
e2 = Entry(rules_frame, width=5) # reproduction range end
e2.grid(column=1, row=3)
rules_frame.pack()

nh_frame = Frame(menu_frame)
Label(rules_frame, text='Neighbourhood:', width=15).grid(column=0, row=4)
A = Entry(nh_frame, width=3)
A.grid(column=0,row=0)
B = Entry(nh_frame, width=3)
B.grid(column=1,row=0)
C = Entry(nh_frame, width=3)
C.grid(column=2,row=0)
D = Entry(nh_frame, width=3)
D.grid(column=0,row=1)
E = Entry(nh_frame, width=3)
E.grid(column=1,row=1)
F = Entry(nh_frame, width=3)
F.grid(column=2,row=1)
G = Entry(nh_frame, width=3)
G.grid(column=0,row=2)
H = Entry(nh_frame, width=3)
H.grid(column=1,row=2)
I = Entry(nh_frame, width=3)
I.grid(column=2,row=2)
nh_frame.pack()

menu_frame.grid(column=1, row=1)

# defaults
rows_entry.insert(0, "100")
cols_entry.insert(0, "140")
cell_size_entry.insert(0, "10")
l.insert(0, "10")
o.insert(0, "25")
e1.insert(0, "10")
e2.insert(0, "25")
A.insert(0, randint(1,9))
B.insert(0, randint(1,9))
C.insert(0, randint(1,9))
D.insert(0, randint(1,9))
E.insert(0, randint(1,9))
F.insert(0, randint(1,9))
G.insert(0, randint(1,9))
H.insert(0, randint(1,9))
I.insert(0, randint(1,9))

run1 = True
run = True

# Stop the program trying to move when window closed
def handler():
    global run, run1
    run1 = False
    run = False
    window.destroy()
window.protocol("WM_DELETE_WINDOW", handler)

# go button press function
def proceed():
    global run1
    run1 = False

go = Button(frame, text="Start", command=proceed)
go.grid(column=1,row=4)

count_tracker = StringVar()
count_tracker.set('')

count_status = Label(frame, textvariable=count_tracker)
count_status.grid(column=1,row=5)

frame.grid(column=1, row=0)

# wait until go pressed
while run1:
    window.update()

rows = int(rows_entry.get())
cols = int(cols_entry.get())
cell_size = int(cell_size_entry.get())

neighbourhood = [-1*cols-1,-1*cols,-1*cols+1,-1,0,1,cols-1,cols,cols+1] # moore

# blank grid
thisgrid = []
for r in range(rows):
    for c in range(cols):
        thisgrid.append(randint(0,1))

neighbour_weights = [int(A.get()),int(B.get()),int(C.get()),int(D.get()),int(E.get()),int(F.get()),int(G.get()),int(H.get()),int(I.get())]



count = 0 # count iterations

# run the thing
while run:
    count += 1
    count_tracker.set(f"{count} iterations")

    prevgrid = []

    canvas.delete("all")

    
    for r in range(rows):
        for c in range(cols):
            # draw current position
            if thisgrid[cols*r+c] == 1:
                colour = "blue"
            else:
                colour = "white"
            canvas.create_rectangle((c*cell_size,r*cell_size), ((c+1)*cell_size,(r+1)*cell_size), fill=colour)
            
            # save current position as previous
            prevgrid.append(thisgrid[cols*r+c])
    
    # iterate
    for r in range(rows):
        for c in range(cols):
            position = cols*r+c

            thissum = 0
            for k in range(len(neighbourhood)):
                g = neighbourhood[k]
                i = position+g # index of adjacent cell in that direction

                w = neighbour_weights[k]

                try:
                    if i>=0 and i<cols*rows and (g<-1 and floor(position/cols)-1 == floor(i/cols)) or (g>1 and floor(position/cols)+1 == floor(i/cols)) or ((g == 1 or g == -1) and floor(position/cols) == floor(i/cols)):
                        thisrow = floor(i/cols)
                        thiscol = i-thisrow*cols

                        thissum += prevgrid[i]*w

                except IndexError: # i has left the grid, skip this one
                    pass
            
            try:
                if prevgrid[position] == 1:
                    if thissum < int(l.get()) or thissum > int(o.get()):
                        thisgrid[position] = 0
                elif thissum >= int(e1.get()) and thissum <= int(e2.get()):
                    thisgrid[position] = 1
            except ValueError:
                pass
            
    window.update()
    sleep(sleeptime) # wait a second so it isn't all over in a flash

window.mainloop() # keeps the window on screen after everyone has escaped

