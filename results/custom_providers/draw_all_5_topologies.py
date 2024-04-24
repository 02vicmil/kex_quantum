# Following two lines are for importing the parent folder
import sys, os
sys.path.append(os.path.join(sys.path[0], '..'))

from qcircuit_runner import Runner
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from qiskit import QuantumCircuit

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

qc = QuantumCircuit()

figure, axes = plt.subplots(7, 3, figsize=(7, 14))
figure.tight_layout(rect=[0, 0.01, 1, 0.99])

mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.size"] = 16

for idx, coupling in enumerate(graphs):
    ax = axes[idx//3][idx%3]
    Runner(qc)\
        .with_coupling_map(coupling, make_bidirectional=True)\
        .and_draw_coupling_map(True, ax)

    ax.set_title(f"{idx}")

plt.savefig("all_5_topologies.pdf")