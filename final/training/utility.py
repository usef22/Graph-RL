import xml.etree.ElementTree as ET
import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from icecream import ic
from config import *
import os

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory created at {directory_path}")
    else:
        print(f"Directory already exists at {directory_path}")

def graph_to_matrix(file_path, number_of_total_nodes):
    """
    Convert a GraphML file to an adjacency matrix and obtain node indices with x, y coordinates.

    Parameters:
    - file_path (str): Path to the GraphML file.
    - number_of_total_nodes (int): Total number of nodes in the graph.

    Returns:
    - adjacency_matrix (numpy.ndarray): Adjacency matrix representation of the graph.
    - node_indices_with_x_y (dict): Dictionary containing node indices and corresponding x, y coordinates.
    - num_nodes (int): Total number of nodes in the graph.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Read graph from the graphml file
    graph = nx.DiGraph()
    
    # Parse nodes and their x, y coordinates
    for node in root.findall('.//{http://graphml.graphdrawing.org/xmlns}node'):
        node_id = node.get('id')
        
        # Find 'x' and 'y' data elements
        x_element = node.find('.//{http://graphml.graphdrawing.org/xmlns}data[@key="d4"]')
        y_element = node.find('.//{http://graphml.graphdrawing.org/xmlns}data[@key="d3"]')

        # Check if the elements exist and have text content
        if x_element is not None and x_element.text is not None and y_element is not None and y_element.text is not None:
            x = float(x_element.text)
            y = float(y_element.text)
            graph.add_node(node_id, pos=(x, y))

    # Parse edges and their weights
    for edge in root.findall('.//{http://graphml.graphdrawing.org/xmlns}edge'): 
        source = edge.get('source')
        target = edge.get('target')
        weight = edge.find('.//{http://graphml.graphdrawing.org/xmlns}data[@key="d9"]')

        if weight is not None and weight.text is not None:
            weight = float(weight.text)
            graph.add_edge(source, target, weight=weight)

    # Create a dictionary to map node indices to their x, y coordinates
    node_indices = {node: index for index, node in enumerate(graph.nodes)}
    node_indices_with_x_y = {}
    
    for index, node in enumerate(graph.nodes):
        node_split_list = node.split(".")
        node_latitude = node_split_list[0] + "." + node_split_list[1][:4]
        node_longitude = node_split_list[1][4:] + "." + node_split_list[2]
        
        node_indices_with_x_y[node] = {"index": index, "x": node_latitude, "y": node_longitude}
        
    num_nodes = len(graph.nodes)
    ic(num_nodes)
    
    # Initialize an adjacency matrix with zeros
    adjacency_matrix = np.zeros((number_of_total_nodes+1, number_of_total_nodes+1))

    # Fill the adjacency matrix with edge weights
    for edge in graph.edges(data=True):
        try:
            source, target, data = edge
            weight = data['weight']
            
            source_index = node_indices[source]
            target_index = node_indices[target]
            
            adjacency_matrix[source_index][target_index] = float(weight)
        except:
            pass

    print(adjacency_matrix)
    return adjacency_matrix, node_indices_with_x_y, num_nodes

def calculate_total_number_of_nodes(file_path):
    # Set XML namespace for GraphML
    namespace = "{http://graphml.graphdrawing.org/xmlns}"
    
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find all the node elements using the defined namespace
    nodes = root.findall(f".//{namespace}node")
    
    # Get the total number of nodes
    total_nodes = len(nodes)
    
    # Print and return the result
    print(f"Total number of nodes: {total_nodes}")
    return total_nodes

def calculate_cost(path, adjacency_matrix):
    """
    Calculate the total cost of a given path in a graph represented by an adjacency matrix.

    Parameters:
    - path (list): List of node indices representing the path.
    - adjacency_matrix (numpy.ndarray): Adjacency matrix representing the graph.

    Returns:
    - cost (float): Total cost of the path based on the weights in the adjacency matrix.
    """
    cost = sum(adjacency_matrix[path[i], path[i + 1]] for i in range(len(path) - 1))
    return cost

def cal_distance(path, D):
    """
    Calculate the total distance of a given path in a graph represented by a distance matrix.

    Parameters:
    - path (list): List of node indices representing the path.
    - D (list): Distance matrix representing the graph.

    Returns:
    - distance (float): Total distance of the path based on the values in the distance matrix.
    """
    return sum(D[path[i]][path[i + 1]] for i in range(len(path) - 1))

def plot_graph(D, node_indices_with_x_y, start_state, end_state, path, epoch, cal_distance):
    """
    Plot the graph with nodes positioned using x, y coordinates and highlight the given path.

    Parameters:
    - D (list): Distance matrix representing the graph.
    - node_indices_with_x_y (dict): Dictionary containing node indices and corresponding x, y coordinates.
    - start_state (int): Index of the start state in the graph.
    - end_state (int): Index of the end state in the graph.
    - path (list): List of node indices representing the path to be highlighted.
    - epoch (int): Current epoch number.
    - cal_distance (function): Function to calculate the total distance of a given path.

    Saves the plot as an image file in the "output" directory.
    """
    # Extract x, y coordinates and indices from the dictionary
    coordinates = [(float(data['y']), float(data['x'])) for data in node_indices_with_x_y.values()]
    indices = [data['index'] for data in node_indices_with_x_y.values()]

    # Create a graph with nodes positioned using x, y coordinates
    G = nx.Graph()
    G.add_nodes_from(indices)
    G.add_edges_from([(path[i], path[i + 1]) for i in range(len(path) - 1)])

    pos = {index: coordinates[index] for index in indices}

    # plt.figure(figsize=(20, 16))
    plt.figure(figsize=FIGSIZE)
    nx.draw(G, pos, node_size=100, node_color='lightblue', with_labels=False)

    # Draw node labels with x, y coordinates
    for index, coord in zip(indices, coordinates):
        plt.text(coord[0], coord[1], f'({coord[0]:.4f}, {coord[1]:.4f})', fontsize=10, ha='left')
        plt.text(coord[0], coord[1], f'{index}', fontsize=10, ha='right')

    path_edges = list(zip(path[:-1], path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=[start_state, end_state], node_size=700, node_color='green')
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    plt.title(f"Epoch {epoch}: Distance = {cal_distance(path, D)}")
    plt.savefig(f"output/output_image_epoch_{epoch}.png")
    plt.close()

def epsilon_greedy(s_curr, q, D, epsilon):
    """
    Select the next state using epsilon-greedy exploration strategy.

    Parameters:
    - s_curr (int): Current state index.
    - q (numpy.ndarray): Q-values matrix representing the learned values for state-action pairs.
    - D (numpy.ndarray): Distance matrix representing the graph.
    - epsilon (float): Exploration-exploitation trade-off parameter.

    Returns:
    - s_next (int): Next state index based on the epsilon-greedy strategy.
    """
    potential_next_states = np.where(D[s_curr] > 0)[0]
    return potential_next_states[np.argmax(q[s_curr][potential_next_states])] if random.random() > epsilon else random.choice(potential_next_states)