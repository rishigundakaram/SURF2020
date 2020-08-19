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
from pprint import pprint
from matplotlib.colors import LinearSegmentedColormap as lsc


flavors = ['nue', 'nuebar', 'numu', 'numubar', 'nutau', 'nutaubar']
interactions = {
    "argon" : ["nue_Ar40", "_e", "nc"], 
    "water" : ["ibd", ["_e", "nue_O16"], "nc"], 
    "scint" : ["ibd", ["_e_", "nue_C12"], "nc"]
}
cdict= {
    'red': ((0.0, 0.0, 1.0), (1.0, 1.0, 0.0)),
    'green': ((0.0,0.0,0.0), (1.0,0.0,0.0)),
    'blue':((0.0,0.0,0.0), (1.0,0.0,0.0)),
    'alpha': ((0.0,0.0,.75), (1.0, .75, 0.0))
}
cmap = lsc("red-constant",cdict)
def total_events_from_flux(detector, config, flux_dir, out_dir, smeared=True): 
    fluxes = os.listdir(flux_dir)
    fluxes = natsorted(fluxes)
    channels = load_detector(detector)
    chan = []
    for inter in interactions[detector]: 
        if type(inter) == list: 
            lst = []
            for cur in inter: 
                check = [i for i in channels if cur in i]
                if inter != 'nc': 
                    check = [i for i in check if 'nc' not in i]
                lst.extend(check)
            chan.append(lst)
        else: 
            check = [i for i in channels if inter in i]
            if inter != 'nc': 
                check = [i for i in check if 'nc' not in i]
            chan.append(check)
    total_events = []
    for flux in fluxes: 
        flux = flux.replace(".dat", "")
        sub_total_events = [0 , 0, 0] 
        for (i, c) in enumerate(chan): 
            subtotal = 0
            for cur in c: 
                filename = f"{out_dir}{flux}_{cur}_{config}_events"
                if smeared: 
                    filename += "_smeared"
                filename += ".dat"
                with open(filename) as f: 
                    for line in f: 
                        data = line.split()
                    subtotal += float(data[1])
            sub_total_events[i] = subtotal
        total_events.append(sub_total_events)
    return total_events

def get_labels(detector): 
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


def time_bins(filename, log_scale, num_bins): 
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

def load_detector(channel): 
    conf = []
    with open(f"../channels/channels_{channel}.dat") as f: 
        for line in f: 
            line = line.split(" ")
            conf.append(line[0])
    return conf
    
def get_raw_points_for_flux(directory): 
    raw_points = []
    direc = os.listdir(directory)
    direc = natsorted(direc)
    for fil in enumerate(direc):
        with open(directory + fil[1]) as f:
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
        raw_points.append((vec[1], vec[4], nux))
    return raw_points

