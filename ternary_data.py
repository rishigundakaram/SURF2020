import os
from natsort import natsorted
import numpy as np


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

def get_raw_points_for_multiple_channels(flux_dir, event_dir, key_dir, interactions, include_channels, osc="", smear=True):
    points = []
    if osc != "": osc += "/"
    for (channel, config) in include_channels: 
        direc = f"{event_dir}{channel}/{osc}"
        points_events = np.array(total_events_from_flux(channel, config, flux_dir, direc, interactions, smeared=smear)) 
        if len(points) == 0: 
            points = np.zeros((len(points_events), 3))
        for (i, inter) in enumerate(interactions[channel]): 
            if 'ibd' in inter: 
                points[:,0] += points_events[:,i]
            elif 'nue' in inter or '_e' in inter: 
                points[:,1] += points_events[:,i]
            elif 'nc' in inter: 
                points[:,2] += points_events[:,i]
    points = points.tolist()
    return points

def total_events_from_flux(detector, config, flux_dir, out_dir, interactions, smeared=True): 
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

def load_detector(channel): 
    conf = []
    with open(f"../channels/channels_{channel}.dat") as f: 
        for line in f: 
            line = line.split(" ")
            conf.append(line[0])
    return conf