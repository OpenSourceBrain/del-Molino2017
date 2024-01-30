set -ex


python GeneratefICurve.py

pynml LEMS_fISim_exc.xml -nogui
pynml LEMS_fISim_pv.xml  -nogui
pynml LEMS_fISim_sst.xml -nogui
pynml LEMS_fISim_vip.xml -nogui

pynml LEMS_fISim_exc.xml -neuron -nogui -run
rm -rf x86_64
pynml LEMS_fISim_pv.xml -neuron -nogui -run
rm -rf x86_64
pynml LEMS_fISim_sst.xml -neuron -nogui -run
rm -rf x86_64
pynml LEMS_fISim_vip.xml -neuron -nogui -run


