from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister

def Uf_oracle(marked: int, qubit_count: int, name = "Uf"):
    # Set up registers
    in_reg = QuantumRegister(qubit_count, "in")
    ancilla_reg = AncillaRegister(qubit_count-1, "ancilla")
    # Out = Ancilla[-1]

    # Set up oracle circuit
    oracle = QuantumCircuit(in_reg, ancilla_reg, name=name)

    # Invert those bits which we want to be 1. For example if marked is 5 = 0b0101
    # then we add X-gates that invert the zero-bits in 0b0101 so we get all 1's 
    # when 5 is inputted (We will undo this operation in the end to not ruin the 
    # input qubits after the oracle. Look at (*) below)
    marked_ = marked
    for qubit_index in range(0, qubit_count):
        if marked_ & 1 == 0:
            oracle.x(in_reg[qubit_index])
        marked_ >>= 1


    # For clarity and simplicity assume that the In qubits are flipped 
    # according to the explanation of the X-gates above

    # Ancilla[0] = In[0] AND In[1]
    oracle.ccx(in_reg[0], in_reg[1], ancilla_reg[0])

    # Ancilla[qubit_index-1] = In[qubit_index] AND Ancilla[qubit_index-2] =
    # = In[qubit_index] AND In[qubit_index-1] AND ... AND In[0]
    for qubit_index in range(2, qubit_count):
        oracle.ccx(in_reg[qubit_index], 
                   ancilla_reg[qubit_index-2], 
                   ancilla_reg[qubit_index-1])

    # Out[0] = In[0] AND In[1] AND ... AND In[qubit_count-1]

    # Resetting Ancillas to be useable for the next gate
    # Ancilla[qubit_index] = Ancilla[qubit_index] XOR Ancilla[qubit_index] =
    # = 0
    for qubit_index in range(qubit_count-2, 1, -1):
        oracle.ccx(in_reg[qubit_index], 
                   ancilla_reg[qubit_index-2], 
                   ancilla_reg[qubit_index-1])
    if qubit_count > 2:
        # When qubit_count = 2 then Ancilla[0] = Ancilla[-1] = Out
        # So we only reset when qubit_count > 2
        oracle.ccx(in_reg[0], in_reg[1], ancilla_reg[0])

    # Unflip input that was done in (*)
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
    oracle = Uf_oracle(marked_element, NUM_QUBITS)
    oracle.draw("mpl")

    qc.append(oracle, qc.qubits)
    qc.draw("mpl")

    plt.show()