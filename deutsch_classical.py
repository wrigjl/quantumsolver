"""This is a classical solver for the Deutsch problem"""


def f1(x: bool) -> bool:
    return True

def f2(x: bool) -> bool:
    return False

def f3(x: bool) -> bool:
    return x

def f4(x: bool) -> bool:
    return not x

def solve(data) -> dict:
    """We expect the incoming json schema to be a list of length two.
    Each entry is either true or false. The first number represents
    f(false), and the second represents f(true)
    """
    if data[0] and data[1]:
        f = f1
    elif not data[0] and not data[1]:
        f = f2
    elif not data[0] and data[1]:
        f = f3
    else:
        f = f4

    # f has been defined. Now we treat it as a black box.
    # Past this point, we pretend that we don't know which function
    # it is and we try to determine if it is constant or balanced.

    result = "constant" if f(False) == f(True) else "balanced"
    return {"answer": result}


if __name__ == "__main__":
    assert solve([True, True])["answer"] == "constant"
    assert solve([False, False])["answer"] == "constant"
    assert solve([True, False])["answer"] == "balanced"
    assert solve([False, True])["answer"] == "balanced"
    print("All tests passed")
