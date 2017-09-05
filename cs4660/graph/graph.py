"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    file_obj = open(file_path)

    node_count = int(file_obj.readline())
    for i in range(0, node_count):
        graph.add_node(Node(i))

    for line in file_obj:
        split_line = line.split(':')
        graph.add_edge(Edge(Node(int(split_line[0])), Node(int(split_line[1])), int(split_line[2])))

    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        for edge in self.adjacency_list[node_1]:
            if edge.to_node == node_2:
                return True
        for edge in self.adjacency_list[node_2]:
            if edge.to_node == node_1:
                return True
        return False

    def neighbors(self, node):
        return [neighbor_edge.to_node for neighbor_edge in self.adjacency_list[node]]

    def add_node(self, node):
        if node in self.adjacency_list:
            return False
        else:
            self.adjacency_list[node] = []
            return True

    def remove_node(self, node):
        if node in self.adjacency_list:
            del self.adjacency_list[node]
            for from_node, edges in self.adjacency_list.items():
                self.adjacency_list[from_node] = [edge for edge in edges if edge.to_node != node]
            return True
        else:
            return False

    def add_edge(self, edge):
        if edge.from_node not in self.adjacency_list or edge.to_node not in self.adjacency_list:
            return False
        adjacent = self.adjacency_list[edge.from_node]
        if edge in adjacent:
            return False
        else:
            adjacent.append(edge)
            return True

    def remove_edge(self, edge):
        if edge.from_node not in self.adjacency_list or edge.to_node not in self.adjacency_list:
            return False
        adjacent = self.adjacency_list[edge.from_node]
        if edge in adjacent:
            adjacent.remove(edge)
            return True
        else:
            return False

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        if node_1 not in self.nodes or node_2 not in self.nodes:
            return False
        if self.adjacency_matrix[self.__get_node_index(node_1)][self.__get_node_index(node_2)] is None:
            return False
        else:
            return True

    def neighbors(self, node):
        if node not in self.nodes:
            return []
        return [Node(neighbor_number)
                for neighbor_number
                in range(0, len(self.adjacency_matrix[self.__get_node_index(node)]))
                if self.adjacency_matrix[self.__get_node_index(node)][neighbor_number] is not None]

    def add_node(self, node):
        if node in self.nodes:
            return False
        self.nodes.append(node)
        for row in self.adjacency_matrix:
            row.append(None)
        self.adjacency_matrix.append([None] * len(self.nodes))
        return True

    def remove_node(self, node):
        if node not in self.nodes:
            return False
        node_index = self.__get_node_index(node)
        self.nodes.remove(node)
        del self.adjacency_matrix[node_index]
        for row in self.adjacency_matrix:
            del row[node_index]
        return True

    def add_edge(self, edge):
        if edge.from_node not in self.nodes or edge.to_node not in self.nodes:
            return False
        if self.adjacency_matrix[self.__get_node_index(edge.from_node)][self.__get_node_index(edge.to_node)] is None:
            self.adjacency_matrix[self.__get_node_index(edge.from_node)][self.__get_node_index(edge.to_node)] = edge.weight
            return True
        else:
            return False

    def remove_edge(self, edge):
        if edge.from_node not in self.nodes or edge.to_node not in self.nodes:
            return False
        if self.adjacency_matrix[self.__get_node_index(edge.from_node)][self.__get_node_index(edge.to_node)] is None:
            return False
        else:
            self.adjacency_matrix[self.__get_node_index(edge.from_node)][self.__get_node_index(edge.to_node)] = None
            return True

    def __get_node_index(self, node):
        """helper method to find node index"""
        return self.nodes.index(node)

class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        pass

    def neighbors(self, node):
        pass

    def add_node(self, node):
        pass

    def remove_node(self, node):
        pass

    def add_edge(self, edge):
        pass

    def remove_edge(self, edge):
        pass
