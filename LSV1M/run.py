# -*- coding: utf-8 -*-
"""
This is implementation of model of self-sustained activitity in balanced networks from: 
Vogels, T. P., & Abbott, L. F. (2005). 
Signal propagation and logic gating in networks of integrate-and-fire neurons. 
The Journal of neuroscience : the official journal of the Society for Neuroscience, 25(46), 10786–95. 
"""
import matplotlib
matplotlib.use('Agg')

from mpi4py import MPI
from model import SelfSustainedPushPull
from experiments import create_experiment_of_StaticImages
from mozaik.controller import run_workflow
import mozaik.controller
from mozaik.export_to_h5py import export_from_datastore_to_H5py

from pyNN import nest


from mpi4py import MPI

mpi_comm = MPI.COMM_WORLD

import nest
nest.Install("stepcurrentmodule")

data_store, model = run_workflow(
    f"V1_model_Dataset",
    SelfSustainedPushPull,
    create_experiment_of_StaticImages,
)

data_store.save()

export_from_datastore_to_H5py(data_store=data_store, st_name='NaturalImages', data_type='mean_rates')

