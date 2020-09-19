import matplotlib
import sys
if 'animation' in sys.argv[1]:
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
from ternary_data import *
import numpy as np


### parameters
flavors = ['nue', 'nuebar', 'numu', 'numubar', 'nutau', 'nutaubar']
flux_dir = "../fluxes/no_osc/scint/"
event_dir = "../out/osc/"
key_dir = "../fluxes/garching/garching_pinched_info_key.dat"
time_length = 10
interactions = {
    "argon" : ["nue_Ar40", "_e", "nc"], 
    "water" : ["ibd", ["_e", "nue_O16"], "nc"], 
    "scint" : ["ibd", ["_e_", "nue_C12"], "nc"]
}
log_scale = .1
num_bins = 50
### specifically for multiple channels 
include_channels = [["water", "wc100kt30prct"], ["argon", "ar40kt"], ["scint", "scint20kt"]]

def multiple_channels_over_time(osc="", smear=True):
    points = get_raw_points_for_multiple_channels(flux_dir, event_dir, key_dir, interactions, include_channels, osc=osc, smear=True)
    (time, time_idx) = generate_time_bins(key_dir, log_scale, num_bins)
    (raw_points_events, ternary_points_events) = consolidate_points(points, time_idx)
    pprint(ternary_points_events)
    fps = len(ternary_points_events) / time_length
    labels = ('nc', 'ibd', 'nue + ES')
    smeared = "non-smeared"
    if smear: 
        smeared = "smeared"
    sub_title = ' '.join([i[0] for i in include_channels])
    sub = f"{sub_title} {smeared} {osc}"
    sub = generate_title("multiple channels over time:", sub )
    # plotting time
    shared_plotting_script(sub, labels, ternary_points_events, raw_points_events, time, time_idx, fps)

def events_over_time(detector, config, smear=True, title=""):
    points_events = total_events_from_flux(detector, config, flux_dir, event_dir, smeared=smear) 
    pprint(points_events)
    (time, time_idx) = generate_time_bins(key_dir, log_scale, num_bins)
    (raw_points_events, ternary_points_events) = consolidate_points(points_events, time_idx)
    fps = len(ternary_points_events) / time_length
    writer = animation.PillowWriter(fps=fps)
    labels = get_labels(detector, interactions)
    smeared = "non-smeared"
    if smear: 
        smeared = "smeared"
    sub = f" {title} {detector} {config} events {smeared}"

    # plotting time
    shared_plotting_script(sub, labels, ternary_points_events, raw_points_events, time, time_idx, fps)

def flux_over_time(title="", smear=True):
    (time, time_idx) = generate_time_bins(key_dir, log_scale, num_bins) 
    raw_points = get_raw_points_for_flux(flux_dir)
    raw_points, ternary_points = consolidate_points(raw_points, time_idx)
    fps = len(ternary_points) / time_length
    writer = animation.PillowWriter(fps=fps)
    pprint(ternary_points)
    labels = ("$\% \\nu_{e}$", "$\% \\nu_{x} (\\nu_{\\mu} + \\overline{\\nu}_{\\mu} + \
        \\nu_{\\tau} + \\overline{\\nu}_{\\tau})$ ","$\%\\overline{\\nu}_e$")
    sub = generate_title("flux over time", title)
    shared_plotting_script(sub, labels, ternary_points, raw_points, time, time_idx, fps)

def plot_with_uncertainty(osc="", smear=True):
    (time, time_idx) = generate_time_bins(key_dir, log_scale, num_bins)
    points = get_raw_points_for_multiple_channels(flux_dir, event_dir, key_dir, interactions, include_channels, osc=osc, smear=True)
    (raw_points_events, ternary_points_events) = consolidate_points(points, time_idx)
    heatmap_data = dict()
    if "animation" not in sys.argv[1]: 
        heatmap_data = generate_heatmap_dict(raw_points_events, ternary_points_events)
    pprint(heatmap_data)
    fps = len(ternary_points_events) / time_length
    labels = ('nc', 'ibd', 'nue + ES')
    smeared = "non-smeared"
    if smear: 
        smeared = "smeared"
    sub_title = ' '.join([i[0] for i in include_channels])
    sub = f"{sub_title} {smeared} {osc}"
    sub = generate_title("multiple channels over time (uncertainty):", sub)
    # plotting time
    shared_plotting_script(sub, labels, ternary_points_events, raw_points_events, time, time_idx, fps, heatmap_data)

def plot_osc_uncertainty(smear=True):
    (time, time_idx) = generate_time_bins(key_dir, log_scale, num_bins)
    ih_points = get_raw_points_for_multiple_channels(flux_dir, event_dir, key_dir, interactions, include_channels, osc="ih", smear=True)
    nh_points = get_raw_points_for_multiple_channels(flux_dir, event_dir, key_dir, interactions, include_channels, osc="nh", smear=True)
    (ih_raw_points_events, ih_ternary_points_events) = consolidate_points(ih_points, time_idx)
    (nh_raw_points_events, nh_ternary_points_events) = consolidate_points(nh_points, time_idx)
    heatmap_data_ih = dict()
    heatmap_data_nh = dict()
    if "animation" not in sys.argv[1]: 
        heatmap_data_ih = generate_heatmap_dict(ih_raw_points_events, ih_ternary_points_events, 1)
        heatmap_data_nh = generate_heatmap_dict(nh_raw_points_events, nh_ternary_points_events, .5)
    heatmap_data = consolidate_heatmap_data(heatmap_data_nh, heatmap_data_ih)
    fps = len(ih_ternary_points_events) / time_length
    labels = ('nc', 'ibd', 'nue + ES')
    smeared = "non-smeared"
    if smear: 
        smeared = "smeared"
    sub_title = ' '.join([i[0] for i in include_channels])
    sub = f"{sub_title} {smeared}"
    sub = generate_title("multiple channels over time (uncertainty):", sub)
    # plotting time
    shared_plotting_script(sub, labels, [ih_ternary_points_events, nh_ternary_points_events], [ih_raw_points_events, nh_raw_points_events], time, time_idx, fps, heatmap_data)

# flux_over_time()
multiple_channels_over_time("nh")
# plot_osc_uncertainty(smear=True)



