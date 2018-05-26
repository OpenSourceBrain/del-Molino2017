import numpy as np
import matplotlib.pyplot as plt
from pyneuroml import pynml

from GeneratefILEMS import generateLEMS, generatefISimulationLEMS

n_units = 20
max_amplitude = [200]
min_amplitude = [60]
populations = ['e']

for population_idx, population in enumerate(populations):
    generateLEMS(population, n_units, max_amplitude[population_idx], min_amplitude[population_idx])
    generatefISimulationLEMS(population, n_units)

lems_file = 'LEMS_fIeSim.xml'

# Run simulation
results = pynml.run_lems_with_jneuroml(lems_file, nogui=True, load_saved_data=True)
# get the last values of the simulation and plot the fI Curve
r = np.zeros((n_units))
v = np.zeros((n_units))
for unit in range(n_units):
    pop_unit_r = 'ePop[%d]/r' %unit
    pop_unit_V = 'ePop[%d]/V' %unit
    r[unit] = results[pop_unit_r][-1]
    v[unit] = results[pop_unit_V][-1]

plt.plot(v, r)
plt.xlabel('Voltage')
plt.ylabel('Rate')
plt.savefig('fI_high_baseline.png')
