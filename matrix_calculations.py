def copy_matrix(M):
    """
    Creates and returns a copy of a matrix.
        :param M: The matrix to be copied
        :return: A copy of the given matrix
    """
    # Section 1: Get matrix dimensions
    rows = len(M)
    cols = len(M[0])

    # Section 2: Create a new matrix of zeros
    MC = zeros_matrix(rows, cols)

    # Section 3: Copy values of M into the copy
    for i in range(rows):
        for j in range(cols):
            MC[i][j] = M[i][j]

    return MC

def zeros_matrix(rows, cols):
    """
    Creates a matrix filled with zeros.
        :param rows: the number of rows the matrix should have
        :param cols: the number of columns the matrix should have
        :return: list of lists that form the matrix
    """
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)

    return M

def determinant_recursive(A, total=0, print_steps=True):
    
    # Section 1: store indices in list for row referencing
    indices = list(range(len(A)))
     
    # Section 2: when at 2x2 submatrices recursive calls end
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val
 
    # Section 3: define submatrix for focus column and 
    #      call this function
    for fc in indices: # A) for each focus column, ...
        # find the submatrix ...
        As = copy_matrix(A) # B) make a copy, and ...
        As = As[1:] # ... C) remove the first row
        height = len(As) # D) 

        if print_steps:
            # Print algorithm steps det = SUM(-1) ^ i+j (aij)(Mij)
            print("###########")
            print('(-1)^ 1+' + str(fc+1)) 
            print('*' + str(A[0][fc])) # Print current step 2
        for i in range(height): 
            # E) for each remaining row of submatrix ...
            #     remove the focus column elements
            As[i] = As[i][0:fc] + As[i][fc+1:] 
            if print_steps:
                print(str(As[i]).replace('[', '|').replace(']','|')) # Print current step 2

        sign = (-1) ** (fc % 2) # F) 
 

        # G) pass submatrix recursively
        sub_det = determinant_recursive(As)
        
        # H) total all returns from recursion
        print('Step Result: ' + str(sign * A[0][fc] * sub_det))
        total += sign * A[0][fc] * sub_det 
 
    if print_steps:
        
        print("###########")
    return total




def determinant_3x3_shortcut(input=[[0,0,0],
                                    [0,0,0],
                                    [0,0,0]]):
    print(50*"#")
    print("Input and Its Index:")

    # Calculate Determinant
    row1 = input[0]
    row2 = input[1]
    row3 = input[2]

    print(str(row1) + '    [a, b, c] a, b')
    print(str(row2) + '    [d, e, f] d, e')
    print(str(row3) + '    [g, h, j] g, h')

    print(50*"_")

    first_calc = row1[0] * row2[1] * row3[2]
    second_calc = row1[1] * row2[2] * row3[0]
    third_calc = row1[2] * row2[0] * row3[1]
    fourth_calc = row1[2] * row2[1] * row3[0]
    fifth_calc = row1[1] * row2[0] * row3[2]
    sixth_calc = row1[0] * row2[2] * row3[1]

    print("1. ( aej  +   bfg   + cdh  ) - (  ceg   +   afh   +   bdj  )")
    print('2. ( (' + str(first_calc) + ') + (' + str(second_calc) + ') + (' + str(third_calc) + ') ) - ( (' + str(fourth_calc) + ') + (' + str(fifth_calc) + ') + (' + str(sixth_calc) + ') )')
    print('3. (' + str((first_calc + second_calc + third_calc)) + ') - (' + str((fourth_calc + fifth_calc + sixth_calc)) + ')')

    print(50*"_")

    determinant = (first_calc + second_calc + third_calc) - (fourth_calc + fifth_calc + sixth_calc)
    
    # print('Determinant =  ' + str(determinant))
    return determinant
    print(50*"#")
    

