# #!/usr/bin/env python

# # bounce detection algorithm
# # https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data

import matplotlib.pyplot as plt
import numpy as np
import time
import random

def thresholding_algo(y, lag, threshold, influence):
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
            if y[i] > avgFilter[i-1]:
                signals[i] = 1
            else:
                signals[i] = -1

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag):i])
            stdFilter[i] = np.std(filteredY[(i-lag):i])
        else:
            signals[i] = 0
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag):i])
            stdFilter[i] = np.std(filteredY[(i-lag):i])

    return dict(signals = np.asarray(signals),
                avgFilter = np.asarray(avgFilter),
                stdFilter = np.asarray(stdFilter))


# Settings: lag = 30, threshold = 5, influence = 0
lag = 30 # for smoothing - the size of the array we'll look at
threshold = 2 # of std deviations of signal
influence = 0 # how much a spike influences the average

x = np.linspace(0,100,101)
y = np.zeros(101)
all_ys = []

plt.ion()
line_graph, point_graph = plt.plot(x,y, '-r',x,y,'.b')
# point_graph = plt.plot(x,y,'.b')[0]
plt.ylim((0,1.3))

n = 0

def new_fake_datapoint():
    new = random.uniform(0, 1)
    if n % 20 == 0:
        new = 0.9
    else:
        new = new / 1.5
    return new


while True:
    new = new_fake_datapoint()
    if n < 101:
        y[n] = new
    else:
        # remove from beginning and add the new one to the end
        y[:-1] = y[1:]
        y[-1] = new_fake_datapoint()
    all_ys.append(new)
    n += 1
    # y = y**2 + np.random.random(x.shape)
    line_graph.set_ydata(y)


    # Run algo with settings from above
    result = thresholding_algo(y, lag=lag, threshold=threshold, influence=influence)
    point_graph.set_ydata(result['signals'])
    if result['signals'][-1] == 1:
        print('BOOOOOOM')
    else:
        print('>')


    plt.draw()
    plt.pause(0.01)
    
    





