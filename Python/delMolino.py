
import numpy as np
import sys


def calculate_phi(Vss, Vth, Vr):
    tau = np.array([[0.0288], [0.0080], [0.0160], [0.0160]])
    # Note: If you do not define sV as int you will end up lost precision
    sV = np.ones((4, 1)) # noise (mV)

    '''This calculates the average rate of each population'''
    return (Vss - Vth) / (tau * (Vth - Vr) * (1 - np.exp(-(Vss - Vth) /sV)))


def calculate_population_rate(r, Ibkg, sol, Vl, Vth, T, dt):
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
    vt = np.ones((4, 1)) * Vl

    for t in np.arange(dt, T, dt):
        if t > T/4:
            Istim[3] = Iloc
        # main computation
        iSyn = np.dot(W, r) + Istim + Ibkg
        V = Vl + (iSyn / gl)
        iSynt = np.append(iSynt, iSyn, axis=1)
        vt = np.append(vt, V, axis=1)
        # dr = dt * (-r + calculate_phi(V, Vth, Vr))
        dr = dt * (-r + calculate_phi(V, Vth, Vr)) / tau_r
        r = r + dr
        sol = np.append(sol, r, axis=1)

    return sol, vt, iSynt

# Settings:
T = 200
dt = 0.1
Vl = -70
Vth = -50 # mV
Vr = -60 # mV
Vr_fI = -40

debug = False
#----------------------------------------------------------------------------------------------------------------------
#                                           Low Baseline Activity
#----------------------------------------------------------------------------------------------------------------------
# spontaneous average rate
r0_low = np.array([[1], [10], [3], [2]])
Ibkg_low = np.array([[115.03], [233.66], [94.31], [89.91]])
sol_low = r0_low
sol_low, vt_low, iSynt_low = calculate_population_rate(r0_low, Ibkg_low, sol_low, Vl, Vth,  T, dt)

# Plots
#----------------------------------------------------------------------------------------------------------------------
# Beautifying with the axis
timeLine = np.arange(0, T, dt)

# Plot rate over time (selected range)
timeLine = timeLine - T/4 + 5

if not '-nogui' in sys.argv:
    import matplotlib
    import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.get_current_fig_manager().set_window_title("Low baseline activity: rates")
    plt.plot(timeLine, sol_low[0, :], 'b')
    plt.plot(timeLine, sol_low[1, :], 'r')
    plt.plot(timeLine, sol_low[2, :], 'm')
    plt.plot(timeLine, sol_low[3, :], 'g')
    plt.xlim(xmin=0, xmax=20)

if debug:
    # Plot membrane
    plt.figure()
    plt.plot(timeLine, vt_low[0, :], 'b')
    plt.plot(timeLine, vt_low[1, :], 'r')
    plt.plot(timeLine, vt_low[2, :], 'm')
    plt.plot(timeLine, vt_low[3, :], 'g')

    # Plot iSyn over time
    plt.figure()
    plt.plot(timeLine, iSynt_low[0, :], 'b')
    plt.plot(timeLine, iSynt_low[1, :], 'r')
    plt.plot(timeLine, iSynt_low[2, :], 'm')
    plt.plot(timeLine, iSynt_low[3, :], 'g')

# Plot f-I Curve
V_Vec = np.arange(Vr, Vr_fI, 0.15)
rr = np.zeros((len(V_Vec), 4))
for idx, VV in enumerate(V_Vec):
    VV_pop = np.ones((4, 1)) * VV
    rr[idx, :] = calculate_phi(VV_pop, Vth, Vr).ravel()

