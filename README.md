# Finding minimal cut sets in fault trees

[![CI testing](https://github.com/sebastiaanbrand/ft-2-quantum-sat/actions/workflows/python-app.yml/badge.svg)](https://github.com/sebastiaanbrand/ft-2-quantum-sat/actions/workflows/python-app.yml)

This repository contains functions to compute minimal cut sets of fault trees by translating the problem to SAT. These SAT queries can either be solved with with (simulated) Grover, or with a classical SAT solver.


## Installation
We recommend running the code and installing any dependencies within a [virtual environment](https://docs.python.org/3/tutorial/venv.html).

The dependencies can be installed with:
```bash
$ pip install -r requirements.txt
```

If [pytest](https://docs.pytest.org/en/6.2.x/getting-started.html) is installed (in the virtual environment), tests can be run from the root of the repo by running:
```bash
$ pytest
```


## Example usage

```python
from ft_2_quantum_sat.fault_tree import FaultTree

# load a fault tree from XML
ft = FaultTree.load_from_xml("models/BSCU/BSCU.xml")

# (if it is not too big) the fault tree can be visualized with
ft.save_as_image('BSCU.png')

# to compute for example the 3 smallest cutsets
cutsets = ft.compute_min_cutsets(m=3, method='classical')
print("cutsets:", cutsets)
```
