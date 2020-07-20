import matplotlib
import sys
if sys.argv[2] == 'animation':
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ternary import plotting
from ternary import ternary_axes_subplot as ternary
import re

import math
from celluloid import Camera
import matplotlib.animation as animation
import os


### parameters for file 
time_length = 10
num_points = 20
fps = num_points / time_length
writer = animation.PillowWriter(fps=fps)

def usage(): 
    print("ternary.py  by R. Gundakaram, \n")
    print("Usage:\n")
    print("python ternary.py title plot-type(scatter or trajectory)\n")
    print("e.g. python ternary.py 'flux: livermore' scatter\n")


if len(sys.argv) != 3: 
    usage()
else: 
    if sys.argv[2] != 'standard':
        scale = 100
        figure, tax = ternary.figure(scale=scale)   
        # figure.set_size_inches(6, 6)
        cam = Camera(figure)
        # Draw Boundary and Gridlines
    

        # Set Axis labels and Title
        fontsize = 12
        tax.set_title(sys.argv[1] + "\n" , fontsize=fontsize)
        tax.left_axis_label("$\%\\nu_{x} (\\nu_{\\mu} + \\overline{\\nu}_{\\mu} + \
        \\nu_{\\tau} + \\overline{\\nu}_{\\tau})$ ", fontsize=fontsize, offset=0.14)
        tax.right_axis_label("$\%\\overline{\\nu}_e$", fontsize=fontsize, offset=0.14)
        tax.bottom_axis_label("$\%\\nu_e$" , fontsize=fontsize, offset=0.14)

        # Set ticks

        # Remove default Matplotlib Axes
        tax.clear_matplotlib_ticks()
        tax.get_axes().axis('off')

    # getting times 
    with open("../fluxes/garching/garching_pinched_info_key.dat") as f: 
        time = []
        for line in f: 
            line = line.rstrip("\n")
            words = line.split()
            time.append(float(words[1]))    # Dealing with files and points
    points = []
    raw_points = []
    for fil in os.listdir("../fluxes/garching_in"):
        with open("../fluxes/garching_in/" + fil) as f:
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
        total = sum(vec)
        nue = vec[1] / total * 100
        nuebar = vec[4] / total * 100
        nux = nux / total * 100
        concentrations = (nue, nuebar, nux)
        points.append(concentrations)

    # reduce the overall number of points \
    frames = math.floor(len(points) / num_points) 
    points = [i[1] for i in enumerate(points) if i[0] % frames == 0]

    # reduce raw points
    raw_points = [i[1] for i in enumerate(raw_points) if i[0] % frames == 0]
    time = [i[1] for i in enumerate(time) if i[0] % frames == 0]
    # dealing with colors goes from blue to red
    m = 1 / len(points)
    red = [1 - m*i for i in range(len(points))]
    green = [0 for i in range(len(points))]
    blue = [m*i for i in range(len(points))]
    rgb = list(zip(red,green,blue))

    if sys.argv[2] == 'scatter': 
        tax.boundary(linewidth=1.5)
        tax.gridlines(color="black", multiple=20)
        tax.gridlines(color="blue", multiple=20, linewidth=0.5)
        tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
        tax.scatter(points, s=30, c=rgb, marker=".", linewidth=3, label="flux", alpha=.8)
        tax.legend()
        tax.show()
    elif sys.argv[2] == 'animation': 
        for (i, point) in enumerate(points): 
            if i == 0: 
                continue
            tax.boundary(linewidth=1.5)
            tax.gridlines(color="black", multiple=20)
            tax.gridlines(color="blue", multiple=20, linewidth=0.5)
            tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
            tax.scatter(points[0:i+1], c=rgb[0:i+1], s=10, marker=".", linewidth=3, label="flux", alpha=.5)
            cam.snap()
            print(f"frame number: {i}")
        ani = cam.animate(repeat=False)
        title = sys.argv[1].replace(" ","_")
        ani.save(f"./out/animation/{title}.gif", writer=writer)
    elif sys.argv[2] == 'trajectory': 
        tax.boundary(linewidth=1.5)
        tax.gridlines(color="black", multiple=20)
        tax.gridlines(color="blue", multiple=20, linewidth=0.5)
        tax.ticks(axis='lbr', linewidth=1, multiple=20, offset=.02)
        tax.plot_colored_trajectory(points, linewidth=.5, label="flux", alpha=.8)
        tax.legend()
        tax.show()
    elif sys.argv[2] == 'standard': 
        nux = [i[0] for i in points]
        nue = [i[1] for i in points]
        nuebar = [i[2] for i in points]
        print(nux)
        print(nue)
        print(nuebar)
        plt.ylabel("% fluence")
        plt.xlabel('time')
        plt.title('Fluence over time')
        plt.plot(time, nux, label='nux')
        plt.plot(time, nue, label='nue')
        plt.plot(time, nuebar, label='nuebar')
        plt.legend()
        plt.savefig(f'./plots/standard_{sys.argv[1]}.png')
        plt.show()
    else: 
        print("valid arguments: scatter, standard, animation")
    