def replace_row_with_constants(matrix, constants, constant_index):
    '''
    Replaces row with constants (A1) to get XYZ values using Cramer's method

    Example:
    5x -3y +4z = -1
    2x + 5y -6z = -26
    7x + 3y -2z = -25
                                    A1   A2  A3
    Matrix of coefficients = |A|  = |5  -3   4|
                                    |2   5  -6|
                                    |7   3  -2|

    |A1| = Replace A1 with constants [-1, -26, -25]

    For example = |A1|  = |-1  -3    4|
                          |-26   5  -6|
                          |-25   3  -2|

    Use 3x3 shortcut to get determinant for |A1|, then:

    x = |A1| / |A|
    y = |A2| / |A|
    z = |A3| / |A|

    So for the function, if input is A, constants are [-1, -26, -25] and index 0, you get: |A1| as shown above

    '''
    a_x_matrix = []
    for row_index in range(len(matrix)):
        row = matrix[row_index]
        new_row = []
        for index in range(len(row)):
            
            if index != constant_index:
                new_row.append(row[index])
            else:
                new_row.append(constants[0][row_index])
        a_x_matrix.append(new_row)
    return a_x_matrix



def matrix_addition(A, B):
    """
    Adds two matrices and returns the sum
        :param A: The first matrix
        :param B: The second matrix
        :return: Matrix sum
    """
    # Section 1: Ensure dimensions are valid for matrix addition
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])
    if rowsA != rowsB or colsA != colsB:
        raise ArithmeticError('Matrices are NOT the same size.')

    # Section 2: Create a new matrix for the matrix sum
    C = zeros_matrix(rowsA, colsB)

    # Section 3: Perform element by element sum
    for i in range(rowsA):
        for j in range(colsB):
            C[i][j] = A[i][j] + B[i][j]

    return C


def matrix_subtraction(A, B):
    """
    Subtracts matrix B from matrix A and returns difference
        :param A: The first matrix
        :param B: The second matrix
        :return: Matrix difference
    """
    # Section 1: Ensure dimensions are valid for matrix subtraction
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])
    if rowsA != rowsB or colsA != colsB:
        raise ArithmeticError('Matrices are NOT the same size.')

    # Section 2: Create a new matrix for the matrix difference
    C = zeros_matrix(rowsA, colsB)

    # Section 3: Perform element by element subtraction
    for i in range(rowsA):
        for j in range(colsB):
            C[i][j] = A[i][j] - B[i][j]

    return C


def matrix_multiply(A, B, print_steps=False, print_slot_index=False):
    """
    Returns the product of the matrix A * B
        :param A: The first matrix - ORDER MATTERS!
        :param B: The second matrix
        :return: The product of the two matrices
    """
    # Section 1: Ensure A & B dimensions are correct for multiplication
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])
    if colsA != rowsB:
        raise ArithmeticError(
            'Number of A columns must equal number of B rows.')

    # Section 2: Store matrix multiplication in a new matrix
    C = zeros_matrix(rowsA, colsB)
    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]

                if print_steps:
                    if print_slot_index:
                        print('Amn:' + str(i) + str(ii) + '  Bpq:' + str(ii) + str(j))
                    print(str(A[i][ii]) + ' * ' + str(B[ii][j]) + ' = ' + str(A[i][ii] * B[ii][j]))
  
            if print_steps:
              print('Step Result: ' + str(total) + '\n#######')
            C[i][j] = total

    return C



# TESTS #

print("_"*80)
print("\n")

################# DETERMINANT BY MINOR AND 3X3 SHORTCUT ################

# # Expects determinent 38 
# A = [[5,-3,4], 
#      [2,5,-6],
#      [7,3,-2]]

# A_constants = [[-1,
#                 -26,
#                 -25]]

# # Expects -693
# B = [[0, 1, 0, -7],
#      [1, 3, 3, 2],
#      [0, 6,-1, 3],
#      [5, 1, 2, 0]]


# output = determinant_recursive(A) 
# print('\nResult: ' + str(output) + '\n')


######################## 3x3 SHORTCUT ################################
# output = determinant_3x3_shortcut(A)
# print('\nResult: ' + str(output) + '\n')

