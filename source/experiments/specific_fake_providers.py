if __name__ != "__main__":
    exit(0)

from . import Runner, grovers_circuit, get_directory_in_results, NUM_QUBITS, NUM_STATES, SHOTS
from .grid_positions import positions
import qiskit_ibm_runtime.fake_provider as fp
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

directory = get_directory_in_results("fake_providers/specific")

# Set up Grover's algorithm versions
grovers : list[Runner] = []
for marked_element in range(0, NUM_STATES):
    grover = grovers_circuit(marked_element, NUM_QUBITS, 1)
    grovers.append(Runner(grover).with_shots(SHOTS))

# Set up common matplotlib values
TICKS = [f"|{{0:0{NUM_QUBITS}b}}⟩".format(i) for i in range(0, NUM_STATES)]
TICKS_RANGE = np.arange(0, NUM_STATES)
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.size"] = 16
measures_figure, measures_ax = plt.subplots(3, 2, figsize=(12, 12), sharey=True, sharex=True)
measures_figure.text(0.5, 0.04, "Measured", ha="center")
measures_figure.text(0.06, 0.5, "Marked", va="center", rotation="vertical")
measures_figure.subplots_adjust(bottom=0.15)

for index, (name, data) in enumerate(sorted(positions.items(), key=lambda kv_pair: kv_pair[0])):
    backend = eval(f"fp.{name}()")

    # Run on grover once for each marked element and store the resulting counts
    counts_per_marked = []
    for marked_element in range(0, NUM_STATES):
        counts_for_marked_element = grovers[marked_element].with_backend(backend).run(plot_results=False)
        counts_for_marked_element_as_array = [0 for _ in range(NUM_STATES)]
        for key_binary, value in counts_for_marked_element.items():
            binary_index = int(key_binary, 2)
            counts_for_marked_element_as_array[binary_index] = value

        values = np.array(counts_for_marked_element_as_array)
        percentage = 100*values / SHOTS
        percentage_int = 100*values // SHOTS
        remainders_with_indices = [(percentage[i] - percentage_int[i], i) for i in range(len(percentage))]
        remainders_with_indices.sort(key=lambda x: x[0], reverse=True)
        aux = 100-sum(percentage_int)
        for i in range(aux):
            idx = remainders_with_indices[i][1]
            percentage_int[idx] += 1

        counts_per_marked.append(percentage_int)

    coupling_figure, coupling_ax = plt.subplots(figsize=data["ratio"], layout="constrained")

    # Draw coupling map first
    grovers[0].and_transpile().and_draw_coupling_map(axis=coupling_ax, color_used_qubits=True, grid_positions=data["positions"])

    axis = measures_ax[index//2][index%2]

    # Draw heatmap
    heatmap = axis.imshow(counts_per_marked, cmap=mpl.colormaps["magma"], vmin=0, vmax=100)
    axis.set_xticks(TICKS_RANGE, TICKS, rotation=90)
    axis.set_yticks(TICKS_RANGE, TICKS)
    axis.set_title(f"{name}")

    for (j,i),label in np.ndenumerate(counts_per_marked):
        color = "black"
        if label < 50:
            color = "white"

        if i == j:
            axis.text(i, j, label, ha='center', va='center', color=color, fontsize=16, weight="bold")


    plt.figure(coupling_figure)
    path = os.path.join(directory, f"{name}_coupling.pdf")
    plt.savefig(path)
    print(f"Done with {name}")

colorbar = measures_figure.colorbar(heatmap, ax=measures_ax.ravel().tolist())
colorbar.ax.set_ylabel("Correctly Measured (%)", rotation=-90, va="bottom")

plt.figure(measures_figure)
path = os.path.join(directory, f"fake_providers_results.pdf")
plt.savefig(path)