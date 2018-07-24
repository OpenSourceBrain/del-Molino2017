set -e

python GeneratefICurve.py

jnml LEMS_fISim_exc.xml -nogui
jnml LEMS_fISim_pv.xml  -nogui
jnml LEMS_fISim_sst.xml -nogui
jnml LEMS_fISim_vip.xml -nogui

jnml LEMS_fISim_exc.xml -neuron -nogui -run
rm -rf x86_64
jnml LEMS_fISim_pv.xml -neuron -nogui -run
rm -rf x86_64
jnml LEMS_fISim_sst.xml -neuron -nogui -run
rm -rf x86_64
jnml LEMS_fISim_vip.xml -neuron -nogui -run


