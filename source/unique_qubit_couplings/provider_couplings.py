# Following two lines are for importing the parent folder
import sys, os
sys.path.append(os.path.join(sys.path[0], '..'))

# Example starts here:

import qiskit_ibm_runtime.fake_provider as fp
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit import QuantumCircuit, transpile
import inspect

circuit = QuantumCircuit(3)
circuit.h(0)
circuit.cx(0,1)
circuit.cx(0,2)
circuit.measure_all()
circuit.draw('mpl')

transpiled_circuit = transpile(circuit, fp.FakeAlgiers())
transpiled_circuit.draw('mpl')

def get_fake_provider_names():
    class_names = [cls_name for cls_name, cls_obj in inspect.getmembers(sys.modules['qiskit_ibm_runtime.fake_provider']) if inspect.isclass(cls_obj)]
    return class_names

def get_fake_providers_and_classes():
    classes = [(cls_name,cls_obj) for cls_name, cls_obj in inspect.getmembers(sys.modules['qiskit_ibm_runtime.fake_provider']) if inspect.isclass(cls_obj)]
    return classes

def get_provider_coupling(provider_class):
    try:
        gates_list = list()
        properties = provider_class().properties().to_dict()
        gates = (properties["gates"])
        for gate in gates:
            gates_list.append((gate["qubits"], gate["gate"]))

        return gates_list
    except Exception as e:
        pass

    try:
        test_dict = provider_class().__dict__
        coupling = test_dict["_coupling_map"]
        assert(coupling == None) # Ensure that the chosen provider has no coupling!
    except Exception as e:
        print("Possible coupling not found!")

    return list()

classes = get_fake_providers_and_classes()


provider_couplings = dict()

for class_ in classes:
    name_ = class_[0]

    if(name_ in ["FakeProviderFactory", "FakeProvider", "FakeProviderForBackendV2"]):
        # Non fake-provider classes!
        continue

    provider_ = class_[1]
    #print(name_)
    provider_coupling = get_provider_coupling(provider_)
    if(len(provider_coupling) > 0):
        provider_couplings[name_] = provider_coupling

for key in provider_couplings.keys():
    multi_qubit_couplings = []
    for coupling_ in provider_couplings[key]:
        if(len(coupling_[0]) > 1):
            multi_qubit_couplings.append(coupling_[0])

    print(key, multi_qubit_couplings)

print("providers with couplings count: ", len(provider_couplings))
    




