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

def reconstruct_stimuli(s):
    pattern_sampler = imagen.image.PatternSampler(
            size_normalization="fit_shortest",
            whole_pattern_output_fns=[MaximumDynamicRange()],
        )

    img = imagen.image.FileImage(
        filename=s.image_path,
        x=0,
        y=0,
        orientation=0,
        xdensity=s.density,
        ydensity=s.density,
        size=s.size,
        bounds=BoundingBox(
            points=(
                (-s.size_x / 2, -s.size_y / 2),
                (s.size_x / 2, s.size_y / 2),
            )
        ),
        scale=2 * s.background_luminance,
        pattern_sampler=pattern_sampler,
    )
    return img()
    

def get_sheetname(sheet):
    if sheet == "V1_Inh_L2/3":
        sheet = "V1_Inh_L23"
    if sheet == "V1_Exc_L2/3":
        sheet= "V1_Exc_L23"
    return sheet


#%%
# run export
path = sys.argv[1]
sheet = sys.argv[2]
base_path = sys.argv[3]

datastore = get_datastore(path)

dsv = param_filter_query(datastore, st_name='NaturalImage')
sheets = ['V1_Exc_L2/3', 'V1_Inh_L2/3', 'V1_Exc_L4', 'V1_Inh_L4', 'X_ON' 'X_OFF']
sheet_folders  = ['V1_Exc_L23', 'V1_Inh_L23', 'V1_Exc_L4', 'V1_Inh_L4', 'X_ON' 'X_OFF']

trials = sorted(list(set( MozaikParametrized.idd(s).trial for s in dsv.get_stimuli())))
img_paths =  sorted(list(set(MozaikParametrized.idd(s).image_path for s in dsv.get_stimuli())))

setup_logging()
logger = mozaik.getMozaikLogger()

dsv1 = param_filter_query(dsv, sheet_name = sheet)
for trial in trials:
    dsv2 = param_filter_query(dsv1, st_trial = trial)
    segs = dsv2.get_segments()
    for seg in tqdm(segs):
        stim = MozaikParametrized.idd(seg.annotations['stimulus'])
        img_number = stim.image_path.split('/')[-1].split('_')[0]
        resp = seg.mean_rates()
        gc.collect()
        if len(trials) == 1:
            print(f'There is a single trial')
            print(f'sheet={sheet}')
            resp_path = os.path.join(base_path, 'single_trial', img_number)
            os.makedirs(resp_path, exist_ok=True)
            np.save(os.path.join(resp_path, get_sheetname(sheet) +'.npy'), resp)
        if len(trials) != 1:
            print(f'There are multiple trials')
            print(f'sheet={sheet}')
            resp_path = os.path.join(base_path, 'multitrial', img_number)
            resp_path_trial = os.path.join(base_path, 'multitrial', img_number, 'trial='+str(trial))
            os.makedirs(resp_path_trial, exist_ok=True)
            np.save(os.path.join(resp_path_trial, get_sheetname(sheet) +'.npy'), resp)
        if sheet == sheets[0]:
            if trial == 0:
                img = reconstruct_stimuli(stim)
                np.save(os.path.join(resp_path, 'stimulus' +'.npy'), img)
                gc.collect()


# if len(trials) == 1:
#     print(f'There is a single trial')
#     print(f'sheet={sheet}')
#     dsv1 = param_filter_query(dsv, sheet_name = sheet)
#     for trial in trials:
#         dsv2 = param_filter_query(dsv1, st_trial = trial)
#         segs = dsv2.get_segments()
#         for seg in tqdm(segs):
#             stim = MozaikParametrized.idd(seg.annotations['stimulus'])
#             img_number = stim.image_path.split('/')[-1].split('_')[0]
#             resp_path = os.path.join(base_path, 'single_trial', img_number)
#             resp = seg.mean_rates()
#             gc.collect()
#             os.makedirs(resp_path, exist_ok=True)
#             np.save(os.path.join(resp_path, get_sheetname(sheet) +'.npy'), resp)
#             if sheet == sheets[0]:
#                 img = reconstruct_stimuli(stim)
#                 np.save(os.path.join(resp_path, 'stimulus' +'.npy'), img)
#                 gc.collect()


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
#                 resp_path = os.path.join('/home/baroni/mozaik-models_v1paper/exported_data', 'multitrial', img_number)
#                 resp_path_trial = os.path.join('/home/baroni/mozaik-models_v1paper/exported_data', 'multitrial', img_number, 'trial='+str(trial))
#                 os.makedirs(resp_path_trial, exist_ok=True)
#                 np.save(os.path.join(resp_path_trial, sf +'.npy'), resps[i])
#                 if trial ==0:
#                     if sheet == sheets[0]:
#                         img = reconstruct_stimuli(parametrized_stim)
#                         np.save(os.path.join(resp_path, 'stimulus' +'.npy'), img)
#                         gc.collect()



# %% 
