import matplotlib
import sys
if 'standard' not in sys.argv[1]:
    matplotlib.use("Agg")
from ternary import plotting
from ternary import ternary_axes_subplot as ternary
import re
import pandas as pd
import math
from celluloid import Camera
import os
from pprint import pprint
from natsort import natsorted, ns
from pprint import pprint
from ternary_helpers import *
import numpy as np


### parameters
flavors = ['nue', 'nuebar', 'numu', 'numubar', 'nutau', 'nutaubar']
flux_dir = "../fluxes/no_osc/scint/"
event_dir = "../out/no_osc/"
key_dir = "../fluxes/garching/garching_pinched_info_key.dat"
time_length = 10

### specifically for multiple channels 
include_channels = [["water", "wc100kt30prct"], ["argon", "ar40kt"], ["scint", "scint20kt"]]

def multiple_channels_over_time(smear=True, title=""):
    points = []
    for (channel, config) in include_channels: 
        points_events = np.array(total_events_from_flux(channel, config, flux_dir, f"{event_dir}{channel}/", smeared=smear)) 
        if len(points) == 0: 
            points = np.zeros((len(points_events), 3))
        for (i, inter) in enumerate(interactions[channel]): 
            if 'ibd' in inter: 
                points[:,0] += points_events[:,i]
            elif 'nue' in inter or '_e' in inter: 
                points[:,1] += points_events[:,i]
            elif 'nc' in inter: 
                points[:,2] += points_events[:,i]
        (time, time_idx) = time_bins(key_dir, .1, 50)
    points = points.tolist()
    (raw_points_events, ternary_points_events) = consolidate_points(points, time_idx)
    uncertainty = calculate_uncertainty(raw_points_events)
    boundaries = run_boundary_points(ternary_points_events, uncertainty)
    fps = len(ternary_points_events) / time_length
    labels = ('ibd', 'nc', 'nue + ES')
    smeared = "non-smeared"
    if smear: 
        smeared = "smeared"
    sub_title = ' '.join([i[0] for i in include_channels])
    sub = f"{title} {sub_title} events {smeared}"
    # plotting time
    shared_plotting_script(sub, labels, ternary_points_events, raw_points_events, time, time_idx, fps, boundaries)

def points_over_time(detector, config, smear=True, title=""):
    points_events = total_events_from_flux(detector, config, flux_dir, event_dir, smeared=smear) 
    pprint(points_events)
    (time, time_idx) = time_bins(key_dir, .1, 50)
    (raw_points_events, ternary_points_events) = consolidate_points(points_events, time_idx)
    fps = len(ternary_points_events) / time_length
    writer = animation.PillowWriter(fps=fps)
    labels = get_labels(detector)
    smeared = "non-smeared"
    if smear: 
        smeared = "smeared"
    sub = f" {title} {detector} {config} events {smeared}"

    # plotting time
    shared_plotting_script(sub, labels, ternary_points_events, raw_points_events, time, time_idx, fps)

multiple_channels_over_time(smear=True, title="No Osc")
# points_over_time("argon", "ar40kt", smear=True, title="No Osc")


