#!/usr/bin/python
# TerraLunar-tkbench.py   tkinter/Tcl/Tk benchmark toy.
#
# 2-D orbital mechanics simulation in Earth-Moon space.
# by Thomas since 2020 for learning Python & SWEng
#    2021-Mar-25 -- "-tkbench" version for tkinter benchmarking
#
# Optimized for portability and learning, not efficiency.
# Consistent benchmarks require the graphics window be all visible, 
# and the computer should be doing not much other work.
#
# Use simplified Newtonian physics and numerical integrations.
# F = ma = -GMm/r^2
# a = F/m = -GM/r^2
# v = v + dv = v + adt
# x = x + dx = x + vdt
# t = t + dt

# This version runs on Linux, Windows, and MacOS with Python2.7 or newer.
# Requires tkinter module and graphics.py wrapper for tkinter, 
# to do graphics in a window on different computing platforms.

TerraLunar_tkbench_version = "0.1.4"       # was derived from TerraLunar 0.1.3

#import graphics as gr        # moved this line to as late as possible
from random import randint
import math
import time

#import code

# Need adaptability for different display devices...

cfg_tinywindow = {'for window dimensions: ': 'you can change these',
           'windowwidth': 1000,
           'windowheight': 540,
           'targetdisplay': 'for small netbook displays'}    # small window is more portable

cfg = cfg_tinywindow

winwidth = int(cfg['windowwidth'])
winheight = int(cfg['windowheight'])
targetdisplay = cfg['targetdisplay']

# Global objects for graphics, Earth, Moon, and one spacecraft...

# define a class to store a set of initial conditions...

class Initset:
    def __init__(self, moondegrees=60.0,
                 shipxmd=1.0,
                 shipymd=0.0,
                 shipvx=0.0,
                 shipvy=851.0,
                 dtime=10,
                 winscale=1.2,
                 radscale=5.0,
                 checktrigger=1000,
                 description='Default setup'):

        self.moondegrees = moondegrees
        self.shipxmd = shipxmd
        self.shipymd = shipymd
        self.shipvx = shipvx
        self.shipvy = shipvy
        self.dtime = dtime
        self.winscale = winscale
        self.radscale = radscale
        self.checktrigger = checktrigger
        self.description = description

# A variety of interesting setups have been accumulated during development...

