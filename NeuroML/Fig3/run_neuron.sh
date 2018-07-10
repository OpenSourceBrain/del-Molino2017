set -e

# activate python virtual enviroment
# TODO: the virtual environment should be self-contained in the project folder
source ../../../gsoc-env/bin/activate

# generate LEMS files
python GeneratePopulationRate.py

jnml LEMS_PopulationSimlowBaseline.xml -neuron

# Generate folder with neuron executables
nrnivmodl

# On neuron with gui and run the simulation
nrngui -python LEMS_PopulationSimlowBaseline_nrn.py
