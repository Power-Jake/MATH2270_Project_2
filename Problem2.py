import sys

poly_in = [1, 2, 4, 5]  # Indices in the array = degree of term - 1
# constraint arrays in the form [preceeding elements] >= [last element]
constraints = [[0, 1, 0, 0, 2], [1, 0, 0, 1, 9], [0, 0, 1, 1, 5], [0, 0, 0, 1, 2]]
constraints_greater_than = [[1, 1, 1, 0]]


class ProblemTwo:
    def __init__(self):
        self.degree = len(poly_in)

    def main(self):
        # ------------------ Problem 2 ------------------
        # get the variable numbers
        vals_by_subscr = []
        counter = 0
        for v in " " * (len(poly_in) + 1):
            temp = []
            for row in constraints:
                temp.append(row[counter])
            vals_by_subscr.append(temp)
            counter += 1
        # Make the initial table
        table = [[vals_by_subscr[0][0], vals_by_subscr[1][0], vals_by_subscr[2][0], vals_by_subscr[3][0], vals_by_subscr[4][0]],  # row 1
                 [vals_by_subscr[0][1], vals_by_subscr[1][1], vals_by_subscr[2][1], vals_by_subscr[3][1], vals_by_subscr[4][1]],  # row 2
                 [vals_by_subscr[0][2], vals_by_subscr[1][2], vals_by_subscr[2][2], vals_by_subscr[3][2], vals_by_subscr[4][2]],  # row 3
                 [vals_by_subscr[0][3], vals_by_subscr[1][3], vals_by_subscr[2][3], vals_by_subscr[3][3], vals_by_subscr[4][3]],  # row 4
                 [poly_in[0], poly_in[1], poly_in[2], poly_in[3], 1]]  # row 5
        table_transpose = gen_transpose(table)

        row1 = [table_transpose[0][0], table_transpose[0][1], table_transpose[0][2], table_transpose[0][3], 1, 0, 0, 0, 0, table_transpose[0][4]]
        row2 = [table_transpose[1][0], table_transpose[1][1], table_transpose[1][2], table_transpose[1][3], 0, 1, 0, 0, 0, table_transpose[1][4]]
        row3 = [table_transpose[2][0], table_transpose[2][1], table_transpose[2][2], table_transpose[2][3], 0, 0, 1, 0, 0, table_transpose[2][4]]
        row4 = [table_transpose[3][0], table_transpose[3][1], table_transpose[3][2], table_transpose[3][3], 0, 0, 0, 1, 0, table_transpose[3][4]]
        row5 = [-1 * table_transpose[4][0], -1 * table_transpose[4][1], -1 * table_transpose[4][2], -1 * table_transpose[4][3], 0, 0, 0, 0, 1 * table_transpose[4][4], 0]

        simplex_table = [row1, row2, row3, row4, row5]

        row_length = len(simplex_table[0])
        # Check if we need to optimize
        # If != -1 then the number represents the column with the lowest negative value in the bottom "cost" row.
        # When == -1 happens then I know the table is optimized and the program prints the results and ends.
        while negativest_in_row(simplex_table) != -1:
            pivot_col = negativest_in_row(simplex_table)

            # This segment of the code finds the row with the pivot
            low_temp = sys.maxsize
            pivot_row = 0
            i = 0
            # i is an integer that keeps count of rows as I read through them one by one.
            while i < (len(simplex_table) - 1):  # The -1 is to take zero indexing into account
                if simplex_table[i][pivot_col] == 0:  # Avoid division by 0
                    i += 1
                    continue
                temp_ratio = simplex_table[i][row_length - 1] / simplex_table[i][pivot_col]
                if low_temp > temp_ratio >= 0:
                    pivot_row = i  # If I find a new smallest ratio then I save it into pivot row.
                    low_temp = temp_ratio
                i += 1

            # This loop reduces the pivot and its row so that the pivot's value is 1
            c = simplex_table[pivot_row][pivot_col]  # c = is the value of the pivot's coefficient
            j = 0  # j is an integer that keeps count of columns as I read through them.
            while j < len(simplex_table[pivot_row]):
                simplex_table[pivot_row][j] = simplex_table[pivot_row][j] / c
                j += 1

            # This loop does row operations to get the values above and below the pivot to zero
            i = 0  # row
            while i < len(simplex_table):
                if i == pivot_row:
                    i += 1
                    continue
                j = 0  # col
                scalar = simplex_table[i][pivot_col]
                while j < row_length:
                    simplex_table[i][j] = simplex_table[i][j] - (scalar * simplex_table[pivot_row][j])
                    j += 1
                i += 1

        # Find the values of X
        # Write out the end values
        print("Minimum of $", simplex_table[len(simplex_table)-1][row_length-1], " for")
        print(simplex_table[len(simplex_table)-1][4], "pints of A")
        print(simplex_table[len(simplex_table)-1][5], "pints of AB")
        print(simplex_table[len(simplex_table)-1][6], "pints of B")
        print(simplex_table[len(simplex_table) - 1][7], "pints of O")


def negativest_in_row(table_in):
    lowest = sys.maxsize
    col = 0
    low_col = -1
    for v in table_in[len(table_in)-1]:
        if v < 0 and v < lowest:
            if col == len(table_in[len(table_in)-1])-1:
                continue
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
    linear_program = ProblemTwo()
    try:
        linear_program.main()
    except KeyboardInterrupt:  # Handle the user ending the program.
        print("Ctrl C")
        sys.exit(1)
