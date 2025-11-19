"""The input to this solver is a json schema:
  {'nbits': N,
   'f': [a list of bits 0 or 1 where f[x] represents f(x)]}

note: len(f) == 2^nbits

The goal is to find a binary string S of length N such that f(x) = S XOR x for
all x in 0..2^N -1. There is a promise that there is such an S.
"""


def solve(data) -> dict:
    """returns the answer as a binary string"""
    nbits = data["nbits"]
    fbits = [bool(x) for x in data["f"]]

    def f(x: int) -> bool:
        if x >= len(fbits) or x < 0:
            return False
        return fbits[x]

    # f has been defined, now we treat it as a black box.
    # Past this point, we pretend that we don't know anything
    # about f and we try to determine S.

    s = 0
    for i in (1 << p for p in range(nbits)):
        if f(i):
            s |= i

    result = f"{s:b}".zfill(nbits)
    return {"answer": result}


if __name__ == "__main__":
    assert solve({"nbits": 3, "f": [0, 1, 0, 1, 1, 0, 1, 0]})["answer"] == "101"
    assert solve({"nbits": 3, "f": [0, 1, 1, 0, 1, 0, 0, 1]})["answer"] == "111"
    assert solve({"nbits": 3, "f": [1, 0, 0, 1, 0, 1, 1, 0]})["answer"] == "000"
    assert solve({"nbits": 3, "f": [0, 1, 0, 1, 0, 1, 0, 1]})["answer"] == "001"
    print("All tests passed")
