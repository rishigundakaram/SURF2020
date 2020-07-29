import math
import sys
from ternary import plotting
from ternary import ternary_axes_subplot as ternary
from celluloid import Camera
from natsort import natsorted
import os


flavors = ['nue', 'nuebar', 'numu', 'numubar', 'nutau', 'nutaubar']
interactions = {
    "nc":["O16"], 
    "cc":["O16", "e"]
}
file_dir = "../out/garching_in/"

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
        print(f"i:{i}")
        if i[0] == 0:
            start = 0
        else:
            start = time_idx[i[0] - 1] + 1
        end = i[1] + 1
        cur = points[start:end]
        nue = sum([j[0] for j in cur])
        nuebar = sum([j[1] for j in cur])
        nux = sum([j[2] for j in cur])
        raw_points.append((nue, nuebar, nux))
        total = nue + nuebar + nux
        concentrations = (nue / total * 100, nuebar / total * 100, nux / total * 100)
        if 0 not in concentrations: 
            ternary_points.append(concentrations)
        else: 
            idx_rem.append(i[1])
    for i in idx_rem: 
        time_idx.remove(i)
    return (raw_points, ternary_points)


def get_events_from_flux(flux, detector, smeared=True):
    events = [0 for i in range(6)]
    for (i, flavor) in enumerate(flavors): 
        for inter in interactions.keys(): 
            events[i] += total_events_from_type(flux, "wc100kt30prct", flavor, inter, smeared=smeared)
    point = (events[0], events[1], sum(events[2:]))
    return point

def total_events_from_type(flux, detector, neutrino, interaction, smeared=True): 
    filename = file_dir + flux + "_"
    if interaction == 'nc': 
        sub = f"nc_{neutrino}_"
    else: 
        sub = f"{neutrino}_"
    if smeared: 
        smear = "events_smeared"
    else: 
        smear = "events"
    filenames = [f"{filename}{sub}{i}_{detector}_{smear}.dat" for i in interactions[interaction]]
    print(filenames)
    total_events = 0
    for filename in filenames: 
        try: 
            with open(filename) as f: 
                for line in f: 
                    data = line.split()
                events = float(data[1])
                total_events += events 
        except:
            print("improper configuration")
    return total_events
    
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