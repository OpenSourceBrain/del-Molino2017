import numpy

from GeneratefILEMS import generateLEMS, generatefISimulationLEMS

n_units = 20
max_amplitude = [200]
min_amplitude = [60]
populations = ['e']

for population_idx, population in enumerate(populations):
    generateLEMS(population, n_units, max_amplitude[population_idx], min_amplitude[population_idx])
    generatefISimulationLEMS(population, n_units)