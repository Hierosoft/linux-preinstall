#!/usr/bin/env python
from __future__ import print_function
import os
import shutil
import traceback
import math
if sys.version_info.major >= 3:
    from tkinter import *
    # from io import StringIO
else:
    # python 2
    from Tkinter import *
    # from StringIO import StringIO


def show_message(msg, console_enable=False):
    outputE.delete(0, END)
    outputE.insert(0, msg)
    if console_enable:
        print(msg)


def get_float(s, name, unit):
    s = s.strip()
    r = None
    if len(s) < 1:
        msg = "You must specify"
        if name is not None:
            msg += " {}".format(name)
        else:
            msg += " a value"
        if unit is not None:
            msg += " in {}".format(unit)
        msg += "."
        show_message(msg)
        return None
    try:
        r = float(s)
    except ValueError:
        msg = "You must specify a length in meters (m). '{}'".format(s)
        if unit is not None:
            msg += " {}".format(unit)
        msg += " is not a number.".format(s)
        show_message(msg)
        return None
    return r


def show_kg_click():
    show_message("")
    length = get_float(lengthE.get(), "length", "m")
    if length is None:
        return
    diameter = get_float(diameterE.get(), "diameter", "mm")
    if diameter is None:
        return
    gPerCC = get_float(gPerCCE.get(), "specific gravity", "g/cc")
    if gPerCC is None:
        return

    d_cm = diameter / 10  # mm to cm
    l_cm = length * 100  # m to cm
    r_cm = d_cm / 2
    totalCC = math.pi * r_cm**2 * l_cm  # volume formula
    g = totalCC * gPerCC
    kg = round(g / 1000, 3)
    kgE.delete(0, END)
    kgE.insert(0, str(kg))
    show_message(
        "Total volume in cc (cm^3): {}".format(
            round(totalCC, 3)
        )
    )


def show_length_click():
    show_message("")
    weightS = kgE.get().strip()
    if len(weightS) < 1:
        show_message("You must specify Kg.")
        return
    diameter = get_float(diameterE.get(), "diameter", "mm")
    if diameter is None:
        return
    gPerCC = get_float(gPerCCE.get(), "specific gravity", "g/cc")
    if gPerCC is None:
        return
    lengthE.delete(0, END)
    lengthE.insert(0, "not yet implemented")


master = Tk()
master.title("FilaCalc by Poikilos")

new_row_i = 0

gPerCCLabel = Label(master, text="g/cc")
gPerCCLabel.grid(row=new_row_i, column=0)
gPerCCE = Entry(master)
gPerCCE.grid(row=new_row_i, column=1)
gPerCCE.delete(0, END)
gPerCCE.insert(0, "1.27")
new_row_i += 1

diameterLabel = Label(master, text="diameter (mm)")
diameterLabel.grid(row=new_row_i, column=0)
diameterE = Entry(master)
diameterE.grid(row=new_row_i, column=1)
diameterE.delete(0, END)
diameterE.insert(0, "1.75")
new_row_i += 1

costPerKgLabel = Label(master, text="cost per kg")
costPerKgLabel.grid(row=new_row_i, column=0)
costPerKgE = Entry(master)
costPerKgE.grid(row=new_row_i, column=1)
costPerKgE.delete(0, END)
costPerKgE.insert(0, "40")
new_row_i += 1

kgB = Button(master, text="Calculate Kg", command=show_kg_click)
# kgB.pack()  # can't pack in grid
kgB.grid(row=new_row_i, column=0)
kgE = Entry(master)
kgE.grid(row=new_row_i, column=1)
new_row_i += 1

lengthB = Button(master, text="Calculate m", command=show_length_click)
lengthB.grid(row=new_row_i, column=0)
lengthE = Entry(master)
lengthE.grid(row=new_row_i, column=1)
lengthE.delete(0, END)
lengthE.insert(0, "120")
new_row_i += 1

outputE = Entry(master)
outputE.grid(row=new_row_i, column=0, columnspan=2, sticky=W+E)

mainloop()
