import matplotlib
matplotlib.use("Agg")
import sys
import matplotlib.pyplot as plt
from ternary import plotting
from ternary import ternary_axes_subplot as ternary
import re
import pandas as pd
import math
from celluloid import Camera
import matplotlib.animation as animation
import os
from pprint import pprint
from natsort import natsorted, ns
from pprint import pprint
from ternary_helpers import *

### parameters 
interactions = {
    "nc":["O16"], 
    "cc":["O16", "e"]
}

### constants
flavors = ['nue', 'nuebar', 'numu', 'numubar', 'nutau', 'nutaubar']
flux_dir = "../fluxes/no osc/ih/"
event_dir = "../out/garching_in"
key_dir = "../fluxes/garching/garching_pinched_info_key.dat"
time_length = 10


def points_over_time(title, detector, smear=True): 
    print(smear)
    fluxes = os.listdir(flux_dir)
    fluxes = natsorted(fluxes)
    points_events = []
    for flux in fluxes: 
        flux = flux.replace(".dat", "")
        points_events.append(get_events_from_flux(flux, detector, smeared=smear))
    points_flux = get_raw_points_for_flux(flux_dir)
    (time, time_idx) = time_bins(key_dir, .1, 50)
    (raw_points_events, ternary_points_events) = consolidate_points(points_events, time_idx)
    (raw_point_flux, ternary_points_flux) = consolidate_points(points_flux, time_idx)
    fps = len(ternary_points_events) / time_length
    writer = animation.PillowWriter(fps=fps)

    # plotting time
    scale = 100
    figure, tax = ternary.figure(scale=scale) 
    cam = Camera(figure)
    fontsize = 12
    tax.set_title(title + "\n" , fontsize=fontsize)
    tax.right_axis_label("$\%\\nu_{x} (\\nu_{\\mu} + \\overline{\\nu}_{\\mu} + \
    \\nu_{\\tau} + \\overline{\\nu}_{\\tau})$ ", fontsize=fontsize, offset=0.14)
    tax.bottom_axis_label("$\%\\overline{\\nu}_e$", fontsize=fontsize, offset=0.14)
    tax.left_axis_label("$\%\\nu_e$" , fontsize=fontsize, offset=0.14)
    tax.clear_matplotlib_ticks()
    tax.get_axes().axis('off')

    rgb_events = [(0, 0, 1)]
    rgb_flux = [(1, 0, 0)]
    if sys.argv[1] == 'animation':
        for (i, point) in enumerate(ternary_points_events):
            tax.boundary(linewidth=1.5)
            tax.gridlines(color="black", multiple=20)
            tax.gridlines(color="blue", multiple=20, linewidth=0.5)
            tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
            tax.scatter(ternary_points_events[0:i+1], c=rgb_events[0:i+1], s=10, marker=".", linewidth=3, label="flux", alpha=.5)
            tax.scatter(ternary_points_flux[0:i+1], c=rgb_flux[0:i+1], s=10, marker=".", linewidth=3, label="flux", alpha=.5)
            tax.annotate(text=f"{time[time_idx[i]][1]}s", position=(.15,.85), xytext=(-20, -20))
            cam.snap()
            print(f"frame number: {i}")
        ani = cam.animate()
        ani.save(f"./out/animation/{title}.gif", writer=writer)
    elif sys.argv[1] == 'scatter':
        tax.boundary(linewidth=1.5)
        tax.gridlines(color="black", multiple=20)
        tax.gridlines(color="blue", multiple=20, linewidth=0.5)
        tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
        tax.scatter(ternary_points_events[0:i+1], c=rgb_events[0:i+1], s=10, marker=".", linewidth=3, label="flux", alpha=.5)
        tax.scatter(ternary_points_flux[0:i+1], c=rgb_flux[0:i+1], s=10, marker=".", linewidth=3, label="flux", alpha=.5)
        plt.savefig(f"./out/plots/{sys.argv[1]}_{title}.png", writer=writer)
        tax.show()


points_over_time("events vs flux smeared Oscillation ~.588 NH", "wc100kt30prct", smear=True)
# points_over_time("events_vs_flux_smeared", "wc100kt30prct", smear=True)

