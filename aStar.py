# A* pathfinding implementation in Python.
# For Clarkson University course CS547 Computer Algorithm in Fall 2017
# By Dennis Weber & Saleh Shehata

import sys
import json
import networkx as nx # Graph library - see https://networkx.github.io/documentation/stable/tutorial.html

# Step 1: Read input
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
        graph.add_edge(edge['start'], edge['end'])
    startNode = problem['startNode']
    targetNode = problem['targetNode']
    f.close()
