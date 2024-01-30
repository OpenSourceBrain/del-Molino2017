set -ex

python GeneratePopulationRate.py


if [[ "$CI" != "true" ]]; then  # Throws out of memory error on GHA
    jnml LEMS_PopulationSimlowBaseline.xml  -nogui
    jnml LEMS_PopulationSimhighBaseline.xml -nogui

    jnml LEMS_PopulationSimlowBaseline.xml  -neuron -run -nogui
    jnml LEMS_PopulationSimhighBaseline.xml -neuron -run -nogui

else 
   echo "Not running pynml due to memory issues"
fi