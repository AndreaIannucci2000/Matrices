def is_matrix(list_):
    if not len(list_):
        return False
    try:
        ncol = len(list_[0])
    except IndexError:
        return False

    for riga in list_:
        if not len(riga) == ncol:
            return False
        if not isinstance(riga, list):
            return False
        if not all(isinstance(x, (int, float)) for x in riga):
            return False

    return True


def create_matrix(rows, columns, filler=0):
    new_matrix = []
    riga = [filler for x in range(columns)]
    for _ in range(rows):
        new_matrix.append(riga[:])
    return new_matrix


def dimensions(matrix):
    if not is_matrix(matrix):
        raise ValueError('arg is not a matrix')

    return len(matrix), len(matrix[0])


def sum(matrix1, matrix2):
    if not is_matrix(matrix1) or not is_matrix(matrix2):
        raise ValueError('Args are not matrices')

    if not dimensions(matrix1) == dimensions(matrix2):
        raise ValueError('args are not similar matrices')

    new_dim = dimensions(matrix1)
    new_matrix = create_matrix(new_dim[0], new_dim[1])
    for i in range(new_dim[0]):
        for j in range(new_dim[1]):
            new_matrix[i][j] = matrix1[i][j]+matrix2[i][j]

    return new_matrix


def transposed(matrix):
    if not is_matrix(matrix):
        raise ValueError('arg is not a matrix')

    dim = dimensions(matrix)
    new_matrix = create_matrix(dim[1], dim[0])
    for i in range(dim[0]):
        for j in range(dim[1]):
            new_matrix[j][i] = matrix[i][j]

    return new_matrix


def identity(n):
    new_identity = create_matrix(n,n)
    for i in range(n):
        new_identity[i][i] = 1

    return new_identity 


def scalar_product(matrix, scalare):
    if not is_matrix(matrix):
        raise ValueError('first arg is not a matrix')

    if not isinstance(scalare, (int, float)):
        raise ValueError('second arg is not a scalar')

    dim = dimensions(matrix)
    new_matrix = create_matrix(dim[0], dim[1])
    for i in range(dim[0]):
        for j in range(dim[1]):
            new_matrix[i][j] = scalare*matrix[i][j]

    return new_matrix


def difference(matrix1, matrix2):
    new_matrix2 = scalar_product(matrix2, -1)
    return sum(matrix1, new_matrix2)


def product(matrix1, matrix2):
    if not is_matrix(matrix1) or not is_matrix(matrix2):
        raise ValueError('args are not matrices')

    dim1 = dimensions(matrix1)
    dim2 = dimensions(matrix2)

    if dim1[1] != dim2[0]:
        raise ValueError('matrices of such dimensions cant be multiplied')

    new_matrix = create_matrix(dim1[0], dim2[1])
    for i in range(dim1[0]):
        for j in range(dim2[1]):
            for k in range(dim2[0]):
                new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]

    return new_matrix


def square(matrix):
    if not is_matrix(matrix):
        raise ValueError()

    dim = dimensions(matrix)
    if dim[1] == dim[0]:
        return True

    return False
    

def det3(mat):
    positive = mat[0][0]*mat[1][1]*mat[2][2]+mat[0][1]*mat[1][2]*mat[2][0]+ \
    mat[0][2]*mat[1][0]*mat[2][1]
    
    negative = mat[0][2]*mat[1][1]*mat[2][0]+mat[0][1]*mat[1][0]*mat[2][2]+ \
    mat[0][0]*mat[1][2]*mat[2][1]
    
    return positive-negative


def new_reduced(matrix, i, j):

    dim = dimensions(matrix)
    new_matrix = []
    no_riga = []
    for q in range(dim[0]):
        if q != i:
            no_riga.append(matrix[q])
    new_transposed =  transposed(no_riga)
    for k in range(dim[1]):
        if k != j:
            new_matrix.append(new_transposed[k])
    
    return new_matrix 
    

def determinant(matrix):
    if not square:
        raise ValueError
    
    dim = dimensions(matrix)
    if dim[0] == 1:
        return matrix[0][0]
    
    if dim[0] == 2:
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    
    if dim[0] == 3:
        return det3(matrix)
    
    det = 0
    for i in range(dim[1]):
        segno = 1
        if i%2 == 1:
            segno = -1
        det += segno * matrix[0][i] * determinant(new_reduced(matrix, 0, i))
    
    return det


def inverse(matrix):
    if not square:
        raise ValueError
    
    dim = dimensions(matrix)
    det = determinant(matrix)
    if det == 0:
        return None

    new_inverse = create_matrix(dim[0], dim[1])
    trasp = transposed(matrix)
    for i in range(dim[0]):
        for j in range(dim[1]):
            sign = 1
            if (i+j)%2 == 1:
                sign = -1
            new_inverse[i][j] = 1 / det * sign * determinant(new_reduced(trasp, i, j))
    return new_inverse


def rank(matrix):
    if not square(matrix):
        raise ValueError
    n_col = dimensions(matrix)[0]
    if matrix == create_matrix(n_col, n_col):
        return 0
    available_columns = list(range(n_col))
    available_rows = available_columns[:]
    min_rows = []
    min_col = []
    # Trova il primo
    for row in available_rows:
        for col in available_columns:
            if matrix[row][col] != 0:
                min_rows.append(row)
                min_col.append(col)
                break
