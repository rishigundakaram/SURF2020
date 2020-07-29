import matplotlib
import sys
if sys.argv[2] == 'animation':
    matplotlib.use("Agg")
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


### parameters for file 
num_bins = 70
log_scale = .05
time_length = 10


def usage(): 
    print("ternary.py  by R. Gundakaram, \n")
    print("Usage:\n")
    print("python ternary.py title plot-type(scatter or trajectory) time-interval(linear orlog)\n")
    print("e.g. python ternary_flux.py 'flux: livermore' scatter\n")


if len(sys.argv) != 3: 
    usage()
else: 
    if 'standard' not in sys.argv[2]:
        scale = 100
        figure, tax = ternary.figure(scale=scale) 
        # figure.set_size_inches(6, 6)
        cam = Camera(figure)
        # Set Axis labels and Title
        fontsize = 12
        tax.set_title(sys.argv[1] + "\n" , fontsize=fontsize)
        tax.right_axis_label("$\%\\nu_{x} (\\nu_{\\mu} + \\overline{\\nu}_{\\mu} + \
        \\nu_{\\tau} + \\overline{\\nu}_{\\tau})$ ", fontsize=fontsize, offset=0.14)
        tax.bottom_axis_label("$\%\\overline{\\nu}_e$", fontsize=fontsize, offset=0.14)
        tax.left_axis_label("$\%\\nu_e$" , fontsize=fontsize, offset=0.14)
        # Remove default Matplotlib Axes
        tax.clear_matplotlib_ticks()
        tax.get_axes().axis('off')

    
    # get the times and figure out time bins 
    (time, time_idx) = time_bins("../fluxes/garching/garching_pinched_info_key.dat", log_scale, num_bins)
            
    # get points from files
    raw_points = get_raw_points_for_flux("../fluxes/garching_in/")
    pprint(raw_points)

    raw_points, ternary_points = consolidate_points(raw_points, time_idx)

    # dealing with graphics
    fps = len(ternary_points) / time_length
    writer = animation.PillowWriter(fps=fps)

    rgb = [(1, 0, 0)]

    if sys.argv[2] == 'scatter': 
        tax.boundary(linewidth=1.5)
        tax.gridlines(color="black", multiple=20)
        tax.gridlines(color="blue", multiple=20, linewidth=0.5)
        tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
        tax.scatter(ternary_points, s=10, c=rgb, marker=".", linewidth=3, label="flux", alpha=.5)
        tax.legend()
        title = sys.argv[1].replace(" ","_")
        plt.savefig(f"./out/plots/{sys.argv[2]}_{sys.argv[3]}_{title}.png", writer=writer)
        tax.show()
    elif sys.argv[2] == 'animation': 
        print(len(ternary_points))
        print(len(time_idx))
        for (i, point) in enumerate(ternary_points):
            tax.boundary(linewidth=1.5)
            tax.gridlines(color="black", multiple=20)
            tax.gridlines(color="blue", multiple=20, linewidth=0.5)
            tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
            tax.scatter(ternary_points[0:i+1], c=rgb, s=10, marker=".", linewidth=3, label="flux", alpha=.5)
            tax.annotate(text=f"{time[time_idx[i]][1]}s", position=(.15,.85), xytext=(-20, -20))
            cam.snap()
            print(f"frame number: {i}")
        ani = cam.animate()
        title = sys.argv[1].replace(" ","_") 
        ani.save(f"./out/animation/{sys.argv[2]}_{title}.gif", writer=writer)
    elif sys.argv[2] == 'trajectory': 
        tax.boundary(linewidth=1.5)
        tax.gridlines(color="black", multiple=20)
        tax.gridlines(color="blue", multiple=20, linewidth=0.5)
        tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
        tax.plot_colored_trajectory(ternary_point, cmap="Spectral",linewidth=1, label="flux", alpha=.5)
        tax.scatter(points, s=10, c=rgb, marker=".", linewidth=3, label="flux", alpha=.5)
        tax.show()
        title = sys.argv[1].replace(" ","_")
        plt.savefig(f'./out/plots/{sys.argv[2]}_{sys.argv[3]}_{title}.png')
    elif 'standard' in sys.argv[2]: 
        if sys.argv[2] == 'standard-fraction': 
            data = ternary_points
        elif sys.argv[2] == 'standard-total': 
            plt.yscale('log')
            data = raw_points
        nux = [i[0] for i in data]
        nue = [i[1] for i in data]
        nuebar = [i[2] for i in data]
        time = [time[i][1] for i in time_idx]
        d = {'time' : time,'nux' : nux, 'nue' : nue, 'nuebar' : nuebar}
        df = pd.DataFrame(d)
        print(df)
        df.to_csv(f"./out/data/raw_data_{sys.argv[1]}.dat")
        plt.ylabel("log(fluence)")
        plt.xlabel('time')
        plt.title('Fluence over time')
        plt.plot(time, nux, label="nux")
        plt.plot(time, nue, label='nue')
        plt.plot(time, nuebar, label='nuebar')
        plt.legend()
        title = sys.argv[1].replace(" ","_")
        plt.savefig(f'./out/plots/{sys.argv[2]}_{sys.argv[3]}_{title}.png')
        plt.show()
    else: 
        print("valid arguments: scatter, standard-fraction, standard-total, animation")
    