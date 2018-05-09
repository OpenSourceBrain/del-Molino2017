import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


def calculate_phi(Vss):
    Vr = -60 # mV
    tau = np.array([[0.0280], [0.0080], [0.0160], [0.0160]])
    sV = np.ones((4, 1)) # noise (mV)

    '''This calculates the average rate of each population'''
    return (Vss - Vth) / (tau * (Vth - Vr) * (1 - np.exp(-(Vss - Vth) /sV)))

# Settings:
T = 200
dt = 0.1
Vl = -70
tau_r = 2
W = np.array([[2.4167, -0.3329, -0.8039,       0],
              [2.9706, -3.4554, -2.1291,       0],
              [4.6440,       0,       0, -2.7896],
              [0.7162,       0, -0.1560,       0]])

# initial voltage
r0 = np.array([[1], [10], [3], [2]])
r = r0
# initial conditions of the different cell populations
Istim = np.zeros((4, 1))
# define leak conductance (nS)
gl = np.array([[6.25], [10], [5], [5]])
V0 = np.array([[-52.1261], [-50.4308], [-51.3239], [-51.9664]])
# On the original code Ibkg0 was loaded from the mat file
Ibkg0 = np.multiply((V0 - Vl), gl) - np.dot(W, r0)

Vth = -50 # mV

# Current of the modulatory input, applied only after 5ms
Iloc = 10

# TODO: find out what sol is
sol = r0
vt = V0
iSynt = np.dot(W, r) + Istim + Ibkg0
tau = np.array([[0.0280], [0.0080], [0.0160], [0.0160]])

for t in np.arange(dt, T, dt):
    if t > T/4:
        Istim[3] = Iloc
    # main computation
    iSyn = np.dot(W, r) + Istim + Ibkg0
    V = Vl + iSyn / gl
    iSynt = np.append(iSynt, iSyn, axis=1)
    vt = np.append(vt, V, axis=1)
    dr = dt * (-r + calculate_phi(V)) / tau_r
    r = r + dr
    sol = np.append(sol, r, axis=1)

#----------------------------------------------------------------------------------------------------------------------
# Plots
#----------------------------------------------------------------------------------------------------------------------
# Beautifying with the axis
timeLine = np.arange(0, T, dt)

# Plot rate over time
plt.plot(timeLine, sol[0, :], 'b')
plt.plot(timeLine, sol[1, :], 'r')
plt.plot(timeLine, sol[2, :], 'm')
plt.plot(timeLine, sol[3, :], 'g')
plt.show()

# Plot rate over time (selected range)
timeLine = timeLine - T/4 + 5
plt.xlim(xmin=0, xmax=20)
plt.plot(timeLine, sol[0, :], 'b')
plt.plot(timeLine, sol[1, :], 'r')
plt.plot(timeLine, sol[2, :], 'm')
plt.plot(timeLine, sol[3, :], 'g')
plt.show()

# Plot membrane voltage over time
plt.figure()
plt.plot(timeLine, vt[0, :], 'b')
plt.plot(timeLine, vt[1, :], 'r')
plt.plot(timeLine, vt[2, :], 'm')
plt.plot(timeLine, vt[3, :], 'g')
plt.show()

# Plot iSyn over time
plt.figure()
plt.plot(timeLine, iSynt[0, :], 'b')
plt.plot(timeLine, iSynt[1, :], 'r')
plt.plot(timeLine, iSynt[2, :], 'm')
plt.plot(timeLine, iSynt[3, :], 'g')
plt.show()

print('done')