import time
import math
import copy
import random
import sys

no_of_nodes = 12
x = math.inf
# To store the Graph ( source to destination )
Map = {}
# To store the Graph with ( destination to source )
Reverse_Map = {}

# To push empty node back in the priority queue
weight = {'null':math.inf}

# To store the previous nodes for each node in the path
prev = {}

# To store the next node for each node in the path
next = {}

temp = {}

# To store the combined weight of two incomplete paths
final_weight = []

# To easily find the position of the nodes in the priority queue
Map_pq = {}

# I resued a modified version of my Priority queue from previous assignment 
# Modifications are minor
class PQueue():

    def __init__(self):
        self.queue = []

    def empty(self):
        if self.queue == [] or self.queue[0] == 'null':
            self.queue = []
            return True
        else:
            return False


    # Here, Node is child
    def Put_Heapify(self,Node_position):
        flag = True
        while flag == True:
            # Check if it is in Root node
            if Node_position == 0:
                break

            # Finding it's parent
            if Node_position%2 == 0:
                Parent_position = int((Node_position-2)/2)
            else:
                Parent_position = int((Node_position-1)/2)

            # Correcting
            if weight[self.queue[Node_position]] < weight[self.queue[Parent_position]]:
                flag = True
                temp = self.queue[Parent_position]

                # with Mapping
                self.queue[Parent_position] = self.queue[Node_position]
                Map_pq[self.queue[Node_position]] = Parent_position

                self.queue[Node_position] = temp
                Map_pq[temp] = Node_position
                

                Node_position = Parent_position
            else:
                flag = False

    
    # Here, Node is the parent
    def Get_Heapify(self,Node_position):
        # Hepify until correct position
        flag = True
        while flag == True:
            # With two childs
            # Finding the child nodes
            if len(self.queue)-1 >= 2*Node_position+2:
                first_child = 2*Node_position+1
                second_child = 2*Node_position+2
                bigger_child = 0
                # Finding the bigger child
                if weight[self.queue[first_child]] < weight[self.queue[second_child]]:
                    # Correcting
                    bigger_child = first_child
                elif weight[self.queue[second_child]] < weight[self.queue[first_child]]:
                    # Correcting
                    bigger_child = second_child
                # if both child have equal keys
                else:
                   bigger_child = first_child

                # Correcting
                if weight[self.queue[bigger_child]] < weight[self.queue[Node_position]]:
                    flag = True
                    temp = self.queue[Node_position]
                    
                    # with Mapping
                    self.queue[Node_position] = self.queue[bigger_child]
                    Map_pq[self.queue[bigger_child]] = Node_position
                    
                    self.queue[bigger_child] = temp
                    Map_pq[temp] = bigger_child

                    Node_position = bigger_child
                else:
                    flag = False

            # With one child
            elif len(self.queue)-1 >= 2*Node_position+1:
                first_child = 2*Node_position+1
                # Correcting
                if weight[self.queue[first_child]] <= weight[self.queue[Node_position]]:
                    flag = True
                    temp = self.queue[Node_position]
                    
                    # with Mapping
                    self.queue[Node_position] = self.queue[first_child]
                    Map_pq[self.queue[first_child]] = Node_position
                    
                    self.queue[first_child]  =  temp
                    Map_pq[temp] = first_child

                    Node_position = first_child
                else:
                   flag = False

            # checking for leaf node
            elif Node_position >= len(self.queue)-2 or self.queue[Node_position] == 'null':
                flag = False



    def put(self,node, *args):

        # If a node is already in the queue, it just modifies it
        try:
            check_node_position = Map_pq[node]
            if self.queue[check_node_position] == node:
                self.Put_Heapify(check_node_position)
                return
        except:
            pass
     

        Node_position = len(self.queue)
        if Node_position != 0:
            # Finding it's parent to check for empty node
            if Node_position%2 == 0:
                Parent_position = int((Node_position-2)/2)
            else:
                Parent_position = int((Node_position-1)/2)

            # If parent position is 0/empty-node then two empty nodes are added as child
            

            while self.queue[Parent_position] == 'null':
          
                if Node_position%2 == 0:
                    self.queue.append('null')
                    Node_position += 1
                    Parent_position += 1
                else:
                    self.queue.append('null')
                    self.queue.append('null')
                    Node_position += 2
                    Parent_position +=1

            # If Parent position is not empty node, then node is simply added
            self.queue.append(node)            
            # Mapping
            Map_pq[node] = Node_position

            self.Put_Heapify(Node_position)
        else:
            self.queue.append(node)
            # Mapping
            Map_pq[node] = Node_position



    def get(self, *args):
        if self.empty() == False:
            score = self.queue[0]
            self.queue[0] = 'null'

            # Mapping
            del Map_pq[score]
            
            self.Get_Heapify(0)
            return score

