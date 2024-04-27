if __name__ != "__main__":
    exit(0)

from . import Runner, Error, grovers_circuit, get_directory_in_results, UNIQUE_5_COUPLINGS, NUM_QUBITS, NUM_STATES, SHOTS
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

directory = get_directory_in_results("custom_providers/all")

# Set up Grover's algorithm versions
grovers = []
for marked_element in range(0, NUM_STATES):
    grover = grovers_circuit(marked_element, NUM_QUBITS, 1)
    grovers.append(grover)

# Set up errors and their sizes
ERROR_TYPES = ["None", "Readout", "Bitflip", "Phaseflip", "Depolarising"]
ERROR_SIZES = [0.001, 0.01]

# Set up common matplotlib values
TICKS = [f"|{{0:0{NUM_QUBITS}b}}⟩".format(i) for i in range(0, NUM_STATES)]
TICKS_RANGE = np.arange(0, NUM_STATES)

mpl.rcParams["font.family"] = "serif"
mpl.rcParams["figure.titlesize"] = 24
mpl.rcParams["font.size"] = 14

for graph_idx, coupling in enumerate(UNIQUE_5_COUPLINGS):
    # Create folder for each graph
    folder_name = os.path.join(directory, f"{graph_idx}")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for error_type in ERROR_TYPES:
        for error_index, error_size in enumerate(ERROR_SIZES):
            
            # Skip duplicating errorless version. Just do it for error_index = 0
            if error_type == ERROR_TYPES[0] and error_index > 0:
                continue

            if error_type == ERROR_TYPES[0]:
                print(f"Running on Graph {graph_idx} with no noise...", end="")
            else:
                print(f"Running on Graph {graph_idx} with {error_type} noise of amount {error_size}...", end="")

            # Run Grover once for each marked element and store the resulting counts
            counts_per_marked = []
            depths_per_marked = []
            for marked_element in range(0, NUM_STATES):
                # Compile Grover for this marked element and for this coupling
                runner = Runner(grovers[marked_element])\
                            .with_coupling_map(coupling, make_bidirectional=True)

                # Get noise
                if error_type == ERROR_TYPES[1]:
                    runner.with_readout_error(error_size, error_size)
                elif error_type != ERROR_TYPES[0]:
                    error = Error.bitflip
                    if error_type == ERROR_TYPES[3]:
                        error = Error.phaseflip
                    elif error_type == ERROR_TYPES[4]:
                        error = Error.depolarizing
                    error = error(error_size)
                    runner.with_errors_on_gates([error], ['rz', 'sx', 'x'])\
                          .with_errors_on_gates([error.tensor(error)], ['cx'])

                counts_for_i = runner.run(plot_results=False)
                depth_for_i = runner.and_transpile().get_depth()
                depths_per_marked.append(depth_for_i)
                counts_for_i_as_array = [0 for _ in range(NUM_STATES)]
                for key_binary, value in counts_for_i.items():
                    index = int(key_binary, 2)
                    counts_for_i_as_array[index] = value
                counts_per_marked.append(counts_for_i_as_array)

            figure, (coupling_ax, measures_ax, depths_ax) = plt.subplots(3, 1, figsize=(9, 24))
            
            # Draw coupling map first
            runner.and_draw_coupling_map(axis=coupling_ax)
            coupling_ax.set_title("Coupling Map")
            
            # Draw heatmap
            heatmap = measures_ax.imshow(np.array(counts_per_marked), cmap=mpl.colormaps["magma"], vmin = 0, vmax=SHOTS)
            colorbar = measures_ax.figure.colorbar(heatmap, ax=measures_ax)
            colorbar.ax.set_ylabel("Amount Measured", rotation=-90, va="bottom")
            measures_ax.set_xticks(TICKS_RANGE, TICKS)
            measures_ax.set_yticks(TICKS_RANGE, TICKS)
            measures_ax.set_xlabel("Measured")
            measures_ax.set_ylabel("Marked")
            measures_ax.set_title(f"Results ({SHOTS} shots)")

            # Draw barplot of depths for each grover of marked element
            depths_ax.bar(TICKS, depths_per_marked)
            depths_ax.set_ylabel("Depth")
            depths_ax.set_xlabel("Marked")
            depths_ax.set_title("Depths per Marked Element")

            file_name = f"{graph_idx}/{error_type}_{error_size}_grover_results.pdf"
            title = f"Graph {graph_idx} with {error_type} noise of amount {error_size}"
            if error_type == ERROR_TYPES[0]:
                file_name = f"{graph_idx}/no_noise_grover_results.pdf"
                title = f"Graph {graph_idx} with no noise"

            plt.suptitle(title)
            path = os.path.join(directory, file_name)
            plt.savefig(path)
            print(f"Done! Results saved in {path}.")
            plt.close()