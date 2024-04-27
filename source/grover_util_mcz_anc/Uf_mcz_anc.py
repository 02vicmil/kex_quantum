from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister

def Uf_mcz_oracle(marked: int, qubit_count: int, name = "Uf_mcz"):
    # Set up registers
    in_reg = QuantumRegister(qubit_count, "in")
    ancilla_reg = AncillaRegister(qubit_count-1, "ancilla")
    # Out = Ancilla[-1]

    oracle = QuantumCircuit(in_reg, ancilla_reg, name=name)

    marked_ = marked
    for qubit_index in range(0, qubit_count):
        if marked_ & 1 == 0:
            oracle.x(in_reg[qubit_index])
        marked_ >>= 1

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

    for qubit_index in range(0, qubit_count):
        if marked & 1 == 0:
            oracle.x(in_reg[qubit_index])
        marked >>= 1

    return oracle


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    NUM_QUBITS = 5
    qc = QuantumCircuit(QuantumRegister(NUM_QUBITS, "in"),
                        AncillaRegister(NUM_QUBITS-2, "ancilla"),
                        QuantumRegister(1, "out"))

    marked_element = 12 # = 0b01100. Must be less than 2**NUM_QUBITS
    oracle = Uf_mcz_oracle(marked_element, NUM_QUBITS)
    oracle.draw("mpl")

    qc.append(oracle, qc.qubits)
    qc.draw("mpl")

    plt.show()