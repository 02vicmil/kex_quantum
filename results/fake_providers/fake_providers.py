# Following two lines are for importing the parent folder
import sys, os
sys.path.append(os.path.join(sys.path[0], '..'))

from qcircuit_runner import Runner
from grover import grovers_circuit
import qiskit_ibm_runtime.fake_provider as fp
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

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
mpl.rcParams["figure.titlesize"] = 24
mpl.rcParams["font.size"] = 14

with open("../../vicmil/couplings/provider_qubit_couplings.txt", "r") as f:
    for line in f:
        name = line.split(" ")[0]
        if not name[0].isalpha():
            continue

        print(f"Running on {name}...", end="")
        try:
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

            figure, (coupling_ax, measures_ax, depths_ax) = plt.subplots(3, 1, figsize=(9, 24))
            
            # Draw coupling map first
            grovers[0].and_draw_coupling_map(ax=coupling_ax, color_used_qubits=True)
            coupling_ax.set_title("Coupling Map")
            
            # Draw heatmap
            heatmap = measures_ax.imshow(np.array(counts_per_marked), cmap=mpl.colormaps["magma"], vmin=0, vmax=SHOTS)
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

            plt.suptitle(f"{name}")
            file_name=f"all/{name}_grover_results.pdf"
            plt.savefig(file_name)
            print(f"Done! Results saved in {file_name}.")
        except Exception as e:
            print(f"Failed. Reason: {e}")