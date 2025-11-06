
'''Test the implementation of the solver for the Deutsch problem'''

import argparse
import requests

def tryit(url, data, expected) -> None:
    '''Try the Deutsch classical solver endpoint with the given data and
       check the expected result'''

    req = requests.post(url, json=data, timeout=5)
    assert req.json()['answer'] == expected

def main():
    '''Main program to test the Deutsch solver endpoint'''
    parser = argparse.ArgumentParser(description='Test the Deutsch classical solver endpoint.')
    parser.add_argument('--baseurl', type=str, default='http://127.0.0.1:5000',
                        help='base of the URL where the server is running')
    parser.add_argument('--endpoint', type=str, default='deutsch-classical',
                        help='endpoint for the Deutsch solver')
    args = parser.parse_args()

    url = f"{args.baseurl}/{args.endpoint}"
    tryit(url, [True, True], 'constant')
    tryit(url, [False, False], 'constant')
    tryit(url, [True, False], 'balanced')
    tryit(url, [False, True], 'balanced')

if __name__ == "__main__":
    main()
