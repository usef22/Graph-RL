import pandas as pd
import networkx as nx
import xml.etree.ElementTree as ET

def graphml_to_csv(input_graphml, output_csv):
    # Parse the input GraphML file
    tree = ET.parse(input_graphml)
    root = tree.getroot()

    # List to store edge information
    edges = []
    
    # Iterate through all edge elements in the GraphML
    for edge in root.findall('.//{http://graphml.graphdrawing.org/xmlns}edge'):
        source = edge.get('source')
        target = edge.get('target')
        
        # Extract time_duration value from data elements
        time_duration = None
        data_elements = edge.findall('.//{http://graphml.graphdrawing.org/xmlns}data')
        for data in data_elements:
            if data.get('key') == 'd9':  # Assuming 'd9' is the key for time_duration
                time_duration = data.text
            if data.get('key') == 'd10':  # Assuming 'd9' is the key for time_duration
                traffic_density = data.text
                print(traffic_density)
                # a = input()
            if data.get('key') == 'd11':  # Assuming 'd9' is the key for time_duration
                bandwidth = data.text
                print(bandwidth)
                # a = input()

        # Append edge information to the list
        edges.append({
            'source': source,
            'target': target,
            'time_duration': time_duration,
            'traffic_density':traffic_density,
            'bandwidth': bandwidth
        })

    # Create a DataFrame from the list of edges
    df_edges = pd.DataFrame(edges)
    
    # Save the DataFrame to a CSV file
    df_edges.to_csv(output_csv, index=False)

if __name__ == "__main__":
    # Set the input GraphML file path
    input_graphml_file = "updated_graphml_files/updated_1270.graphml"
    
    # Set the output CSV file path
    output_csv_file = "converted_output.csv"
    
    # Convert GraphML to CSV
    graphml_to_csv(input_graphml_file, output_csv_file)
