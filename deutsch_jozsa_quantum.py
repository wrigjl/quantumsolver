'''
Deutsch-Jozsa problem quantum solver.
'''

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def dj_algorithm(function: QuantumCircuit):
    '''Determine if a function is constant or balanced.'''

    qc = compile_circuit(function)

    result = AerSimulator().run(qc, shots=1, memory=True).result()
    measurements = result.get_memory()
    if "1" in measurements[0]:
        return "balanced"
    return "constant"

def compile_circuit(function: QuantumCircuit):
    '''Compiles a circuit for use in the Deutsch-Jozsa algorithm.'''

    n = function.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    qc.compose(function, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

def dj_constant(num_qubits, output=True):
    '''Return a constant DJ function circuit.'''
    qc = QuantumCircuit(num_qubits + 1)
    if output:
        qc.x(num_qubits)
    return qc

def dj_balanced(num_qubits, values):
    '''Return a balanced DJ function circuit.'''
    qc = QuantumCircuit(num_qubits + 1)

    def add_cx(qc, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                qc.x(qubit)
        return qc

    for state in values:
        qc.barrier()
        qc = add_cx(qc, f"{state:0b}")
        qc.mcx(list(range(num_qubits)), num_qubits)
        qc = add_cx(qc, f"{state:0b}")

    qc.barrier()
    return qc

def solve(data) -> dict:
    ''' Solves the Deutsch-Jozsa problem for the given function data.
        The input data is a json schema:
        {'nbits': N,
         'values': [list of integers X where f(X) = true]}
    '''
    nbits = data['nbits']
    values = set(data['values'])

    if len(values) == 0:
        func = dj_constant(nbits, output=False)
    elif len(values) == 2**nbits:
        func = dj_constant(nbits, output=True)
    else:
        func = dj_balanced(nbits, values)

    answer = dj_algorithm(func)
    return {'answer': answer}

if __name__ == "__main__":
    assert solve({'nbits': 3, 'values': []})['answer'] == 'constant'
    assert solve({'nbits': 3, 'values': [0,1,2,3,4,5,6,7]})['answer'] == 'constant'
    assert solve({'nbits': 3, 'values': [1,3,4,6]})['answer'] == 'balanced'
    assert solve({'nbits': 3, 'values': [1,2,4,7]})['answer'] == 'balanced'
    print("All tests passed")
