#!/usr/local/bin/ipython -i
from mozaik.experiments import *
from mozaik.experiments.vision import *
from mozaik.sheets.population_selector import RCRandomPercentage
from parameters import ParameterSet


def create_experiment_of_StaticImages(model, experiment_parameters):
    images_dir = experiment_parameters['images_dir']
    num_images = experiment_parameters['num_images']
    num_trials = experiment_parameters['num_trials']
    num_skipped_images = experiment_parameters['num_skipped_images']    

    if images_dir is 0:
        images_dir = "/projects/ImageDatasets/imagenet/all_imagenet_images"
    if images_dir is 1:
        images_dir = "/CSNG/baroni/mozaik-models/Images/gratings"
    if images_dir is 2:
        images_dir = "/CSNG/baroni/mozaik-models/Images/MNIST_220x220"
    if images_dir is 'imagenet':
        images_dir = "/projects/ImageDatasets/imagenet/all_imagenet_images"

    return [
        NoStimulation(model, ParameterSet({"duration": 270})),
        # Measure response to sequence of static natural images
        MeasureStaticImages(
            model,
            ParameterSet(
                {
                    "duration": 560,
                    "images_dir": images_dir,
                    "num_images": num_images,
                    "image_display_duration": 560.0,
                    "num_trials": num_trials,
                    "num_skipped_images": num_skipped_images,
                    "size": 11,
                    'shuffle_stimuli': True, 
                }
            ),
        ),
    ]

def create_experiments(model):
    return [
        # Lets kick the network up into activation

        # Spontaneous Activity
        NoStimulation(model, ParameterSet(
            {'duration': 3*8*2*5*3*8*7})),

        # Measure orientation tuning with full-filed sinusoidal gratins
        MeasureOrientationTuningFullfield(model, ParameterSet(
            {'num_orientations': 10, 'spatial_frequency': 0.8, 'temporal_frequency': 2, 'grating_duration': 2*143*7, 'contrasts': [10,30,100], 'num_trials':10, 'shuffle_stimuli': True})),

        # Measure response to natural image with simulated eye movement
        MeasureNaturalImagesWithEyeMovement(model, ParameterSet(
            {'stimulus_duration': 2*143*7, 'num_trials': 10, 'size':30, 'shuffle_stimuli': False})),
    ]

def create_experiments_stc(model):

    return [

        # Spontaneous Activity
        NoStimulation(model, ParameterSet({'duration': 2*5*3*8*7})),

        # Size Tuning
        MeasureSizeTuning(model, ParameterSet({'num_sizes': 12, 'max_size': 5.0, 'log_spacing': True, 'orientations': [0], 'positions': [(0,0)],
                                               'spatial_frequency': 0.8, 'temporal_frequency': 2, 'grating_duration': 2*143*7, 'contrasts': [10, 100], 'num_trials': 10, 'shuffle_stimuli': True})),
    ]


def create_experiments_spont(model):
    return [
        # Spontaneous Activity
        NoStimulation(model, ParameterSet(
            {'duration': 3*8*2*5*3*8*7})),
    ]

