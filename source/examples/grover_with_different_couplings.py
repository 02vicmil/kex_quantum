if __name__ != "__main__":
    exit(0)

from .. import grovers_circuit, Runner
from qiskit.transpiler.coupling import CouplingMap
import matplotlib.pyplot as plt

NUM_QUBITS = 3
MARKED = 10
TOTAL_QUBITS = 2*NUM_QUBITS - 1
circuit = grovers_circuit(MARKED, NUM_QUBITS, iteration_num=1)

depth_star = Runner(circuit)\
    .with_coupling_map([[0, i] for i in range(1, TOTAL_QUBITS)])\
    .and_transpile()\
    .and_draw_coupling_map()\
    .and_draw_transpiled_circuit()\
    .get_depth()

depth_full = Runner(circuit)\
    .with_coupling_map(CouplingMap.from_full(TOTAL_QUBITS))\
    .and_transpile()\
    .and_draw_coupling_map()\
    .and_draw_transpiled_circuit()\
    .get_depth()

depth_hex = Runner(circuit)\
    .with_coupling_map(CouplingMap.from_hexagonal_lattice(2, 2))\
    .and_transpile()\
    .and_draw_coupling_map()\
    .and_draw_transpiled_circuit()\
    .get_depth()

depth_grid = Runner(circuit)\
    .with_coupling_map(CouplingMap.from_grid(3, 2))\
    .and_transpile()\
    .and_draw_coupling_map()\
    .and_draw_transpiled_circuit()\
    .get_depth()

print("Coupling\tDepth")
print("--------\t-----")
print(f"Star\t\t{depth_star}")
print(f"Full\t\t{depth_full}")
print(f"Hex\t\t{depth_hex}")
print(f"Grid\t\t{depth_grid}")

plt.show()