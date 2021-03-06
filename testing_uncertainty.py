import math
import sys
from ternary import plotting
from ternary import ternary_axes_subplot as ternary
from celluloid import Camera
from natsort import natsorted
import matplotlib.animation as animation
import os
import string
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lsc
from ternary_helpers import *

flavors = ['nue', 'nuebar', 'numu', 'numubar', 'nutau', 'nutaubar']
flux_dir = "../fluxes/no_osc/scint/"
event_dir = "../out/no_osc/"
key_dir = "../fluxes/garching/garching_pinched_info_key.dat"
time_length = 10

### specifically for multiple channels 
include_channels = [["water", "wc100kt30prct"], ["argon", "ar40kt"], ["scint", "scint20kt"]]

### for heatmap
scale = 100
probability_threshold = .5

def plot_with_uncertainty(title, smear=True): 
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
    heatmap_data = dict()
    if "animation" not in sys.argv[1]: 
        heatmap_data = generate_heatmap_dict(raw_points_events, ternary_points_events)
    fps = len(ternary_points_events) / time_length
    labels = ('nc', 'ibd', 'nue + ES')

    smeared = "non-smeared"
    if smear: 
        smeared = "smeared"
    sub_title = ' '.join([i[0] for i in include_channels])

    sub = f"{title} {sub_title} {smeared} {osc}"
    sub = generate_title(sub, )
    # plotting time
    shared_plotting_script(sub, labels, ternary_points_events, raw_points_events, time, time_idx, fps, heatmap_data)

plot_with_uncertainty("testing")