pq = PQueue()

sortest_distance = 0

# To store the weights after the dijkstra's algorithm 
directory_of_weights = []
shortest_path = []

# Reading the first line
f = open(sys.argv[1],"r")
cases = f.readline().split()
no_of_nodes = int(cases[0])
no_of_edges = int(cases[1])

def reading(no_of_edges):
    global Map
    global Reverse_Map
    # Storing the edges in an dictionary
    for i in range(no_of_edges):
        edges = f.readline().split()
        try:
            Map[edges[0]].append([edges[1],float(edges[2])])           
        except:
            Map[edges[0]] = []          
            Map[edges[0]].append([edges[1],float(edges[2])])            
            # Map { [source]:[ [destination,weight] , [destination,weight],...] }          
        
        try:
            Reverse_Map[edges[1]].append([edges[0],float(edges[2])])
        except:
            Reverse_Map[edges[1]] = []
            Reverse_Map[edges[1]].append([edges[0],float(edges[2])])
            # Reverse_Map { [destination] : [ [source,weight] , [source,weight]...] }


reading(no_of_edges)
cases = f.readline().split()
source = cases[0]
final_destination = cases[1]
K = int(cases[2])

def initialization(source):
    # Setting the weight of each node to infinity except the source node, which is set to 0
    global Map
    global weight
    global pq
    global prev

    for i in Map:
        if i == source:
            weight[i] = 0
        else:
            weight[i] = math.inf
        prev[i] = 'null'
        # Each node will be added to the priority Queue
        pq.put(i)


def dijkstra(destination):
    global Map
    global pq
    global weight
    global prev

    # Getting the nodes from priority queue
    while(pq.empty()==False):
        node = pq.get()
        for destination_node in Map[node]:

            # Updating the weight of the nodes if the new weight is less than the previous weight
            if weight[node] + destination_node[1] < weight[destination_node[0]]:
                weight[destination_node[0]] = weight[node] + destination_node[1]
                # updating the previos node of the current node to track the path
                prev[destination_node[0]] = node
                pq.put(destination_node[0])
    
    
    temp = copy.deepcopy(weight)
    # storing the weight in a list
    directory_of_weights.append(temp)

def Reverse_dijkstra(source):
    global Reverse_Map
    global pq
    global weight
    global next

    # Getting the nodes from priority queue
    while(pq.empty()==False):
        node = pq.get()
        for source_node in Reverse_Map[node]:

            # Updating the weight of the nodes if the new weight is less than the previous weight
            if weight[node] + source_node[1] < weight[source_node[0]]:
                weight[source_node[0]] = weight[node] + source_node[1]    
                # updating the next node of the current node to track the path
                next[source_node[0]] = node
                pq.put(source_node[0])
    
    
    temp = copy.deepcopy(weight)
    # storing the weight in a list
    directory_of_weights.append(temp)


# Quick sort 
def sort(weight):
    less = []
    equal = []
    more = []

    if len(weight) > 1:
        pivot = weight[random.randint(0,len(weight)-1)]
        # rearranging the Weights relative to pivot
        for i in weight:
            if i < pivot:
                less.append(i)
            elif i == pivot:
                equal.append(i)
            elif i > pivot:
                more.append(i)
        # returns sorted list each time by recursion 
        return sort(less)+equal+sort(more) 
    else:  
        return weight

# initial run from source to destination
initialization(source)
dijkstra(final_destination)

# Stores K Shortest paths
final_array = []

# Storing the shortest path of the algorithm
node = final_destination
while(node != source):
    shortest_path.append(node)
    node = prev[node]
shortest_path.append(node)
prev.clear()

# Second run from destination to source
initialization(final_destination)
dijkstra(source)

# After the second run, we add two incomplete paths to create a all possible paths's distance
for i in directory_of_weights[0]:
    final_weight.append(directory_of_weights[0][i] + directory_of_weights[1][i])


sorted_array = []
sorted_array = sort(final_weight)

for i in range(len(sorted_array)-1):
    if (sorted_array[i+1]-sorted_array[i])>0.000000001:
        final_array.append(sorted_array[i])

print()
# Top K sortest path
for i in range(K):
    print("K = ",i+1," ",final_array[i])

print("time taken is : ", time.process_time())



