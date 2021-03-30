# Utility module to help identify which version of Tcl/Tk is being used.

import _tkinter

def getver():
    '''Return a string with Tcl and Tk versions reported by _tkinter.
    Apparently the most minor revision number is omitted.'''
    tclver = str(_tkinter.TCL_VERSION)
    tkver  = str(_tkinter.TK_VERSION)
    versions = "Tcl " + tclver + " Tk " + tkver
    return versions

def getpatch():
    '''Return a string with Tcl/Tk patchlevel.'''
    tk = _tkinter.create()
    patchlevel  = str(tk.call("info", "patchlevel"))
    #del tk      # I'm not sure this is a good idea.
    return "Tcl/Tk " + patchlevel

# Test:
'''
print("    Tcl/Tk versions = " + getver())
print("    Tcl/Tk patchlevel = " + getpatch())

busywait = _tkinter.getbusywaitinterval()
print("    _tk busywait = " + str(busywait))
'''
