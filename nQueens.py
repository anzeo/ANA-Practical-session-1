CLAUSE_COUNTER = 0


def reduce_nq_sat(n):
    global CLAUSE_COUNTER
    CLAUSE_COUNTER = 0
    board = [[row * n + col for col in range(1, n + 1)] for row in range(n)]
    clause = ''

    for i in range(n):
        # At least one queen in a row
        clause += alo(board[i])
        # At most one queen in a row
        clause += amo(board[i])

        column_elements = [row[i] for row in board]

        # At least one queen in a column
        clause += alo(column_elements)
        # At most one queen in a column
        clause += amo(column_elements)

        # Diagonal elements at the top right part of the board
        tr_diagonal_elements = [board[j][j + i] for j in range(n - i)]
        # Diagonal elements at the bottom left part of the board
        bl_diagonal_elements = [board[j + i][j] for j in range(n - i)]
        # Diagonal elements at the top left part of the board
        tl_diagonal_elements = [board[n - i - j - 1][j] for j in range(n - i)]
        # Diagonal elements at the bottom right part of the board
        br_diagonal_elements = [board[n - j - 1][j + i] for j in range(n - i)]

        # At most one queen on each diagonal
        clause += amo(tr_diagonal_elements)
        clause += amo(bl_diagonal_elements)
        clause += amo(tl_diagonal_elements)
        clause += amo(br_diagonal_elements)

    return 'p cnf ' + str(n * n) + ' ' + str(CLAUSE_COUNTER) + '\n' + clause


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


f = open("sat.txt", "w")
sat = reduce_nq_sat(4)
f.write(sat)
f.close()
print("SAT problem je zapisan v datoteki sat.txt")
