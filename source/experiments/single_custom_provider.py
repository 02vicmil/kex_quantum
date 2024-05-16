if __name__ != "__main__":
    exit(0)

from . import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys
import os

directory = get_directory_in_results(f"custom_providers/specific_couplings")

# Set up Grover's algorithm versions
grovers = []
for i in range(0, NUM_STATES):
    grover = grovers_circuit(i, NUM_QUBITS, 1)
    grovers.append(grover)

# Set up errors and their sizes
noise_types = ["Noiseless", "Readout", "Bitflip", "Phaseflip", "Depolarising"]
noise_sizes = [0.001, 0.01]

# Set up common matplotlib values
TICKS = [f"|{{0:0{NUM_QUBITS}b}}⟩".format(i) for i in range(0, NUM_STATES)]
TICKS_RANGE = np.arange(0, NUM_STATES)
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.size"] = 20

for graph_index in range(len(UNIQUE_5_COUPLINGS)):
    coupling = UNIQUE_5_COUPLINGS[graph_index]

    figure, axes = plt.subplots(3, 3, figsize=(15, 12), sharey=True, sharex=True)

    figure.text(0.5, 0.04, "Measured", ha="center")
    figure.text(0.04, 0.5, "Marked", va="center", rotation="vertical")
    figure.subplots_adjust(bottom=0.15)

    print(f"Running for graph {GRAPH_DEGREE_ENCODING[graph_index]}...")
    plot_index = 0
    index_permutation = [0, 1, 2, 3, 6, 4, 7, 5, 8]
    for noise in noise_types:
        for noise_idx, noise_size in enumerate(noise_sizes):
            if noise == noise_types[0] and noise_idx > 0:
                continue

            # Run on grover once for each marked element and store the resulting counts
            counts_per_marked = []
            depths_per_marked = []
            for i in range(0, NUM_STATES):
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
                    runner.with_errors_on_gates([error], ['rz', 'sx', 'x'])\
                        .with_errors_on_gates([error.tensor(error)], ['cx'])
                
                counts_for_i = runner.run(plot_results=False)
                counts_for_i_as_array = [0 for _ in range(NUM_STATES)]
                for key_binary, value in counts_for_i.items():
                    index = int(key_binary, 2)
                    counts_for_i_as_array[index] = value

                values = np.array(counts_for_i_as_array)
                percentage = 100*values / SHOTS
                percentage_int = 100*values // SHOTS
                remainders_with_indices = [(percentage[i] - percentage_int[i], i) for i in range(len(percentage))]
                remainders_with_indices.sort(key=lambda x: x[0], reverse=True)
                aux = 100-sum(percentage_int)
                for i in range(aux):
                    idx = remainders_with_indices[i][1]
                    percentage_int[idx] += 1

                counts_per_marked.append(percentage_int)


            index = index_permutation[plot_index]
            axis = axes[index//3][index%3]

            heatmap = axis.imshow(np.array(counts_per_marked), cmap=mpl.colormaps["magma"], vmin = 0, vmax=100)
            axis.set_xticks(TICKS_RANGE, TICKS, rotation=90)
            axis.set_yticks(TICKS_RANGE, TICKS)
            title = f"{noise_size} {noise}"
            if noise == noise_types[0]:
                title = f"{noise}"
            axis.set_title(title)
            plot_index += 1

            for (j,i),label in np.ndenumerate(counts_per_marked):
                color = "black"
                if label < 50:
                    color = "white"

                if i == j:
                    axis.text(i, j, label, ha='center', va='center', color=color, fontsize=16, weight="bold")

    # Draw heatmap
    colorbar = figure.colorbar(heatmap, ax=axes.ravel().tolist())
    colorbar.ax.set_ylabel("Correctly Measured (%)", rotation=-90, va="bottom")

    file_name = f"graph_{GRAPH_DEGREE_ENCODING[graph_index]}_grover_results.pdf"
    path = os.path.join(directory, file_name)

    plt.savefig(path)
    print(f"Done! Results saved in {path}.")
    plt.close()