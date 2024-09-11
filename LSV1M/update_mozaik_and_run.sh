#!/bin/bash

# A simple script to update mozaik and run simulation

cd /home/baroni/mozaik_v1paper
python setup.py install
cd /CSNG/baroni/mozaik-models/LSV1M
python run_parameter_search.py run.py nest param_nat_img/defaults