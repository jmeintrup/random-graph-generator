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
    edges=random_spanning_tree(n)
    for v in range(1,n+1):
        for u in range(v+1, n+1):
            if random.random() <= p:
                edges.add((v, u))
    edges=list(edges)
    edges.sort()
    return edges

def fixed(n, m):
    spanning_tree=random_spanning_tree(n)
    edges=spanning_tree
    if len(spanning_tree)>m:
        return spanning_tree
    all_edges=set()
    for u in range(0,n):
        for v in range(u+1,n):
            all_edges.add((u, v))
    candidates=all_edges-spanning_tree
    while len(edges) < m and len(candidates) > 0:
        edge = random.sample(candidates, 1).pop()
        candidates.remove(edge)
        edges.add(edge)
    edges=list(edges)
    edges.sort()
    return edges
    

def random_spanning_tree(n):
    vertices=list(range(0,n))
    S=set(vertices)
    T=set()
    v = random.sample(S, 1).pop()
    S.remove(v)
    T.add(v)

    edges=set()
    while len(S)>0:
        u=random.sample(vertices, 1).pop()
        if u not in T:
            edges.add((min(u,v), max(u,v)))
            S.remove(u)
            T.add(u)
        v=u
    return edges

def print_dimacs(n, edges, comment=None):
    print(f"p edges {n} {len(edges)}")
    for edge in edges:
        print(f"e {edge[0]+1} {edge[1]+1}")

if args.type == 'erdos':
    edges=erdos(args.n, args.p)
    print(f"c Randomly Generated Erdos-Reyni Graph with p={args.p} and n={args.n}")
    print_dimacs(args.n, edges)
if args.type == 'fixed':
    if args.m == None:
        raise argparse.ArgumentTypeError('Fixed type requires "m" argument')
    print(f"c Randomly Generated graph with fixed number of edges and vertices")
    edges=fixed(args.n, args.m)
    print_dimacs(args.n, edges)
