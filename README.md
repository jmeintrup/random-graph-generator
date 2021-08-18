# Random Graph Generator
Simple random graph generator written in python, generates graph in DIMACS .col format.
All graphs are simple and connected. For this, a random spanning tree is constructed and missing edges are added at random.
This means that all graphs with n vertices contain at least n-1 edges.

### Usage
```
usage: main.py [-h] [-n N] [-p P] [-s SEED] [--type type] [-m M]

Random Graph Generation Tool

optional arguments:
  -h, --help   show this help message and exit
  -n N         Num Vertices
  -p P         Probability per Edge
  -s SEED      Seed for RNG
  --type type  Type: "erdos" or "fixed", fixed requires "-m" argument
  -m M         Num Edges for fixed generation
```
