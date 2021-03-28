# Utility module to help identify which version of Tcl/Tk is being used.

import _tkinter

def whichTclTk():
    '''Return a string with Tcl and Tk versions reported by _tkinter.
    Apparently the most minor revision number is omitted.'''
    tclver = str(_tkinter.TCL_VERSION)
    tkver  = str(_tkinter.TK_VERSION)
    versions = "Tcl " + tclver + "  Tk " + tkver
    return versions

def whichTclTkpatch():
    '''Return a string with Tcl and Tk patchlevels.   NOT YET FINISHED.'''
    #tclpatchlev = str(_tkinter.TCL_VERSION)
    #tkpatchlev  = str(_tkinter.TK_VERSION)
    tclpatchlev = str(_tkinter.TCL_VERSION)
    tkpatchlev  = str(_tkinter.TK_VERSION)

    patchlevels = "Tcl " + tclpatchlev + "  Tk " + tkpatchlev
    return patchlevels

#versionstr = whichTclTk()
#print("    Tcl/Tk versions = " + versionstr)

#patchlevels = whichTclTkpatch()
#print("    Tcl/Tk patchlevels = " + patchlevels)
