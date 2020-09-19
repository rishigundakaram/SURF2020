import math
import matplotlib
import sys
if "animation" in sys.argv[1]:
    matplotlib.use("Agg")
from ternary import plotting
from ternary import ternary_axes_subplot as ternary
from celluloid import Camera
from natsort import natsorted
import matplotlib.animation as animation
import os
import string
import matplotlib.pyplot as plt
from pprint import pprint
from matplotlib.colors import LinearSegmentedColormap as lsc
from ternary.helpers import simplex_iterator
import numpy as np

flavors = ['nue', 'nuebar', 'numu', 'numubar', 'nutau', 'nutaubar']

cdict= {
    'red': ((0.0, 0.0, 1.0), (1.0, 1.0, 0.0)),
    'green': ((0.0,0.0,0.0), (1.0,0.0,0.0)),
    'blue':((0.0,0.0,0.0), (1.0,0.0,0.0)),
    'alpha': ((0.0,0.0,.75), (1.0, .75, 0.0))
}
cmap_red = lsc("red-constant",cdict)


def get_labels(detector, interactions): 
    out = interactions[detector]
    labels = [0, 0, 0]
    for (i, label) in enumerate(out): 
        separator = ""
        if type(label) == list: 
            for l in label: 
                l = l.replace("_", "")
                separator += f"%{l}, "
        else: 
            separator = f"%{label}"
        labels[i] = separator
        separator = ""
    return labels


def generate_time_bins(filename, log_scale, num_bins): 
    with open(filename) as f: 
        time = []
        for line in f: 
            line = line.rstrip("\n")
            words = line.split()
            for i in enumerate(words): 
                words[i[0]] = float(i[1])
            time.append(words)
    end_time = time[len(time) - 1][1]
    end_time = math.log(end_time / log_scale + 1) 
    time_bin = end_time / num_bins
    time_bins = [log_scale * math.exp(time_bin* (i + 1)) - log_scale for i in range(num_bins)]

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
    return (time, time_idx)

# points is a list of tuples in the format(nue, neubar, nux), time_idx is a list of the cutoffs for binning
def consolidate_points(points, time_idx): 
    idx_rem = []
    raw_points = []
    ternary_points = []
    for i in enumerate(time_idx): 
        if i[0] == 0:
            start = 0
        else:
            start = time_idx[i[0] - 1] + 1
        end = i[1] + 1
        cur = points[start:end]
        nue = sum([j[0] for j in cur])
        nuebar = sum([j[1] for j in cur])
        nux = sum([j[2] for j in cur])
        total = nue + nuebar + nux
        concentrations = (nue / total * 100, nuebar / total * 100, nux / total * 100)
        if 0 not in concentrations: 
            ternary_points.append(concentrations)
            raw_points.append((nue, nuebar, nux))
        else: 
            idx_rem.append(i[1])
    for i in idx_rem: 
        time_idx.remove(i)
    return (raw_points, ternary_points)


    
def generate_title(typee="", sub=""):
    sp1 =  ""
    if typee != "": 
        sp1 = " "
    sp2 = ""
    if sub != "": 
        sp2 = " "
    return f"{typee}{sp1}{sub}{sp2}{sys.argv[1]}"

