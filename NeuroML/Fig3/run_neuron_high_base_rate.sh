set -e
# remove files
if [ -d x86_64 ]; then
        rm -r x86_64
        echo Removed x86_64 folder
fi
if [ -d arm64 ]; then
        rm -r arm64
        echo Removed arm64 folder
fi

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
