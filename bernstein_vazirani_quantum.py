"""The input to this solver is a json schema:
{'nbits': N,
 'f': [a list of integers, X, where 0 <= X < 2^N for which f(X) = true]}

 This uses a quantum algorithm to find a binary string S of length N such that
  f(x) = S XOR x for all x in 0..2^N

 There is a promise that there is such an S.

 This code can also generate all possible problem instances for a given N
 (in other words, it generates a description of the function f for all possible S).
"""

import argparse
import json
import requests
from qiskit import QuantumCircuit, qasm2
from qiskit_aer import AerSimulator
import deutsch_jozsa_quantum


def bv_query(s):
    """Create a quantum circuit implementing a query gate for the
    Bernstein-Vazirani problem."""

    qc = QuantumCircuit(len(s) + 1)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, len(s))
    return qc


def bv_algorithm(function: QuantumCircuit):
    """Runs the Bernstein-Vazirani algorithm using the given function"""
    qc = deutsch_jozsa_quantum.compile_circuit(function)
    result = AerSimulator().run(qc, shots=1, memory=True).result()
    return (result.get_memory()[0], qc)


def solve(data) -> dict:
    """returns the answer as a binary string"""
    nbits = data["nbits"]
    ftrue = set(data["f"])

    def f(x: int) -> bool:
        return x in ftrue

    bit_string = ["1" if f(1 << i) else "0" for i in range(nbits)]
    bit_string = "".join(reversed(bit_string))

    answer, circuit = bv_algorithm(bv_query(bit_string))
    return {"answer": answer, "qasm": qasm2.dumps(circuit)}


def generate(nbits, s):
    """Generates a Bernstein-Vazirani problem instance with hidden string 's'."""
    assert len(s) == nbits
    ftrue = set()

    si = int(s, 2)
    for i in range(2**nbits):
        if ((si & i).bit_count() % 2) == 1:
            ftrue.add(i)

    return (nbits, s, ftrue)


def generate_all(nbits):
    """Yields all possible problem instances for nbits."""
    for i in range(2**nbits):
        s = f"{i:b}".zfill(nbits)
        yield generate(nbits, s)


def tryit(url, nbits, ftrue, expected_s, show_circuits=False):
    """Helper function to test the solver."""

    data = {"nbits": nbits, "f": list(ftrue)}
    if url is None:
        solution = solve({"nbits": nbits, "f": list(ftrue)})
    else:

        req = requests.post(url, json=data, timeout=5)
        solution = req.json()

    answer = solution["answer"]
    assert answer == expected_s, \
        f"Failed for nbits={nbits}, ftrue={ftrue}, expected_s={expected_s}, got {answer}"
    if show_circuits:
        print(f"// Bernstein-Vazirani circuit for nbits={nbits}, s={expected_s}:")
        print(solution["qasm"])

def main():
    """Main function to either run tests or generate problem instances."""

    parser = argparse.ArgumentParser(
        description="Run the Bernstein-Vazirani quantum algorithm."
    )
    parser.add_argument(
        "--generate",
        type=int,
        required=False,
        default=None,
        help="The size of the problem to generate.",
    )
    parser.add_argument(
        "--show-circuits",
        action="store_true",
        help="Show the generated quantum circuits during tests.",
    )
    parser.add_argument(
        "--baseurl",
        type=str,
        default=None,
        help="Base URL for the quantum solver server.",
    )
    parser.add_argument(
        "--endpoint",
        type=str,
        default="bernstein-vazirani-quantum",
        help="Endpoint for the quantum solver.",
    )
    args = parser.parse_args()

    # if we're not generating a problem, run tests
    fullurl = None
    if args.baseurl is not None:
        fullurl = f"{args.baseurl}/{args.endpoint}"

    if args.generate is None:
        tryit(fullurl, 3, [1, 3, 4, 6], "101", args.show_circuits)
        tryit(fullurl, 3, [1, 2, 4, 7], "111", args.show_circuits)
        tryit(fullurl, 3, [],  "000", args.show_circuits)
        tryit(fullurl, 3, [1, 3, 5, 7], "001", args.show_circuits)
        print("All tests passed")
        return

    for nbits, s, ftrue in generate_all(args.generate):
        a = {"nbits": nbits, "f": list(ftrue), "s": s}
        print(json.dumps(a))


if __name__ == "__main__":
    main()
