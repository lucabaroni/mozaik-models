# -*- coding: utf-8 -*-
import sys
from mozaik.meta_workflow.parameter_search import CombinationParameterSearch, SlurmSequentialBackend
import numpy
import time
import numpy as np

# if True:
#     bs = list(np.arange(50000, 100000, 100))
#     CombinationParameterSearch(
#         SlurmSequentialBackend(
#             num_threads=1,
#             num_mpi=16,
#             path_to_mozaik_env="/home/baroni/virt_env/mozaik_v1paper/bin/activate",
#             slurm_options=[
#                 "--hint=nomultithread",
#                 "-J NaturalImages",
#                 "-N 1-1",
#                 "-x w[1-2,8-12]",
#                 # "--exclusive"
#             ],
#         ),
#         {"trial": [0], "baseline": bs}
#     ).run_parameter_search()

if True:
    bs = list(np.arange(300000, 301000, 50))
    CombinationParameterSearch(
        SlurmSequentialBackend(
            num_threads=1,
            num_mpi=16,
            path_to_mozaik_env="/home/baroni/virt_env/mozaik_v1paper/bin/activate",
            slurm_options=[
                "--hint=nomultithread",
                "-J NaturalImages",
                "-N 1-1",
                "-x w[1,5-9,11-17]",
                # "--exclusive"
            ],
        ),
        {"trial": [0], "baseline": bs}
    ).run_parameter_search()