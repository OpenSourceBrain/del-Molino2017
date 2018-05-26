from pyneuroml.lems.LEMSSimulation import LEMSSimulation

# Create LEMS file
sim_id = 'fIeSim'
ls = LEMSSimulation(sim_id, 200, 0.1, 'net2')

# Add additional LEMS file
# Add Rate Base Components
ls.include_lems_file('RateBased.xml', include_included=True)
# Add specifications for these Rate Based Components
ls.include_lems_file('RateBasedSpecifications_high_baseline.xml', include_included=True)
# Add the the network definition
ls.include_lems_file('fi.nml', include_included=True)

# Display outputs
disp0 = 'Rate'
ls.create_display(disp0, 'Rates', '-2', '45')
ls.add_line_to_display(disp0, 'e0', 'ePop[0]/r', color='#0000ff')
ls.add_line_to_display(disp0, 'e11', 'ePop[11]/r', color='#DDA0DD')
ls.add_line_to_display(disp0, 'e19', 'ePop[19]/r', color='#00ff00')

disp1 = 'Voltage'
ls.create_display(disp1, 'Voltages', '-.072', '-.035')
ls.add_line_to_display(disp1, 'e0', 'ePop[0]/V', color='#0000ff')
ls.add_line_to_display(disp1, 'e11', 'ePop[11]/V', color='#DDA0DD')
ls.add_line_to_display(disp1, 'e19', 'ePop[19]/V', color='#00ff00')

# Create output file
of1 = 'of1'
ls.create_output_file(of1, 'fI0.dat')
ls.add_column_to_output_file(of1, 'e', 'ePop[0]/r')

ls.save_to_file()
















#
# # find a way to load the rateCell definition
# sim_id = 'sim1'
# duration = 200
# dt = .1
# lems_file = 'RateBased.xml'
# lems = LEMSSimulation(sim_id, duration, dt)
# lems.include_lems_file(lems_file, include_included=True)

# pass Vth, V, Vl, g for the rate cell

# # Create Silent Synapse
# silent_syn = SilentSynapse(id='silent1')
# nml_doc.silent_synapses.append(silent_syn)
#
# # import the rateSynapse
#
# # Create PulseGenerator (iterate over different amplitudes)
# pulse = PulseGenerator(id='baseline_e', delay=0, duration=200, amplitude=amplitude_e[test])
# nml_doc.pulse_generators.append(pulse)
#
# net = Network(id='netfI')
# nml_doc.networks.append(net)
#
# pop_e = Population(id='ePop', component='E', size=n_units)
# net.populations.append(pop_e)
#
# for unit in range(n_units):
#     exp_input = ExplicitInput(target='ePop[%i]' %unit, input='baseline_e', destination='synapses')
#     net.explicit_inputs.append(exp_input)
#
# print 'hi'
