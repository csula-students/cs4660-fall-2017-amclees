"""
Searches module defines all different search algorithms
"""

import Queue

from graph import graph as g

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    return queue_search(graph, initial_node, dest_node, Queue.Queue())

def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    parents = {}
    dfs_rec(graph, initial_node, {}, parents)

    path = []
    current_node = dest_node
    while current_node != initial_node:
        next_node = parents[current_node]
        path = [g.Edge(next_node, current_node, graph.distance(next_node, current_node))] + path
        current_node = next_node

    return path

def dfs_rec(graph, current, discovered, parents):
    for neighbor in graph.neighbors(current):
        if neighbor in discovered:
            continue
        discovered[neighbor] = True
        parents[neighbor] = current
        dfs_rec(graph, neighbor, discovered, parents)

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    return queue_search(graph, initial_node, dest_node, Queue.PriorityQueue(), True)

def queue_search(graph, initial_node, dest_node, visit_queue, dijkstra=False):
    distances = {}
    parents = {}

    path = []
    path_trace_tile = None

    distances[initial_node] = 0
    visit_queue.put((0, initial_node))

    while not visit_queue.empty():
        entry = visit_queue.get()
        current = entry[1]
        if entry[0] != distances[current]:
            continue

        for adjacent in graph.neighbors(current):
            possible_distance = distances[current] + graph.distance(current, adjacent)
            if adjacent not in distances or (dijkstra and possible_distance < distances[adjacent]):
                distances[adjacent] = possible_distance
                parents[adjacent] = current
                if dest_node == adjacent:
                    path_trace_tile = adjacent
                visit_queue.put((distances[adjacent], adjacent))

    while path_trace_tile in parents:
        path.append(g.Edge(parents[path_trace_tile], path_trace_tile, graph.distance(parents[path_trace_tile], path_trace_tile)))
        path_trace_tile = parents[path_trace_tile]

    return list(reversed(path))

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass
