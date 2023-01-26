#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:02:14 2023

@author: danger

A graph class

"""

import random

from Digraph import Digraph
from Matrices import SquareMatrix as sm

class Graph(Digraph):
    def __init__(self, vertices):
        '''
        See Digraph DocString for more info
        
        The difference between Graph and Digraph will be that edges in Graph 
        are not directed as they were in Digraph

        '''
        Digraph.__init__(self, vertices)
        
    #######################
    ## Getters & Setters ##
    #######################
    
    def remove_edge(self, v0, v1):
        if (v0, v1) in self.edges:
            self.edges.remove((v0, v1))
            del self.weights[(v0, v1)]
        elif (v1, v0) in self.edges:
            self.edges.remove((v1, v0))
            del self.weights[(v1, v0)]
        else:
            print("Those vertices are not connected.")
            
    def get_edge(self, v0 = None, v1 = None):
        '''
        self.get_edge() returns all the edges of self
        self.get_edge(v) returns all the edges connecting to v
        self.get_edge(v0, v1) returns all the edges connecting v0 to v1

        '''
        if v1 == None:
            if v0 == None:
                return self.edges.copy()
            else:
                neighboring_edges = []
                for edge in self.edges:
                    if v0 in edge:
                        neighboring_edges.append(edge)
                return neighboring_edges
        else:
            if (v0, v1) in self.edges:
                return (v0, v1)
            elif (v1, v0) in self.edges:
                return (v1, v0)
            else:
                print("Those vertices are not connected.")
                
    def change_weight(self, v0, v1, new_weight):
        if (v0, v1) in self.edges:
            self.weights[(v0, v1)] = new_weight
        elif (v1, v0) in self.edges:
            self.weights[(v1, v0)] = new_weight
        else:
            print("Those vertices are not connected.")
            
    def get_weight(self, v0 = None, v1 = None):
        if v1 == None:
            if v0 == None:
                return self.weights.copy()
            else:
                neighboring_edges = self.get_edge(v0)
                v0_weights = {}
                for edge in neighboring_edges:
                    v0_weights[edge] = self.weights[edge]
                if len(v0_weights) > 0:
                    return v0_weights
                else:
                    print(f"There are no edges neighboring {v0}.")
        else:
            if (v0, v1) in self.edges:
                return self.weights[(v0, v1)]
            elif (v1, v0) in self.edges:
                return self.weights[(v1, v0)]
            else:
                print("Those vertices are not connected.")
        
    ####################
    ## Vertex Methods ##
    ####################
    
    def add_vertex(self, v):
        '''
        Returns a new graph object with an additional vertex
        Checks if the 'new' vertex already exists in the original graph
        All edges and their weights from the previous graph are maintained

        '''
        if v in self.vertices:
            print(f"A vertex with label {v} already exists.")
            return self
        else:
            new_vertices = self.vertices.copy() + [v]
            new_graph = Graph(new_vertices)
            new_graph.edges = self.edges
            new_graph.weights = self.weights
            return new_graph
    
    def get_neighbors(self, v):
        neighboring_edges = self.get_edge(v)
        neighbors = []
        try:
            for edge in neighboring_edges:
                if edge[0] == v:
                    new_neighbor = edge[1]
                else:
                    new_neighbor = edge[0]
                if new_neighbor not in neighbors:
                    neighbors.append(new_neighbor)
            return neighbors
        except:
            return neighbors
    
    ###################
    ## Graph Methods ##
    ###################
    
    def spanning_tree(self, root):
        '''
        Builds a rooted spanning tree of (the connected component containing root of) self
        The given vertex is the root of the spanning tree
        
        '''
        
        # Initializing
        tree = Graph([root])
        vertices_added = tree.vertices.copy()
        old_vertices_added = []
        new_vertex_count = len(vertices_added) - len(old_vertices_added)
        
        # Build the spanning tree
        while new_vertex_count > 0:
            old_vertices_added = vertices_added.copy()
            for v in old_vertices_added:
                neighbors = self.get_neighbors(v)
                for w in vertices_added:
                    if w in neighbors:
                        neighbors.remove(w)
                if len(neighbors) > 0:
                    new_vertex = random.choice(neighbors)
                    vertices_added.append(new_vertex)
                    tree = tree.add_vertex(new_vertex)
                    tree.add_edge(v, new_vertex)
            new_vertex_count = len(vertices_added) - len(old_vertices_added)
        return tree
    
    def is_connected(self):
        '''
        A graph is connected if every pair of vertices can be connected by a path
        This method works by building a spanning tree rooted at the first vertex of self
        If the spanning tree contains every vertex of self, then self is connected

        '''
        
        first_vertex = self.vertices[0]
        tree = self.spanning_tree(first_vertex)
        if self.num_vertices == tree.num_vertices:
            return True
        else:
            return False
    
    
    '''
    This method needs to be fixed: currently the same as the digraph method, i.e.,
    returning a non-symmetric matrix
    '''
    def adjacency_matrix(self):
        adj_mat = sm(self.num_vertices) # Square matrix
        v_position = -1
        for v in self.vertices:
            v_position += 1
            v_row = [0 for k in range(self.num_vertices)]
            for w in [vertex for vertex in self.vertices if vertex != v]:
                if (v, w) in self.edges:
                    w_position = self.vertices.index(w)
                    v_row[w_position] = 1
            adj_mat.set_row(v_position, v_row)
        return adj_mat
    
    ########################
    ## Overloaded Methods ##
    ########################
    
    def __str__(self):
        vertices_str = "The vertices of the graph are " + str(self.vertices) + ".\n"
        edges_str = "The edges of the graph are " + str(self.edges) + ".\n"
        # weights_str = "The weights of each edge are " + str(self.weights) + "."
        return vertices_str + edges_str #+ weights_str
    
    
    
    
    
    
    
    
    
    