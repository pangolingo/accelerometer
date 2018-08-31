#!/usr/bin/env python
# Implementation of algorithm from https://stackoverflow.com/a/22640362/6029703
import numpy as np
import pylab
import time

# declarations
# prevAvgFilter = 0
# currentAvgFilter = 0
# prevStdFilter = 0
# currentStdFilter  = 0

# def thresholding_algo(y, lag, threshold, influence):
#     signals = np.zeros(len(y))
#     filteredY = np.array(y)
#     avgFilter = [0]*len(y)
#     stdFilter = [0]*len(y)
#     avgFilter[lag - 1] = np.mean(y[0:lag])
#     stdFilter[lag - 1] = np.std(y[0:lag])
#     for i in range(lag, len(y)):
#         if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
#             if y[i] > avgFilter[i-1]:
#                 signals[i] = 1
#             else:
#                 signals[i] = -1

#             filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
#             avgFilter[i] = np.mean(filteredY[(i-lag):i])
#             stdFilter[i] = np.std(filteredY[(i-lag):i])
#         else:
#             signals[i] = 0
#             filteredY[i] = y[i]
#             avgFilter[i] = np.mean(filteredY[(i-lag):i])
#             stdFilter[i] = np.std(filteredY[(i-lag):i])

#     return dict(signals = np.asarray(signals),
#                 avgFilter = np.asarray(avgFilter),
#                 stdFilter = np.asarray(stdFilter))


# declarations
# do we need to prepopulate these?
# YES: see above for how i guess?
# signals = np.array([0] * 50) # orig code sets this to all zeroes
# filteredY = np.array([0] * 50) # orig code sets this to a copy of the original data array
signals = [0] * 1
filteredY = [0] * 1
avgFilter = [0] * 1 # orig code sets this to all zeroes, then sets lag-1 to the mean of it i guess
stdFilter = [0] * 1 # orig code sets this to all zeroes, then sets lag-1 to the std dev of it i guess
# avgFilter[lag - 1] = np.mean(y[0:lag])
# stdFilter[lag - 1] = np.std(y[0:lag])


# datapoint: the new accelerometer data coming in
# i: the numberth datapoint that this is
# lag: number of previous observations to use for smoothing
# threshold: will signal if a datapoint is this many std deviations away from the mean
# influence: the influence of signals vs normal datapoints
def update_stuff(datapoint, i, lag, threshold, influence):
    prevAvgFilter = avgFilter[i - 1]
    prevStdFilter = stdFilter[i - 1]
    if abs(datapoint - prevAvgFilter) > threshold * prevStdFilter:
        # exceeded the threshold. signal!
        if datapoint > prevAvgFilter:
            # signals[i] = 1
            signals.append(1)
        else:
            # signals[i] = -1
            signals.append(-1)

        # we want this signaling datapoint to be saved as having more or less influence than a standard datapoint
        # filteredY[i] = influence * datapoint + (1 - influence) * filteredY[i-1]
        filteredY.append(influence * datapoint + (1 - influence) * filteredY[i-1])
    else:
        # did not exceed the required threshold
        # no signal
        # signals[i] = 0
        signals.append(0)
        # filteredY[i] = datapoint
        filteredY.append(datapoint)
        
    # always update the avg and std filters
    # in theory we could clear out older filteredY and avgFilter and stdFilter values
    # as long as we keep enough for lag to use
    # that would improve memory usage if this is long-running
    # avgFilter[i] = np.mean(filteredY[(i-lag):i])
    avgFilter.append(np.mean(filteredY[(i-lag):i]))
    stdFilter.append(np.std(filteredY[(i-lag):i]))
    # stdFilter[i] = np.std(filteredY[(i-lag):i])
    # return the signal
    return signals[len(signals) - 1]





#### DO IT!

# Data
# a vector of timeseries data of at least length lag+2
y = np.array([1,1,1.1,1,0.9,1,1,1.1,1,0.9,1,1.1,1,1,0.9,1,1,1.1,1,1,1,1,1.1,0.9,1,1.1,1,1,0.9,
       1,1.1,1,1,1.1,1,0.8,0.9,1,1.2,0.9,1,1,1.1,1.2,1,1.5,1,3,2,5,3,2,1,1,1,0.9,1,1,3,
       2.6,4,3,3.2,2,1,1,0.8,4,4,2,2.5,1,1,1])

# number of previous observations to use for smoothing
lag = 7
# will signal if a datapoint is this many std deviations away from the mean
threshold = 5
# the influence of signals vs normal datapoints
influence = 0.1

# Run algo with settings from above
# result = thresholding_algo(y, lag=lag, threshold=threshold, influence=influence)
it = np.nditer(y, flags=['f_index'])
while not it.finished:
    # print(it[0])
    update_stuff(it[0], it.index, lag, threshold, influence)
    it.iternext()

result = dict(signals = np.asarray(signals),
            avgFilter = np.asarray(avgFilter),
            stdFilter = np.asarray(stdFilter))

# get the length right
y = np.insert(y, 0, 0)

# Plot result
pylab.subplot(211)
pylab.plot(np.arange(1, len(y)+1), y)

pylab.plot(np.arange(1, len(y)+1),
           result["avgFilter"], color="cyan", lw=2)

pylab.plot(np.arange(1, len(y)+1),
           result["avgFilter"] + threshold * result["stdFilter"], color="green", lw=2)

pylab.plot(np.arange(1, len(y)+1),
           result["avgFilter"] - threshold * result["stdFilter"], color="green", lw=2)

pylab.subplot(212)
pylab.step(np.arange(1, len(y)+1), result["signals"], color="red", lw=2)
pylab.ylim(-1.5, 1.5)

pylab.show()
# while True:
#     time.sleep(1)
