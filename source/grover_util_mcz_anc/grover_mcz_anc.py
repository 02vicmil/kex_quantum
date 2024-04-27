from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister, ClassicalRegister
from math import pi, sqrt, floor
from .Uf_mcz_anc import Uf_mcz_oracle
from .Uf0_mcz_anc import Uf0_mcz_oracle

def grovers_circuit(marked: int, num_qubits: int, iteration_num: int = -1) -> QuantumCircuit:
    # Setup registers
    in_reg = QuantumRegister(num_qubits, "in")
    ancilla_reg = AncillaRegister(num_qubits-2, "ancilla")
    out_reg = QuantumRegister(1, "out")
    classical_reg = ClassicalRegister(num_qubits, "classic")

    circuit = QuantumCircuit(in_reg, ancilla_reg, out_reg, classical_reg)
    
    circuit.h(in_reg)

    # Flip to allow for Phase-flip from Z gates inside oracles
    circuit.x(out_reg)

    if iteration_num < 0:
        # Optimal iteration number is ≈ π√(N)/4, N = 2**num_qubits
        iteration_num = floor(sqrt(2**num_qubits)*pi/4.0)

    Uf_z = Uf_mcz_oracle(marked, num_qubits)
    Uf0_z = Uf0_mcz_oracle(num_qubits)

    for _ in range(iteration_num):
        # Apply Phase Oracle
        circuit.append(Uf_z, circuit.qubits)

        # Apply Diffusor/Mean Inversion
        circuit.h(in_reg)
        circuit.append(Uf0_z, circuit.qubits)
        circuit.h(in_reg)
    
    circuit.measure(in_reg, classical_reg)

    return circuit


if __name__ == "__main__":
    from .. import Runner
    import matplotlib.pyplot as plt
    
    NUM_QUBITS = 5
    MARKED_ELEMENT = 14 # 14 = 0b01110... So we should measure that a lot!
    qc = grovers_circuit(MARKED_ELEMENT, NUM_QUBITS, iteration_num=1)
    qc.draw("mpl")

    Runner(qc).run(draw_transpiled_circuit=True, plot_results=True)

    plt.show()