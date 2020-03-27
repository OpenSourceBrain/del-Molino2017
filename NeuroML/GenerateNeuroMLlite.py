from neuromllite import Network, Cell, InputSource, Population, Synapse,RectangularRegion,RandomLayout
from neuromllite import Projection, RandomConnectivity, Input, Simulation
from neuromllite.NetworkGenerator import generate_and_run
from neuromllite.NetworkGenerator import generate_neuroml2_from_network
import sys

################################################################################
###   Build new network

net = Network(id='delMolinoEtAl')
net.notes = 'delMolinoEtAl eLife 2017'

net.parameters = { 'inputVIP':10 }

cell = Cell(id='ifcell', pynn_cell='IF_cond_alpha')
cell.parameters = { "tau_refrac":5, "i_offset":.1 }
net.cells.append(cell)


input_source0 = InputSource(id='iclamp0', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':10, 'start':50., 'stop':150.})
                           
net.input_sources.append(input_source0)

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

pE = Population(id='Exc', size=1, component=cell.id, properties={'color':color_str[0]},random_layout = RandomLayout(region=r1.id))
pPV = Population(id='PV', size=1, component=cell.id, properties={'color':color_str[1]},random_layout = RandomLayout(region=r1.id))
pSST = Population(id='SST', size=1, component=cell.id, properties={'color':color_str[2]},random_layout = RandomLayout(region=r1.id))
pVIP = Population(id='VIP', size=1, component=cell.id, properties={'color':color_str[3]},random_layout = RandomLayout(region=r1.id))

net.populations.append(pE)
net.populations.append(pVIP)
net.populations.append(pSST)
net.populations.append(pPV)

pops = [pE,pPV,pSST,pVIP]


net.synapses.append(Synapse(id='ampa', 
                            pynn_receptor_type='excitatory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':-10, 'tau_syn':2}))
net.synapses.append(Synapse(id='gaba', 
                            pynn_receptor_type='inhibitory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':-80, 'tau_syn':10}))

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
                                              synapse='ampa',
                                              delay=0,
                                              weight=weight))
                               
'''
bkgE = InputSource(id='bkgEstim', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':2, 'start':0., 'stop':1e6})
                        
net.input_sources.append(bkgE)

net.inputs.append(Input(id='bkgE',
                        input_source=bkgE.id,
                        population=pE.id,
                        percentage=100))'''
                        
                        
net.inputs.append(Input(id='modulation',
                        input_source=input_source0.id,
                        population=pVIP.id,
                        percentage=100))

print(net)
print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='SimdelMolinoEtAl',
                 network=new_file,
                 duration='200',
                 dt='0.025',
                 recordTraces={'all':'*'})
                 
sim.to_json_file()



################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)

                        
print('\n********************\n****  NOT YET COMPLETE! Connections & real cell need to be used!\n********************')
