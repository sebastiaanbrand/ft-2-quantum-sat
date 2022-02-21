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

To visualize the fault trees, [Graphviz](https://graphviz.org/) is used. This is _only_ required to visualize the fault trees, it is not necessary to install Graphviz to just compute the cut sets. Graphviz can be installed with:
```bash
$ sudo apt-get install graphviz
```


## Example usage

The complete documentation can be found [here](https://neasqc.github.io/ft-2-quantum-sat/). Below an example showing the main usage is given.

The `example.py` file loads a number of fault trees from XML files in the Open-PSA Model Exchange Format and computes minimal cut sets. An example script is given below.

```python
from ft_2_quantum_sat.fault_tree import FaultTree

# load a fault tree from XML
ft = FaultTree.load_from_xml("models/Theatre/theatre.xml")

# (if it is not too big) the fault tree can be visualized with
ft.save_as_image('theatre.png')

# compute the m=2 smallest cut sets with Grover
cutsets = ft.compute_min_cutsets(m=2, method='grover') 
print("cut sets:", cutsets)

# alternatively, method='classical' uses a classical SAT solver
```


Fault trees can also be constructed from scratch, rather than loading an XML file.

```python
from ft_2_quantum_sat.fault_tree import FaultTree

# build simple fault tree
ft = FaultTree()
ft.set_top_event('car breaks')
ft.add_basic_event('engine breaks', 0.05) # (probabilities are currently ignored)
ft.add_basic_event('wheel breaks', 0.1)
ft.add_basic_event('no spare', 0.3)
ft.add_gate('car breaks', 'or', ['engine breaks', 'wheel issue'])
ft.add_gate('wheel issue', 'and', ['wheel breaks', 'no spare'])

# compute the m=2 smallest cut sets with Grover
cutsets = ft.compute_min_cutsets(m=2, method='grover') 
print("cut sets:", cutsets)
```
