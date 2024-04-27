if __name__ != "__main__":
    exit(0)

from . import Runner, Error, grovers_circuit, get_directory_in_results, UNIQUE_5_COUPLINGS, NUM_QUBITS, NUM_STATES, SHOTS
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

directory = get_directory_in_results("custom_providers")
NOISE_PROBABILITY = 0.005
NUM_OPTIMISATION_LEVELS = 4

# Set up Grover's algorithm versions
grovers = []
for marked_element in range(0, NUM_STATES):
    grover = grovers_circuit(marked_element, NUM_QUBITS, 1)
    grovers.append(grover)

# Set up common matplotlib variables
mpl.rcParams["font.family"] = "serif"
TICKS = [f"|{{0:0{NUM_QUBITS}b}}⟩".format(i) for i in range(0, NUM_STATES)]
TICKS_RAGE = np.arange(0, NUM_STATES)
average_depth_per_graph_per_opt: list[list[float]] = []
average_correct_count_per_graph_per_opt: list[list[float]] = []

depth_figure, depth_axis = plt.subplots(layout="constrained")
count_figure, count_axis = plt.subplots(layout="constrained")

X_TICKS = np.arange(len(UNIQUE_5_COUPLINGS))
WDITH = 0.2

depth_axis.set_xticks(X_TICKS + 1.5*WDITH, range(0, len(UNIQUE_5_COUPLINGS)))
depth_axis.set_xlabel("Graph Number")
depth_axis.set_ylabel("Depth")

count_axis.set_xticks(X_TICKS + 1.5*WDITH, range(0, len(UNIQUE_5_COUPLINGS)))
count_axis.set_xlabel("Graph Number")
count_axis.set_ylabel("Number of Correctly Measured")
count_axis.set_ylim(0, SHOTS)

# Experiment starts here
for optimisation_level in range(0, NUM_OPTIMISATION_LEVELS):
    print(f"OPT {optimisation_level}")
    depths_at_optimisation_level = []
    counts_at_optimisation_level = []

    for graph_index, coupling in enumerate(UNIQUE_5_COUPLINGS):
        print(f" GRAPH {graph_index}. i = ", end="")
        all_depths = []
        all_counts = []
        for marked_element in range(0, NUM_STATES):
            print(f"{marked_element} ", end="")
            # Compile grover for this marked element and for this coupling
            runner = Runner(grovers[marked_element])\
                    .with_coupling_map(coupling, True)\
                    .with_optimisation_level(optimisation_level)\
                    .with_errors_on_gates([Error.depolarizing(NOISE_PROBABILITY)], ['sx', 'rz', 'x'])\
                    .with_errors_on_gates([Error.depolarizing(NOISE_PROBABILITY).tensor(Error.bitflip(NOISE_PROBABILITY))], ['cx'])\
                    .and_transpile()

            depth_for_marked_element = runner.get_depth()

            counts = runner.run()
            count_for_marked_element = counts[f"{{0:0{NUM_QUBITS}b}}".format(marked_element)]

            all_depths.append(depth_for_marked_element)
            all_counts.append(count_for_marked_element)
        print()

        # Store average of all depths
        depths_at_optimisation_level.append(sum(all_depths)/len(all_depths))

        # Store average of all counts
        counts_at_optimisation_level.append(sum(all_counts)/len(all_counts))

    average_depth_per_graph_per_opt.append(depths_at_optimisation_level)
    average_correct_count_per_graph_per_opt.append(counts_at_optimisation_level)

# Format and plot results
multiplier = 0
for optimisation_level, (result_depth, result_count) in enumerate(
        zip(average_depth_per_graph_per_opt, 
            average_correct_count_per_graph_per_opt)):

    offset = WDITH * multiplier
    depth_axis.bar(X_TICKS + offset, result_depth, WDITH, label=f"Opt. Level {optimisation_level}")
    count_axis.bar(X_TICKS + offset, result_count, WDITH, label=f"Opt. Level {optimisation_level}")
    multiplier += 1

depth_axis.legend(loc="upper right")
count_axis.legend(loc="upper right")

plt.savefig(os.path.join(directory, "avg_count_per_graph_per_opt.pdf"))
plt.figure(depth_figure)
plt.savefig(os.path.join(directory, "avg_depth_per_graph_per_opt.pdf"))