setuplib = (['moondeg','xmd','ymd','vx','vy','dt','wscale','rscale','chktrig','Description'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 30, 19.0, 5.0, 10000, '9.4M steps to escape'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 60, 1.6, 5.0, 10000, '323k steps to lunar impact'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 1, 5.0, 5.0, 40000, 'escape within 1B steps; small dt'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 10, 2.0, 5.0, 10000, 'eventual lunar impact; medium dt'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 60, 2.0, 5.0, 10000, 'eventual lunar impact; big dt'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 30, 2.0, 5.0, 10000, '8M steps to escape'],
            [0.0, 0.017, 0.0, 0.0, 9200.0, 1, 0.03, 1.0, 1000, 'elliptical orbit'],
            [0.0, 0.017, 0.0, 0.0, 7900.0, 1, 0.02, 1.0, 1000, 'LEO = low Earth orbit'],
            [0.0, 0.10968811, 0.0, 0.0, 3074.7937, 1, 0.15, 1.0, 1000, 'geosynchronous orbit'],
            [0.0, 0.8491, 0.0, 0.0, 861.2724303351446, 10, 1.2, 1.0, 10000, 'just outside L1'],
            [0.0, 0.8491, 0.0, 0.0, 861.2724303351447, 10, 1.2, 1.0, 10000, 'outside 22M inside outside L1'],
            [0.0, 0.8491, 0.0, 0.0, 861.27243, 10, 1.2, 1.0, 10000, 'just below L1'],
            [0.0, 0.85, 0.0, 0.0, 870.0, 10, 1.2, 1.0, 10000, 'near L1'],
            [0.0, 0.90, 0.0, 0.0, 770.0, 10, 1.2, 1.0, 10000, 'distant lunar orbit'],
            [135.4, 0.0168, 0.0, 0.0, 11050.0, 1, 2.7, 1.0, 10000, 'escape with lunar assist'],
            [135.0, 0.0168, 0.0, 0.0, 11050.0, 1, 0.7, 1.0, 10000, 'Ranger direct lunar impact'],
            [0.0, 0.995, 0.0, 0.0, 2590.0, 10, 1.1, 1.0, 10000, 'Apollo 8 orbiting moon'],
            [135.0, 0.017, 0.0, 0.0, 10998.0, 1, 0.7, 1.0, 10000, 'Apollo 13 safe return'],
            [135.0, 0.017, 0.0, 0.0, 10990.0, 1, 0.7, 1.0, 10000, 'direct lunar impact'],
            [135.0, 0.017, 0.0, 0.0, 11000.0, 1, 0.8, 1.0, 10000, 'lost Apollo 13'],
            [130.0, 0.02, 0.0, 0.0, 10080.0, 10, 1.1, 1.0, 10000, '2-orbit lunar impact'],
            [60.0, 0.8, 0.0, 400.0, 1100., 50, 1.8, 5.0, 10000, 'failed L4; 11M steps to moon'],
            [60.0, 0.8, 0.0, 100.0, 1073., 10, 5.0, 10.0, 10000, 'eventual lunar impact #2'],
            [60.0, 1.0, 0.0, 0.0, 900.0, 101, 1.3, 1.0, 10000, 'lunar impact 1.5M loops'],
            [60.0, 1.0, 0.0, 0.0, 900.0, 60, 39.5, 5.0, 10000, 'many lunar interactions'],
            [60.0, 1.0, 0.0, 0.0, 900.0, 30, 1.3, 1.0, 10000, 'lunar impact, 2.2M steps'],
            [60.0, 1.0, 0.0, 0.0, 900.0, 10, 2.0, 5.0, 40000, 'temporary lunar orbits then impact'],
            [55.0, 3.0, 0.0, 0.0, 0.0, 10, 2.0, 1.0, 10000, 'non-fall to Earth from 3 moondistances.'],
            [40.0, 5.0, 0.0, 0.0, 0.0, 1, 3.0, 1.0, 10000, 'fall to Earth from 5 moondistances.'],
            [60.0, 0.9, 0.0, 0.0, 950.0, 60, 1.7, 5.0, 10000, '11.85M steps to Lunar Impact'],
            [60.0, 0.8, 0.0, 0.0, 1073., 10, 1.3, 1.0, 10000, 'lunar impact'],
            [60.0, 1.0, 0.0, 0.0, 923.0, 10, 1.1, 1.0, 10000, 'lunar impact, vy=921-926'],
            [0.0, 0.98, 0.0, 0.0, 2000.0, 10, 1.1, 1.0, 10000, 'medium distance lunar orbit 1'],
            [0.0, 0.95, 0.0, 0.0, 1500.0, 10, 1.1, 1.0, 10000, 'medium distance lunar orbit 2'],
)

def grabsetup(i):   # return one setup from library
    return Initset(moondegrees=setuplib[i][0],
                   shipxmd=setuplib[i][1],
                   shipymd=setuplib[i][2],
                   shipvx=setuplib[i][3],
                   shipvy=setuplib[i][4],
                   dtime=setuplib[i][5],
                   winscale=setuplib[i][6],
                   radscale=setuplib[i][7],
                   checktrigger=setuplib[i][8],
                   description=setuplib[i][9])


setupnum = 2        # setup number 2 is good for a quick tkinter benchmark test

if setupnum < 1:
    setupnum = 1
if setupnum > len(setuplib)-1:
    setupnum = len(setuplib)-1

inz = grabsetup(setupnum)


# Create the graphics display window...

import graphics as gr        # graphics.py is a wrapper for the tkinter module

win = gr.GraphWin("TerraLunar-tkbench Python program", winwidth, winheight)
win.setBackground('black')

# plot some random stars...

for i in range(50):
    x = randint(0, winwidth-1)
    y = randint(0, winheight-1)
    win.plotPixel(x, y, color='white')

# For the numerical physics model, use MKS units:  meter, kilogram, second.
# Use the average Earth-Moon distance as a unit for view scaling.

moondistance = 3.84399e8

# Set up initial conditions in our simulated universe...
# Earth is at display center origin.

earthrad = 6.3781e6
earthx = 0.0
earthy = 0.0

# Set up window with worldly plot coordinates lower left and upper right...

yll = -moondistance * inz.winscale
yur = moondistance * inz.winscale
xll = yll * winwidth/winheight
xur = yur * winwidth/winheight
win.setCoords(xll, yll, xur, yur)

earth = gr.Circle(gr.Point(earthx, earthy), inz.radscale*earthrad)
earth.setWidth(2)
earth.setFill('blue')
trendcolor = 'blue'  # Earth outline color will provide hints
earth.setOutline(trendcolor)
earth.draw(win)

