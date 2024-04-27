if __name__ != "__main__":
    exit(0)

from .. import grovers_circuit, Runner, Error
import matplotlib.pyplot as plt

NUM_QUBITS = 4
MARKED = 10
circuit = grovers_circuit(MARKED, NUM_QUBITS, 1)
basis_gates = ['id', 'u1', 'u2', 'u3', 'cx']

Runner(circuit)\
    .with_basis_gates(basis_gates)\
    .with_errors_on_gates([Error.bitflip(0.01), Error.depolarizing(0.01)], ['u1'])\
    .with_errors_on_gates([Error.identity().tensor(Error.phaseflip(0.005))], ['cx'])\
    .run(draw_transpiled_circuit=True)

plt.show()