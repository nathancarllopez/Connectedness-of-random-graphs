#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 18:18:40 2023

@author: danger
"""

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    Returns: a list of all permutations of sequence
    '''
    #Initialize
    all_permutations = []
    
    # Recursive check
    if len(sequence) == 1:
        all_permutations.append(sequence)
    else:
        first_char = sequence[0]
        smaller_permutations = get_permutations(sequence[1:])
        permutation_length = len(smaller_permutations[0])
        for permutation in smaller_permutations:
            for index in range(permutation_length + 1):
                new_permutation = permutation[:index] + first_char + permutation[index:]
                all_permutations.append(new_permutation)
    
    # Results
    return all_permutations

def transpose(sequence, transposition):
    '''
    Applies the transposition to the sequence

    Parameters
    ----------
    sequence : string
        The sequence to be transposed
    transposition : tuple
        Of the form (index1, index2), indicates that the characters at index1 and index2 of sequence should be swapped

    Returns
    -------
    t_sequence : string
        The transposed sequence

    '''
    char_list = [letter for letter in sequence]
    index1 = transposition[0]
    index2 = transposition[1]
    
    char_list[index1], char_list[index2] = char_list[index2], char_list[index1]
    
    t_sequence = ''
    for char in char_list:
        t_sequence += char
    
    return t_sequence
    

def signature(sequence, permuted_sequence):
    '''
    Counts the number of transpositions needed to get sequence back from permuted_sequence

    Parameters
    ----------
    sequence : string
        The original sequence
    permuted_sequence : string
        The mixed up sequence

    Returns
    -------
    signature : int
        (-1) ^ num_transp

    '''
    n = len(sequence)
    transpositions = []
    
    for index in range(n):
        shouldbe_char = sequence[index]
        actual_char = permuted_sequence[index]
        if actual_char != shouldbe_char:
            actual_index = permuted_sequence.index(shouldbe_char)
            new_transp = (index, actual_index)
            transpositions.append(new_transp)
            permuted_sequence = transpose(permuted_sequence, new_transp)
    
    num_transp = len(transpositions)
    signature = (-1) ** num_transp
        
    return signature
        
        
        
        
        
        
        
        
        
        