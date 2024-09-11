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
from mozaik.storage.datastore import Hdf5DataStore, PickledDataStore
from parameters import ParameterSet
from analysis_and_visualization import perform_analysis_and_visualization
from model import SelfSustainedPushPull
from experiments import create_experiments, create_experiment_of_NaturalImages
import mozaik
from mozaik.controller import run_workflow, setup_logging, run_workflow_with_exp_params
import mozaik.controller
import sys
from pyNN import nest
from mozaik.cli import parse_workflow_args

from mpi4py import MPI

mpi_comm = MPI.COMM_WORLD

import nest
nest.Install("stepcurrentmodule")

# if True:
#     data_store, model = run_workflow(
#         'SelfSustainedPushPull', SelfSustainedPushPull, create_experiments)
#     if False:
#         model.connectors['V1AffConnectionOn'].store_connections(data_store)
#         model.connectors['V1AffConnectionOff'].store_connections(data_store)
#         model.connectors['V1AffInhConnectionOn'].store_connections(data_store)
#         model.connectors['V1AffInhConnectionOff'].store_connections(data_store)
#         model.connectors['V1L4ExcL4ExcConnection'].store_connections(
#             data_store)
#         model.connectors['V1L4ExcL4InhConnection'].store_connections(
#             data_store)
#         model.connectors['V1L4InhL4ExcConnection'].store_connections(
#             data_store)
#         model.connectors['V1L4InhL4InhConnection'].store_connections(
#             data_store)
#         model.connectors['V1L23ExcL23ExcConnection'].store_connections(
#             data_store)
#         model.connectors['V1L23ExcL23InhConnection'].store_connections(
#             data_store)
#         model.connectors['V1L23InhL23ExcConnection'].store_connections(
#             data_store)
#         model.connectors['V1L23InhL23InhConnection'].store_connections(
#             data_store)
#         model.connectors['V1L4ExcL23ExcConnection'].store_connections(data_store)
#         model.connectors['V1L4ExcL23InhConnection'].store_connections(data_store)
#     data_store.save()
# else:
#     setup_logging()
#     data_store = PickledDataStore(load=True, parameters=ParameterSet(
#         {'root_directory': 'SelfSustainedPushPull_test____', 'store_stimuli': False}), replace=True)

# if mpi_comm.rank == 0:
#     print("Starting visualization")
#     perform_analysis_and_visualization(data_store)


# NATURAL IMAGES EXPERIMENTS

# multitrial
# num_images = 50
# num_trials = 100

# multitrial for david
num_images = 50
num_trials = 20

# single trial
# num_images = 100
# num_trials = 1


(
    simulation_run_name,
    simulator_name,
    num_threads,
    parameters_url,
    modified_parameters,
) = parse_workflow_args()

baseline = modified_parameters["baseline"]
num_skipped_images = baseline
exp_params = {
    "num_skipped_images": num_skipped_images,
    "num_images": num_images,
    "num_trials": num_trials,
}

data_store, model = run_workflow_with_exp_params(
    f"NewDataset_Images_from_{num_skipped_images}_to_{num_skipped_images + num_images}",
    SelfSustainedPushPull,
    create_experiment_of_NaturalImages,
    exp_params,
)


# #%%
# import sys
# from unicodedata import name
# from mozaik.controller import Global, setup_logging
# from mozaik.storage.datastore import PickledDataStore
# from parameters import ParameterSet
# from mozaik.storage.queries import param_filter_query
# import mozaik
# import os
# import gc
# import pickle
# import numpy as np
# from mozaik.tools.mozaik_parametrized import MozaikParametrized
# from tqdm import tqdm
# import logging
# import imagen 
# from imagen.image import BoundingBox
# from mozaik.stimuli.vision.topographica_based import MaximumDynamicRange

# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

# def get_datastore(root):
#     Global.root_directory = root
#     datastore = PickledDataStore(
#         load=True,
#         parameters=ParameterSet({"root_directory": root, "store_stimuli": False}),
#         replace=True,
#     )
#     return datastore


# def extract_images(path):
#     path = path.split("from_")[1].split("_")[0]
#     return path


# def get_filename(path, sheet):
#     if sheet == "V1_Inh_L2/3":
#         sheet_n = "V1_Inh_L23"
#     if sheet == "V1_Exc_L2/3":
#         sheet_n = "V1_Exc_L23"
#     img_n = extract_images(path)
#     filename = (
#         sheet_n + "_img_" + str(img_n) + "_to_" + str(int(img_n) + 24) + ".pickle"
#     )
#     return filename


# def pickledump(path, file):
#     with open(path, "wb") as f:
#         pickle.dump(file, f)

