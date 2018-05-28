import os
import numpy as np
import matplotlib.pyplot as plt
from pyneuroml import pynml

from GeneratefILEMS import generateLEMS, generatefISimulationLEMS

n_units = 20
max_amplitude = [220, 270, 165, 165]
min_amplitude = [60, 110, 45, 45]
populations = ['e', 'pv', 'sst', 'vip']
colours = ['blue', 'red', 'darkorchid', 'green']


r = {}
v = {}

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

    plt.plot(v[population], r[population], colours[population_idx])
plt.xlabel('Voltage (V)')
plt.ylabel('Rate (Hz)')
plt.xlim(-.060, -.040)
plt.ylim(0, 60)
plt.savefig('fI_high_baseline.png')
