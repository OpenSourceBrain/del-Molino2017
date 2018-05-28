import os
import numpy as np
import matplotlib.pyplot as plt
from pyneuroml import pynml

from GeneratefILEMS import generateLEMS, generatefISimulationLEMS

n_units = 20
baselines = ['low', 'high']
max_amplitude = [220, 270, 165, 165]
min_amplitude = [60, 90, 45, 45]
populations = ['e', 'pv', 'sst', 'vip']
colours = ['blue', 'red', 'darkorchid', 'green']


r = {}
v = {}

for baseline in baselines:
    print('Analysing %s baseline' %baseline)
    plt.figure()
    for population_idx, population in enumerate(populations):

        generateLEMS(population, n_units, max_amplitude[population_idx], min_amplitude[population_idx])

        generatefISimulationLEMS(population, n_units)

        lems_file = 'LEMS_fISim_%s.xml' %population

        # Run simulation
        # cleanup: remove the .dat file after loading them
        results = pynml.run_lems_with_jneuroml(lems_file, nogui=True, load_saved_data=True, cleanup=True)
        # get the last values of the simulation and plot the fI Curve

        r[population] = np.zeros((n_units))
        v[population] = np.zeros((n_units))
        for unit in range(n_units):
            pop_unit_r = '%sPop[%d]/r' %(population, unit)
            pop_unit_V = '%sPop[%d]/V' %(population, unit)
            r[population][unit] = results[pop_unit_r][-1]
            v[population][unit] = results[pop_unit_V][-1]

        plt.plot(v[population], r[population], color=colours[population_idx])

        # load the low_baseline results and plot them on the fI curve
        baseline_lems = '../Fig1/LEMS_RateBased_%s_baseline.xml' %baseline
        results_baseline = pynml.run_lems_with_jneuroml(baseline_lems, nogui=True, load_saved_data=True, cleanup=True)
        population_v = '%sPop[0]/V' %population
        population_r = '%sPop[0]/r' %population
        # Note: I am taking the first time point as at time point 0 the membrane voltage has not yet reached the baseline
        #  activity steady-state
        plt.plot(results_baseline[population_v][1], results_baseline[population_r][1], 'o', color=colours[population_idx])
        print('')
    plt.xlabel('Voltage (V)')
    plt.ylabel('Rate (Hz)')
    plt.xlim(-.060, -.040)
    plt.ylim(0, 60)
    plot_name = 'fI_%s_baseline.png' %baseline
    plt.savefig(plot_name)