def shared_plotting_script(title, labels, ternary_points_events, raw_points_events, time, time_idx, fps, boundary=None):
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
    if 'standard' not in sys.argv[1]:
        scale = 100
        figure, tax = ternary.figure(scale=scale) 
        cam = Camera(figure)
        fontsize = 12
        tax.set_title(title , fontsize=fontsize)
        tax.right_axis_label(center, fontsize=fontsize, offset=0.14)
        tax.bottom_axis_label(left, fontsize=fontsize, offset=0.14)
        tax.left_axis_label(right, fontsize=fontsize, offset=0.14)
        tax.clear_matplotlib_ticks()
        tax.get_axes().axis('off')
    rgb_events = [(0, 0, 1)]
    rgb_green = [(0, 1, 0)]
    rgb_flux = [(1, 0, 0,.5)]
    if sys.argv[1] == 'animation':
        if not boundary: 
            for (i, point) in enumerate(ternary_points_events):
                tax.boundary(linewidth=1.5)
                tax.gridlines(color="black", multiple=20)
                tax.gridlines(color="blue", multiple=20, linewidth=0.5)
                tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
                tax.scatter(ternary_points_events[0:i+1], c=rgb_events[0:i+1], s=10, marker=".", linewidth=3, label="flux", alpha=.5)
                tax.plot_colored_trajectory(ternary_points_events[0:i+1], linewidths=1, cmap=cmap)
                tax.annotate(text=f"{time[time_idx[i]][1]}s", position=(.15,.85), xytext=(-20, -20))
                cam.snap()
                print(f"frame number: {i}")
        else: 
            temp = []
            for i in range(len(time_idx)):
                temp.extend(boundary[i])
                tax.boundary(linewidth=1.5)
                tax.gridlines(color="black", multiple=20)
                tax.gridlines(color="blue", multiple=20, linewidth=0.5)
                tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
                tax.scatter(temp, c=rgb_events[0:i+1], s=10, marker=".", linewidth=3, label="flux", alpha=.5)
                tax.scatter(ternary_points_events[0:i+1], c=rgb_green[0:i+1], s=10, marker=".", linewidth=3, label="flux", alpha=.5)
                tax.plot_colored_trajectory(ternary_points_events[0:i+1], linewidths=1, cmap=cmap)
                tax.annotate(text=f"{time[time_idx[i]][1]}s", position=(.15,.85), xytext=(-20, -20))
                cam.snap()
                print(f"frame number: {i}")
        ani = cam.animate()
        ani.save(f"./out/animation/{sys.argv[1]}_{title}.gif", writer=writer)
    elif sys.argv[1] == 'scatter':
        tax.boundary(linewidth=1.5)
        tax.gridlines(color="black", multiple=20)
        tax.gridlines(color="blue", multiple=20, linewidth=0.5)
        tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
        tax.scatter(ternary_points_events, c=rgb_events, s=10, marker=".", linewidth=3, label="flux", alpha=.5)
        plt.savefig(f"./out/plots/{sys.argv[1]}_{title}.png", writer=writer)
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
        plt.savefig(f"./out/plots/{sys.argv[1]}_{title}.png", writer=writer)
        plt.show()

def calculate_uncertainty(raw_points): 
    x = lambda num, tot : math.sqrt(num * (tot - num) / math.pow(tot, 3))
    y = [[100 * x(j, sum(i)) for j in i] for i in raw_points]
    pprint(y)
    return y 

def within(x, p, e):
    if x >= p - e and x <= p + e: 
        return True 
    return False 

def boundary_points(points, uncertainty): 
    check = []
    sub = [[x + uncertainty[i], x - uncertainty[i]] for (i, x) in enumerate(points)]
    pprint(sub)
    check.append((sub[0][0], sub[1][0], 100 - sub[0][0] - sub[1][0]))
    check.append((sub[0][0], sub[1][1], 100 - sub[0][0] - sub[1][1]))
    check.append((sub[0][1], sub[1][0], 100 - sub[0][1] - sub[1][0]))
    check.append((sub[0][1], sub[1][1], 100 - sub[0][1] - sub[1][1]))
    check.append((100 - sub[1][0] - sub[2][0], sub[1][0], sub[2][0]))
    check.append((100 - sub[1][0] - sub[2][1], sub[1][0], sub[2][1]))
    check.append((100 - sub[1][1] - sub[2][0], sub[1][1], sub[2][0]))
    check.append((100 - sub[1][1] - sub[2][1], sub[1][1], sub[2][1]))
    check.append((sub[0][0], 100 - sub[0][0] - sub[2][0], sub[2][0]))
    check.append((sub[0][0], 100 - sub[0][0] - sub[2][1], sub[2][1]))
    check.append((sub[0][1], 100 - sub[0][1] - sub[2][0], sub[2][0]))
    check.append((sub[0][1], 100 - sub[0][1] - sub[2][1], sub[2][1]))
    print(check)
    check = [i for i in check if within(i[0] + i[1] + i[2], 100, .5)]
    check = [i for i in check if within(i[0], points[0], uncertainty[0])]
    check = [i for i in check if within(i[1], points[1], uncertainty[1])]
    check = [i for i in check if within(i[2], points[2], uncertainty[2])]
    return check 

def run_boundary_points(raw_points, uncertainty): 
    ret = []
    for i in range(len(raw_points)): 
        ret.append(boundary_points(raw_points[i], uncertainty[i]))
    return ret

