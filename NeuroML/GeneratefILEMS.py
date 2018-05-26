import numpy as np
from neuroml import (NeuroMLDocument, PulseGenerator, SilentSynapse, Network, ExplicitInput, Population, )
import neuroml.writers as writers
from neuroml import SilentSynapse, PulseGenerator


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


nml_doc = NeuroMLDocument(id='fI')

# Add silent synapsis
silent_syn = SilentSynapse(id='silent1')
nml_doc.silent_synapses.append(silent_syn)

n_units = 20
max_amplitude = 200
min_amplitude = 60
step = (max_amplitude - min_amplitude)/n_units
amplitudes = np.arange(min_amplitude, max_amplitude, step)

net = Network(id='net2')
nml_doc.networks.append(net)
generatePopulation('e', n_units, net)

for idx, amplitude in enumerate(amplitudes):
    generatePulse('e', idx, amplitude)

    generateExmplicitInput('e', idx,  net)

# Write to file
nml_file = 'fI.nml'
writers.NeuroMLWriter.write(nml_doc, nml_file)
print('Written network file to: %s' %nml_file)

# Validate the NeuroML
from neuroml.utils import validate_neuroml2
validate_neuroml2(nml_file)