if not '-nogui' in sys.argv:
    fig = plt.figure()
    plt.get_current_fig_manager().set_window_title("Low baseline activity: tuning curves")
    plt.plot(V_Vec, rr[:, 0], label='ePop', color='blue')
    plt.plot(V_Vec, rr[:, 1], label='pvPop', color='red')
    plt.plot(V_Vec, rr[:, 2], label='sstPop', color='darkorchid')
    plt.plot(V_Vec, rr[:, 3], label='vipPop', color='green')

    # get the markers from your calculate_population function
    plt.plot(vt_low[:, 1][0], sol_low[:, 1][0], 'o', color='blue')
    plt.plot(vt_low[:, 1][1], sol_low[:, 1][1], 'o', color='red')
    plt.plot(vt_low[:, 1][2], sol_low[:, 1][2], 'o', color='darkorchid')
    plt.plot(vt_low[:, 1][3], sol_low[:, 1][3], 'o', color='green')

    plt.plot()
    plt.xlabel('Voltage (ms)')
    plt.ylabel('r (Hz)')
    plt.ylim(ymin=0, ymax=60)
    plt.legend(loc=(1.04,0))

#----------------------------------------------------------------------------------------------------------------------
#                                           High Baseline Activity
#----------------------------------------------------------------------------------------------------------------------
# spontaneous average rate
r0_high = np.array([[30], [50], [30], [20]])
# those are not mentioned on the paper
Ibkg_high = np.array([[147.2512], [386.7281], [40.2657], [98.4368]])
sol_high = r0_high
sol_high, vt_high, iSynt_high = calculate_population_rate(r0_high, Ibkg_high, sol_high, Vl, Vth, T, dt)

# Beautifying with the axis
timeLine = np.arange(0, T, dt)
# Plot rate over time (selected range)
timeLine = timeLine - T/4 + 5

if not '-nogui' in sys.argv:
    fig = plt.figure()
    plt.get_current_fig_manager().set_window_title("High baseline activity: rates")
    plt.plot(timeLine, sol_high[0, :], 'b')
    plt.plot(timeLine, sol_high[1, :], 'r')
    plt.plot(timeLine, sol_high[2, :], 'm')
    plt.plot(timeLine, sol_high[3, :], 'g')
    plt.xlim(xmin=0, xmax=20)

if debug:
    # Plot membrane voltage over time
    plt.figure()
    plt.plot(timeLine, vt_high[0, :], 'b')
    plt.plot(timeLine, vt_high[1, :], 'r')
    plt.plot(timeLine, vt_high[2, :], 'm')
    plt.plot(timeLine, vt_high[3, :], 'g')

    # Plot iSyn over time
    plt.figure()
    plt.plot(timeLine, iSynt_high[0, :], 'b')
    plt.plot(timeLine, iSynt_high[1, :], 'r')
    plt.plot(timeLine, iSynt_high[2, :], 'm')
    plt.plot(timeLine, iSynt_high[3, :], 'g')

# Plot f-I Curve
# Use the data for the low baseline activity population
if not '-nogui' in sys.argv:
    fig = plt.figure()
    plt.get_current_fig_manager().set_window_title("High baseline activity: tuning curves")
    plt.plot(V_Vec, rr[:, 0], label='ePop', color='blue')
    plt.plot(V_Vec, rr[:, 1], label='pvPop', color='red')
    plt.plot(V_Vec, rr[:, 2], label='sstPop', color='darkorchid')
    plt.plot(V_Vec, rr[:, 3], label='vipPop', color='green')

    # get the markers from your calculate_population function
    plt.plot(vt_high[:, 1][0], sol_high[:, 1][0], 'o', color='blue')
    plt.plot(vt_high[:, 1][1], sol_high[:, 1][1], 'o', color='red')
    plt.plot(vt_high[:, 1][2], sol_high[:, 1][2], 'o', color='darkorchid')
    plt.plot(vt_high[:, 1][3], sol_high[:, 1][3], 'o', color='green')

    plt.plot()
    plt.xlabel('Voltage (ms)')
    plt.ylabel('r (Hz)')
    plt.ylim(ymin=0, ymax=60)
    plt.legend(loc=(1.04,0))

    plt.show()

print('Done')
