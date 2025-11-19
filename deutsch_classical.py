"""This is a classical solver for the Deutsch problem"""

import argparse
import requests


def solve(data: list) -> dict:
    """We expect the incoming json schema to be a list of length two.
    Each entry is either 0 or 1. The first number represents
    f(0), and the second represents f(1)
    """

    # convert input data to booleans
    data = [bool(x) for x in data]

    def f(x: bool) -> bool:
        """This is the hidden function f we are trying to analyze"""
        return data[1] if x else data[0]

    # f has been defined. Now we treat it as a black box.
    # Past this point, we pretend that we don't know which function
    # it is and we try to determine if it is constant or balanced.

    result = "constant" if f(False) == f(True) else "balanced"
    return {"answer": result}


def tryit(url, data, expected):
    """Helper function to test the solver."""

    if url is None:
        solution = solve(data)
    else:
        req = requests.post(url, json=data, timeout=5)
        solution = req.json()

    answer = solution["answer"]
    assert (
        answer == expected
    ), f"Failed for data={data}, expected={expected}, got {answer}"


def main():
    """Main function to run the tests locally or on a server."""
    parser = argparse.ArgumentParser(description="Deutsch Classical Solver")
    parser.add_argument(
        "--baseurl",
        type=str,
        default=None,
        help="Base URL for the quantum solver to test against.",
    )
    parser.add_argument(
        "--endpoint",
        type=str,
        default="deutsch-classical",
        help="Endpoint for the classical solver.",
    )

    args = parser.parse_args()
    url = None
    if parser.parse_args().baseurl is not None:
        url = f"{args.baseurl}/{args.endpoint}"

    tryit(url, [0, 0], "constant")
    tryit(url, [0, 1], "balanced")
    tryit(url, [1, 0], "balanced")
    tryit(url, [1, 1], "constant")

    if url is None:
        url = "local"
    print(f"All tests passed ({url})")


if __name__ == "__main__":
    main()