# def reconstruct_stimuli(s):
#     pattern_sampler = imagen.image.PatternSampler(
#             size_normalization="fit_shortest",
#             whole_pattern_output_fns=[MaximumDynamicRange()],
#         )

#     img = imagen.image.FileImage(
#         filename=s.image_path,
#         x=0,
#         y=0,
#         orientation=0,
#         xdensity=s.density,
#         ydensity=s.density,
#         size=s.size,
#         bounds=BoundingBox(
#             points=(
#                 (-s.size_x / 2, -s.size_y / 2),
#                 (s.size_x / 2, s.size_y / 2),
#             )
#         ),
#         scale=2 * s.background_luminance,
#         pattern_sampler=pattern_sampler,
#     )
#     return img()
    

# dsv = param_filter_query(data_store, st_name='NaturalImage')
# sheets = ['V1_Exc_L4', 'V1_Inh_L4', 'V1_Exc_L2/3', 'V1_Inh_L2/3']
# sheet_folders  = ['V1_Exc_L4', 'V1_Inh_L4', 'V1_Exc_L23', 'V1_Inh_L23']
# trials = sorted(list(set( MozaikParametrized.idd(s).trial for s in dsv.get_stimuli())))
# img_paths =  sorted(list(set(MozaikParametrized.idd(s).image_path for s in dsv.get_stimuli())))

# setup_logging()
# logger = mozaik.getMozaikLogger()

# dsv = param_filter_query(data_store, st_name='NaturalImage')

# if len(trials) == 1:
#     print(f'There is a single trial')
#     for sheet, sf in zip(sheets, sheet_folders):
#         print(f'sheet={sheet}')
#         dsv1 = param_filter_query(dsv, sheet_name = sheet)
#         for trial in trials:
#             dsv2 = param_filter_query(dsv1, st_trial = trial)
#             segs = dsv2.get_segments()
#             stims = dsv2.get_stimuli()
#             stims_n = [MozaikParametrized.idd(st).image_path.split('/')[-1].split('_')[0] for st in stims]
#             segs = [seg for _, seg in sorted(zip(stims_n, segs))]
            
#             gc.collect()
#             resps = [s.mean_rates() for s in tqdm(segs)]
#             gc.collect()
#             for i, stim in enumerate(tqdm(stims)):
#                 parametrized_stim = MozaikParametrized.idd(stim)
#                 img_number = parametrized_stim.image_path.split('/')[-1].split('_')[0]
#                 resp_path = os.path.join('/home/baroni/mozaik-models_v1paper/exported_data_test', 'single_trial', img_number)
#                 os.makedirs(resp_path, exist_ok=True)
#                 np.save(os.path.join(resp_path, sf +'.npy'), resps[i])
#                 if trial ==0:
#                     if sheet == sheets[0]:
#                         img = reconstruct_stimuli(parametrized_stim)
#                         np.save(os.path.join(resp_path, 'stimulus' +'.npy'), img)
#                         gc.collect()

# if len(trials) != 1:
#     print(f'There are multiple trials ({len(trials)})')
#     for sheet, sf in zip(sheets, sheet_folders):
#         print(f'sheet={sheet}')
#         dsv1 = param_filter_query(dsv, sheet_name = sheet)
#         for trial in trials:
#             print(f'trial={trial}')
#             dsv2 = param_filter_query(dsv1, st_trial = trial)
#             segs = dsv2.get_segments()
#             stims = dsv2.get_stimuli()
#             stims_n = [MozaikParametrized.idd(st).image_path.split('/')[-1].split('_')[0] for st in stims]
#             segs = [seg for _, seg in sorted(zip(stims_n, segs))]
#             gc.collect()
#             resps = [s.mean_rates() for s in tqdm(segs)]
#             gc.collect()
#             for i, stim in enumerate(tqdm(stims)):
#                 parametrized_stim = MozaikParametrized.idd(stim)
#                 img_number = parametrized_stim.image_path.split('/')[-1].split('_')[0]
#                 resp_path = os.path.join('/home/baroni/mozaik-models_v1paper/exported_data_test', 'multitrial', img_number)
#                 resp_path_trial = os.path.join('/home/baroni/mozaik-models_v1paper/exported_data', 'multitrial', img_number, 'trial='+str(trial))
#                 os.makedirs(resp_path_trial, exist_ok=True)
#                 np.save(os.path.join(resp_path_trial, sf +'.npy'), resps[i])
#                 if trial ==0:
#                     if sheet == sheets[0]:
#                         img = reconstruct_stimuli(parametrized_stim)
#                         np.save(os.path.join(resp_path, 'stimulus' +'.npy'), img)
#                         gc.collect()