winmin = min(winwidth, winheight)
winmax = max(winwidth, winheight)
viewscale = winmin / (3.0 * moondistance * inz.winscale)  # pixels/meter
apixel = 2.5 / viewscale   # movement size to provoke a screen update
#apixel = 100. * 2.5 / viewscale   # to test slowdown caused by tkinter
offscreen = 0.4 * winmax / viewscale     # meters to be out of view
crumbinterval = 5
crumbsteps = crumbinterval


moonrad = 1.7374e6   # radius of moon in meters

moonangle = math.radians(inz.moondegrees)  # calculate with radians
moonx = earthx + moondistance*math.cos(moonangle)
moony = earthy + moondistance*math.sin(moonangle)

moon = gr.Circle(gr.Point(moonx, moony), inz.radscale*moonrad)
moon.setWidth(1)
moon.setFill('grey')
moon.setOutline('white')
moon.draw(win)
win.plot(moonx, moony, color='red')  # leave one red dot where moon started
oldmx = moonx  # to keep track of previous displayed moon location
oldmy = moony

# Display some textual information...

textversion = gr.Text(gr.Point(xll*0.75, yur*0.95), "TerraLunar-tkbench  " + TerraLunar_tkbench_version)
textversion.setTextColor('cyan')
textversion.draw(win)

textul = gr.Text(gr.Point(xll*0.75, yur*0.80), inz.description)
textul.setTextColor('cyan')
textul.draw(win)

textur = gr.Text(gr.Point(xur*0.80, yur*0.95), text='Click to exit')
textur.setTextColor('pink')
textur.draw(win)

textlr = gr.Text(gr.Point(xur*0.75, yll*0.95), text='########## steps @ ###### / sec')
textlr.setTextColor('yellow')
textlr.draw(win)

shipstatus = 'in orbit'
textll = gr.Text(gr.Point(xll*0.75, yll*0.95), text='Status:    ' + shipstatus)
textll.setTextColor('white')
textll.draw(win)

shipx = earthx + moondistance*inz.shipxmd
shipy = earthy + moondistance*inz.shipymd
d2e = math.hypot(shipx - earthx, shipy - earthy)
moonunits = d2e / moondistance
shipvx = inz.shipvx
shipvy = inz.shipvy

pathcolors = ['red', 'tan', 'green', 'cyan', 'magenta', 'yellow']
pathcolor = 0
colorsteps = 0

win.plot(shipx, shipy, color=pathcolors[pathcolor])
oldx = shipx  # to keep track of previous displayed ship location
oldy = shipy

# draw ship as a small red square
halfship = 1.5 / viewscale
ship = gr.Rectangle(gr.Point(shipx-halfship, shipy-halfship),
                    gr.Point(shipx+halfship, shipy+halfship))
ship.setWidth(1)
ship.setFill('red')
ship.setOutline('red')
ship.draw(win)

simtime = 0             # elapsed simulation time
dtime = inz.dtime       # time step for simulation
gravcon = -6.67430e-11
earthgrav = gravcon * 5.972e24
moongrav = gravcon * 7.342e22
# moon orbits counterclockwise 360 degrees/(27 days + 7 hr + 43 min + 12 sec)
moonstep = math.radians(360.*dtime/(27.*24*60*60 + 7.*3600 + 43.*60 + 12.))

orbits = 0     # to count orbits around Earth
steps = 0
oldsteps = steps
starttime = time.time()     # benchmark real time for portability

oldtime = starttime
plots = 0
sps = 0           # steps per second
maxsps = 0
starttimestamp = time.asctime(time.localtime())
running = True

# top of big numerical integration simulation loop...

