#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:02:14 2023

@author: danger

A digraph class

"""

import random

from Matrices import SquareMatrix as sm

class Digraph():
    def __init__(self, vertices):
        '''
        A digraph is created by first specifying a list of vertices.
        Edges are added manually by specifying a starting and ending vertex

        Parameters
        ----------
        vertices : list
            The vertices of the digraph

        Attributes
        ----------
        self.vertices : list
            The same list as vertices
        self.num_vertices : int
            len(self.vertices)
        self.edges : list
            Initially empty list, will contain tuples of vertices
        self.weights : dictionary
            The edges in the graph are the keys of self.weights
            The value of self.weights[edge] will be a float assigned to edge
            Default value of weights is 1

        '''
        
        self.vertices = vertices
        self.num_vertices = len(vertices)
        self.edges = []
        self.weights = {}
        
        
    #######################
    ## Getters & Setters ##
    #######################
        
    def add_edge(self, v0, v1):
        '''
        Edges in digraphs are directed, i.e., this edge starts at v0 and ends at v1
        When an edge is added, a default weight of 1 is added to self.weights
        
        '''
        
        self.edges.append((v0, v1))
        self.weights[(v0, v1)] = 1
        
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
                departing_edges = []
                for edge in self.edges:
                    if edge[0] == v0:
                        departing_edges.append(edge)
                return departing_edges
        else:
            if (v0, v1) in self.edges:
                return (v0, v1)
            else:
                print("Those vertices are not connected.")
                
    def change_weight(self, v0, v1, new_weight):
        if (v0, v1) in self.edges:
            self.weights[(v0, v1)] = new_weight
        else:
            print("Those vertices are not connected.")
    
    def get_weight(self, v0 = None, v1 = None):
        if v1 == None:
            if v0 == None:
                return self.weights.copy()
            else:
                departing_edges = self.get_edge(v0)
                v0_weights = {}
                for edge in departing_edges:
                    v0_weights[edge] = self.weights[edge]
                if len(v0_weights) > 0:
                    return v0_weights
                else:
                    print(f"There are no edges leaving {v0}.")
        else:
            if (v0, v1) in self.edges:
                return self.weights[(v0, v1)]
            else:
                print("Those vertices are not connected.")
    
    ######################        
    ### Vertex methods ###
    ######################
    
    def add_vertex(self, v):
        '''
        Returns a new digraph object with an additional vertex
        Checks if the 'new' vertex already exists in the original digraph
        All edges and their weights of the previous graph are maintained

        '''
        if v in self.vertices:
            print("A vertex with that label already exists.")
        else:
            new_vertices = self.vertices.copy() + [v]
            new_graph = Digraph(new_vertices)
            new_graph.edges = self.edges
            new_graph.weights = self.weights
            return new_graph
    
    def get_neighbors(self, v):
        departing_edges = self.get_edge(v)
        neighbors = [edge[1] for edge in departing_edges]
        return neighbors
    
    def get_valence(self, v):
        return len(self.get_neighbors(v))
    
    def is_neighbor(self, v0, v1):
        v0_neighbors = self.get_neighbors(v0)
        if v1 in v0_neighbors:
            return True
        else:
            return False
    
    def find_path(self, v0, v1):
        # Finds a path (sequence of edges) starting at v0 and ending at v1
        
        # Pseudocode #
        # Find all the neighbors [n0, n1,...,nN] of v0
        # If v1 is a neighbor, return the edge (v0, v1)
        # Otherwise, find all the neighbors of each neighbor of v0
        # ... think about how to handle already visited vertices and stop condition
        pass
    
    ####################
    ### Edge Methods ###
    ####################

    def remove_edge(self, v0, v1):
        if (v0, v1) in self.edges:
            self.edges.remove((v0, v1))
            del self.weights[(v0, v1)]
        else:
            print("Those vertices are not connected.")    
    
    #####################
    ### Graph methods ###
    #####################
    
    def make_subgraph(self, sub_vertices):
        # Creates a new graph object with the specified vertices
        # All possible edges from the super graph are included in the subgraph
        subgraph = Digraph(sub_vertices)
        for edge in self.edges:
            if edge[0] in sub_vertices and edge[1] in sub_vertices:
                subgraph.edges.append(edge)
                subgraph.weights[edge] = self.weights[edge]
        return subgraph
    
    def spanning_tree(self, root):
        '''
        Builds a rooted spanning tree of (the connected component containing root of) self
        The given vertex is the root of the spanning tree
        
        '''
        
        # Initializing
        tree = Digraph([root])
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
    
    ### Overloaded methods ###
    
    def __str__(self):
        vertices_str = "The vertices of the graph are " + str(self.vertices) + ".\n"
        edges_str = "The edges of the graph are " + str(self.edges) + ".\n"
        weights_str = "The weights of each edge are " + str(self.weights) + "."
        return vertices_str + edges_str + weights_str
        
    
    
    
    