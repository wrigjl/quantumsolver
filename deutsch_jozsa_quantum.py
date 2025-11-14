"""
Deutsch-Jozsa problem quantum solver.

In this problem the input is a function f:{0,1}^n -> {0,1} which is either
constant (all outputs are the same) or balanced (half the outputs are 0, half
are 1).

The input to this solver is a dictionary:
    {'nbits': N,
     'values': [a list of integers, X, where 0 <= X < 2^N for which f(X) = true]}

The result is a dictionary:
    {'answer': 'constant' or 'balanced'}
"""

import argparse
from qiskit import QuantumCircuit, qasm2
from qiskit_aer import AerSimulator


def dj_algorithm(function: QuantumCircuit):
    """Determine if a function is constant or balanced."""

    qc = compile_circuit(function)
    result = AerSimulator().run(qc, shots=1, memory=True).result()
    measurements = result.get_memory()
    return ("balanced", qc) if "1" in measurements[0] else ("constant", qc)


def compile_circuit(function: QuantumCircuit):
    """Compiles a circuit for use in the Deutsch-Jozsa algorithm."""

    n = function.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    qc.compose(function, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


def dj_constant(num_qubits, output=True):
    """Return a constant DJ function circuit."""

    qc = QuantumCircuit(num_qubits + 1)
    if output:
        qc.x(num_qubits)
    return qc


def dj_balanced(num_qubits, values):
    """Return a balanced DJ function circuit."""

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
    """Solves the Deutsch-Jozsa problem for the given function data.
    The input data is a json schema:
    {'nbits': N,
     'values': [list of integers X where f(X) = true]}
    """

    nbits = data["nbits"]
    values = set(data["values"])

    if len(values) == 0:
        func = dj_constant(nbits, output=False)
    elif len(values) == 2**nbits:
        func = dj_constant(nbits, output=True)
    else:
        func = dj_balanced(nbits, values)

    (answer, qc) = dj_algorithm(func)
    return {"answer": answer, "qasm": qasm2.dumps(qc)}


def testit(data, expected, show_circuits=False):
    """Test the deutsch-jozsa solver with given data and expected result."""
    result = solve(data)
    assert (
        result["answer"] == expected
    ), f"expected {expected}, got {result['answer']} for {data}"
    if show_circuits:
        print(f"Deutsch-Jozsa circuit for input {data}:")
        print(result["qasm"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-circuits", action="store_true")
    args = parser.parse_args()

    testit({"nbits": 3, "values": []}, "constant", args.show_circuits)
    testit(
        {"nbits": 3, "values": [0, 1, 2, 3, 4, 5, 6, 7]}, "constant", args.show_circuits
    )
    testit({"nbits": 3, "values": [1, 3, 4, 6]}, "balanced", args.show_circuits)
    testit({"nbits": 3, "values": [1, 2, 4, 7]}, "balanced", args.show_circuits)
    print("All tests passed")
