from neuromllite import Network, Cell, InputSource, Population, Synapse,RectangularRegion,RandomLayout
from neuromllite import Projection, RandomConnectivity, Input, Simulation
from neuromllite.NetworkGenerator import generate_and_run
from neuromllite.NetworkGenerator import generate_neuroml2_from_network
import sys

#######################################Low Baseline###########################################

################################################################################
###   Build new network

net = Network(id='delMolinoEtAl_low_baseline')

net.notes = 'delMolinoEtAl eLife 2017: low baseline parameters'

net.parameters = {}
net.parameters['baseline_current_Exc'] = '0.11503  nA'
net.parameters['baseline_current_PV'] = '0.23366 nA' 
net.parameters['baseline_current_SST'] = '0.09431 nA' 
net.parameters['baseline_current_VIP'] = '0.08991 nA'
#net.parameters['baseline_current_Exc'] = '0.0  nA'
#net.parameters['baseline_current_PV'] = '0.0 nA' 
#net.parameters['baseline_current_SST'] = '0.0 nA' 
#net.parameters['baseline_current_VIP'] = '0.0 nA'
net.parameters['global_offset_current'] = '0.0 nA'
net.parameters['mod_current_VIP'] = '0.01 nA'

net.parameters['weight_scale_Exc'] =  1
net.parameters['weight_scale_PV'] =  1
net.parameters['weight_scale_SST'] =  1
net.parameters['weight_scale_VIP'] =  1

net.parameters['delay_baseline_curr'] =  '0ms'
net.parameters['delay_vip_mod_curr'] =  '5ms'


excCell = Cell(id='EXC', lems_source_file='RateBasedSpecifications_low_baseline.xml')
net.cells.append(excCell)
pvCell = Cell(id='PV', lems_source_file='RateBasedSpecifications_low_baseline.xml')
net.cells.append(pvCell)
sstCell = Cell(id='SST', lems_source_file='RateBasedSpecifications_low_baseline.xml')
net.cells.append(sstCell)
vipCell = Cell(id='VIP', lems_source_file='RateBasedSpecifications_low_baseline.xml')
net.cells.append(vipCell)

cell = Cell(id='ifcell', pynn_cell='IF_cond_alpha')
cell.parameters = { "tau_refrac":5, "i_offset":.1 }
#net.cells.append(cell)


vip_mod_current = InputSource(id='vip_mod_current',
                            neuroml2_input='PulseGenerator',
                            parameters={'amplitude':'mod_current_VIP', 'delay':'delay_vip_mod_curr', 'duration':'100 ms'})

net.input_sources.append(vip_mod_current)

r1 = RectangularRegion(id='network', x=0,y=0,z=0,width=100,height=100,depth=10)
net.regions.append(r1)

colors = [[8,48,107],         # dark-blue
          [228,26,28],        # red
          [152,78,163],       # purple
          [77,175,74]]

color_str = {}
for i in range(len(colors)):
    color_str[i] = ''
    for c in colors[i]:
        color_str[i]+='%s '%(c/255.)
    color_str[i] = color_str[i][:-1]

pE = Population(id='Exc', size=1, component=excCell.id, properties={'color':color_str[0]},random_layout = RandomLayout(region=r1.id))
pPV = Population(id='PV', size=1, component=pvCell.id, properties={'color':color_str[1]},random_layout = RandomLayout(region=r1.id))
pSST = Population(id='SST', size=1, component=sstCell.id, properties={'color':color_str[2]},random_layout = RandomLayout(region=r1.id))
pVIP = Population(id='VIP', size=1, component=vipCell.id, properties={'color':color_str[3]},random_layout = RandomLayout(region=r1.id))

net.populations.append(pE)
net.populations.append(pPV)
net.populations.append(pSST)
net.populations.append(pVIP)


pops = [pE,pPV,pSST,pVIP]


r_syn = Synapse(id='rs', lems_source_file='RateBasedSpecifications_low_baseline.xml')
net.synapses.append(r_syn)


