"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

from graph import utils
from graph import graph

import json
import os.path

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

try:
    import Queue as queue
except ImportError:
    import queue

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

cached_states = {}
def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    if room_id in cached_states:
        return cached_states[room_id]
    body = {'id': room_id}
    response = __json_request(GET_STATE_URL, body)
    cached_states[room_id] = response
    return response


cached_transitions = {}
def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    transition_str = room_id + ':' + next_room_id
    if transition_str in cached_transitions:
        return cached_transitions[transition_str]
    body = {'id': room_id, 'action': next_room_id}
    response = __json_request(STATE_TRANSITION_URL, body)
    cached_transitions[transition_str] = response
    return response

def load_caches():
    if not os.path.isfile('./cached_states.json'):
        return
    with open('cached_states.json') as json_str:
        cached_states = json.load(json_str)
    with open('cached_transitions.json') as json_str:
        cached_transitions = json.load(json_str)

def save_caches():
    with open('cached_states.json', 'w') as out:
        json.dump(cached_states, out)
    with open('cached_transitions.json', 'w') as out:
        json.dump(cached_transitions, out, ensure_ascii=False)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = json.load(urlopen(req, jsondataasbytes))
    return response

def pretty_print(json_doc):
    print(json.dumps(json_doc, indent=2, sort_keys=True))

def bfs(initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    return queue_search(initial_node, dest_node, queue.Queue())

def dijkstra_search(initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    return queue_search(initial_node, dest_node, queue.PriorityQueue(), True)

def queue_search(initial_node, dest_node, visit_queue, dijkstra=False):
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

        current_state = get_state(current)
        for neighbor in current_state['neighbors']:
            adjacent = neighbor['id']
            if dijkstra:
                possible_distance = distances[current] + (-1 * transition_state(current, neighbor['id'])['event']['effect'])
            if adjacent not in distances:
                if not dijkstra:
                    possible_distance = distances[current] + (-1 * transition_state(current, neighbor['id'])['event']['effect'])

                distances[adjacent] = possible_distance
                parents[adjacent] = current
                if dest_node == adjacent:
                    path_trace_tile = adjacent
                visit_queue.put((distances[adjacent], adjacent))

    while path_trace_tile in parents:
        distance = transition_state(parents[path_trace_tile], path_trace_tile)['event']['effect']
        path.append(graph.Edge(graph.Node(parents[path_trace_tile]), graph.Node(path_trace_tile), distance))
        path_trace_tile = parents[path_trace_tile]

    return list(reversed(path))

def node_str(node):
    node_name = get_state(node.data)['location']['name']
    return node_name + '(' + node.data + ')'

def print_path(path):
    hp = 0
    for edge in path:
        print(node_str(edge.from_node) + ':' + node_str(edge.to_node) + ':' + str(edge.weight))
        hp += edge.weight
    print('Total hp: ' + str(hp))

if __name__ == "__main__":
    load_caches()
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dark_room = get_state('f1f131f647621a4be7c71292e79613f9')
    print('BFS Path:')
    bfs_path = bfs(empty_room['id'], dark_room['id'])
    print_path(bfs_path)
    print('\nDijkstra Path:')
    dijkstra_path = dijkstra_search(empty_room['id'], dark_room['id'])
    print_path(dijkstra_path)
    save_caches()