def shared_plotting_script(title, labels, ternary_points_events, raw_points_events, time, time_idx, fps, heatmap_data=None):
    labels = [i.replace("_", "") for i in labels]
    left, center, right = labels
    writer = animation.PillowWriter(fps=fps)
    cmap = lsc("red-constant",cdict, gamma=0)
    if 'standard' not in sys.argv[1]:
        scale = 100
        figure, tax = ternary.figure(scale=scale) 
        cam = Camera(figure)
        fontsize = 12
        tax.set_title(title , fontsize=fontsize)
        tax.right_axis_label(right, fontsize=fontsize, offset=0.14)
        tax.bottom_axis_label(center, fontsize=fontsize, offset=0.14)
        tax.left_axis_label(left , fontsize=fontsize, offset=0.14)
        tax.clear_matplotlib_ticks()
        tax.get_axes().axis('off')
    rgb_events = [(0, 1, 0)]
    rgb_green = [(0,1,0)]
    rgb_flux = [(1, 0, 0,.5)]
    if sys.argv[1] == 'animation':
        for (i, point) in enumerate(ternary_points_events):
            tax.boundary(linewidth=1.5)
            tax.gridlines(color="black", multiple=20)
            tax.gridlines(color="blue", multiple=20, linewidth=0.5)
            tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
            tax.scatter(ternary_points_events[0:i+1], c=rgb_events[0:i+1], s=10, marker=".", linewidth=3, label="flux", alpha=.5, zorder=4)
            tax.plot_colored_trajectory(ternary_points_events[0:i+1], linewidths=1, cmap=cmap, zorder=3)
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
        tax.scatter(ternary_points_events, c=rgb_events, s=10, marker=".", linewidth=3, label="flux", alpha=.5)
        plt.savefig(f"./out/plots/{title}.png", writer=writer)
        tax._redraw_labels()
        tax.show()
    elif 'standard' in sys.argv[1]: 
        if sys.argv[1] == 'standard-fraction': 
            data = ternary_points_events
            plt.ylabel('events')
        elif sys.argv[1] == 'standard-total': 
            plt.yscale('log')
            plt.ylabel('log(events)')
            data = raw_points_events
        nux = [i[0] for i in data]
        nue = [i[1] for i in data]
        nuebar = [i[2] for i in data]
        time = [time[i][1] for i in time_idx]
        plt.xlabel('time')
        plt.title('events over time')
        plt.plot(time, nux, label=left)
        plt.plot(time, nue, label=center)
        plt.plot(time, nuebar, label=right)
        plt.legend()
        plt.savefig(f"./out/plots/{title}.png", writer=writer)
        plt.show()
    elif 'heatmap' in sys.argv[1]: 
        if "animation" in sys.argv[1]: 
            red = [(1,0,0)]
            green = [(0,1,0)]
            for i in range(len(ternary_points_events[0])): 
                tax.boundary(linewidth=1.5)
                tax.gridlines(color="black", multiple=20)
                tax.gridlines(color="blue", multiple=20, linewidth=0.5)
                tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
                heatmap_data_ih = generate_heatmap_dict(raw_points_events[0][0:i+1], ternary_points_events[0][0:i+1], 1)
                heatmap_data_nh = generate_heatmap_dict(raw_points_events[1][0:i+1], ternary_points_events[1][0:i+1], .5)
                heatmap_data = consolidate_heatmap_data(heatmap_data_nh, heatmap_data_ih)
                tax.heatmap(heatmap_data, style='hexagonal', colorbar=False)
                tax.scatter(ternary_points_events[0][0:i+1], c=red, s=10, marker=".", linewidth=3, label="flux", alpha=.5, zorder=5)
                tax.scatter(ternary_points_events[1][0:i+1], c=green, s=10, marker=".", linewidth=3, label="flux", alpha=.5, zorder=5)
                # tax.plot_colored_trajectory(ternary_points_events[0][0:i+1], linewidths=1, cmap=cmap, zorder=4)
                tax.annotate(text=f"{time[time_idx[i]][1]}s", position=(.15,.85), xytext=(-20, -20))
                cam.snap()
                print(f"frame number: {i}")
            ani = cam.animate()
            ani.save(f"./out/animation/{title}.gif", writer=writer)
        elif "scatter" in sys.argv[1]:
            tax.boundary(linewidth=1.5)
            tax.gridlines(color="black", multiple=20)
            tax.gridlines(color="blue", multiple=20, linewidth=0.5)
            tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
            tax.heatmap(heatmap_data, style='hexagonal', colorbar=True)
            for ternary_points in ternary_points_events: 
                tax.scatter(ternary_points, c=rgb_events, s=10, marker=".", linewidth=3, label="flux", alpha=.5, zorder=5)
                rgb_events = [(1, 0, 0)]
            plt.savefig(f"./out/plots/{title}.png", writer=writer)
        plt.show()

def error_function(check_point, measured_point): 
    """
    Parameters: 
    check_point: 3-tuple of index of point which is being considered. i + j + k = 100
    measured point: 3-tuple of number of events in each channel 
    Returns: 
    prob(check_point[0] / 100, check_point[1] / 100)
    """
    A = measured_point[0]
    B = measured_point[1]
    fA = check_point[0] / sum(check_point)
    fB = check_point[1] / sum(check_point)
    mfA = measured_point[0] / sum(measured_point) 
    mfB = measured_point[1] / sum(measured_point)
    sigfA = math.sqrt(mfA * (1 - mfA) / sum(measured_point))
    sigfB = math.sqrt(mfB * (1 - mfB) / sum(measured_point))
    sigAB = -1 * A  * B / math.pow(sum(measured_point), 3)
    rho = sigAB / (sigfA * sigfB)
    p1 = 1 / (2 * math.pi * sigfA * sigfB * math.sqrt(1 - rho * rho))
    p3 = (fA - mfA) * (fA - mfA) / (sigfA * sigfA) + (fB - mfB) * (fB - mfB) / (sigfB * sigfB) - 2 * rho * (fA - mfA) * (fB - mfB) / (sigfA * sigfB)

    p2 = math.exp(-.5 / (1 - rho * rho) * p3)
    prob = p1 * p2 
    return prob

def heatmap_shader(check_point, measured_point, shader): 
    """
    takes in the current point to check and the mean point. returns 1 if error functions is larger for 
    current point than measured point. returns 0 otherwise. 
    """
    p1 = error_function(check_point, measured_point)
    p2 = error_function(measured_point, measured_point) / math.pi
    if p1 > p2: return shader
    return 0


def get_closest_point(check_point, ternary_points, raw_points): 
    norm = [np.linalg.norm([a - b for a, b, in zip(check_point, i)]) for i in ternary_points]
    return raw_points[norm.index(min(norm))]

def generate_heatmap_dict(raw_points, ternary_points, shader=1, scale=100): 
    d = dict()
    for (i, j, k) in simplex_iterator(scale):
        mean = get_closest_point((i, j, k), ternary_points, raw_points)
        d[(i, j, k)] = heatmap_shader((i,j,k), mean, shader)
    return d

def consolidate_heatmap_data(h1, h2): 
    ret = dict()
    for key in h1.keys(): 
        v1 = h1[key]
        v2 = h2[key]
        if v1 == 0 and v2 == 0: 
            cur = 0
        elif v1 == 0: 
            cur = v2 
        elif v2 == 0: 
            cur = v1
        else: 
            cur = (v1 + v2) / 2
        ret[key] = cur
    return ret
