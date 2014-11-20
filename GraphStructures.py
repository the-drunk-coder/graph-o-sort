# Import graphviz
import sys, os
sys.path.append('..')
sys.path.append('/usr/lib/graphviz/python/')
sys.path.append('/usr/lib64/graphviz/python/')
import graphviz

from graphviz import Digraph

class GraphError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class Node():
    def __init__(self, node_id, node_content):
        self.id = node_id
        self.content = node_content

class Graph():
    def __init__(self):
        self.nodes = {}
        self.edges = {}
    def add_node(self, node):
        self.nodes[node.id] = node
        self.edges[node.id] = []
    def add_edge(self, source_node_id, destination_node_id):
        if(source_node_id not in self.nodes or destination_node_id not in self.nodes):
            raise GraphError("nodes for this edge not present")
        else:
            self.edges[source_node_id].append(destination_node_id)
    def render(self, filename, comment):
        dot = Digraph(comment=comment,edge_attr={'len': '6', 'weight':'0.001'})
        dot.engine = 'dot'
        # add nodes to dot graph
        for node_key in self.nodes.keys():
            node_content = "nil"
            if len(self.nodes[node_key].content) > 0:
                node_content = ', '.join(str(x) for x in self.nodes[node_key].content)
            dot.node(str(self.nodes[node_key].id), node_content)
        #add edges to dot graph
        for edge_key in self.edges.keys():
            for dest_node in self.edges[edge_key]:
                dot.edge(str(edge_key), str(dest_node))

        if not os.path.exists("graph"):
            os.makedirs("graph")

        dot.render("graph/" + filename + ".gv")
