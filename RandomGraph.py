#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 13:32:26 2023

@author: danger
"""

import random

from Graph import Graph
from math import comb

class RandomGraph(Graph):
    def __init__(self, vertices, num_edges, simple = False):
        '''
        Generates a random graph with num_edges randomly generated edges.
        
        To make the graph simple, uncomment the block in the constructor.

        Parameters
        ----------
        vertices : list
            List of vertices
        num_edges : int
            The number of edges we want to generate

        Attributes
        -------
        No new attributes. See Graph docstring for old attributes

        '''
        assert num_edges <= comb(len(vertices), 2), f"The number of edges cannot be larger than {comb(len(vertices), 2)}"
        
        Graph.__init__(self, vertices)
        
        while len(self.edges) < num_edges:
            v0 = random.choice(self.vertices)
            v1 = random.choice(self.vertices)
            if simple:
                while v0 == v1:
                    v1 = random.choice(self.vertices)
                if (v0, v1) not in self.edges:
                    if (v1, v0) not in self.edges:
                        self.edges.append((v0, v1))
            else:
                self.edges.append((v0, v1))

###########################
## Monte Carlo Functions ##
###########################
                    
def connected_simulation(num_vertices, num_edges, simple = False):
    '''
    Checks if a random graph with the specified number of vertices and edges
    is connected
    
    '''
    
    vertices = [k for k in range(num_vertices)]
    graph = RandomGraph(vertices, num_edges, simple)
    return graph.is_connected()

def montecarlo_count(trials, num_vertices, simple = False):
    '''
    Runs connected_simulation trials number of times
    
    '''
    possible_edge_num = [k for k in range(comb(num_vertices, 2) + 1)]
    count = 0
    
    for trial in range(trials):
        num_edges = random.choice(possible_edge_num)
        if connected_simulation(num_vertices, num_edges, simple):
            count += 1
    
    return count / trials
    
if __name__ == '__main__':
    # vertices = [k for k in range(8)]
    # graph = RandomGraph(vertices, 10)
    # print(graph)
    
    # tree = graph.spanning_tree(0)
    # print(tree)
    
    # print("Connected:", graph.is_connected())
    
    print("Not simple")
    total = 0
    for k in range(10):
        probability = montecarlo_count(10000, 5)
        total += probability
        print(probability)
    print("aggregate:", total / 10)
    
    print("Simple")
    total = 0
    for k in range(10):
        probability = montecarlo_count(10000, 5, True)
        total += probability
        print(probability)
    print("aggregate:", total / 10)
        
    # print("Question: What is the probability that a random graph with n vertices is connected?")