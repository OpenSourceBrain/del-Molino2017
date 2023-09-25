set -ex

python GeneratePopulationRate.py

jnml LEMS_PopulationSimlowBaseline.xml  -nogui
jnml LEMS_PopulationSimhighBaseline.xml -nogui

jnml LEMS_PopulationSimlowBaseline.xml  -neuron -run -nogui
jnml LEMS_PopulationSimhighBaseline.xml -neuron -run -nogui