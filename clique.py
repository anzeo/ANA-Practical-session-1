import sys

import networkx as nx

CLAUSE_COUNTER = 0


def reduce_clique_sat(G, k):
    global CLAUSE_COUNTER
    CLAUSE_COUNTER = 0
    clause = ''
    vertices = 0

    table = {v: [i * k + r for r in range(1, k + 1)] for i, v in enumerate(nx.nodes(G))}

    # Some node is the r-th node of clique
    for r in range(k):
        column_elements = [v[r] for key, v in table.items()]
        clause += alo(column_elements)

    # # No node is both the r-th and s-th node of the clique
    for key, v in table.items():
        clause += amo(v)

    for j, (key_j, v_j) in enumerate(table.items()):
        for i, (key_i, v_i) in enumerate(list(table.items())[:j]):
            if not G.has_edge(str(key_i), str(key_j)):
                for s in range(k):
                    clauses_tmp = [str(-v_i[r]) + ' ' + str(-v_j[s]) + ' 0\n' for r in range(k) if r != s]
                    clause += ''.join(clauses_tmp)
                    CLAUSE_COUNTER += len(clauses_tmp)

    return 'p cnf ' + str(len(table) * k) + ' ' + str(CLAUSE_COUNTER) + '\n' + clause


def alo(elements):
    global CLAUSE_COUNTER
    CLAUSE_COUNTER += 1
    return ' '.join(str(element) for element in elements) + ' 0\n'


def amo(elements):
    global CLAUSE_COUNTER
    clause = ''
    for i, current in enumerate(elements):
        clause += ''.join(
            [str(-current) + ' ' + str(-other_el) + ' 0\n' for other_el in elements[i + 1:]])
        CLAUSE_COUNTER += len(elements[i + 1:])
    return clause


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise TypeError('Manjkajo argumenti. Program sprejme 2 argumenta - ime datoteke z grafom in velikost klike')
    else:
        filename = sys.argv[1]
        k = int(sys.argv[2])
        f = open(filename, "rb")
        G = nx.read_edgelist(f)
        f.close()

        f = open("sat_clique.txt", "w")
        sat = reduce_clique_sat(G, k)
        f.write(sat)
        f.close()
        print("\nSAT problem je zapisan v datoteki sat_clique.txt")

