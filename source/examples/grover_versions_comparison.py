if __name__ != "__main__":
    exit(0)

from .. import Runner, grovers_circuit as grover_tof
from ..misc.grover_matrix_version import grovers_circuit as grover_mtx
from ..grover_util_mcz import grover_circuit_mcz as grover_mcz
from ..grover_util_mcz_anc import grover_circuit_mcz_anc as grover_mcz_anc
import matplotlib.pyplot as plt
import qiskit_ibm_runtime.fake_provider as fp

NUM_QUBITS = 7
MARKED = 2**NUM_QUBITS - 1
circuit_tof = grover_tof(MARKED, NUM_QUBITS, iteration_num=1)
circuit_mtx = grover_mtx(MARKED, NUM_QUBITS, iteration_num=1)
circuit_mcz_anc = grover_mcz_anc(MARKED, NUM_QUBITS, iteration_num=1)
circuit_mcz = grover_mcz(MARKED, NUM_QUBITS, iteration_num=1)

print("Transpiling Toffoloi Version...")
depth_tof = Runner(circuit_tof)\
            .with_backend(fp.FakeBoeblingen())\
            .and_transpile()\
            .get_depth()
print("Done!")

print("Transpiling Matrix Version...")
depth_mtx = Runner(circuit_mtx)\
            .with_backend(fp.FakeBoeblingen())\
            .and_transpile()\
            .get_depth()
print("Done!")

print("Transpiling Multi-CZ Version...")
depth_mcz_anc = Runner(circuit_mcz_anc)\
            .with_backend(fp.FakeBoeblingen())\
            .and_transpile()\
            .get_depth()
print("Done!")

print("Transpiling Multi-CZ-anc Version...")
depth_mcz = Runner(circuit_mcz)\
            .with_backend(fp.FakeBoeblingen())\
            .and_transpile()\
            .get_depth()
print("Done!")

print(f"Toffoli      Version: {depth_tof}")
print(f"Matrix       Version: {depth_mtx}")
print(f"Multi-CZ     Version: {depth_mcz}")
print(f"Multi-CZ-anc Version: {depth_mcz_anc}")

plt.show()