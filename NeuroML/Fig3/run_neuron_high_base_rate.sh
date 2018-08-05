set -e
# remove files
if [ -d x86/64 ]; then
        rm -r x86/64
fi
echo Removed x86/64 folder

################################################################################
# High Base Rate
################################################################################
if [ -f LEMS_PopulationSimhighBaseline_nrn.py ]; then
    rm LEMS_PopulationSimhighBaseline_nrn.py
fi
echo Removed LEMS_PopulationSimhighBaseline file

# generate LEMS files
python GeneratePopulationRate.py

jnml LEMS_PopulationSimhighBaseline.xml -neuron

# Generate folder with neuron executables
nrnivmodl

# On neuron with gui and run the simulation
nrngui -python LEMS_PopulationSimhighBaseline_nrn.py