# Expects determinent 38 
# A = [[1,2,-1], 
#      [2,-1,3],
#      [0,-2,-1]]

# output = determinant_recursive(A) 
# print('\nResult: ' + str(output) + '\n')


############## CRAMMER'S METHOD ######################################

'''
    Replaces row with constants (A1) to get XYZ values using Cramer's method

    Example:
    5x -3y +4z = -1
    2x + 5y -6z = -26
    7x + 3y -2z = -25
                                    A1   A2  A3
    Matrix of coefficients = |A|  = |5  -3   4|
                                    |2   5  -6|
                                    |7   3  -2|

    |A1| = Replace A1 with constants [-1, -26, -25]

    For example = |A1|  = |-1  -3    4|
                          |-26   5  -6|
                          |-25   3  -2|

    Use 3x3 shortcut to get determinant for |A1|, then:

    x = |A1| / |A|
    y = |A2| / |A|
    z = |A3| / |A|

    '''

# # Expects determinent 38 
# A = [[5,-3,4], 
#      [2,5,-6],
#      [7,3,-2]]

# A_constants = [[-1,
#                 -26,
#                 -25]]
# A1 = replace_row_with_constants(A, A_constants, 0) #     0 = A1         1 = A2      2 = A3
# print(A)
# print(A1)
# # det_a = determinant_recursive(A) 
# # det_a1 = determinant_recursive(A1) 
# det_a = determinant_3x3_shortcut(A) 
# det_a1 = determinant_3x3_shortcut(A1) 

# print('\nDeterminant A: ' + str(det_a))
# print('Determinant A1: ' + str(det_a1))
# print('Result X: ' + str(det_a1/det_a) + '\n')



############## MATRIX ADDITION, SUBTRACTION, MULTIPLICATION ######################################


'''
    Addition and Subtraction
    1. Addition and subtraction, find the same index in each matrix and add/subtract the values
    2. Only works for matrices of the same size
'''

# A = [[3,5,], 
#      [9,7,],
#      [0,1,]]

# B = [[0,8,], 
#      [1,2,],
#      [5,-3,]]

# C = [[2,0,], 
#      [9,-8,]]


# # output = matrix_addition(A, B)   # A+B
# # output = matrix_subtraction(B, A)   # B-A
# # output = matrix_addition(A, C)   # A+C    -  CANNONT BE DONE, MATRICES ARE NTO THE SAME SIZE
# # output = matrix_subtraction(A, C)   # B-C    -  CANNONT BE DONE, MATRICES ARE NTO THE SAME SIZE
# print('Result:')
# for row in output:
#     print(row)

'''
    Multiplication
    1. Not commutative: AxB =/= BxA
    2. If inside values of the dimention match, then you can multiply them
       M = up/down, number of rows       N = left/right, number of columns 
       A       X     B
        m x n        p x q             n must be = to p    (inside ones)
        2 x 2        2 x 1             Allowed             
        2 x 3        3 x 2             Can NOT be done

    3. Size of the result is equal of the outside values. For example M and Q
        2 x 2        2 x 1             Allowed   -> Result: 2 x 1 (m x q)


    DO IT MANUALLY
    1. Row 1 times Column 1
    2. Row 2 times Column 1
    e.g.
    [1, 2] * [x] = [x + 2y]
    [3, 4] * [y] = [3x + 4y]


'''

# A = [[1,4,], 
#      [3,2,]]

# B = [[3,], 
#      [5,]]

# output = matrix_multiply(A, B) # Expects [[23], [19]]
# print('Result:')
# for row in output:
#     print(row)


# A = [[1,3,], 
#      [7,2,]]

# B = [[2, 8, 10, 12], 
#      [5, 9, 11, 13]]


# output = matrix_multiply(A, B, True, False) # Expects [[23], [19]]
# print('Result:')
# for row in output:
#     print(row)





