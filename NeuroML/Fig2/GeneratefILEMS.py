import os
import numpy as np
import math
from neuroml import (NeuroMLDocument, PulseGenerator, SilentSynapse, Network, ExplicitInput, Population, )
import neuroml.writers as writers
from pyneuroml.lems.LEMSSimulation import LEMSSimulation


def generateLEMS(population, n_units, max_amplitude, min_amplitude):
    def generatePulse(population, idx, amplitude):
        pulse = PulseGenerator(id='baseline_%s%d' %(population, idx), delay='0ms', duration='200ms',
                               amplitude='%.02f pA' %amplitude)
        nml_doc.pulse_generators.append(pulse)


    def generatePopulation(population, n_units, net):
        population_uc = population.upper()
        pop = Population(id='%sPop' %population, component='%s' %population_uc, size=n_units)
        net.populations.append(pop)


    def generateExmplicitInput(population, idx, net):
            exp_input = ExplicitInput(target='%sPop[%d]' %(population, idx), input='baseline_%s%d' %(population, idx),
                                      destination='synapses')
            net.explicit_inputs.append(exp_input)


    nml_doc = NeuroMLDocument(id='fI_%s' %population)

    # Add silent synapsis
    silent_syn = SilentSynapse(id='silent1_%s' %population)
    nml_doc.silent_synapses.append(silent_syn)

    step = (max_amplitude - min_amplitude)/n_units
    amplitudes = np.arange(min_amplitude, max_amplitude, step)

    net = Network(id='net_%s' %population)
    nml_doc.networks.append(net)
    generatePopulation('%s' %population, n_units, net)

    for idx, amplitude in enumerate(amplitudes):
        generatePulse('%s' %population, idx, amplitude)

        generateExmplicitInput('%s' %population, idx,  net)

    # Write to file
    nml_file = 'fI_%s.nml' %population
    writers.NeuroMLWriter.write(nml_doc, nml_file)
    print('Written network file to: %s' %nml_file)

    # Validate the NeuroML
    from neuroml.utils import validate_neuroml2
    validate_neuroml2(nml_file)


def generatefISimulationLEMS(population, units):
    # Create LEMS file
    sim_id = 'LEMS_fISim_%s.xml' %population
    ls = LEMSSimulation(sim_id, 200, 0.1, 'net_%s' %population)

    # Add additional LEMS file
    # Add Rate Base Components
    ls.include_lems_file('../RateBased.xml', include_included=True)
    # Add specifications for these Rate Based Components
    ls.include_lems_file('../RateBasedSpecifications_high_baseline.xml', include_included=True)
    # Add the network definition
    ls.include_lems_file('fI_%s.nml' %population, include_included=True)

    # Display outputs and check the results plot the lowest, middle and highest values
    middle = math.ceil(units/2)
    disp0 = 'Rate'
    ls.create_display(disp0, 'Rates', '-2', '45')
    ls.add_line_to_display(disp0, '%s0'  % population,           '%sPop[0]/r'  % population,           color='#0000ff')
    ls.add_line_to_display(disp0, '%s%d' %(population, middle),  '%sPop[%d]/r' %(population, middle),  color='#DDA0DD')
    ls.add_line_to_display(disp0, '%s19' % population,           '%sPop[19]/r' % population,           color='#00ff00')

    disp1 = 'Voltage'
    ls.create_display(disp1, 'Voltages', '-.072', '-.035')
    ls.add_line_to_display(disp1, '%s0' % population         , '%sPop[0]/V' % population,          color='#0000ff')
    ls.add_line_to_display(disp1, '%s%d'%(population, middle), '%sPop[%d]/V'%(population, middle), color='#DDA0DD')
    ls.add_line_to_display(disp1, '%s19'% population         , '%sPop[19]/V'% population,          color='#00ff00')

    # Create output file
    of1 = 'of1'
    ls.create_output_file(of1, 'fI_%s.dat' % population)
    for unit in range(units):
        ls.add_column_to_output_file(of1, 'r%d' % unit, '%sPop[%d]/r' % (population, unit))
        ls.add_column_to_output_file(of1, 'V%d' % unit, '%sPop[%d]/V' % (population, unit))

    save_path = os.path.join(sim_id)
    ls.save_to_file(file_name=save_path)

