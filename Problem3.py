"""
A toy factory produces two toys, a doll and an action figure. Each toy uses two machines to be made, one
 that manufactures the parts and one that assembles them. Manufacturing a doll takes 3 hours, and
 assembling it takes 2 hours. Manufacturing an action figure takes 4 hours, and assembling it takes 3
 hours. The factory allows 80 hours for manufacturing, and 60 hours for assembling. The profit per
 doll is $30, and the profit per action figure is $45. How many of each should be produced to maximize
 the profit? (I assigned x1 to the doll and x2 to the action figure).
"""

import sys

poly_in = [30, 45]  # Indices in the array = degree of term - 1
constraints = [[3, 4, 80], [2, 3, 60]]
constraints_greater_than = [[1, 1, 0]]


class ProblemThree:
    def __init__(self):
        self.degree = len(poly_in)

    def main(self):
        # ------------------ Problem 3 ------------------
        # get the variable numbers
        vals_by_subscr = []
        counter = 0
        for v in " "*(len(poly_in)+1):
            temp = []
            for row in constraints:
                temp.append(row[counter])
            vals_by_subscr.append(temp)
            counter += 1
        # Make the initial table of inputs
        table = [[vals_by_subscr[0][0], vals_by_subscr[1][0], vals_by_subscr[2][0]],
                 [vals_by_subscr[0][1], vals_by_subscr[1][1], vals_by_subscr[2][1]],
                 [poly_in[0], poly_in[1], 1]]

        # Maximize using simplex method
        # nb vars (2), slack vars (2), z, col to max (1)
        row1 = [table[0][0], table[0][1], 1, 0, 0, table[0][2]]
        row2 = [table[1][0], table[1][1], 0, 1, 0, table[1][2]]
        row3 = [-1*table[2][0], -1*table[2][1], 0, 0, 1*table[2][2], 0]
        # Manually setting these because generating the table would be a ton of work

        simplex_table = [row1, row2, row3]
        row_length = len(row1)
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

        # Find the values of x
        # Write out the end values
        print("Maximum of $", simplex_table[len(simplex_table)-1][row_length-1], " making")
        action = 0
        dolls = 0
        i = 0
        while i < len(simplex_table)-1:  # Check the number of action figures
            if simplex_table[i][1] == 1:
                action = simplex_table[i][row_length-1]
            i += 1
        i = 0
        while i < len(simplex_table)-1:  # Check the number of dolls
            if simplex_table[i][0] == 1:
                dolls = simplex_table[i][row_length - 1]
            i += 1
        print(action, " action figures and ", dolls, " dolls")


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
    linear_program = ProblemThree()
    try:
        linear_program.main()
    except KeyboardInterrupt:  # Handle the user ending the program.
        print("Ctrl C")
        sys.exit(1)
