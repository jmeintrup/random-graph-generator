import argparse
import random
import re
pat = re.compile(r"^erdos|fixed$")

def generation_type(arg_value, pat=pat):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError('Expected "erdos" or "fixed" as type')
    return arg_value

parser = argparse.ArgumentParser(description='Random Graph Generation Tool')
parser.add_argument('-n', metavar='N', type=int, help='Num Vertices')
parser.add_argument('-p', metavar='P', type=float, help='Probability per Edge')
parser.add_argument('-s', metavar='SEED', type=int, help='Seed for RNG')
parser.add_argument('--type', metavar='type', type=generation_type,default='erdos', help='Type: "erdos" or "fixed", fixed requires "-m" argument')
parser.add_argument('-m', metavar='M', type=int, help='Num Edges for fixed generation')

args = parser.parse_args()
random.seed(args.s)

def erdos(n, p):
    edges=[]
    for v in range(1,n+1):
        for u in range(v+1, n+1):
            if random.random() <= p:
                edges.append((v, u))
    return edges

def fixed(n, m):
    max_edges = (n*(n-1))/2
    if m > max_edges:
        return None
    edges=set()
    if m <= max_edges/2:
        while len(edges) < m:
            v=random.randint(1, n)
            u=random.randint(1, n)
            if v == u:
                continue
            edges.add((min(u, v), max(u, v)))
    else:
        for v in range(1, n+1):
            for u in range(v+1, n+1):
                edges.add((v, u))
        while len(edges) > m:
            v=random.randint(1, n)
            u=random.randint(1, n)
            edges.discard((u, v))
    edges=list(edges)
    edges.sort()
    return edges


def print_dimacs(n, edges, comment=None):
    print(f"p edges {n} {len(edges)}")
    for edge in edges:
        print(f"e {edge[0]} {edge[1]}")

if args.type == 'erdos':
    edges=erdos(args.n, args.p)
    print(f"c Randomly Generated Erdos-Reyni Graph with p={args.p} and n={args.n}")
    print_graph(args.n, edges)
if args.type == 'fixed':
    print(f"c Randomly Generated graph with fixed number of edges and vertices")
    edges=fixed(args.n, args.m)
    print_graph(args.n, edges)
