"""
utils package is for some quick utility methods

such as parsing
"""

import graph as g

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.symbol)

def block_at_position(lines, x, y):
    if y >= len(lines) - 1 or x >= len(lines[0]) - 1 or x <= 1 or y <= 1:
        return '--'
    return lines[y][x] + lines[y][x + 1]

def edges_at_position(lines, x, y, tag):
    positions = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
    edges = []
    for position in positions:
        block = block_at_position(lines, position[0], position[1])
        if block == '--':
            continue
        edges.append(g.Edge(g.Node(Tile(x, y, tag)), g.Node(Tile(position[0], position[1], block)), 1))
    return edges

def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph

    Returns graph object
    """
    file_obj = open(file_path)
    lines = []
    for line in file_obj:
        lines.append(line)

    tiles = []
    edges = []
    y = 0
    for line in lines:
        if line[0] == '+':
            continue
        x = 1
        while x < len(line):
            block = line[x] + line[x + 1]
            if block == '  ' or block[0] == '@':
                tiles.append(g.Node(Tile(x, y, block)))
                edges += edges_at_position(lines, x, y, block)
            x += 2
        y += 1

    for tile in tiles:
        graph.add_node(tile)
    for edge in edges:
        graph.add_edge(edge)

    return graph

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """
    if not edges:
        return ''

    actions = []
    for edge in edges:
        if edge.from_node.x > edge.to_node.x:
            actions.append('S')
        elif edge.from_node.x < edge.to_node.x:
            actions.append('N')
        elif edge.from_node.y > edge.to_node.y:
            actions.append('E')
        else:
            actions.append('W')

    return ''.join(actions)

