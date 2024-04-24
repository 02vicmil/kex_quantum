# Following two lines are for importing the parent folder
import sys, os
sys.path.append(os.path.join(sys.path[0], '..'))

from qcircuit_runner import Runner
from grover import grovers_circuit
import qiskit_ibm_runtime.fake_provider as fp
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from grid_positions import positions

NUM_QUBITS = 3
N = 2**NUM_QUBITS
SHOTS = 1000

grovers : list[Runner] = []

for i in range(0, N):
    grover = grovers_circuit(i, NUM_QUBITS, 1)
    grovers.append(Runner(grover).with_shots(SHOTS))

ticks = [f"|{{0:0{NUM_QUBITS}b}}⟩".format(i) for i in range(0, N)]
ticks_range = np.arange(0, N)

mpl.rcParams["font.family"] = "serif"


for name, data in positions.items():

    backend = eval(f"fp.{name}()")

    # Run on grover once for each marked element and store the resulting counts
    counts_per_marked = []
    depths_per_marked = []
    for i in range(0, N):
        counts_for_i = grovers[i].with_backend(backend).run(plot_results=False)
        depth_for_i = grovers[i].and_transpile().get_depth()
        depths_per_marked.append(depth_for_i)
        counts_for_i_as_array = [0 for _ in range(N)]
        for key_binary, value in counts_for_i.items():
            index = int(key_binary, 2)
            counts_for_i_as_array[index] = value
        counts_per_marked.append(counts_for_i_as_array)

    coupling_figure, coupling_ax = plt.subplots(figsize=data["ratio"], layout="constrained")
    measures_figure, measures_ax = plt.subplots()

    # Draw coupling map first
    grovers[0].and_draw_coupling_map(ax=coupling_ax, color_used_qubits=True, grid_positions=data["positions"])

    # Draw heatmap
    heatmap = measures_ax.imshow(np.array(counts_per_marked), cmap=mpl.colormaps["magma"], vmin=0, vmax=SHOTS)
    colorbar = measures_ax.figure.colorbar(heatmap, ax=measures_ax)
    colorbar.ax.set_ylabel("Amount Measured", rotation=-90, va="bottom")
    measures_ax.set_xticks(ticks_range, ticks)
    measures_ax.set_yticks(ticks_range, ticks)
    measures_ax.set_xlabel("Measured")
    measures_ax.set_ylabel("Marked")

    plt.savefig(f"{name}_grover_results.pdf")
    plt.figure(coupling_figure)
    plt.savefig(f"{name}_coupling.pdf")
    print(f"Done with {name}")