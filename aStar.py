# A* pathfinding implementation in Python.
# For Clarkson University course CS547 Computer Algorithm in Fall 2017
# By Dennis Weber & Saleh Shehata

# Call the program like this:
# >> python aStar.py inputfile
# Parameters::
# inputfile (optional): The json file to read the problem from. Defaults to 'exampleProblem.json'

import sys # For using program parameters
import math # For math operations (square root)
import json # For json parsing
import networkx as nx # Graph library - see https://networkx.github.io/documentation/stable/tutorial.html

# Helper functions:
def calcHeuristic(fromNode, toNode):
    # We assume that the cost for each edge is lower-limited by the distance between the nodes.
    # E.g. If node A is at (5|5) and node B is at (6|7), the x distance is 6-5 = 1 and the y distance is 7-5 = 2.
    # Therefore the total distance is sqrt(1^2 + 2^2) = 2.236...
    diffX = abs(graph.nodes[fromNode]['x'] - graph.nodes[toNode]['x'])
    diffY = abs(graph.nodes[fromNode]['y'] - graph.nodes[toNode]['y'])
    diffTotal = math.sqrt(diffX**2 + diffY**2)
    return diffTotal

# Step 1: Read input into graph
if (len(sys.argv) > 1) and (sys.argv[1] != ""):
    inputfile = sys.argv[1]
else:
    inputfile = "exampleProblem.json"
graph = nx.DiGraph()
startNode = ''
targetNode = ''
with open(inputfile) as f:
    problem = json.loads(f.read())
    for node in problem['nodes']:
        graph.add_node(node['id'], x=node['X'], y=node['Y'])
    for edge in problem['edges']:
        graph.add_edge(edge['start'], edge['end'], cost=edge['cost'])
    startNode = problem['startNode']
    targetNode = problem['targetNode']
    f.close()

# Step 2: Perform A* on graphs
checkedNodes = set()
toCheckNodes = set(startNode) # Begin with the start node
graph.nodes[startNode]['costToReach'] = 0 # cost to reach start Node is 0.
graph.nodes[startNode]['heuristic'] = calcHeuristic(startNode, targetNode)
print('Starting at >'+ str(startNode) + '<')

while len(toCheckNodes) > 0: # As long as there are nodes which could lead to the target....
    # find the node with the smallest fScore (current cost + heuristic)
    bestNode = ''
    bestNodeScore = float("inf")
    for toCheckNode in toCheckNodes:
        score = graph.nodes[toCheckNode]['costToReach'] + graph.nodes[toCheckNode]['heuristic']
        if score < bestNodeScore:
            bestNode = toCheckNode
            bestNodeScore = score

    if bestNode == targetNode:
        # We arrived at the target node!
        print('=============')
        print('Found path!')
        currNode = targetNode
        path = [currNode] # We reconstruct the path backwards by following the predecessors
        while 'predecessor' in graph.nodes[currNode]:
            predecessor = graph.nodes[currNode]['predecessor']
            path.append(predecessor)
            currNode = predecessor
        path.reverse()
        print(path)
        sys.exit()

    for neighbor in list(graph.neighbors(bestNode)):
        if neighbor in checkedNodes:
            continue # We already came across this node from a better path. So we're not interested.
        if neighbor not in toCheckNodes:
            toCheckNodes.add(neighbor) # We should  check the paths going through here!
        print('New neighbor: >' + str(neighbor) + '<')
        costToGetToNeighbor = graph.nodes[bestNode]['costToReach'] + graph.edges[bestNode, neighbor]['cost']
        if 'costToReach' not in  graph.nodes[neighbor] or costToGetToNeighbor < graph.nodes[neighbor]['costToReach']:
            print('  With a better path!')
            graph.nodes[neighbor]['predecessor'] = bestNode
            graph.nodes[neighbor]['costToReach'] = costToGetToNeighbor
            graph.nodes[neighbor]['heuristic'] = calcHeuristic(neighbor, targetNode)
        else:
            print('  But the current path is already better')

    toCheckNodes.remove(bestNode) # Node has been checked!
    checkedNodes.add(bestNode) # Node has been checked!

# No more possible nodes to lead to the target!
# I.e. there is no way to reach the target.
print('There is no route to the target.')
