#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 11:48:19 2023

@author: danger
"""

# import math
import random
from Signatures import get_permutations
from Signatures import signature

def symmetric_group(n):
    '''
    Set of permutations of the integers 0,1,...,n-1

    Parameters
    ----------
    n : integer
        The number of elements to permute

    Returns
    -------
    permutations : list
        All the permutations of the integers 0,1,...,n-1

    '''
    numbers = [k for k in range(n)]
    numbers_string = ''
    for num in numbers:
        numbers_string += str(num)
        
    return get_permutations(numbers_string)
    

class Matrix(object):
    def __init__(self, num_rows, num_cols):
        '''
        A matrix will be a collection of rows, each of length num_cols

        Parameters
        ----------
        num_rows : positive integer
            The number of rows of the matrix. Also the dimension of the columns
        num_cols : positive integer
            The number of columns of the matrix. Also the dimension of the rows.
            
        Attributes
        ----------
        self.rows : list
            A list of rows, each row also a list, filled with floats. Initialized as filled with zeros
        self.num_rows : positive integer
            The number of rows of the matrix. Also the dimension of the columns
        self.num_cols : positive integer
            The number of columns of the matrix. Also the dimension of the rows.

        '''
        assert (type(num_rows) == int) and (num_rows > 0), 'First parameter needs to be a positive integer'
        assert (type(num_cols) == int) and (num_cols > 0), 'Second parameter needs to be a positive integer'
        
        self.rows = []
        for index in range(num_rows):
            new_row = [0 for k in range(num_cols)]
            self.rows.append(new_row)
            
        self.num_rows = num_rows
        self.num_cols = num_cols
        
    def set_row(self, index, new_row):
        try:
            self.rows[index] = new_row
        except:
            print("Index cannot be bigger than", self.num_rows)
            
    def get_row(self, index = -1):
        if index == -1:
            return self.rows.copy()
        else:
            try:
                return self.rows[index].copy()
            except:
                print("Index cannot be bigger than", self.num_rows)
                
    def set_entry(self, row_index, col_index, value):
        try:
            self.rows[row_index][col_index] = value
        except:
            print("Given parameters not within matrix size.")
                
    def get_entry(self, row_index, col_index):
        try:
            return self.rows[row_index][col_index]
        except:
            print("Given parameters not within matrix size.")
            
    def duplicate_matrix_shape(self):
        duplicate = Matrix(self.num_rows, self.num_cols)
        return duplicate
        
    def __str__(self):
        printed = ''
        for row in self.rows:
            for comp in row:
                printed += ' ' + str(comp)
            printed += ' \n'
        return printed
    
    def __add__(self, other):
        assert self.num_rows == other.num_rows, 'Two matrices need to have the same number of rows to be added/subtracted.'
        assert self.num_cols == other.num_cols, 'Two matrices need to have the same number of columns to be added/subtracted.'
        
        s = self.duplicate_matrix_shape()
        m = self.num_rows
        n = self.num_cols
        
        for row_num in range(m):
            for col_num in range(n):
                s.rows[row_num][col_num] = self.rows[row_num][col_num] + other.rows[row_num][col_num]
        
        return s
        
    def transpose(self):
        m = self.num_rows
        n = self.num_cols
        
        if m == n:
            t = self.duplicate_matrix_shape()
        else:
            t = Matrix(n, m)
        
        for row_num in range(m):
            for col_num in range(n):
                t.rows[row_num][col_num] = self.rows[col_num][row_num]
        
        return t
    
    def scale(self, factor):
        sc = self.duplicate_matrix_shape()
        m = sc.num_rows
        n = sc.num_cols
        
        for row_num in range(m):
            for col_num in range(n):
                sc.rows[row_num][col_num] = factor * self.rows[row_num][col_num]
        
        return sc
    
    def __sub__(self, other):
        neg_other = other.scale(-1)
        return self + neg_other
    
    def __eq__(self, other):
        if self.num_rows != other.num_rows:
            if self.num_cols != other.num_cols:
                return False
            
        m = self.num_rows
        n = self.num_cols
        for row_num in range(m):
            for col_num in range(n):
                if self.rows[row_num][col_num] != other.rows[row_num][col_num]:
                    return False
                
        return True
    
    def get_col(self, index = -1):
        # Access the rows of the transpose
        # Index controls which column you access, index == 0 returns all columns
        
        # Initialize
        transpose = self.transpose()
        columns = transpose.rows.copy()
        
        # Evaluate index
        if index == -1:
            return columns
        else:
            try:
                return columns[index]
            except:
                print("Index cannot be bigger than", self.num_cols)
    
    def __mul__(self, other):
        # Checks that self and other have compatible sizes
        # Uses _inner_product to calculate new matrix entries
        m = self.num_rows
        n = self.num_cols
        p = other.num_rows
        q = other.num_cols   
        
        assert n == p, 'Cannot multiply matrices with these sizes.'
        
        product = Matrix(m,q)
        # print(product)
        for row_num in range(m):
            for col_num in range(q):
                row_vals = self.rows[row_num].copy()
                col_vals = other.get_col(col_num)
                # print(row_vals, type(row_vals), col_vals, type(col_vals))
                # print()
                inner_product = 0
                for position in range(n):
                    inner_product += row_vals[position] * col_vals[position]
                product.rows[row_num][col_num] = inner_product
                
        return product     
        
    def randomize_matrix(self):
        # Returns a matrix the same size as self but with random entries
        # Randomness here means chosen uniformly from (-5,5) and rounded to two decimal places
        random_self = self.duplicate_matrix_shape()
        m = self.num_rows
        n = self.num_cols
        
        for row_num in range(m):
            for col_num in range(n):
                random_self.rows[row_num][col_num] = round(random.uniform(-5, 5),2)
                
        return random_self
    
    def get_minor(self, row_rem, col_rem):
        m = self.num_rows
        n = self.num_cols
        minor = Matrix(m - 1, n - 1)
        
        for row_num in range(row_rem):
            for col_num in range(col_rem):
                minor.rows[row_num][col_num] = self.rows[row_num][col_num]
            for col_num in range(col_rem, minor.num_cols):
                minor.rows[row_num][col_num] = self.rows[row_num][col_num + 1]
        for row_num in range(row_rem, minor.num_rows):
            for col_num in range(col_rem):
                minor.rows[row_num][col_num] = self.rows[row_num + 1][col_num]
            for col_num in range(col_rem, minor.num_cols):
                minor.rows[row_num][col_num] = self.rows[row_num + 1][col_num + 1]
                
        return minor
    
def identity(size):
    '''
    Returns the identity matrix of size n

    Parameters
    ----------
    n : Positive integer
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    i = Matrix(size, size)
    for index in range(size):
        new_row = [0 for k in range(index)] + [1] + [0 for k in range(index + 1, size)]
        i.set_row(index, new_row)
    return i

class SquareMatrix(Matrix):
    def __init__(self, size):
        '''
        A matrix with the same number of rows and columns

        Parameters
        ----------
        size : positive integer
            The number of rows/columns the matrix has

        Attributes
        ----------
        self.rows
        self.size

        '''
        Matrix.__init__(self, size, size)
        self.size = size
        
    def duplicate_matrix_shape(self):
        duplicate = SquareMatrix(self.size)
        return duplicate
    
    def __mul__(self, other):
        # Checks that self and other have compatible sizes
        # Uses _inner_product to calculate new matrix entries
        assert self.size == other.size, 'Cannot multiply matrices with these sizes'
        
        n = self.size
        product = self.duplicate_matrix_shape()
        
        for row_num in range(n):
            for col_num in range(n):
                row_vals = self.get_row(row_num)
                col_vals = other.get_col(col_num)
                inner_product = 0
                for position in range(n):
                    inner_product += row_vals[position] * col_vals[position]
                product.rows[row_num][col_num] = inner_product
        return product
    
    def __pow__(self, power):
        identity = SquareMatrix(self.size)
        for index in range(identity.size):
            new_row = [0 for k in range(index)] + [1] + [0 for k in range(index + 1, identity.size)]
            identity.set_row(index, new_row)
            
        for k in range(power):
            identity *= self
            
        return identity
    
    def get_minor(self, row_rem, col_rem):
        minor = SquareMatrix(self.size - 1)
        n = minor.size
        
        for row_num in range(row_rem):
            for col_num in range(col_rem):
                minor.rows[row_num][col_num] = self.rows[row_num][col_num]
            for col_num in range(col_rem, n):
                minor.rows[row_num][col_num] = self.rows[row_num][col_num + 1]
        for row_num in range(row_rem, n):
            for col_num in range(col_rem):
                minor.rows[row_num][col_num] = self.rows[row_num + 1][col_num]
            for col_num in range(col_rem, n):
                minor.rows[row_num][col_num] = self.rows[row_num + 1][col_num + 1]
        
        return minor
    
    #################################################################
    ### The following methods all relate to row reducing a matrix ###
    #################################################################   
    
    '''
    Assume all matrices have non-zero entries
    '''
    
    def find_starting_row(self):
        # If there is a row with a non-zero first entry, move that row to the top of the list
        # If not, return 'None'
        pass
    
    def normalize_row(self, row_num):
        # Find the first non-zero entry in the row with value v, and multiply the whole row by 1/v
        pass
    
    def lin_comb_rows(self, row_num1, factor, row_num2):
        # Changes row_num2 to row_num2 + factor * row_num1
        pass
    
    def upper_triangular(self):
        # Returns an upper triangular version of self through row reduction
        pass
    
    def row_reduce(self):
        # Runs upper_triangular on self, transposes the result, and then runs upper_triangular again
        pass
    
    #################################################################
    #################################################################
    
    def product_diagonals(self):
        product = 1
        for index in range(self.size):
            product *= self.rows[index][index]
            
        return product
    
    def determinant(self):
        n = self.size
        permutations = symmetric_group(n)
        det = 0
        
        unmixed = permutations[0]
        for perm in permutations:
            next_term = 1
            for index in range(n):
                next_term *= self.rows[index][int(perm[index])]
            det += signature(unmixed, perm) * next_term
            
        return det
    
    def adjugate(self):
        n = self.size
        adjugate = self.duplicate_matrix_shape()
        
        for row_num in range(n):
            for col_num in range(n):
                minor = self.get_minor(row_num, col_num)
                cofactor = (-1) ** (row_num + col_num) * minor.determinant()
                adjugate.rows[row_num][col_num] = cofactor
                
        return adjugate.transpose()
    
    def inverse(self):
        try:
            return self.adjugate().scale(1 / self.determinant())
        except ZeroDivisionError:
            print('This matrix is not invertible.') 
                
class Vector(Matrix):
    def __init__(self, length):
        '''
        A vector will be a 1 x length matrix, i.e., a column vector

        Parameters
        ----------
        length : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        Matrix.__init__(self, length, 1)
        self.length = length
        
    def set_vect(self, entries):
        assert len(entries) == self.length, 'List of entries needs to be the same length as vector.'
         
        for index in range(len(entries)):
            self.rows[index] = [entries[index]]
            
    def is_perp(self, other):
        assert self.length == other.length, 'Vectors need to be the same size'
        
        inner_product = self.transpose() * other
        value = inner_product.rows[0][0]
        
        if value == 0:
            return True
        else:
            return False
        
class IdentityMatrix(SquareMatrix):
    def __init__(self, size):
        '''
        Subclass used to product identity matrices of any size

        '''
        SquareMatrix.__init__(self, size)
        for index in range(size):
            self.rows[index][index] = 1

if __name__ == '__main__':
    A = SquareMatrix(3)
    A.set_row(0, [1,2,3])
    A.set_row(1, [0,4,5])
    A.set_row(2, [0,0,6])
    print('A =')
    print(A)
    
    print(A.determinant())
    
    I = IdentityMatrix(3)
    print(I.determinant())
    
    B = SquareMatrix(3)
    for row_num in range(3):
        B.set_row(row_num, [random.randint(-5, 5) for k in range(3)])
    print(B)
    print(B.determinant())
    
    Binv = B.inverse()
    print(Binv)
    
    print(B*Binv)
    
    C = Matrix(2,3)
    C.set_row(0, [1,1,1])
            
            
            
            
            
            
            