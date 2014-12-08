# Import graphviz
import sys, os, copy
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
    def __init__(self, node_id, node_content, meta=""):
        self.id = node_id
        self.content = node_content
        # space for arbitrary meta information
        self.meta = meta
        
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
    def render(self, filename, comment, render="content"):
        dot = Digraph(comment=comment,edge_attr={'len': '6', 'weight':'0.00001'})
        dot.engine = 'dot'
        # add nodes to dot graph
        for node_key in self.nodes.keys():
            node_content = "nil"
            # either use id or content to mark graph nodes
            if render == "id":
                    node_content = str(self.nodes[node_key].id)
            elif render == "content":
                if len(self.nodes[node_key].content) > 0:
                    node_content = ', '.join(str(x) for x in self.nodes[node_key].content)
            else:
                node_content = str(self.nodes[node_key].id) + ":"
                if len(self.nodes[node_key].content) > 0:
                    node_content += ', '.join(str(x) for x in self.nodes[node_key].content) + ":"
                else:
                    node_content += "nil:"
                if len(self.nodes[node_key].meta) > 0:
                    node_content += self.nodes[node_key].meta
                else:
                    node_content += "nil"
            dot.node(str(self.nodes[node_key].id), node_content)
        #add edges to dot graph
        for edge_key in self.edges.keys():
            for dest_node in self.edges[edge_key]:
                dot.edge(str(edge_key), str(dest_node))
        if not os.path.exists("graph"):
            os.makedirs("graph")
        dot.render("graph/" + filename + ".gv")

class GraphTool():
    # reverse direction of edges ...
    def reverse_digraph(self, graph):
        reverse_graph = copy.deepcopy(graph)
        for i in range(0, len(graph.nodes)):
            node = graph.nodes[i]
            for dest_node_id in graph.edges[node.id]:
                reverse_graph.add_edge(dest_node_id, node.id)
                reverse_graph.edges[node.id].remove(dest_node_id)
        return reverse_graph
    
class TraversalTool():
    # returns node traversal, breadth first
    def bf_trav(self, graph):
        node_stack = []
        nodes_unvisited = [x for x in range(0,len(graph.nodes) + 1)]
        traversal_list = []
        #remove start node and push to stack
        nodes_unvisited.remove(0)
        node_stack.append(0)
        traversal_list.append(0)
        while len(node_stack) != 0:
            current_node = node_stack.pop()
            for child in graph.edges[current_node]:
                if child in nodes_unvisited:
                    nodes_unvisited.remove(child)
                    node_stack.append(child)
                    traversal_list.append(child)
        return traversal_list
    # return (dfs) topological sorting of the nodes
    def topo_trav(self, graph):
        dfs_tree = DfsTree(graph)
        sorted_tuples = sorted(list(zip(dfs_tree.all_node_ids, dfs_tree.finish_time)), key=lambda time:time[1])
        sorted_node_ids = [tpl[0] for tpl in sorted_tuples]
        return list(reversed(sorted_node_ids))
                           
class DfsTree():
    def __init__(self, graph):
        self.graph = graph
        self.node_stack = []
        self.node_color = []
        self.discovery_time =[]
        self.finish_time = []
        self.predecessor = []
        self.time = 0
        self.all_node_ids = []
        for i in range(0, len(graph.nodes)):
            self.node_color.append('white')
            self.discovery_time.append(0)
            self.finish_time.append(0)
            self.predecessor.append(None)
            self.all_node_ids.append(graph.nodes[i].id)
        self.dfs()
    def dfs(self):
        for i in range(0, len(self.graph.nodes)):
            if self.node_color[self.graph.nodes[i].id] == 'white':
                self.dfs_visit(self.graph.nodes[i])
    def dfs_visit(self, node):
        # actual algorithm ..
        self.node_color[node.id] = 'gray'
        self.time += 1
        self.discovery_time[node.id] = self.time
        # the child nodes are directly stored as integers, so we can use them directly here 
        for succ in self.graph.edges[node.id]:
            if self.node_color[succ] == 'white':
                self.predecessor[succ] = node.id
                self.dfs_visit(self.graph.nodes[succ])
        self.node_color[node.id] = 'black'
        self.time += 1
        self.finish_time[node.id] = self.time
    def print_results(self):
        # generate result lists
        finish = sorted(list(zip(self.all_node_ids, self.finish_time)), key=lambda time:time[1])
        disc = list(zip(self.all_node_ids, self.discovery_time))
        col = list(zip(self.all_node_ids, self.node_color))
        pre = list(zip(self.all_node_ids, self.predecessor))
        # print them
        print("SORTED FINISH TIMES:" + str(finish))
        print("DISCOVERY TIMES:" + str(disc))
        print("COLORS:" + str(col))
        print("PREDECESSORS:" + str(pre))
 
