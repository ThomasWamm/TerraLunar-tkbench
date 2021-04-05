# TerraLunar-tkbench.py
'''
"TerraLunar-tkbench.py" is a simplified more portable fork of my earlier "TerraLunar.py". 

The -tkbench fork is primarily intended to explore the performance of the 
Python "tkinter" portable windowing interface for graphics on a variety of 
computing platforms (MacOS, Windows, and Linux).

The program draws graphics in a window, and also reports in the window 
and to the console terminal what software versions are running, 
and how long it takes in seconds to do its fixed amount of work.
There is no file I/O.  One or two mouse clicks end the program.

Typical output examples are:
  Python 3.8.2 on darwin  Tcl/Tk 8.5.9  TerraLunar-tkbench 0.1.8  runtime = 36
or
  Python 3.8.2 on darwin  Tcl/Tk 8.5.9  TerraLunar-tkbench 0.1.8    ABNORMAL FINISH, invalid benchmark.

See also the image file:  typical_screen_image.png

SYSTEM REQUIREMENTS:
Python 2.7 or newer, on Windows, MacOS, or Linux,
with a GUI that supports the Python module 'Tkinter' or 'tkinter'.

Use git to clone this project to your computer, then 
in a command line terminal window type:
    python TerraLunar-tkbench.py


This program may be helpful to people working on these software issues: 

  "tkinter with Tk 8.6.11 is slow on macOS"
      https://bugs.python.org/issue43511

  "MacOS slow performance of 8.6.11 vs 8.6.8"
      https://core.tcl-lang.org/tk/tktview/f642d7c0f4


Usage of this code is unrestricted. It was a learning project.
  Thomas Wamm 4-Apr-2021
'''
