from mpi4py import MPI
from model import SelfSustainedPushPull
from experiments import create_experiment_of_StaticImages
from mozaik.controller import run_workflow
from mozaik.tools.export_to_hdf5 import export_from_datastore_to_hdf5
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

if mpi_comm.rank == 0:
    export_from_datastore_to_hdf5(data_store=data_store, st_name='StaticImage', data_type='mean_rates')

