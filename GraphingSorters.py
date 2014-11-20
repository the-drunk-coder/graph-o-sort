# A set of sorting algorithm implementations that will log the sorting
# process in a neat graph. Thus, the main goal is more of an educational
# one, or, in my case, algorithmic composition.

from GraphStructures import *

class QuickSorter():
    # this implementation doesn't really work in-place, but it's not that
    # important for this type of task ...
    def __init__(self, unsorted):
       self.unsorted = unsorted
       self.sorting_graph = Graph()
       self.node_counter = 0
    def quicksort(self, node_to_sort):
        if len(node_to_sort.content) == 0:
            return node_to_sort

        # generate pivot and unsorted lists
        pivot = node_to_sort.content[0]
        left_unsorted = [x for x in node_to_sort.content[1:] if x <= pivot]
        right_unsorted = [x for x in node_to_sort.content[1:] if x > pivot]

        # generate graph
        self.node_counter += 1
        left_unsorted_node = Node(self.node_counter, left_unsorted)
        self.sorting_graph.add_node(left_unsorted_node)
        self.sorting_graph.add_edge(node_to_sort.id, left_unsorted_node.id)

        self.node_counter += 1
        pivot_node = Node(self.node_counter, [pivot])
        self.sorting_graph.add_node(pivot_node)
        self.sorting_graph.add_edge(node_to_sort.id, pivot_node.id)

        self.node_counter += 1
        right_unsorted_node = Node(self.node_counter, right_unsorted)
        self.sorting_graph.add_node(right_unsorted_node)
        self.sorting_graph.add_edge(node_to_sort.id, right_unsorted_node.id)

        # SORTING RECURSION !!!
        left_sorted_node = self.quicksort(left_unsorted_node)
        right_sorted_node = self.quicksort(right_unsorted_node)
        # SORTING RECURSION !!!

        # assemble sorted lists
        result = left_sorted_node.content + [pivot] + right_sorted_node.content

        # complete graph
        self.node_counter += 1
        result_node = Node(self.node_counter, result)
        self.sorting_graph.add_node(result_node)

        self.sorting_graph.add_edge(left_sorted_node.id, result_node.id)
        self.sorting_graph.add_edge(right_sorted_node.id, result_node.id)
        self.sorting_graph.add_edge(pivot_node.id, result_node.id)

        return result_node
    def sort(self):
        # generate initial node
        initial_node = Node(self.node_counter, self.unsorted)
        self.sorting_graph.add_node(initial_node)
        # return the final node's content
        return self.quicksort(initial_node).content

class MergeSorter():
    def __init__(self, unsorted):
       self.unsorted = unsorted
       self.sorting_graph = Graph()
       # count the sorting steps, this will serve as node id
       # the incremental nature of this also allows us to recunstruct the
       # sorting process lateron
       self.step_counter = 0
    def merge(self, left_sorted_node, right_sorted_node):
         result = []
         i = 0
         j = 0
         while(i < len(left_sorted_node.content) and j < len(right_sorted_node.content)):
             if (left_sorted_node.content[i] <= right_sorted_node.content[j]):
                 result.append(left_sorted_node.content[i])
                 i = i + 1
             else:
                 result.append(right_sorted_node.content[j])
                 j = j + 1

         result += left_sorted_node.content[i:]
         result += right_sorted_node.content[j:]

         self.step_counter += 1

         merged_node = Node(self.step_counter, result)

         self.sorting_graph.add_node(merged_node)

         self.sorting_graph.add_edge(left_sorted_node.id, merged_node.id)
         self.sorting_graph.add_edge(right_sorted_node.id, merged_node.id)

         # return list and node id
         return merged_node
    def mergesort(self, current_node):
        if len(current_node.content) < 2:
            return current_node
        else:
            middle = len(current_node.content) // 2

            # add UNsorted nodes to graph, whilst increasing step counters
            self.step_counter += 1
            left_unsorted_node = Node(self.step_counter, current_node.content[:middle])
            self.step_counter += 1
            right_unsorted_node = Node(self.step_counter, current_node.content[middle:])

            self.sorting_graph.add_node(left_unsorted_node)
            self.sorting_graph.add_node(right_unsorted_node)

            #add edges for UNsorted nodes to graph
            self.sorting_graph.add_edge(current_node.id, left_unsorted_node.id)
            self.sorting_graph.add_edge(current_node.id, right_unsorted_node.id)

            # actually sort the lists ...
            left_sorted_node = self.mergesort(left_unsorted_node)
            right_sorted_node = self.mergesort(right_unsorted_node)

            return self.merge(left_sorted_node, right_sorted_node)
    def sort(self):
        # generate initial node
        initial_node = Node(self.step_counter, self.unsorted)
        self.sorting_graph.add_node(initial_node)
        # return the final node's content
        return self.mergesort(initial_node).content
