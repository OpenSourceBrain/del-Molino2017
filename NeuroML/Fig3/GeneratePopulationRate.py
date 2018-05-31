from GenerateRandomPopulationLEMS import generatePopulationLEMS, generatePopulationSimulationLEMS

# Size of the network for e, pv, sst, vip, respectively
# n_pop = [800, 100, 50, 50]
# test values
n_pop = [200, 25, 12, 12]
# Iterate over the different combination of populations and create a random connectivity between the units
pops = ['e', 'pv', 'sst', 'vip']
amplitudes = {
              'high':  ['147.2512 pA', '386.7281 pA', '40.2657 pA', '98.4368 pA'],
              'low': ['115.03 pA', '233.66 pA', '94.31 pA', '89.91 pA']
             }
baselines = ['high', 'low']

# todo: fill in the correct arguments and make it run for the e population
for baseline in baselines:
    generatePopulationLEMS(pops, n_pop, amplitudes[baseline], baseline)
    generatePopulationSimulationLEMS(n_pop, baseline, pops)

