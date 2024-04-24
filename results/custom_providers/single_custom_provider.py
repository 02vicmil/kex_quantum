
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

noise_types = ["Noiseless", "Readout", "Bitflip", "Phaseflip", "Depolarizing"]
noise_sizes = [0.001, 0.01]

mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.size"] = 20

graph_idx = 0
if len(sys.argv) > 1:
    graph_idx = int(sys.argv[1])
coupling = graphs[graph_idx]

figure, axes = plt.subplots(3, 3, figsize=(15, 12), sharey=True, sharex=True)

figure.text(0.5, 0.04, "Measured", ha="center")
figure.text(0.04, 0.5, "Marked", va="center", rotation="vertical")
figure.subplots_adjust(bottom=0.15)

print("Running...")
plot_idx = 0
index_permutation = [0, 1, 2, 3, 6, 4, 7, 5, 8]
for noise in noise_types:
    for noise_idx, noise_size in enumerate(noise_sizes):
        if noise == noise_types[0] and noise_idx > 0:
            continue

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
            counts_for_i_as_array = [0 for _ in range(N)]
            for key_binary, value in counts_for_i.items():
                index = int(key_binary, 2)
                counts_for_i_as_array[index] = value
            counts_per_marked.append(counts_for_i_as_array)

        idx = index_permutation[plot_idx]
        ax = axes[idx//3][idx%3]
        heatmap = ax.imshow(np.array(counts_per_marked), cmap=mpl.colormaps["magma"], vmin = 0, vmax=SHOTS)
        ax.set_xticks(ticks_range, ticks, rotation=90)
        ax.set_yticks(ticks_range, ticks)
        title = f"{noise_size} {noise}"
        if noise == noise_types[0]:
            title = f"{noise}"
        ax.set_title(title)
        plot_idx += 1

# Draw heatmap
colorbar = figure.colorbar(heatmap, ax=axes.ravel().tolist())
colorbar.ax.set_ylabel("Amount Measured", rotation=-90, va="bottom")

file_name = f"graph_{graph_idx}_grover_results.pdf"

plt.savefig(file_name)
print(f"Done! Results saved in {file_name}.")
plt.close()