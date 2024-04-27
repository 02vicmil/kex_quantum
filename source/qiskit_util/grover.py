from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister, ClassicalRegister
from math import pi, sqrt, floor
from .Uf import Uf_oracle
from .Uf0 import Uf0_oracle

def grovers_circuit(marked: int, num_qubits: int, iteration_num: int = -1) -> QuantumCircuit:
    # Setup registers
    in_reg = QuantumRegister(num_qubits, "in")
    ancilla_reg = AncillaRegister(num_qubits-2, "ancilla")
    out_reg = QuantumRegister(1, "out")
    classical_reg = ClassicalRegister(num_qubits, "classic")

    # Set up circuit
    circuit = QuantumCircuit(in_reg, ancilla_reg, out_reg, classical_reg)
    
    # Put In qubits in uniform superposition state
    circuit.h(in_reg)

    # Put Out qubits as H|1>
    circuit.x(out_reg)
    circuit.h(out_reg)
    
    # If iteration number is negative then we use the optimal  
    if iteration_num < 0:
        # Optimal iteration number is ≈ π√(N)/4, N = 2**num_qubits
        iteration_num = floor(sqrt(2**num_qubits)*pi/4.0)

    # Get the oracles
    Uf = Uf_oracle(marked, num_qubits, name="Uf")
    Uf0 = Uf0_oracle(num_qubits, name="Uf0")

    for _ in range(iteration_num):
        # Apply Phase Oracle
        circuit.append(Uf, circuit.qubits)

        # Apply Diffusor/Mean Inversion
        circuit.h(in_reg)
        circuit.append(Uf0, circuit.qubits)
        circuit.h(in_reg)
    
    circuit.measure(in_reg, classical_reg)

    return circuit

if __name__ == "__main__":
    from .qcircuit_runner import Runner
    import matplotlib.pyplot as plt
    
    NUM_QUBITS = 5
    MARKED_ELEMENT = 14 # 14 = 0b01110... So we should measure that a lot!
    qc = grovers_circuit(MARKED_ELEMENT, NUM_QUBITS, iteration_num=1)
    qc.draw("mpl")

    Runner(qc).run(draw_transpiled_circuit=True, plot_results=True)

    plt.show()