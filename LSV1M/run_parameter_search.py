# -*- coding: utf-8 -*-
from mozaik.meta_workflow.parameter_search import CombinationParameterSearch, SlurmSequentialBackend
import numpy as np


if True:
    start_image = 50000
    end_image = 56000
    experiment_images_dir = [0]
    experiment_num_images = [100]
    experiment_num_trials = [1]
    experiment_num_skipped_images = list(np.arange(start_image, end_image, experiment_num_images[0])) 
    CombinationParameterSearch(
        SlurmSequentialBackend(
            num_threads=1,
            num_mpi=16,
            path_to_mozaik_env="/home/baroni/virt_env/mozaik_v1paper/bin/activate",
            slurm_options=[
                "--hint=nomultithread",
                "-J NaturalImages",
                "-N 1-1",
                "-x w[4-12, 16-17]",
                # "--exclusive"
            ],
        ),
        {"trial": [0], 
         "experiments.images_dir": experiment_images_dir,
         "experiments.num_skipped_images": experiment_num_skipped_images, 
         "experiments.num_images": experiment_num_images, 
         "experiments.num_trials": experiment_num_trials,
        }
    ).run_parameter_search()



    
