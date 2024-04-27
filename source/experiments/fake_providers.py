if __name__ != "__main__":
    exit(0)

from . import Runner, grovers_circuit, get_directory_in_results, NUM_QUBITS, NUM_STATES, SHOTS
import qiskit_ibm_runtime.fake_provider as fp
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

directory = get_directory_in_results("fake_providers/all")

# Set up Grover's algorithm versions
grovers : list[Runner] = []
for marked_element in range(0, NUM_STATES):
    grover = grovers_circuit(marked_element, NUM_QUBITS, 1)
    grovers.append(Runner(grover).with_shots(SHOTS))

# Set up common matplotlib values
TICKS = [f"|{{0:0{NUM_QUBITS}b}}⟩".format(i) for i in range(0, NUM_STATES)]
TICKS_RANGE = np.arange(0, NUM_STATES)
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["figure.titlesize"] = 24
mpl.rcParams["font.size"] = 14

couplings_directory = get_directory_in_results("unique_qubit_couplings")
with open(os.path.join(couplings_directory, "provider_qubit_couplings.txt"), "r") as providers_file:
    for line in providers_file:
        name = line.split(" ")[0]
        if not name[0].isalpha():
            continue

        print(f"Running on {name}...", end="")
        try:
            backend = eval(f"fp.{name}()")

            # Run on grover once for each marked element and store the resulting counts
            counts_per_marked = []
            depths_per_marked = []
            for marked_element in range(0, NUM_STATES):
                counts_for_marked_element = grovers[marked_element].with_backend(backend).run(plot_results=False)
                depth_for_marked_element = grovers[marked_element].and_transpile().get_depth()
                depths_per_marked.append(depth_for_marked_element)
                counts_for_marked_element_as_array = [0 for _ in range(NUM_STATES)]
                for key_as_binary, value in counts_for_marked_element.items():
                    index = int(key_as_binary, 2)
                    counts_for_marked_element_as_array[index] = value
                counts_per_marked.append(counts_for_marked_element_as_array)

            figure, (coupling_axis, measures_axis, depths_axis) = plt.subplots(3, 1, figsize=(9, 24))
            
            # Draw coupling map first
            grovers[0].and_draw_coupling_map(axis=coupling_axis, color_used_qubits=True)
            coupling_axis.set_title("Coupling Map")
            
            # Draw heatmap
            heatmap = measures_axis.imshow(np.array(counts_per_marked), cmap=mpl.colormaps["magma"], vmin=0, vmax=SHOTS)
            colorbar = measures_axis.figure.colorbar(heatmap, ax=measures_axis)
            colorbar.ax.set_ylabel("Amount Measured", rotation=-90, va="bottom")
            measures_axis.set_xticks(TICKS_RANGE, TICKS)
            measures_axis.set_yticks(TICKS_RANGE, TICKS)
            measures_axis.set_xlabel("Measured")
            measures_axis.set_ylabel("Marked")
            measures_axis.set_title(f"Results ({SHOTS} shots)")

            # Draw barplot of depths for each grover of marked element
            depths_axis.bar(TICKS, depths_per_marked)
            depths_axis.set_ylabel("Depth")
            depths_axis.set_xlabel("Marked")
            depths_axis.set_title("Depths per Marked Element")

            plt.suptitle(f"{name}")
            file_name=f"{name}_grover_results.pdf"
            path = os.path.join(directory, file_name)
            plt.savefig(path)
            print(f"Done! Results saved in {path}.")
        except Exception as e:
            print(f"Failed. Reason: {e}")