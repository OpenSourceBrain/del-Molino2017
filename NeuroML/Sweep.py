import sys

import pprint; pp = pprint.PrettyPrinter(depth=6)

from neuromllite.sweep.ParameterSweep import ParameterSweep
from neuromllite.sweep.ParameterSweep import NeuroMLliteRunner
       

if __name__ == '__main__':

    heatmap_lims=[-110,20]
    
    #standard_stim_amps = ['%snA'%(i/50.) for i in range(1,10,1)] #0.02nA - 0.18nA (10 runs)
    #standard_stim_amps = ["0.1nA", "0.05nA"]
    #standard_stim_amps = ['%snA'%(i/100.) for i in range(1,20,1)] #0.01nA - 0.18nA (20 runs)
    standard_stim_amps = ['%snA'%(i/100.) for i in range(-10,30,1)]

    #standard_stim_amps = ['%snA'%(i/100.) for i in range(-10,30,1)] #-0.1nA - 0.3nA (40 runs)
    pyr_stim_amps = ["-0.1nA", "-0.2nA", "-0.3nA", "-0.4nA", "0.1nA"]
    PV_stim_amps = ["-0.1nA", "-0.2nA", "-0.3nA", "-0.4nA", "0.2nA"]
    SST_stim_amps = ["-0.05nA", "-0.1nA", "-0.15nA","-0.2nA", "0.1nA"]
    VIP_stim_amps = ["-0.1nA", "-0.15nA","-0.2nA", "-0.25nA", "0.2nA"]

    if '-all' in sys.argv:
        
        pass

    else:

        fixed = {'dt':0.01, 'duration':100}
        fixed["delay_baseline_curr"] = "20ms"
        fixed['delay_vip_mod_curr'] = '100s'
        fixed['weight_scale_Exc'] = 0
        fixed['weight_scale_PV'] = 0
        fixed['weight_scale_SST'] = 0
        fixed['weight_scale_VIP'] = 0

        fixed['baseline_current_Exc'] = "0.0nA"
        fixed['baseline_current_PV'] = "0.0nA"
        fixed['baseline_current_SST'] = "0.0nA"
        fixed['baseline_current_VIP'] = "0.0nA"

        #fixed['baseline_current_Exc']= '0.11503nA'
        #fixed['baseline_current_PV']= '0.23366nA'
        #fixed['baseline_current_SST']= '0.09431nA'
        #fixed['baseline_current_VIP']= '0.08991nA'

        quick = False
        #quick=True

        vary = {}
        #vary['baseline_current_Exc']= standard_stim_amps
        #vary['baseline_current_PV']= standard_stim_amps
        #vary['baseline_current_SST']= standard_stim_amps
        #vary['baseline_current_VIP']= standard_stim_amps

        #vary['baseline_current_Exc']= pyr_stim_amps
        #vary['baseline_current_PV']= PV_stim_amps
        #vary['baseline_current_SST']= SST_stim_amps
        #vary['baseline_current_VIP']= VIP_stim_amps

        #vary['global_offset_current'] = ["0.05nA", "0.15nA"]
        vary['global_offset_current'] = ['%snA'%(i/50.1) for i in range(1,10,1)]
        vary['global_offset_current'] = ['%snA'%(i/100.1) for i in range(0,30,1)]
        #vary['global_offset_current'] = ['%snA'%(i/100.1) for i in range(-10,30,1)]
                
        #vary = {'number_per_cell':[i for i in range(0,250,10)]}
        #vary = {'stim_amp':['1pA','1.5pA','2pA']}
        #vary = {'stim_amp':['%spA'%(i/10.0) for i in range(-3,60,1)]}

        #type = 'delMolinoEtAl_high_baseline'
        type = 'delMolinoEtAl_low_baseline'

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

        #ps.plotLines('baseline_current_Exc','average_last_1percent',save_figure_to='average_last_1percent_%s.png'%type)
        ps.plotLines('global_offset_current','average_last_1percent',save_figure_to='average_last_1percent_%s.png'%type)

        ###ps.plotLines('stim_amp','mean_spike_frequency',save_figure_to='mean_spike_frequency_%s.png'%type)
        #ps.plotLines('dt','mean_spike_frequency',save_figure_to='mean_spike_frequency_%s.png'%type, logx=True)
        #ps.plotLines('number_per_cell','mean_spike_frequency',save_figure_to='poisson_mean_spike_frequency_%s.png'%type)

        import matplotlib.pyplot as plt
        if not '-nogui' in sys.argv:
            print("Showing plots")
            print("\n\n")
            ps.print_report()
            plt.show()
