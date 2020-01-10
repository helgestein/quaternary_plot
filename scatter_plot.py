import numpy as np
import matplotlib.pyplot as plt
from myquaternaryutility import QuaternaryPlot
from quaternary_faces_shells import ternaryfaces_shells


#Relevant Variables
nrows = 2
ncols = 2
intervs = 10
results=np.empty((0,4))
ellabels=['Au', 'Mg', 'Si', 'Na']
n_click = 0
n_of_measurments = 10

#Data for uniform Point-Distribution
compsint = [[b, c, (intervs - a - b - c), a] for a in np.arange(0, intervs + 1)[::-1] for b in
            np.arange(0, intervs + 1 - a) for c in np.arange(0, intervs + 1 - a - b)][::-1]
print len(compsint)
comps = np.float32(compsint) / intervs

#Declaration of the figure with the given number of columns and rows
fig, axis = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True)

#Iteration over every axis where the data is used to plot the ternary_shells
for i in range(0, nrows, 1):
    for j in range(0, ncols, 1):
        #Get the object QuaternaryPlot
        stpquat = QuaternaryPlot()
        cols = stpquat.rgb_comp(comps)
        tf = ternaryfaces_shells(axis[i][j], ellabels, nintervals=intervs)
        tf.label()
        tf.scatter(comps, cols, skipinds=[0, 1, 2, 3], s='patch')



# def onpick(event):
#     print(event.artist)
#     '''
#     print(event.artist)
#     for points in points_list:
#         if event.artist == points:
#             points._facecolors[event.ind, :] = (1, 1, 0, 1)
#             points._edgecolors[event.ind, :] = (1, 0, 0, 1)
#
#     fig.canvas.draw()
#     '''

#A Press event executed on mouscliks
#It takes the clicked coordinates and
def on_press(event):
    global n_click
    global results
    clicked_comp = tf.toComp(event.xdata, event.ydata)

    if n_click < n_of_measurments:
        #tf.pick(event.xdata, event.ydata)
        #Forms the results Array
        results = np.vstack([results, [clicked_comp]])
        n_click += 1

        #Print Formatting
        print('Measurment: {} '.format(n_click))
        for elements in range(len(ellabels)):
            print('{}: {}'.format(ellabels[elements], clicked_comp[elements]))
        print ('\n')
    else:
        print('Coordinates of {} measurments'.format(n_of_measurments))
        print(results)
        #Results are saved to csv
        np.savetxt('results.csv', results, delimiter=",")

        exit()

#The Click event
cid = fig.canvas.mpl_connect('button_press_event', on_press)
plt.show()
