import random
import networkx as nx
import matplotlib.pyplot as plt
import sys

def generate_graph(n, min_edges=random.choice([3, 4, 5, 6])):
    """
    Function to generate a random graph with 'n' nodes and at least 'min_edges' edges per node.
    """
    graph = [[False] * n for _ in range(n)]  # Initialize an empty adjacency matrix
    indices = [i for i in range(n)]  # List of node indices
    for i in range(n):
        check = 0
        # Count the number of existing edges for node i
        for j in range(n):
            if graph[i][j]:
                check += 1
        # Skip the node if it already has at least 'min_edges' edges
        if check >= min_edges:
            continue
        # Calculate the number of edges needed to meet the minimum requirement
        k = min_edges - check
        copy = indices.copy()  # Make a copy of node indices
        if i in copy:
            copy.remove(i)  # Remove the current node from the list of available nodes
        # Randomly select nodes to connect with node i until the minimum edge requirement is met
        while k != 0 and copy:
            choice = random.choice(
                copy
            )  # Randomly choose a node to connect with node i
            if not graph[i][choice]:
                graph[i][choice] = True  # Connect node i with the chosen node
                graph[choice][i] = True  # Make the connection bidirectional
                k -= 1  # Decrement the number of edges needed
            copy.remove(
                choice
            )  # Remove the chosen node from the list of available nodes
        # Remove nodes from the list of available nodes if they already have 'min_edges' edges
        for g in indices:
            c = 0
            for j in range(n):
                if graph[g][j]:
                    c += 1
            if c >= min_edges:
                if g in indices:
                    indices.remove(g)
    return graph


def visualize_graph(graph):
    """
    Function to visualize a graph using NetworkX and Matplotlib.
    """
    G = nx.Graph()
    # Add edges to the graph based on the adjacency matrix
    for i, row in enumerate(graph):
        for j, connected in enumerate(row):
            if connected:
                G.add_edge(i, j)
    # Draw the graph with node labels
    nx.draw(G, with_labels=True)
    plt.show()


def is_connected(graph):
    """
    Function to check if a graph is connected using Depth-First Search (DFS).
    """

    def dfs(node):
        visited[node] = True
        # Traverse all neighbors of the current node
        for neighbor in range(len(graph)):
            if graph[node][neighbor] and not visited[neighbor]:
                dfs(
                    neighbor
                )  # Recursively explore the neighbor if it has not been visited

    visited = [False] * len(graph)  # Initialize visited array
    dfs(0)  # Start DFS from node 0
    # Check if all nodes were visited
    return all(visited)


def generate_connected_graph(n):
    """
    Function to generate a connected graph with 'n' nodes.
    """
    while True:
        graph = generate_graph(n)  # Generate a random graph
        if is_connected(graph):  # Check if the graph is connected
            return graph  # Return the connected graph


# Call the functions
if sys.argv[1] == "--generate":
    graph = generate_graph(10)  # Generate a random graph with 10 nodes
    visualize_graph(graph)  # Visualize the graph
