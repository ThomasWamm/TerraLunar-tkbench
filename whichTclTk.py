# Utility module to help identify which version of Tcl/Tk is being used.

import _tkinter

def getver():
    '''Return a string with Tcl and Tk versions as imagined by _tkinter.
    Apparently the most minor revision number is omitted.'''
    tclver = str(_tkinter.TCL_VERSION)
    tkver  = str(_tkinter.TK_VERSION)
    return "Tcl " + tclver + " Tk " + tkver

def getpatch():
    '''Return a string with Tcl/Tk patchlevel.'''
    tk = _tkinter.create()
    return "Tcl/Tk " + str(tk.call("info", "patchlevel"))

# uncomment for testing:
'''
print("    Tcl/Tk versions = " + getver())
print("    Tcl/Tk patchlevel = " + getpatch())

busywait = _tkinter.getbusywaitinterval()
print("    _tk busywait = " + str(busywait))
'''
