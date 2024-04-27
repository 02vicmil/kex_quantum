if __name__ != "__main__":
    exit(0)

from . import Runner,  get_directory_in_results, UNIQUE_5_COUPLINGS
import matplotlib.pyplot as plt
import matplotlib as mpl
from qiskit import QuantumCircuit
import os

directory = get_directory_in_results("custom_providers")

# Empty circuit... just to draw the coupling
empty_circuit = QuantumCircuit()

# Set up common matplotlib values
figure, axes = plt.subplots(7, 3, figsize=(7, 14))
figure.tight_layout(rect=[0, 0.01, 1, 0.99])
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.size"] = 16

for index, coupling in enumerate(UNIQUE_5_COUPLINGS):
    axis = axes[index//3][index%3]
    Runner(empty_circuit)\
        .with_coupling_map(coupling, make_bidirectional=True)\
        .and_draw_coupling_map(draw_circular=True, axis=axis)

    axis.set_title(f"{index}")

plt.savefig(os.path.join(directory, "all_5_topologies.pdf"))