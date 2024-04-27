from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister

def Uf0_oracle(qubit_count: int, name = "Uf0"):
    # Set up registers
    in_reg = QuantumRegister(qubit_count, "in")
    ancilla_reg = AncillaRegister(qubit_count-1, "ancilla")
    # Out = Ancilla[-1]

    # Set up oracle circuit
    oracle = QuantumCircuit(in_reg, ancilla_reg, name=name)

    # Flip all input and output to utilise De Morgan's Laws later on
    oracle.x(in_reg) # (*)
    oracle.x(ancilla_reg[-1]) 

    # Ancilla[0] = !In[0] AND !In[1]
    oracle.ccx(in_reg[0], in_reg[1], ancilla_reg[0])

    # Ancilla[qubit_index-1] = !In[qubit_index] AND Ancilla[qubit_index-2] =
    # = !In[qubit_index] AND !In[qubit_index-1] AND ... AND !In[0]
    for qubit_index in range(2, qubit_count):
        oracle.ccx(in_reg[qubit_index], 
                   ancilla_reg[qubit_index-2], 
                   ancilla_reg[qubit_index-1])

    # Out[0] = 1 XOR (!in[0] AND !in[1] AND ... AND !in[qubit_count-1]) =
    #        = !(!In[0] AND ... And !In[qubit_count-1]) = {De Morgan's} =
    #        = In[0] OR In[1] OR ... OR In[qubit_count-1]

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
    oracle.x(in_reg)

    return oracle

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    NUM_QUBITS = 5
    qc = QuantumCircuit(QuantumRegister(NUM_QUBITS, "in"),
                        AncillaRegister(NUM_QUBITS-2, "ancilla"),
                        QuantumRegister(1, "out"))

    oracle = Uf0_oracle(NUM_QUBITS)
    oracle.draw("mpl")

    qc.append(oracle, qc.qubits)
    qc.draw("mpl")

    plt.show()