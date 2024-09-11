#%%
import sys
from unicodedata import name
from mozaik.controller import Global, setup_logging
from mozaik.storage.datastore import PickledDataStore
from parameters import ParameterSet
from mozaik.storage.queries import param_filter_query
import mozaik
import os
import gc
import pickle
import numpy as np
from mozaik.tools.mozaik_parametrized import MozaikParametrized
from tqdm import tqdm
import logging
import imagen 
from imagen.image import BoundingBox
from mozaik.stimuli.vision.topographica_based import MaximumDynamicRange

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

def get_datastore(root):
    Global.root_directory = root
    datastore = PickledDataStore(
        load=True,
        parameters=ParameterSet({"root_directory": root, "store_stimuli": False}),
        replace=True,
    )
    return datastore

def extract_images(path):
    path = path.split("from_")[1].split("_")[0]
    return path

def pickledump(path, file):
    with open(path, "wb") as f:
        pickle.dump(file, f)
path = '/CSNG/baroni/mozaik-models/LSV1M/20240124-093921[param_nat_img.defaults]CombinationParamSearch{trial:[0],baseline:500}/NewDataset_Images_from_50000_to_50100_ParameterSearch_____baseline:50000_trial:0'

ds = get_datastore(path)
# %%
pickledump('neuron_annotations.pickle', ds.get_neuron_annotations())
pickledump('neuron_positions.pickle', ds.get_neuron_positions())
# %%
