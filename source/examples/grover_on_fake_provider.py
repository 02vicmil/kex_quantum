if __name__ != "__main__":
    exit(0)

from .. import Runner, grovers_circuit
import matplotlib.pyplot as plt
import qiskit_ibm_runtime.fake_provider as fp

NUM_QUBITS = 4
MARKED = 10
circuit = grovers_circuit(MARKED, NUM_QUBITS, iteration_num=1)

Runner(circuit)\
    .with_backend(fp.FakeBoeblingen())\
    .run(draw_transpiled_circuit=True)

plt.show()