if __name__ != "__main__":
    exit(0)

from .. import grovers_circuit, Runner, Error
import matplotlib.pyplot as plt

NUM_QUBITS = 4
MARKED = 10
circuit = grovers_circuit(MARKED, NUM_QUBITS, 1)

Runner(circuit)\
    .with_errors_on_gates([Error.bitflip(0.01), Error.depolarizing(0.01)], ['sx'])\
    .with_errors_on_gates([Error.identity().tensor(Error.phaseflip(0.005))], ['cx'])\
    .with_readout_error(0.1, 0.05)\
    .run(draw_transpiled_circuit=True)

plt.show()