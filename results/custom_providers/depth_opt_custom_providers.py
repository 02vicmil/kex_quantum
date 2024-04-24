# Following two lines are for importing the parent folder
import sys, os
sys.path.append(os.path.join(sys.path[0], '..'))

from qcircuit_runner import Runner, Error
from grover import grovers_circuit
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

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
NOISE_PROBABILITY = 0.005

grovers = []

for i in range(0, N):
    grover = grovers_circuit(i, NUM_QUBITS, 1)
    grovers.append(grover)

ticks = [f"|{{0:0{NUM_QUBITS}b}}⟩".format(i) for i in range(0, N)]
ticks_range = np.arange(0, N)

average_depth_per_graph_per_opt: list[list[float]] = []
average_correct_ratio_per_graph_per_opt: list[list[float]] = []

for optimization_level in range(0, 4):
    print(f"OPT {optimization_level}")
    depth_at_opt_level = []
    ratio_at_opt_level = []

    for graph_idx, coupling in enumerate(graphs):
        print(f" GRAPH {graph_idx}. i = ", end="")
        all_depths = []
        all_ratios = []
        for i in range(0, N):
            print(f"{i} ", end="")
            # Compile grover for this marked element and for this coupling
            runner = Runner(grovers[i])\
                    .with_coupling_map(coupling, True)\
                    .with_optimization_level(optimization_level)\
                    .with_errors_on_gates([Error.depolarizing(NOISE_PROBABILITY)], ['sx', 'rz'])\
                    .with_errors_on_gates([Error.depolarizing(NOISE_PROBABILITY).tensor(Error.bitflip(NOISE_PROBABILITY))], ['cx'])\
                    .and_transpile()

            depth_for_i = runner.get_depth()

            counts = runner.run(plot_results=False)
            ratio_for_i = counts[f"{{0:0{NUM_QUBITS}b}}".format(i)]

            all_depths.append(depth_for_i)
            all_ratios.append(ratio_for_i)
        print()

        # Store average of all depths
        depth_at_opt_level.append(sum(all_depths)/len(all_depths))

        # Store average of all ratios
        ratio_at_opt_level.append(sum(all_ratios)/len(all_ratios)/SHOTS)

    average_depth_per_graph_per_opt.append(depth_at_opt_level)
    average_correct_ratio_per_graph_per_opt.append(ratio_at_opt_level)

mpl.rcParams["font.family"] = "serif"

depth_figure, depth_axis = plt.subplots(layout="constrained")
ratio_figure, ratio_axis = plt.subplots(layout="constrained")

x = np.arange(len(graphs))
width = 0.2
multiplier = 0
for opt, (result_depth, result_ratio) in enumerate(zip(average_depth_per_graph_per_opt, average_correct_ratio_per_graph_per_opt)):
    offset = width * multiplier
    depth_axis.bar(x + offset, result_depth, width, label=f"Opt. Level {opt}")
    ratio_axis.bar(x + offset, result_ratio, width, label=f"Opt. Level {opt}")
    multiplier += 1

depth_axis.set_xticks(x + 1.5*width, range(0, len(graphs)))
depth_axis.legend(loc="upper right")
depth_axis.set_xlabel("Graph Number")
depth_axis.set_ylabel("Depth")

ratio_axis.set_xticks(x + 1.5*width, range(0, len(graphs)))
ratio_axis.legend(loc="upper right")
ratio_axis.set_xlabel("Graph Number")
ratio_axis.set_ylabel("Correct Ratio")
ratio_axis.set_ylim(0, 1)

plt.savefig("avg_correctness_per_graph_per_opt.pdf")
plt.figure(depth_figure)
plt.savefig("avg_depth_per_graph_per_opt.pdf")