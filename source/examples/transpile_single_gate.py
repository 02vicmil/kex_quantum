if __name__ != "__main__":
    exit(0)

from .. import Runner
from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
import qiskit_ibm_runtime.fake_provider as fp

circuit = QuantumCircuit(3)
circuit.ccx(0, 1, 2)

Runner(circuit)\
    .with_backend(fp.FakeBelem())\
    .and_transpile()\
    .and_draw_transpiled_circuit()

plt.show()