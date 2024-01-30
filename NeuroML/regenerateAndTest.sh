#!/bin/bash
set -ex

cd Fig1

./testAll.sh

cd ../Fig2 
./testall.sh

cd ../Fig3

./run_neuron_high_base_rate.sh -nogui
./run_neuron_low_base_rate.sh -nogui

cd ..

omv all -V 

