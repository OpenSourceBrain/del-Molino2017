from GenerateRandomPopulationLEMS import generatePopulationLEMS, generatePopulationSimulationLEMS

# Size of the network for e, pv, sst, vip, respectively
n_pop = [800, 100, 50, 50]
# n_pop = [80, 10, 5, 5]
# n_pop = [1, 1, 1, 1]
# test values
# n_pop = [200, 25, 12, 12]
# Iterate over the different combination of populations and create a random connectivity between the units
pops = ['exc', 'pv', 'sst', 'vip']
amplitudes = {
              'high':  ['147.2512 pA', '386.7281 pA', '40.2657 pA', '98.4368 pA'],
              'low': ['115.03 pA', '233.66 pA', '94.31 pA', '89.91 pA']
             }
baselines = ['high', 'low']
# duration of the simulation
sim_length = 300 #ms
# time delay until the modulatory current is applied
delay = 100 #ms
# todo: fill in the correct arguments and make it run for the e population
for baseline in baselines:
    generatePopulationLEMS(pops, n_pop, amplitudes[baseline], baseline,
                           sim_length, delay)
    generatePopulationSimulationLEMS(n_pop, baseline, pops, sim_length)