while win.checkMouse() is None:     # break out on mouse click
    oldd2e = d2e
    d2e = math.hypot(shipx - earthx, shipy - earthy)
    if d2e < earthrad:
        earth.setFill('red')
        earth.move(0, 0)
        shipstatus = "Crashed on Earth !"
        break

    d2m = math.hypot(shipx - moonx, shipy - moony)
    if d2m < moonrad:
        moon.setFill('red')
        moon.move(0, 0)
        shipstatus = "Crashed on Moon !"
        break

    s2eaccel = dtime * earthgrav / (d2e * d2e * d2e)
    s2maccel = dtime * moongrav / (d2m * d2m * d2m)
    shipvx += s2eaccel * (shipx - earthx) + s2maccel * (shipx - moonx)
    shipvy += s2eaccel * (shipy - earthy) + s2maccel * (shipy - moony)
    oldshipy = shipy  # to detect crossing of x-axis each orbit of Earth
    shipx += dtime * shipvx
    shipy += dtime * shipvy

    if oldshipy < earthy and shipy >= earthy:  # detect x-axis crossings
        orbits += 1
        colorsteps += 1   # change ship color every orbit around Earth

    moonangle += moonstep
    moonx = earthx + moondistance*math.cos(moonangle)
    moony = earthy + moondistance*math.sin(moonangle)

    ''' Graphic update is done less often than numerical integration. '''

    if abs(shipx - oldx) + abs(shipy - oldy) + abs(moonx - oldmx) + abs(moony - oldmy) > apixel:
        # only update display when ship or moon moves at least a pixel
        moon.move(moonx - oldmx, moony - oldmy)
        ship.move(shipx - oldx, shipy - oldy)
        crumbsteps -= 1   # occasionally drop a crumb on the path
        if crumbsteps <= 0:
            crumbsteps = crumbinterval
            pathcolor = colorsteps % len(pathcolors)
            win.plot(shipx, shipy, color=pathcolors[pathcolor])

        oldx = shipx
        oldy = shipy
        oldmx = moonx
        oldmy = moony
        plots += 1

    if steps % inz.checktrigger == 0:
        # display periodic status updates
        trendcolor = 'green'
        if d2e > oldd2e:
            trendcolor = 'red'     # increasing distance to Earth
        earth.setOutline(trendcolor)
        # calculate current sps (steps per second)...
        newtime = time.time()
        delta = newtime - oldtime
        if delta != 0:
            sps = int((steps - oldsteps)/delta)
            maxsps = max(maxsps, sps)
            # print(0, sps)   # for studying loop slowdown vs. time
            oldtime = newtime
            oldsteps = steps
            steps_string = str(steps) + " steps  @  " + str(sps) + " / sec"
            textlr.setText(steps_string)

        moonunits = d2e / moondistance
        status_string = "Ship status:   " + shipstatus
        textll.setText(status_string)

        velocity = math.hypot(shipvx, shipvy)
        escapevelocity = math.sqrt(-2.0 * (earthgrav + moongrav) / d2e)

        if (velocity > escapevelocity) and (d2e > offscreen):
            earth.setFill('green')  # show green Earth then quit
            earth.setOutline('green')
            shipstatus = "Escape velocity !  Lost in space!"
            break

    simtime += dtime
    steps += 1
    # Bottom of big numerical integration loop; repeat until terminated.

running = False
# Simulation loop has exited. Output stats and clean up...

stoptimestamp = time.asctime(time.localtime())

#print('Started @  ' + starttimestamp)
#print('Stopped @  ' + stoptimestamp)   # sometimes I run it for days

stoptime = time.time()

elapsedtime = stoptime - starttime
if elapsedtime == 0:
    elapsedtime = 1.0
itrate = int(steps / elapsedtime)
plotrate = int(plots / elapsedtime)
moonunits = d2e / moondistance
velocity = math.hypot(shipvx, shipvy)

status_string = "Ship status:   " + shipstatus
textll.setText(status_string)

steps_string = str(steps) + " steps  @  " + str(sps) + " / sec"
textlr.setText(steps_string)

#print('\nShip status:  ' +  shipstatus)

"""# optional console output:
print(str(setupnum) + " : " + inz.description + "\n" +
      str(steps) + " steps in " + str(int(elapsedtime)) + " seconds\n" +
      "avg.sps=" + str(itrate) + "   last.sps=" + str(sps) + "   max.sps=" + str(maxsps) + "\n" +
      "plot.rate=" + str(plotrate) + "   orbits=" + str(orbits) + "\n")
print(str(moonunits) + " moonu  @  " + str(velocity) + " mps")
"""

# display benchmark time near centre of window
benchresult = "    TerraLunar-tkbench time =   " + str(int(elapsedtime))
finalcolor = 'green'

if abs(steps - 322881) > 2:     # simulation results should not vary too much
    benchresult = "    ABNORMAL FINISH, invalid benchmark."
    finalcolor = 'red'

textcentre = gr.Text(gr.Point(xll*0.0, yll*0.2), text=benchresult)
textcentre.setTextColor(finalcolor)
textcentre.setSize(24)
textcentre.draw(win)


win.getMouse()    # wait for final mouse click
win.close()

timestamp = time.asctime(time.localtime())
#print('Exited  @  ' + timestamp)   # sometimes I ignore it for days

print(benchresult)

# optionally drop into a Python shell
#code.interact(local=dict(globals(), **locals()))
# end.
