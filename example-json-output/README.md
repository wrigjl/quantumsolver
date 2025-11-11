This is proposed output from our server for a couple of quantum
solvers. The idea is we will provide the "solution"/"circuit"
to the visualization team as a string. It's a QASM 2.0
representation of the circuit used to solve the problem.

You can use the json in this directory like so:

```python
import json

with open("example-deutsch.json") as f:
    obj = json.load(f)

print(obj["solution"]["circuit"])
```
