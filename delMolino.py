import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


def calculate_phi(Vss, Vth):
    Vr = -60 # mV
    tau = np.array([[0.0288], [0.0080], [0.0160], [0.0160]])
    # Note: If you do not define sV as int you will end up lost precision
    sV = np.ones((4, 1), dtype=int) # noise (mV)

    '''This calculates the average rate of each population'''
    return (Vss - Vth) / (tau * (Vth - Vr) * (1 - np.exp(-(Vss - Vth) /sV)))

def calculate_population_rate(r, Ibkg, sol, T, dt):
    Vl = -70
    tau_r = 2
    # connectivity matrix
    W = np.array([[2.4167, -0.3329, -0.8039,       0],
                  [2.9706, -3.4554, -2.1291,       0],
                  [4.6440,       0,       0, -2.7896],
                  [0.7162,       0, -0.1560,       0]])
    Istim = np.zeros((4, 1))
    iSynt = np.dot(W, r) + Istim + Ibkg
    # Current of the modulatory input, applied only after 5ms
    Iloc = 10
    # define leak conductance (nS)
    gl = np.array([[6.25], [10], [5], [5]])
    Vth = -50 # mV
    vt = np.ones((4, 1)) * Vl

    for t in np.arange(dt, T, dt):
        if t > T/4:
            Istim[3] = Iloc
        # main computation
        iSyn = np.dot(W, r) + Istim + Ibkg
        V = Vl + (iSyn / gl)
        iSynt = np.append(iSynt, iSyn, axis=1)
        vt = np.append(vt, V, axis=1)
        dr = dt * (-r + calculate_phi(V, Vth))
        #dr = dt * (-r + calculate_phi(V, Vth)) / tau_r
        r = r + dr
        sol = np.append(sol, r, axis=1)

    return sol, vt, iSynt

# Settings:
T = 200
dt = 0.1
#----------------------------------------------------------------------------------------------------------------------
#                                           Low Baseline Activity
#----------------------------------------------------------------------------------------------------------------------
# spontaneous average rate
r0_low = np.array([[1], [10], [3], [2]])
Ibkg_low = np.array([[115.03], [233.66], [94.31], [89.91]])
sol_low = r0_low
sol_low, vt_low, iSynt_low = calculate_population_rate(r0_low, Ibkg_low, sol_low, T, dt)

# Plots
#----------------------------------------------------------------------------------------------------------------------
# Beautifying with the axis
timeLine = np.arange(0, T, dt)

# Plot rate over time (selected range)
timeLine = timeLine - T/4 + 5
plt.figure()
plt.plot(timeLine, sol_low[0, :], 'b')
plt.plot(timeLine, sol_low[1, :], 'r')
plt.plot(timeLine, sol_low[2, :], 'm')
plt.plot(timeLine, sol_low[3, :], 'g')
plt.xlim(xmin=0, xmax=20)
plt.show()

# Plot membrane voltage over time
plt.figure()
plt.plot(timeLine, vt_low[0, :], 'b')
plt.plot(timeLine, vt_low[1, :], 'r')
plt.plot(timeLine, vt_low[2, :], 'm')
plt.plot(timeLine, vt_low[3, :], 'g')
plt.show()

# Plot iSyn over time
plt.figure()
plt.plot(timeLine, iSynt_low[0, :], 'b')
plt.plot(timeLine, iSynt_low[1, :], 'r')
plt.plot(timeLine, iSynt_low[2, :], 'm')
plt.plot(timeLine, iSynt_low[3, :], 'g')
plt.show()


#----------------------------------------------------------------------------------------------------------------------
#                                           High Baseline Activity
#----------------------------------------------------------------------------------------------------------------------
# spontaneous average rate
r0_high = np.array([[30], [50], [30], [20]])
# those are not mentioned on the paper
Ibkg_high = np.array([[147.2512], [386.7281], [40.2657], [98.4368]])
sol_high = r0_high
sol_high, vt_high, iSynt_high = calculate_population_rate(r0_high, Ibkg_high, sol_high, T, dt)

# Beautifying with the axis
timeLine = np.arange(0, T, dt)
# Plot rate over time (selected range)
timeLine = timeLine - T/4 + 5

plt.figure()
plt.plot(timeLine, sol_high[0, :], 'b')
plt.plot(timeLine, sol_high[1, :], 'r')
plt.plot(timeLine, sol_high[2, :], 'm')
plt.plot(timeLine, sol_high[3, :], 'g')
plt.xlim(xmin=0, xmax=20)
plt.show()


print('done')