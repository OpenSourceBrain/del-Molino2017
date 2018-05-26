from pyneuroml.lems.LEMSSimulation import LEMSSimulation

# Create LEMS file
sim_id = 'PopulationRateSim'
ls = LEMSSimulation(sim_id, 10, 0.1, 'net2')

# Add additional LEMS file
# Add Rate Base Components
ls.include_lems_file('RateBased.xml', include_included=True)
# Add specifications for these Rate Based Components
ls.include_lems_file('RateBasedSpecifications_high_baseline.xml', include_included=True)
# Add the the network definition
ls.include_neuroml2_file('RandomPopulationRate.nml')

# Display outputs
disp0 = 'd0'
ls.create_display(disp0, 'Rates', '0', '25')
ls.add_line_to_display(disp0, 'e', 'ePop[0]/r', color='#0000ff')
ls.add_line_to_display(disp0, 'pv', 'pvPop[0]/r', color='#ff0000')
ls.add_line_to_display(disp0, 'sst', 'sstPop[0]/r', color='#DDA0DD')
ls.add_line_to_display(disp0, 'vip', 'vipPop[0]/r', color='#00ff00')

# Create output file
of1 = 'of1'
ls.create_output_file(of1, 'rates_network_model_py.dat')
ls.add_column_to_output_file(of1, 'e', 'ePop[0]/r')
ls.add_column_to_output_file(of1, 'pv', 'ePop[0]/r')
ls.add_column_to_output_file(of1, 'sst', 'ePop[0]/r')
ls.add_column_to_output_file(of1, 'vip', 'ePop[0]/r')

ls.save_to_file()
