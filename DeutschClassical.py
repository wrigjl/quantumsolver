
'''This is a classical solver for the Deutsch problem'''

def solve(data) -> dict:
    ''' We expect the incoming json schema to be a list of length two.
        Each entry is either true or false. The first number represents
        f(false), and the second represents f(true)
    '''
    result = "constant" if data[0] == data[1] else "balanced"
    return {'answer': result}