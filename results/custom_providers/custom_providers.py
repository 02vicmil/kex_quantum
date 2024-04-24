# Following two lines are for importing the parent folder
import sys, os
sys.path.append(os.path.join(sys.path[0], '..'))

from qcircuit_runner import Runner, Error
from grover import grovers_circuit
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# All connected graphs with 5 vertices
# See vicmil/couplings/find_all_unique_couplings.py and
#     vicmil/couplings/unique_couplings.txt
graphs = [
    [(0, 1), (0, 2), (0, 3), (0, 4)],
    [(0, 1), (0, 3), (0, 4), (1, 2)],
    [(0, 2), (0, 4), (1, 2), (1, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2)],
    [(0, 1), (0, 2), (0, 4), (1, 2), (1, 3)],
    [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3)],
    [(0, 1), (0, 4), (1, 2), (1, 3), (2, 3)],
    [(0, 3), (0, 4), (1, 2), (1, 4), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3)],
    [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)],
    [(0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 3)],
    [(0, 1), (0, 3), (0, 4), (1, 2), (1, 4), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 4), (2, 3)],
    [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
]

NUM_QUBITS = 3
N = 2**NUM_QUBITS
SHOTS = 1000

grovers = []

for i in range(0, N):
    grover = grovers_circuit(i, NUM_QUBITS, 1)
    grovers.append(grover)

ticks = [f"|{{0:0{NUM_QUBITS}b}}⟩".format(i) for i in range(0, N)]
ticks_range = np.arange(0, N)

noise_types = ["none", "readout", "bitflip", "phaseflip", "depolarizing"]
noise_sizes = [0.001, 0.01]

current_directory = os.getcwd()
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["figure.titlesize"] = 24
mpl.rcParams["font.size"] = 14

for graph_idx, coupling in enumerate(graphs):
    # Create folder for each graph
    folder_name = os.path.join(current_directory, f"{graph_idx}")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for noise in noise_types:
        for noise_idx, noise_size in enumerate(noise_sizes):
            if noise == noise_types[0] and noise_idx > 0:
                continue

            if noise == noise_types[0]:
                print(f"Running on Graph {graph_idx} with no noise...", end="")
            else:
                print(f"Running on Graph {graph_idx} with {noise} noise of amount {noise_size}...", end="")

            # Run on grover once for each marked element and store the resulting counts
            counts_per_marked = []
            depths_per_marked = []
            for i in range(0, N):
                # Compile grover for this marked element and for this coupling
                runner = Runner(grovers[i]).with_coupling_map(coupling, make_bidirectional=True)

                # Get noise
                if noise == noise_types[1]:
                    runner.with_readout_error(noise_size, noise_size)
                elif noise != noise_types[0]:
                    error = Error.bitflip
                    if noise == noise_types[3]:
                        error = Error.phaseflip
                    elif noise == noise_types[4]:
                        error = Error.depolarizing

                    error = error(noise_size)
                    runner.with_errors_on_gates([error], ['rz', 'sx'])\
                          .with_errors_on_gates([error.tensor(error)], ['cx'])

                counts_for_i = runner.run(plot_results=False)
                depth_for_i = runner.and_transpile().get_depth()
                depths_per_marked.append(depth_for_i)
                counts_for_i_as_array = [0 for _ in range(N)]
                for key_binary, value in counts_for_i.items():
                    index = int(key_binary, 2)
                    counts_for_i_as_array[index] = value
                counts_per_marked.append(counts_for_i_as_array)


            figure, (coupling_ax, measures_ax, depths_ax) = plt.subplots(3, 1, figsize=(9, 24))
            
            # Draw coupling map first
            runner.and_draw_coupling_map(ax=coupling_ax)
            coupling_ax.set_title("Coupling Map")
            
            # Draw heatmap
            heatmap = measures_ax.imshow(np.array(counts_per_marked), cmap=mpl.colormaps["magma"], vmin = 0, vmax=SHOTS)
            colorbar = measures_ax.figure.colorbar(heatmap, ax=measures_ax)
            colorbar.ax.set_ylabel("Amount Measured", rotation=-90, va="bottom")
            measures_ax.set_xticks(ticks_range, ticks)
            measures_ax.set_yticks(ticks_range, ticks)
            measures_ax.set_xlabel("Measured")
            measures_ax.set_ylabel("Marked")
            measures_ax.set_title(f"Results ({SHOTS} shots)")

            # Draw barplot of depths for each grover of marked element
            depths_ax.bar(ticks, depths_per_marked)
            depths_ax.set_ylabel("Depth")
            depths_ax.set_xlabel("Marked")
            depths_ax.set_title("Depths per Marked Element")

            file_name = f"{graph_idx}/{noise}_{noise_size}_grover_results.pdf"
            title = f"Graph {graph_idx} with {noise} noise of amount {noise_size}"
            if noise == noise_types[0]:
                file_name = f"{graph_idx}/no_noise_grover_results.pdf"
                title = f"Graph {graph_idx} with no noise"

            plt.suptitle(title)
            plt.savefig(file_name)
            print(f"Done! Results saved in {file_name}.")
            plt.close()