import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from config import FIGSIZE

def save_graph_plot(graphml_file_path, graph_plot_image_path):
    """
    Load a GraphML file, create a directed graph, and save a plot of the graph.

    Args:
    - graphml_file_path (str): Path to the GraphML file.
    - graph_plot_image_path (str): Path to save the graph plot image.

    Returns:
    - None
    """
    # Load the GraphML file
    tree = ET.parse(graphml_file_path)
    root = tree.getroot()

    # Create a directed graph
    G = nx.DiGraph()

    # Extract nodes and their positions from the GraphML file
    for node in root.findall('.//{http://graphml.graphdrawing.org/xmlns}node'):
        node_id = node.get('id')
        
        # Find 'x' and 'y' data elements
        x_element = node.find('.//{http://graphml.graphdrawing.org/xmlns}data[@key="d4"]')
        y_element = node.find('.//{http://graphml.graphdrawing.org/xmlns}data[@key="d3"]')
        
        # Check if the elements exist and have text content
        if x_element is not None and x_element.text is not None and y_element is not None and y_element.text is not None:
            x = float(x_element.text)
            y = float(y_element.text)
            G.add_node(node_id, pos=(y, x))

    # Extract edges from the GraphML file
    for edge in root.findall('.//{http://graphml.graphdrawing.org/xmlns}edge'):
        source = edge.get('source')
        target = edge.get('target')
        G.add_edge(source, target)

    # Increase the size of the plot
    plt.figure(figsize=FIGSIZE)

    # Visualize the graph
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=False, node_size=100, node_color='skyblue', edge_color='gray', arrowsize=10)

    # Add coordinates as labels for each node
    for node, (x, y) in pos.items():
        plt.text(x, y, f'({y:.4f}, {x:.4f})', fontsize=8, ha='right', va='bottom')

    # Save the plot as an image
    plt.savefig(graph_plot_image_path)

if __name__ == "__main__":
    print("---")
    save_graph_plot("modified_graph_updated_new_logic.graphml", "modified_graph_updated_new_logic.png")
