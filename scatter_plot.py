import numpy as np
import matplotlib.pyplot as plt
from myquaternaryutility import QuaternaryPlot
from quaternary_faces_shells import ternaryfaces_shells
import pylab

# Relevant Variables
nrows = 5
ncols = 3
n_of_measurments = 10
ellabels = ['Au', 'Mg', 'Si', 'Na']

# Helper Variables
intervs = 10
results = np.empty((0, 4))
n_click = 0


# Data for uniform Point-Distribution
compsint = [[b, c, (intervs - a - b - c), a] for a in np.arange(0, intervs + 1)[::-1] for b in
            np.arange(0, intervs + 1 - a) for c in np.arange(0, intervs + 1 - a - b)][::-1]
print len(compsint)
comps = np.float32(compsint) / intervs


# Declaration of the figure with the given number of columns and rows
fig, axis = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True)

# Iteration over every axis where the data is used to plot the ternary_shells
points_list = []
for i in range(0, nrows, 1):
    for j in range(0, ncols, 1):
        # Get the object QuaternaryPlot
        stpquat = QuaternaryPlot()
        cols = stpquat.rgb_comp(comps)
        tf = ternaryfaces_shells(axis[i][j], ellabels, nintervals=intervs)
        tf.label()
        #Saves all tthe picked data inside a list for the color changing
        points_list.append(tf.scatter(comps, cols, skipinds=[0, 1, 2, 3], s=None))

# Pick event for changing color of the picked Data
def onpick(event):
    event.artist._facecolors[event.ind, :] = (1, 0, 0, 1)
    fig.canvas.draw()


# A Press event executed on mouse-clicks
# It takes the clicked coordinates and turns them into the comp coordinates
# Closes the program after reaching the number of measurments
def on_press(event):
    global n_click
    global results
    clicked_comp = tf.toComp(event.xdata, event.ydata)
    fig.canvas.draw()
    if n_click < n_of_measurments:
        # Forms the results Array
        results = np.vstack([results, [clicked_comp]])
        n_click += 1

        # Print Formatting
        print('Measurment: {} '.format(n_click))
        for elements in range(len(ellabels)):
            print('{}: {}'.format(ellabels[elements], clicked_comp[elements]))
        print ('\n')
    else:
        print('Coordinates of {} measurments'.format(n_of_measurments))
        print(results)
        # Results are saved to csv
        np.savetxt('results.csv', results, delimiter=",")

        exit()


# The Click event
fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect('button_press_event', on_press)
plt.show()
