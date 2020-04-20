import sys

poly_in = [20, 10, 15]  # Indices in the array = degree of term - 1
constraints = [[3, 2, 5, 55], [2, 1, 1, 26], [1, 1, 3, 30], [5, 2, 4, 57]]
constraints_greater_than = [[1, 1, 1, 0]]


class ProblemOne:
    def __init__(self):
        self.degree = len(poly_in)

    def main(self):
        # ------------------ Problem 1 ------------------
        # get the variable numbers
        vals_by_subscr = []
        counter = 0
        for v in " "*(len(poly_in)+1):
            temp = []
            for row in constraints:
                temp.append(row[counter])
            vals_by_subscr.append(temp)
            counter += 1
        # Make the initial table
        table = [[vals_by_subscr[0][0], vals_by_subscr[1][0], vals_by_subscr[2][0], vals_by_subscr[3][0]],
                 [vals_by_subscr[0][1], vals_by_subscr[1][1], vals_by_subscr[2][1], vals_by_subscr[3][1]],
                 [vals_by_subscr[0][2], vals_by_subscr[1][2], vals_by_subscr[2][2], vals_by_subscr[3][2]],
                 [vals_by_subscr[0][3], vals_by_subscr[1][3], vals_by_subscr[2][3], vals_by_subscr[3][3]],
                 [poly_in[0], poly_in[1], poly_in[2], 1]]
        # Transpose the table
        table_transpose = gen_transpose(table)
        # Maximize

        # nb vars (3), slack vars (3), z, col to max (1)
        row1 = [table_transpose[0][0], table_transpose[0][1], table_transpose[0][2], table_transpose[0][3], 1, 0, 0, 0, table_transpose[0][4]]
        row2 = [table_transpose[1][0], table_transpose[1][1], table_transpose[1][2], table_transpose[1][3], 0, 1, 0, 0, table_transpose[1][4]]
        row3 = [table_transpose[2][0], table_transpose[2][1], table_transpose[2][2], table_transpose[2][3], 0, 0, 1, 0, table_transpose[2][4]]
        row4 = [-1*table_transpose[3][0], -1*table_transpose[3][1], -1*table_transpose[3][2], -1*table_transpose[3][3], 0, 0, 0, 1*table_transpose[3][4], 0]

        simplex_table = [row1, row2, row3, row4]
        row_length = len(row1)
        # Check if we need to pivot
        while negativest_in_row(simplex_table) != -1:  # need to pivot if true
            pivot_col = negativest_in_row(simplex_table)

            low_temp = sys.maxsize
            pivot_row = 0
            i = 0
            while i < len(simplex_table)-1:  # The +2 is 1 for Z column and one to account for 0 indexing
                temp_ratio = simplex_table[i][row_length-1]/simplex_table[i][pivot_col]
                if low_temp > temp_ratio > 0:
                    pivot_row = i
                    low_temp = temp_ratio
                i += 1

            #  Pivot the table around pivot_row x low_col
            c = simplex_table[pivot_row][pivot_col]
            j = 0
            while j < len(simplex_table[pivot_row]):
                simplex_table[pivot_row][j] = simplex_table[pivot_row][j]/c
                j += 1

            i = 0  # row
            while i < len(simplex_table):
                if i == pivot_row:
                    i += 1
                    continue
                j = 0  # col
                scalar = simplex_table[i][pivot_col]
                while j < row_length:
                    simplex_table[i][j] = simplex_table[i][j] - (scalar*simplex_table[pivot_row][j])
                    j += 1
                i += 1

        # Find the values of x
        # Write out the end values
        print("minimum of ", simplex_table[len(simplex_table)-1][row_length-1], " at")
        print(" x1", " = ", simplex_table[len(simplex_table)-1][4])
        print(" x2", " = ", simplex_table[len(simplex_table)-1][5])
        print(" x3", " = ", simplex_table[len(simplex_table)-1][6])


def negativest_in_row(table_in):
    lowest = sys.maxsize
    col = 0
    low_col = -1
    for v in table_in[len(table_in)-1]:
        if v < 0 and v < lowest:
            lowest = v
            low_col = col
        col += 1
    return low_col


def gen_transpose(table_in):
    transpose = []
    # Set the size to avoid index out of bounds
    j = 0
    while j < len(table_in[0]):
        i = 0
        row = []
        while i < len(table_in):
            row.append(table_in[i][j])
            i += 1
        transpose.append(row)
        j += 1
    return transpose


def print_table(table_in):
    rows = len(table_in)
    cols = len(table_in[0])
    i = 0
    while i < cols:
        j = 0
        line = ""
        while j < rows:
            line += table_in[i][j], " "
            j += 1
        i += 1
        print(line)


if __name__ == '__main__':
    linear_program = ProblemOne()
    try:
        linear_program.main()
    except KeyboardInterrupt:  # Handle the user ending the program.
        print("Ctrl C")
        sys.exit(1)
