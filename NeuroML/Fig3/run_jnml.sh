set -ex

python GeneratePopulationRate.py


if [[ "$CI" != "true" ]]; then  # Throws out of memory error on GHA
    pynml LEMS_PopulationSimlowBaseline.xml  -nogui
    pynml LEMS_PopulationSimhighBaseline.xml -nogui

    pynml LEMS_PopulationSimlowBaseline.xml  -neuron -run -nogui
    pynml LEMS_PopulationSimhighBaseline.xml -neuron -run -nogui
fi