########## DIVISION , IDENTITY MATRIX ##############################
'''
    YOU CAN NOT DIVIDE MATRICES so you have to "cheat"
    We will focus only in square matrices for this part

    |I| = 1 (always)

    Some matrices are not invertible (not all of them)
    If they do they are "invertable"   Determinant =/= 0
    Some matrices do not have an inverse
    We call them "singular"   Determinant = 0

    AA^=1 =     A^-1 * A    = I

    1. If determinant is 0, then the matrix is singular
    2. If determinant is different than 0, then the matrix is invertible
'''
   
# A = [[2,1,], 
#      [5,3,]]

# B = [[3,-1,], 
#      [-5,2,]]

# output = matrix_multiply(A, B, True, False) # If you get identity, then they are inverse
# print('Result:')
# for row in output:
#     print(row)

'''
Generating inverse:
    # Original
    A = [a, b]
        [c, d]

    # Inverse
    A^-1 = 1 / |A| [d, -b]
                   [-c, a]

    So:
    2x + y = 4
    x + 3y = 9

 
'''



############ MISC #####################################################

# determinant_3x3_shortcut(input=[[-2,3,-1],
#                                 [2,2,-1],
#                                 [-1,3,2]])
# print("Expected: -31")           # Is invertible, Not singular       


# A = [[5,-3,4],
#      [2,5,-6],
#      [7,3,-2]]

# output = determinant_recursive(A) # Expects 38
# print(output)

# B = [[0, 1, 0, -7],
#      [1, 3, 3, 2],
#      [0, 6,-1, 3],
#      [5, 1, 2, 0]]

# output = determinant_recursive(B) 
# print('\nResult: ' + str(output) + '\n')


# C = [[4, 4, 2, 1],
#      [0, 3, 2, 3],
#      [0, 2, 4, 1],
#      [0, 4, 2, 3]]

#               # This point replaced by result
# # C = [[4, 4, 2, 1],
# #      [0, 3, 7, 3],
# #      [0, 2, 0, 1],
# #      [0, 4, 0, 3]]

# # output = determinant_recursive(C) # Expects -40
# # print(output)

# print(-56/-40)
# # 
# # __


# D = [[0, 2, -1],
#      [0, -3, -2],
#      [-3, 3, 3]]
# D = [[0, -11, -1],
#      [0, 27, -2],
#      [-3, -51, 3]]


# output = determinant_recursive(D) # Expects -40
# print(output)


# print(-147/21)

# C = [[4, 4, 2, 1],
#      [0, 3, 2, 3],
#      [0, 2, 4, 1],
#      [0, 4, 2, 3]]
# C = [[4, 4, 5, 1],
#      [0, 3, 6, 3],
#      [0, 2, 0, 1],
#      [0, 4, 0, 3]]

# output = determinant_recursive(C)
# print(output)

# print(-48/-40)


# print(-147/21)

#############

# M = [[2,0,-4], 
#      [10,-8,2]]

# N = [[-3,1,7], 
#      [0,1,0]]


# # # output = matrix_addition(A, B)   # A+B
# output = matrix_subtraction(M, N)   # B-A
# print('Result:')
# for row in output:
#     print(row)


#################### 

# B = [[1, -2, 3],
#      [-1, 3, 0],
#      [2, -5,5]]
# B = [[15/2, -5/2, -9/2],
#      [5/2, -1/2, -3/2],
#      [-1/2, 1/2, 1/2]]


# # output = determinant_recursive(B) 
# # print('\nResult: ' + str(output) + '\n')


# ######################## 3x3 SHORTCUT ################################
# output = determinant_3x3_shortcut(B)
# print('\nResult: ' + str(output) + '\n')




# inverse = [[15/2,-5/2, -9/2], 
#      [5/2,-1/2, -3/2],
#      [-1/2,1/2, 1/2]]

# B = [[9],
#      [-4],
#      [17]]

# print(inverse)

# output = matrix_multiply(inverse, B) 
# print('Result:')
# for row in output:
#     print(row)
