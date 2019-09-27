#!/usr/bin/python

import Tkinter

import time


# Tkinter is a library to 2D graphic.
# Creating of a GUI with specific size and a canvas used to draw shapes and animation.

def my_gui():
    gui = Tkinter.Tk()
    var = Tkinter.IntVar()
    gui.geometry("800x800")
    c = Tkinter.Canvas(gui, width=800, height=800)
    c.pack()
    oval = c.create_oval(5, 5, 60, 60, fill='pink')

    # The animation. Vector [a, b] describes a move of an oval at one frame.
    # The time of pause between frames is equal 100 ms.
    # The mainloop() method stops execution of a code at this position and waits for a user to close the window.

    a = 5
    b = 5
    for x in range(0, 100):
        c.move(oval, a, b)
        gui.update()
        time.sleep(.01)
    gui.title("First title")
    gui.mainloop()

    # Drawing of a sticky man.

    top = Tkinter.Tk()

    print("zrobione")

    top.width = 200
    top.height = 300
    canvas = Tkinter.Canvas(top, width=200, height=200)
    canvas.pack()

    # can.create_line(0, 200, 200, 0, fill="red", dash=(4, 4))
    # can.create_line(0, 0, 200, 200)

    canvas.create_oval(50, 0, 100, 50, fill="red")
    canvas.create_line(75, 50, 75, 125)
    canvas.create_line(75, 75, 50, 100)
    canvas.create_line(75, 75, 100, 100)

    canvas.create_line(75, 125, 50, 150)
    canvas.create_line(75, 125, 100, 150)

    # can.create_rectangle(50, 25, 150, 75, fill="blue")

    top.mainloop()
