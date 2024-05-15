from qiskit.circuit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.providers.backend import Backend
from qiskit import transpile
from qiskit.result.counts import Counts
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, QuantumError, pauli_error, depolarizing_error, kraus_error, ReadoutError
from qiskit.visualization import plot_histogram
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.transpiler.coupling import CouplingMap
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Error:
    @staticmethod
    def identity() -> QuantumError:
        return pauli_error([('I', 1.)])

    @staticmethod
    def bitflip(p_error: float) -> QuantumError:
        return Error.__get_pauli_error(p_error, 'X')

    @staticmethod
    def phaseflip(p_error: float) -> QuantumError:
        return Error.__get_pauli_error(p_error, 'Z')

    @staticmethod
    def bitphaseflip(p_error: float) -> QuantumError:
        return Error.__get_pauli_error(p_error, 'Y')

    @staticmethod
    def depolarizing(p_error: float) -> QuantumError:
        return depolarizing_error(p_error, 1)

    @staticmethod
    def kraus(matrices: list[np.ndarray]) -> QuantumError:
        return kraus_error(matrices)

    @staticmethod
    def __get_pauli_error(p_error: float, gate: str) -> QuantumError:
        error = [(gate, p_error), ('I', 1.0-p_error)]
        return pauli_error(error)


class Runner:
    def __init__(self, circuit: QuantumCircuit) -> 'Runner':
        self.circuit = circuit
        self.num_qubits = circuit.num_qubits
        self.shots = 1000
        self.basis = ['id', 'rz', 'sx', 'cx']
        self.noise_model = NoiseModel()
        self.backend = GenericBackendV2(self.num_qubits, basis_gates=self.basis)
        self.coupling_map = self.backend.coupling_map
        self.optimisation_level = 3
        self.transpiled_circuit = None

    def with_shots(self, shots: int) -> 'Runner':
        self.shots = shots
        return self
    
    def with_optimisation_level(self, level: int) -> 'Runner':
        self.optimisation_level = level
        self.transpiled_circuit = None
        return self

    def with_basis_gates(self, basis: list[str]) -> 'Runner':
        self.basis = basis
        self.backend = GenericBackendV2(self.num_qubits,
                                        basis_gates=self.basis,
                                        coupling_map=self.coupling_map)
        self.transpiled_circuit = None
        return self

    def with_coupling_map(self, mapping: list[list[int]] | CouplingMap, make_bidirectional: bool = False) -> 'Runner':
        resulting_mapping = []
        if make_bidirectional:
            for v, w in mapping:
                resulting_mapping.append((v, w))
                resulting_mapping.append((w, v))
        else:
            resulting_mapping = mapping
            
        self.coupling_map = CouplingMap(resulting_mapping)
        self.num_qubits = max(self.num_qubits, len(self.coupling_map.graph.nodes()))
        self.backend = GenericBackendV2(self.num_qubits,
                                        basis_gates=self.basis,
                                        coupling_map=self.coupling_map)
        self.transpiled_circuit = None
        return self
    
    def with_backend(self, backend: Backend) -> 'Runner':
        self.backend = backend
        try:
            self.coupling_map = backend.coupling_map
            self.num_qubits = backend.num_qubits
        except:
            self.coupling_map = backend.configuration().coupling_map
            self.num_qubits = backend.configuration().num_qubits

        self.transpiled_circuit = None
        return self

    def with_errors_on_gates(self, errors: list[QuantumError], gates: list[str], qubits: list[int] = None) -> 'Runner':
        # Given errors [E1, E2, ..., En], gates [G1, G2, ... Gk], and qubits [Q1, Q2, ..., Qm]
        # Add composition En En-1...E2 E1 to the given gates on given qubits. If qubits is None then all qubits are chosen

        if not errors or not gates or (qubits is not None and not qubits):
            return self

        # Assert: errors and gates are not empty. qubits is either None or not empty

        add_error = self.noise_model.add_all_qubit_quantum_error
        if qubits: # is not None
            add_error = lambda _error, _gates : self.noise_model.add_quantum_error(_error, _gates, qubits)
        
        total_error = errors.pop(0)
        for error in errors:
            total_error = total_error.compose(error)
        
        add_error(total_error, gates)

        self.transpiled_circuit = None

        return self

    def with_readout_error(self, p1given0: float, p0given1: float , qubits: list[int] = None) -> 'Runner':
        error = ReadoutError([[1 - p1given0, p1given0],
                              [p0given1, 1 - p0given1]])

        if qubits:
            self.noise_model.add_readout_error(error, qubits)
        else:
            self.noise_model.add_all_qubit_readout_error(error)

        return self

    def and_transpile(self) -> 'Runner':
        self.transpiled_circuit = transpile(self.circuit, self.backend, optimization_level=self.optimisation_level)

        return self

    def and_draw_transpiled_circuit(self) -> 'Runner':
        '''
        Requires the circuit to be transpiled with `and_transpile()`
        '''
        self.transpiled_circuit.draw("mpl")
        return self
    
    def and_draw_coupling_map(self, draw_circular: bool = False, axis=None, color_used_qubits: bool = False, grid_positions: list[list[int]] = None) -> 'Runner':     
        graph = nx.DiGraph()
        graph.add_nodes_from(range(0, self.num_qubits))
        graph.add_edges_from(list(self.coupling_map))
        labels = {n : str(n) for n in graph.nodes}
        highlight = []

        if color_used_qubits:
            dag = circuit_to_dag(self.transpiled_circuit)
            for i, q in enumerate(dag.qubits):
                if not q in dag.idle_wires():
                    highlight.append(i)

        highlight_labels = {n : str(n) for n in highlight}

        if not axis:
            plt.figure()
            
        if grid_positions is not None:
            x = -1
            y = 1
            width = 1/max(map(lambda l: len(l), grid_positions))
            height = 1/len(grid_positions)
            pos = {}
            for row in grid_positions: 
                for col in row:
                    if col >= 0:
                        pos[col] = np.array([x, y])
                    x += width
                x = -1
                y -= height
        elif nx.is_planar(graph) and not draw_circular:
            pos = nx.spring_layout(graph)
        else:
            pos = nx.circular_layout(graph)
        nx.draw(graph, pos, labels=labels, 
                arrowsize=5, node_color="cyan", 
                font_color="black", font_weight="bold",
                ax=axis)
        nx.draw(graph.subgraph(highlight), pos, labels=highlight_labels, 
                arrowsize=5, node_color="purple", 
                font_color = "white", font_weight="bold",
                ax=axis)
        return self

    def get_depth(self) -> int:
        '''
        Requires the circuit to be transpiled with `and_transpile()`
        '''
        return self.transpiled_circuit.depth()

    def reset_noise(self):
        self.noise_model = NoiseModel()

    def run(self, draw_transpiled_circuit: bool = False, plot_results: bool = False) -> Counts:
        backend = self.backend
        if isinstance(backend, GenericBackendV2):
            backend = AerSimulator.from_backend(backend, noise_model = self.noise_model)
        
        transpiled_circuit = transpile(self.circuit, backend, optimization_level=self.optimisation_level)

        if draw_transpiled_circuit:
            transpiled_circuit.draw("mpl")

        results = backend.run(transpiled_circuit, shots=self.shots).result()
        counts = results.get_counts()
        
        if plot_results:
            plot_histogram(counts)

        return counts
