from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister

def Uf0_mcz_oracle(qubit_count: int, name = "Uf0_mcz"):
    # Set up registers
    in_reg = QuantumRegister(qubit_count, "in")
    ancilla_reg = AncillaRegister(qubit_count-1, "ancilla")
    # Out = Ancilla[-1]

    oracle = QuantumCircuit(in_reg, ancilla_reg, name=name)

    oracle.x(in_reg) # (*)
    oracle.z(ancilla_reg[-1]) 

    if qubit_count > 2:
        oracle.ccx(in_reg[0], in_reg[1], ancilla_reg[0])
    elif qubit_count == 2:
        oracle.ccz(in_reg[0], in_reg[1], ancilla_reg[0])

    for qubit_index in range(2, qubit_count-1):
        oracle.ccx(in_reg[qubit_index], 
                   ancilla_reg[qubit_index-2], 
                   ancilla_reg[qubit_index-1])

    if qubit_count > 2:
        oracle.ccz(in_reg[-1], 
                   ancilla_reg[-2], 
                   ancilla_reg[-1])

    for qubit_index in range(qubit_count-2, 1, -1):
        oracle.ccx(in_reg[qubit_index], 
                   ancilla_reg[qubit_index-2], 
                   ancilla_reg[qubit_index-1])
    
    if qubit_count > 2:
        oracle.ccx(in_reg[0], in_reg[1], ancilla_reg[0])

    oracle.x(in_reg)

    return oracle

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    NUM_QUBITS = 5
    qc = QuantumCircuit(QuantumRegister(NUM_QUBITS, "in"),
                        AncillaRegister(NUM_QUBITS-2, "ancilla"),
                        QuantumRegister(1, "out"))

    oracle = Uf0_mcz_oracle(NUM_QUBITS)
    oracle.draw("mpl")

    qc.append(oracle, qc.qubits)
    qc.draw("mpl")

    plt.show()