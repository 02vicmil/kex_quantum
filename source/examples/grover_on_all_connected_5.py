if __name__ != "__main__":
    exit(0)

from .. import grovers_circuit, Runner, UNIQUE_5_COUPLINGS
import matplotlib.pyplot as plt
plt.rcParams["figure.max_open_warning"] = len(UNIQUE_5_COUPLINGS) # supress warning from mpl

NUM_QUBITS = 3
MARKED = 10
TOTAL_QUBITS = 2*NUM_QUBITS - 1
circuit = grovers_circuit(MARKED, NUM_QUBITS, iteration_num=1)

runner = Runner(circuit)
print("Coupling\tDepth per optimisation level")
print("        \tOpt0\tOpt1\tOpt2\tOpt3")
print("--------\t----\t----\t----\t----")

for i,g in enumerate(UNIQUE_5_COUPLINGS):
    runner.with_coupling_map(g, make_bidirectional=True)\
          .and_draw_coupling_map(draw_circular=True)

    depth = [runner\
                .with_optimisation_level(i)\
                .and_transpile()\
                .get_depth() 
             for i in range(4)
            ]

    print(f"{i}\t",end="")
    for d in depth:
        print(f"\t{d}",end="")
    print()

plt.show()