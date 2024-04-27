if __name__ != "__main__":
    exit(0)

from .. import Runner, grovers_circuit
import matplotlib.pyplot as plt
import qiskit_ibm_runtime.fake_provider as fp

NUM_QUBITS = 4
MARKED = 10
circuit = grovers_circuit(MARKED, NUM_QUBITS, iteration_num=1)

depths = [0, 0, 0, 0]

depths[0] = Runner(circuit)\
                .with_optimisation_level(0)\
                .with_backend(fp.FakeBoeblingen())\
                .and_transpile()\
                .and_draw_transpiled_circuit()\
                .get_depth()
depths[1] = Runner(circuit)\
                .with_optimisation_level(1)\
                .with_backend(fp.FakeBoeblingen())\
                .and_transpile()\
                .and_draw_transpiled_circuit()\
                .get_depth()
depths[2] = Runner(circuit)\
                .with_optimisation_level(2)\
                .with_backend(fp.FakeBoeblingen())\
                .and_transpile()\
                .and_draw_transpiled_circuit()\
                .get_depth()
depths[3] = Runner(circuit)\
                .with_optimisation_level(3)\
                .with_backend(fp.FakeBoeblingen())\
                .and_transpile()\
                .and_draw_transpiled_circuit()\
                .get_depth()

print("Opt\t\tDepth")
for opt,d in enumerate(depths):
    print(f"{opt}\t\t{d}")

plt.show()