W = [[2.4167,   -0.3329,   -0.8039,         0],
    [2.9706,   -3.4554,   -2.1291,         0],
    [4.6440,         0,         0,   -2.7896],
    [0.7162,         0,   -0.1560,         0]]

for pre in pops:
    for post in pops:

        weight = W[pops.index(post)][pops.index(pre)]
        print('Connection %s -> %s weight %s'%(pre.id, post.id, weight))
        if weight!=0:

            net.projections.append(Projection(id='proj_%s_%s'%(pre.id,post.id),
                                                                presynaptic=pre.id,
                                                                postsynaptic=post.id,
                                                                synapse='rs',
                                                                type='continuousProjection',
                                                                delay=0,
                                                                weight='weight_scale_%s * %s' % (pre.id, weight),
                                                                random_connectivity=RandomConnectivity(probability=1)))

#Individual Currents
for pop in pops:

    input_source = InputSource(id='baseline_exc_%s'%pop.id,
                               neuroml2_input='PulseGenerator',
                               parameters={'amplitude':'baseline_current_%s'%pop.id, 'delay':'delay_baseline_curr', 'duration':'2000 ms'})

    net.input_sources.append(input_source)
    
    net.inputs.append(Input(id='baseline_curr_%s'%pop.id,
                            input_source=input_source.id,
                            population=pop.id,
                            percentage=100))

#Global Offset Current
for pop in pops:

    input_source = InputSource(id='global_offset_curr_%s'%pop.id,
                               neuroml2_input='PulseGenerator',
                               parameters={'amplitude':'global_offset_current', 'delay':'delay_baseline_curr', 'duration':'2000 ms'})

    net.input_sources.append(input_source)
    
    net.inputs.append(Input(id='global_offset_curr_%s'%pop.id,
                            input_source=input_source.id,
                            population=pop.id,
                            percentage=100))

#Modulation Current
net.inputs.append(Input(id='modulation',
                        input_source=vip_mod_current.id,
                        population=pVIP.id,
                        percentage=100))

print(net)
print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)
new_file_y = net.to_yaml_file('%s.yaml'%net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='SimdelMolinoEtAl_low_baseline',
                 network=new_file,
                 duration='20',
                 dt='0.01',
                 record_rates={'all':'*'}) 
'''record_traces={'all':'*'},'''

sim.to_json_file()



################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)


#################################High Baseline##############################

################################################################################
###   Build new network

net.id = "delMolinoEtAl_high_baseline"
net.notes = 'delMolinoEtAl eLife 2017: high baseline parameters'

net.parameters['baseline_current_Exc'] = '0.14725  nA'
net.parameters['baseline_current_PV'] = '0.38673 nA' 
net.parameters['baseline_current_SST'] = '0.04027 nA' 
net.parameters['baseline_current_VIP'] = '0.09844 nA' 
net.parameters['global_offset_current'] = '0.0 nA'
net.parameters['mod_current_VIP'] = '0.01 nA'

net.cells = []
net.synapses = []

excCell = Cell(id='EXC', lems_source_file='RateBasedSpecifications_high_baseline.xml')
net.cells.append(excCell)
pvCell = Cell(id='PV', lems_source_file='RateBasedSpecifications_high_baseline.xml')
net.cells.append(pvCell)
sstCell = Cell(id='SST', lems_source_file='RateBasedSpecifications_high_baseline.xml')
net.cells.append(sstCell)
vipCell = Cell(id='VIP', lems_source_file='RateBasedSpecifications_high_baseline.xml')
net.cells.append(vipCell)

r_syn = Synapse(id='rs', lems_source_file='RateBasedSpecifications_high_baseline.xml')
net.synapses.append(r_syn)

print(net)
print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)
new_file_y = net.to_yaml_file('%s.yaml'%net.id)

################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='SimdelMolinoEtAl_high_baseline',
                 network=new_file,
                 duration='20',
                 dt='0.01',
                 record_rates={'all':'*'}) 
'''record_traces={'all':'*'},'''

sim.to_json_file()

################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)