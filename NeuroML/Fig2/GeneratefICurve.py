import matplotlib.pyplot as plt

from GeneratefILEMS import generateLEMS, generatefISimulationLEMS

n_units = 20
baselines = ['low', 'high']
max_amplitude = [220, 270, 165, 165]
min_amplitude = [60, 90, 45, 45]
populations = ['exc', 'pv', 'sst', 'vip']
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
