import sys

import pprint; pp = pprint.PrettyPrinter(depth=6)

from neuromllite.sweep.ParameterSweep import ParameterSweep
from neuromllite.sweep.ParameterSweep import NeuroMLliteRunner
       

if __name__ == '__main__':

    heatmap_lims=[-110,20]
    
    standard_stim_amps = ['%snA'%(i/50.) for i in range(1,10,1)]
    #standard_stim_amps = ["0.1nA", "0.05nA"]


    if '-all' in sys.argv:
        
        pass

    else:
        
        fixed = {'dt':0.025, 'duration':100}
        fixed["delay_baseline_curr"] = "20ms"
        fixed['delay_vip_mod_curr'] = '100s'
        fixed['weight_scale_Exc'] = 0
        fixed['weight_scale_PV'] = 0
        fixed['weight_scale_SST'] = 0
        fixed['weight_scale_VIP'] = 0

        quick = False
        #quick=True

        vary = {}
        vary['baseline_current_Exc']= standard_stim_amps
        #vary['baseline_current_PV']= standard_stim_amps
        #vary['baseline_current_SST']= standard_stim_amps
        #vary['baseline_current_VIP']= standard_stim_amps

        
        #vary = {'number_per_cell':[i for i in range(0,250,10)]}
        #vary = {'stim_amp':['1pA','1.5pA','2pA']}
        #vary = {'stim_amp':['%spA'%(i/10.0) for i in range(-3,60,1)]}

        type = 'delMolinoEtAl'

        nmllr = NeuroMLliteRunner('Sim%s.json'%(type),
                                  simulator='jNeuroML')

        if quick:
            pass

        ps = ParameterSweep(nmllr, vary, fixed,
                            num_parallel_runs=6,
                                  plot_all=True, 
                                  save_plot_all_to='firing_rates_%s.png'%type,
                                  show_plot_already=False)

        report = ps.run()
        ps.print_report()

        ps.plotLines('baseline_current_Exc','average_last_1percent',save_figure_to='average_last_1percent_%s.png'%type)

        ###ps.plotLines('stim_amp','mean_spike_frequency',save_figure_to='mean_spike_frequency_%s.png'%type)
        #ps.plotLines('dt','mean_spike_frequency',save_figure_to='mean_spike_frequency_%s.png'%type, logx=True)
        #ps.plotLines('number_per_cell','mean_spike_frequency',save_figure_to='poisson_mean_spike_frequency_%s.png'%type)

        import matplotlib.pyplot as plt
        if not '-nogui' in sys.argv:
            print("Showing plots")
            plt.show()
