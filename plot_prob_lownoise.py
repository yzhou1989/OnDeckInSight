"""
Read csv file with probability and number of expected events as function of
a and b values of Gutenberg-Richter relation and plot it up
"""
import matplotlib.pyplot as plt
# from matplotlib.mlab import griddata
from scipy.interpolate import griddata
import matplotlib.colors as colors
import numpy as np
import csv
from obspy.imaging.cm import pqlx

model = 'ice20'
snr = '50.0'
depth = '1.0km'
f1 = '0.100'
f2 = '1.000'
probfile = "{}_{}_{}_{}_{}_lownoise_prob.csv".format(model, snr, depth, f1, f2)
nevfile = "{}_{}_{}_{}_{}_lownoise_nev.csv".format(model, snr, depth, f1, f2)
m0totalfile = "{}_{}_{}_{}_{}_lownoise_m0total.csv".format(model, snr, depth, f1, f2)

with open(probfile) as csvfile:
    csvreader = csv.reader(csvfile)
    csvdata = [r for r in csvreader]

csvdata = np.array(csvdata)
avals = np.array(csvdata[1:, 0], dtype='float')
bvals = np.array(csvdata[0, 1:], dtype='float')
probs = np.array(csvdata[1:, 1:], dtype='float')

with open(nevfile) as csvfile:
    csvreader = csv.reader(csvfile)
    csvdata = [r for r in csvreader]

csvdata = np.array(csvdata)
nevs = np.array(csvdata[1:, 1:], dtype='float')

# Subsample for plot
astep = 0.03125
bstep = 0.00625
aa = np.arange(avals.min(), avals.max() + astep, astep)
bb = np.arange(bvals.min(), bvals.max() + bstep, bstep)

grid_bb, grid_aa = np.meshgrid(bb, aa)
bgrid, agrid = np.meshgrid(bvals, avals)
zz = griddata((np.transpose(bgrid).flatten(), np.transpose(agrid).flatten()),
              np.transpose(probs).flatten(),
              (np.transpose(grid_bb), np.transpose(grid_aa)), method='linear')
# zz = griddata(np.transpose(bgrid).flatten(), np.transpose(agrid).flatten(),
#               np.transpose(probs).flatten(),
#               (np.transpose(grid_bb), np.transpose(grid_aa)), method='linear')
fig = plt.figure()
ax = plt.gca()
im = ax.pcolormesh(grid_bb, grid_aa, np.transpose(zz), cmap='gnuplot2')
plt.xlabel('b value')
plt.ylabel('a value')
cbar = fig.colorbar(im, ax=ax)
cbar.ax.set_ylabel('Probability of event detection')

# Add in contours at 95% and 99%
CS = plt.contour(grid_bb, grid_aa, np.transpose(zz),
                 levels=[0.5, 0.95, 0.99], colors='g')
plt.clabel(CS, inline=1, fontsize=10, fmt='%.2f')

# Add in some relevant models (G92, M06, MQS)
# # G92
# g92a = [4.55]
# g92b = [0.9]
# plt.plot(g92b, g92a, 'go', label="Golombek et al., 1992")

# # MQS
# MQSa = [4.8]
# MQSb = [1.0]
# plt.plot(MQSb, MQSa, 'ro', label="MQS blind test")

# # K06
# k06a = [3.0, 4.5, 5.0, 5.1, 6.7]
# k06b = [0.9375, 0.9375, 0.9375, 0.9375, 0.9375]
# plt.plot(k06b, k06a, 'co', label="Knapmeyer et al., 2006")
# Models A-D
plt.plot([1.0], [3.13], 'co', label='Model A', markersize=10,
         markeredgewidth=1, markeredgecolor='k')
plt.plot([1.0], [3.63], 'co', label='Model B', markersize=10,
         markeredgewidth=1, markeredgecolor='k')
plt.plot([1.0], [5.13], 'co', label='Model C', markersize=10,
         markeredgewidth=1, markeredgecolor='k')
plt.plot([1.0], [5.63], 'co', label='Model D', markersize=10,
         markeredgewidth=1, markeredgecolor='k')

# Preferred
plt.plot([1.0], [4.47], 'co', label='Preferred', markersize=10,
         markeredgewidth=1, markeredgecolor='k')


plt.legend(loc=1)

# Add in contours for m0 total
with open(m0totalfile) as csvfile:
    csvreader = csv.reader(csvfile)
    csvdata = [r for r in csvreader]

csvdata = np.array(csvdata)
m0total = np.array(csvdata[1:, 1:], dtype='float')
zz = griddata((np.transpose(bgrid).flatten(), np.transpose(agrid).flatten()),
              np.transpose(m0total).flatten(),
              (np.transpose(grid_bb), np.transpose(grid_aa)), method='linear')
CS = plt.contour(grid_bb, grid_aa, np.transpose(zz),
                 levels=[1.e15, 1.e16, 1.e17, 1.e18, 1.e19, 1.e20], colors='r')
plt.clabel(CS, inline=1, fontsize=10, fmt='%g')

plotfile = "{}_{}_{}_{}_{}_lownoise_probmatrix.png".format(model, snr, depth, f1, f2)
fig.savefig(plotfile)

# Make a similar plot for expected number of events
zz = griddata((np.transpose(bgrid).flatten(), np.transpose(agrid).flatten()),
              np.transpose(nevs).flatten(),
              (np.transpose(grid_bb), np.transpose(grid_aa)), method='linear',
              fill_value=nevs.min())
fig = plt.figure()
ax = plt.gca()
im = ax.pcolormesh(grid_bb, grid_aa, np.transpose(zz),
                   norm=colors.LogNorm(vmin=zz.min(), vmax=zz.max()),
                   cmap='gnuplot2')
plt.xlabel('b value')
plt.ylabel('a value')
cbar = fig.colorbar(im, ax=ax)
cbar.ax.set_ylabel('Number of expected event detections')

# Models A-D
plt.plot([1.0], [3.13], 'co', label='Model A', markersize=10,
         markeredgewidth=1, markeredgecolor='k')
plt.plot([1.0], [3.63], 'co', label='Model B', markersize=10,
         markeredgewidth=1, markeredgecolor='k')
plt.plot([1.0], [5.13], 'co', label='Model C', markersize=10,
         markeredgewidth=1, markeredgecolor='k')
plt.plot([1.0], [5.63], 'co', label='Model D', markersize=10,
         markeredgewidth=1, markeredgecolor='k')

# Preferred
plt.plot([1.0], [4.47], 'co', label='Preferred', markersize=10,
         markeredgewidth=1, markeredgecolor='k')


plt.legend(loc=1)


# Add in contours for m0 total
zz = griddata((np.transpose(bgrid).flatten(), np.transpose(agrid).flatten()),
              np.transpose(m0total).flatten(),
              (np.transpose(grid_bb), np.transpose(grid_aa)), method='linear')
CS = plt.contour(grid_bb, grid_aa, np.transpose(zz),
                 levels=[1.e15, 1.e16, 1.e17, 1.e18, 1.e19, 1.e20], colors='r')
plt.clabel(CS, inline=1, fontsize=10, fmt='%g')

plotfile = "{}_{}_{}_{}_{}_lownoise_nevmatrix.png".format(model, snr, depth, f1, f2)
fig.savefig(plotfile)
