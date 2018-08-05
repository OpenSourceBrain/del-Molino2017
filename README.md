# del-Molino2017
Implementation in NeuromL2/LEMS of del Molino, L. C. G., Yang, G. R., Mejias, J.
F., & Wang, X. J. (2017). Paradoxical response reversal of top-down modulation
in cortical circuits with three interneuron types. [Elife, 6,
e29742](https://cdn.elifesciences.org/articles/29742/elife-29742-v2.pdf).

## The model
<p float="left">
    <img src="NeuroML/Fig1/Fig1a.png" width="400" />
    <img src="NeuroML/Fig3/RandomPopulationRate_high_baseline.nml36.png" width="400" />
</p>

The model simulates the dynamics of Pyramidal cells (E)
with three interneurons types (parvalbumin (PV), somatostatin (SST) and
vasoactive intestinal peptide (VIP)). With this model the authors provide
answers to two conunterintuive phenoma: (I) the external activation of a
population that inhibits a second population can trigger a positive response in
the latter. (II) Depending on the sensory input a top-down modulation can
trigger both a positive and a negative response.

## NeuroML version of the model
<!-- We simulated the population firing rate for a low baseline and high baseline -->
<!-- activity. -->
<!-- More details of how these plots were obtained can be found -->
A reproduction of the main findings of the paper using the NeuroML code can be
found [here](https://github.com/OpenSourceBrain/del-Molino2017/blob/master/notebooks/Figures.ipynb).
