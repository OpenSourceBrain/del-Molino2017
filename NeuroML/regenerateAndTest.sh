#!/bin/bash
set -ex

cd Fig1

./testAll.sh

cd ../Fig2 
./testall.sh

cd ../Fig3
./run_jnml.sh

cd ..

omv all -V 

