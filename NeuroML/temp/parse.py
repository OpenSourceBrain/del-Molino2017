from neuromllite import Network, Population, Projection, RandomConnectivity

import random

################################################################################
###   Build a new network

net = Network(id='net0')
net.notes = "...."

f = open('Neuron_2015_Table.csv')
all_tgts = []

for l in f:
    #print l
    w = l.split(',')
    tgt = w[0]
    src = w[1]
    if tgt!='TARGET':
        if not tgt in all_tgts:
            all_tgts.append(tgt)
        
print all_tgts
print(len(all_tgts))

f = open('Neuron_2015_Table.csv')
pop_ids = []

for l in f:
    #print l
    w = l.split(',')
    tgt = w[0]
    src = w[1]
    if tgt!='TARGET' and src in all_tgts:
        fln = float(w[2])
        print('Adding conn from %s to %s with FLN: %s'%(src,tgt,fln))
        for pop_id in [tgt,src]:
            if not pop_id in pop_ids:
                p0 = Population(id=pop_id, size=1, component='iaf', properties={'color':'%s %s %s'%(random.random(),random.random(),random.random())})

                net.populations.append(p0)
                pop_ids.append(pop_id)


        ################################################################################
        ###   Add a projection

        if fln>0.0:
            net.projections.append(Projection(id='proj_%s_%s'%(src,tgt),
                                              presynaptic=src, 
                                              postsynaptic=tgt,
                                              synapse='ampa',
                                              weight=fln))

            #net.projections[0].random_connectivity=RandomConnectivity(probability=0.5)



print(net)
net.id = 'TestNetwork'

print(net.to_json())
new_file = net.to_json_file('Example1_%s.json'%net.id)


################################################################################
###   Export to some formats
###   Try:
###        python Example1.py -graph2

from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite import Simulation
import sys

check_to_generate_or_run(sys.argv, Simulation(id='SimExample1',network=new_file))

