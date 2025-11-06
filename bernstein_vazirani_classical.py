
''' The input to this solver is a json schema:
      {'nbits': N,
       'f': [a list of integers, X, where 0 <= X < 2^N for which f(X) = true]}

    The goal is to find a binary string S of length N such that f(x) = S XOR x for
    all x in 0..2^N -1. There is a promise that there is such an S.
'''

def solve(data) -> dict:
    ''' returns the answer as a binary string '''
    nbits = data['nbits']
    top = pow(2, nbits)

    ftrue = set()
    for i in data['f']:
        ftrue.add(i)

    s = 0
    i = 1
    while i < top:
        if i in ftrue:
            s |= i
        i <<= 1

    result = f"{s:b}".zfill(nbits)
    return {'answer': result}

if __name__ == "__main__":
    assert solve({'nbits': 3, 'f': [1,3,4, 6]})['answer'] == '101'
    assert solve({'nbits': 3, 'f': [1, 2, 4, 7]})['answer'] == '111'
    assert solve({'nbits': 3, 'f': []})['answer'] == '000'
    assert solve({'nbits': 3, 'f': [1,3,5,7]})['answer'] == '001'
    print("All tests passed")
