
from neuromllite.utils import load_simulation_json
from neuromllite.utils import load_network_json
from neuromllite.NetworkGenerator import generate_and_run

import numpy as np
import matplotlib.pyplot as plt

pops_vs_colors = {'Exc':'b','SST':'m','PV':'r','VIP':'g'}

pre_mod_vals = {}
post_mod_vals = {}

def analyse(version):

    sim = load_simulation_json('Sim%s.json'%version)
    net = load_network_json('%s.json'%version)

    net.parameters['weight_scale_SST'] = 0
    net.parameters['delay_vip_mod_curr'] = '100s'

    traces, events = generate_and_run(sim, 
                                      network=net, 
                                      simulator="jNeuroML",
                                      base_dir='./',
                                      target_dir='./',
                                      return_results=True)

    fig, ax = plt.subplots()
    plt.get_current_fig_manager().set_window_title('Rate traces: %s'%version)

    for key in sorted(traces.keys()):
        if key != "t":
            ts = traces['t']
            vs = traces[key]
            pop = key.split('/')[0]

            color = 'k' # black
            colour = pops_vs_colors[pop]
            ax.plot(ts,vs, label=pop, color=colour)
            ax.legend()
                                    
            plt.xlabel("Time (s)")
            plt.ylabel("(SI units)")

            pre_mod_vals[pop] = vs[0]
            post_mod_vals[pop] = vs[-1]
    
    pops = [pop for pop in pops_vs_colors.keys()]
    rates = [pre_mod_vals[pop]for pop in pops_vs_colors.keys()]
    colors = pops_vs_colors.values()

    fig, ax = plt.subplots()
    plt.get_current_fig_manager().set_window_title('Steady state rates (start simulation): %s'%version)
    ax.set_ylabel('Avg firing rate (Hz)')
    ax.bar(pops, rates, color=colors)

    fig, ax = plt.subplots()
    plt.get_current_fig_manager().set_window_title('Steady state rates (end simulation): %s'%version)
    ax.set_ylabel('Avg firing rate (Hz)')
    rates = [post_mod_vals[pop]for pop in pops_vs_colors.keys()]
    ax.bar(pops, rates, color=colors)

    

if __name__ == '__main__':

    for v in ['delMolinoEtAl_low_baseline','delMolinoEtAl_high_baseline']:
        analyse(v)

    plt.show()