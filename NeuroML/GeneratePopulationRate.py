import numpy as np
from random import random

from neuroml import (NeuroMLDocument, Network, Population, ContinuousConnectionInstanceW, ContinuousProjection,
                     ExplicitInput)
import neuroml.writers as writers

# This script generates a new xml file that describes the connection between the different network population


def generatePopulationProjection(from_pop, to_pop, n_from_pop, n_to_pop, p_to_from_pop, from_unit, to_unit, net):
    connection_count = 0
    for idx_from_pop in range(n_from_pop):
        for idx_to_pop in range(n_to_pop):
            if random() <= p_to_from_pop:
                projection = ContinuousProjection(id='%s%i_%s%i' %(from_unit, idx_from_pop, to_unit, idx_to_pop),
                                                  presynaptic_population=from_pop,
                                                  postsynaptic_population=to_pop)
                net.continuous_projections.append(projection)
                connection = ContinuousConnectionInstanceW(id=connection_count,
                                                           pre_cell='../%s[%i]' %(from_pop, idx_from_pop),
                                                           post_cell='../%s[%i]' %(to_pop, idx_to_pop),
                                                           pre_component='silent1',
                                                           post_component='rs',
                                                           weight=p_to_from_pop * n_from_pop)
                projection.continuous_connection_instance_ws.append(connection)
                connection_count += 1


def run():
    # Size of the network for e, pv, sst, vip, respectively
    #n_pop = [800, 100, 50, 50]
    # test values
    n_pop = [6, 4, 2, 2]

    # Connection probabilities for each unit in the population
    p_to_from_pops = np.array([[0.02, 1,    1,     0],
                               [0.01, 1, 0.85,     0],
                               [0.01, 0,    0, -0.55],
                               [0.01, 0,  0.5,     0]])

    nml_doc = NeuroMLDocument(id='RandomPopulation')

    # Create the network and add the 4 different populations
    net = Network(id='net2')
    nml_doc.networks.append(net)

    pop_e   = Population(id='ePop',   component='E',   size=n_pop[0])
    pop_pv  = Population(id='pvPop',  component='PV',  size=n_pop[1])
    pop_sst = Population(id='sstPop', component='SST', size=n_pop[2])
    pop_vip = Population(id='vipPop', component='VIP', size=n_pop[3])
    net.populations.append(pop_e)
    net.populations.append(pop_pv)
    net.populations.append(pop_sst)
    net.populations.append(pop_vip)

    # Iterate over the different combination of populations and create a random connectivity between the units
    pops = ['ePop', 'pvPop', 'sstPop', 'vipPop']
    units = ['e', 'pv', 'sst', 'vip']
    for from_idx, from_unit in enumerate(units):
        for to_idx, to_unit in enumerate(units):
            generatePopulationProjection(pops[from_idx], pops[to_idx], n_pop[from_idx], n_pop[to_idx],
                                         p_to_from_pops[to_idx, from_idx], from_unit, to_unit, net)

    # Add inputs
    for unit_idx, unit in enumerate(units):
        for n_idx in range(n_pop[unit_idx]):
            exp_input = ExplicitInput(target='%s[%i]' %(unit, n_idx), input='baseline_%s' %unit, destination='synapses')
            net.explicit_inputs.append(exp_input)

            # if vip add modulatory input
            if unit == 'vip':
                mod_input = ExplicitInput(target='vip[%i]' %n_idx, input='modVIP', destination='synapses')
                net.explicit_inputs.append(mod_input)

    # Write to file
    nml_file = 'RandomPopulationRate.nml'
    writers.NeuroMLWriter.write(nml_doc, nml_file)
    print('Written network file to: %s' %nml_file)

    # Validate the NeuroML
    from neuroml.utils import validate_neuroml2
    validate_neuroml2(nml_file)


run()