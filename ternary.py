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


### parameters for file 
num_bins = 70
log_scale = .05
time_length = 10


def usage(): 
    print("ternary.py  by R. Gundakaram, \n")
    print("Usage:\n")
    print("python ternary.py title plot-type(scatter or trajectory) time-interval(linear orlog)\n")
    print("e.g. python ternary.py 'flux: livermore' scatter linear\n")


if len(sys.argv) != 4: 
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
        tax.left_axis_label("$\%\\nu_{x} (\\nu_{\\mu} + \\overline{\\nu}_{\\mu} + \
        \\nu_{\\tau} + \\overline{\\nu}_{\\tau})$ ", fontsize=fontsize, offset=0.14)
        tax.right_axis_label("$\%\\overline{\\nu}_e$", fontsize=fontsize, offset=0.14)
        tax.bottom_axis_label("$\%\\nu_e$" , fontsize=fontsize, offset=0.14)
        # Remove default Matplotlib Axes
        tax.clear_matplotlib_ticks()
        tax.get_axes().axis('off')

    
    # get the times and figure out time bins 
    with open("../fluxes/garching/garching_pinched_info_key.dat") as f: 
        time = []
        for line in f: 
            line = line.rstrip("\n")
            words = line.split()
            for i in enumerate(words): 
                words[i[0]] = float(i[1])
            time.append(words)
    
    end_time = time[len(time) - 1][1]
    if sys.argv[3] == 'log':
        end_time = math.log(end_time / log_scale + 1) 
        time_bin = end_time / num_bins
        time_bins = [log_scale * math.exp(time_bin* (i + 1)) - log_scale for i in range(num_bins)]
    elif sys.argv[3] == 'linear': 
        time_bin = end_time / num_bins
        time_bins = [time_bin * i for i in range(num_bins)]
    else: 
        print('valid time bin options: log, linear')
    cur = 0
    time_idx = []
    i = 0
    while cur < len(time): 
        current = time[cur][1] + .5 * time[cur][2]
        if current > time_bins[i]: 
            i += 1
            time_idx.append(cur)
        elif cur == len(time) - 1: 
            time_idx.append(cur)
        cur += 1
            
    # Dealing with files and points
    raw_points = []
    direc = os.listdir("../fluxes/garching_in")
    direc = natsorted(direc)
    for fil in enumerate(direc):
        with open("../fluxes/garching_in/" + fil[1]) as f:
            data = []
            for line in f:
                line = line.rstrip("\n")
                words = line.split()
                try: 
                    words = [float(word) for word in words]
                except: 
                    continue
                if words[0] != 0 :
                    data.append(words)
        vec = [sum(i) for i in zip(*data)]
        nux = vec[2] + vec[3] + vec[5] + vec[6]
        raw_points.append((nux, vec[1], vec[4]))
    
    points = []
    points_total = []
    for i in enumerate(time_idx): 
        if i[0] == 0: 
            start = 0
            end = i[1] + 1
            cur = raw_points[:i[1] + 1]
        else:
            start = time_idx[i[0] - 1] + 1
        end = i[1] + 1
        cur = raw_points[start:end]
        nue = sum([i[1] for i in cur])
        nuebar = sum([i[2] for i in cur])
        nux = sum([i[0] for i in cur])
        points_total.append((nue, nuebar, nux))
        total = nue + nuebar + nux
        concentrations = (nue / total * 100, nuebar / total * 100, nux / total * 100)
        # if 0 not in concentrations: 
        #     points.append(concentrations)

    # dealing with graphics
    fps = len(points) / time_length
    writer = animation.PillowWriter(fps=fps)

    # dealing with colors goes from blue to red
    # m = 1 / len(points)
    # red = [1 - m*i for i in range(len(points))]
    # green = [0 for i in range(len(points))]
    # blue = [m*i for i in range(len(points))]
    # rgb = list(zip(red,green,blue))
    rgb = [(1, 0, 0)]

    if sys.argv[2] == 'scatter': 
        tax.boundary(linewidth=1.5)
        tax.gridlines(color="black", multiple=20)
        tax.gridlines(color="blue", multiple=20, linewidth=0.5)
        tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
        tax.scatter(points, s=10, c=rgb, marker=".", linewidth=3, label="flux", alpha=.5)
        tax.legend()
        title = sys.argv[1].replace(" ","_")
        plt.savefig(f"./out/plots/{sys.argv[2]}_{sys.argv[3]}_{title}.png", writer=writer)
        tax.show()
    elif sys.argv[2] == 'animation': 
        for (i, point) in enumerate(points): 
            tax.boundary(linewidth=1.5)
            tax.gridlines(color="black", multiple=20)
            tax.gridlines(color="blue", multiple=20, linewidth=0.5)
            tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
            tax.scatter(points[0:i+1], c=rgb[0:i+1], s=10, marker=".", linewidth=3, label="flux", alpha=.5)
            cam.snap()
            print(f"frame number: {i}")
        ani = cam.animate()
        title = sys.argv[1].replace(" ","_") 
        ani.save(f"./out/animation/{sys.argv[2]}_{sys.argv[3]}_{title}.gif", writer=writer)
    elif sys.argv[2] == 'trajectory': 
        tax.boundary(linewidth=1.5)
        tax.gridlines(color="black", multiple=20)
        tax.gridlines(color="blue", multiple=20, linewidth=0.5)
        tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
        tax.plot_colored_trajectory(points, cmap="Spectral",linewidth=1, label="flux", alpha=.5)
        tax.scatter(points, s=10, c=rgb, marker=".", linewidth=3, label="flux", alpha=.5)
        tax.show()
        title = sys.argv[1].replace(" ","_")
        plt.savefig(f'./out/plots/{sys.argv[2]}_{sys.argv[3]}_{title}.png')
    elif 'standard' in sys.argv[2]: 
        if sys.argv[2] == 'standard-fraction': 
            data = points
        elif sys.argv[2] == 'standard-total': 
            plt.yscale('log')
            data = points_total
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
    