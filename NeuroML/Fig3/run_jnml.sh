set -ex

python GeneratePopulationRate.py

pynml LEMS_PopulationSimlowBaseline.xml  -nogui
pynml LEMS_PopulationSimhighBaseline.xml -nogui

pynml LEMS_PopulationSimlowBaseline.xml  -neuron -run -nogui
pynml LEMS_PopulationSimhighBaseline.xml -neuron -run -nogui