# import pandas as pd
# import networkx as nx
# import xml.etree.ElementTree as ET
# import json

# class CSVTOGRAPH():
#     def __init__(self):
#         pass

#     def process(self, input_csv_file_path, json_file_path, output_graphml_file_path):
#         # Load CSV data into a DataFrame
#         df = pd.read_csv(input_csv_file_path)
        
#         # Create a directed graph
#         G = nx.DiGraph()
        
#         # Add nodes and edges to the graph
#         for index, row in df.iterrows():
#             G.add_node(row['unique_node_id'], x=str(row['longitude']), y=str(row['latitude']), osmid=str(row['nid']), speed=str(row['speed']), direction=str(row['direction']))
#             if index < len(df):
#                 next_node_id = df.at[index, 'next_unique_node_id']
#                 distance = df.at[index, 'distance']  # Assuming you have a 'distance' column in your CSV
#                 time_duration = df.at[index, 'time_difference']  # Assuming you have a 'time_difference' column in your CSV
#                 G.add_edge(row['unique_node_id'], next_node_id, time_duration=str(row["time_difference"]), distance=str(distance), time=str(time_duration))

#         # Create the GraphML structure
#         graphml = ET.Element('graphml', xmlns="http://graphml.graphdrawing.org/xmlns", xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance", xsi_schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd")
        
#         # Add keys
#         keys = [
#             ('distance', 'string', 'edge', 'd6'),
#             ('time_duration', 'string', 'edge', 'd9'),
#             ('speed', 'string', 'node', 'd8'),
#             ('direction', 'string', 'node', 'd7'),
#             ('edge', 'string', 'edge', 'd13'),
#             ('unique_node_id', 'string', 'node', 'd5'),
#             ('longitude', 'string', 'node', 'd4'),
#             ('latitude', 'string', 'node', 'd3'),
#             ('streets_per_node', 'string', 'graph', 'd2'),
#             ('name', 'string', 'graph', 'd1'),
#         ]

#         # Add keys to the GraphML structure
#         for key in keys:
#             key_element = ET.SubElement(graphml, 'key', attrib={'attr.name': key[0], 'attr.type': key[1], 'for': key[2], 'id': key[3]})

#         # Add graph element
#         graph_element = ET.SubElement(graphml, 'graph', attrib={'edgedefault': 'directed'})
        
#         # Add data elements to the graph element
#         ET.SubElement(graph_element, 'data', attrib={'key': 'd1'}).text = "graph for 1270"
        
#         # Read the JSON file into a dictionary
#         with open(json_file_path, 'r') as json_file:
#             data = json.load(json_file)
        
#         ET.SubElement(graph_element, 'data', attrib={'key': 'd2'}).text = str(data)

#         # Add node elements
#         for node in G.nodes():
#             node_element = ET.SubElement(graph_element, 'node', attrib={'id': str(node)})
#             result = df[df['unique_node_id'] == node]

#             for key in keys:  # Select relevant keys for nodes
#                 attribute = key[0]
#                 key_id = key[3]
                
#                 # Check if the attribute is in the result columns
#                 if attribute in result.columns:
#                     try:
#                         ET.SubElement(node_element, 'data', attrib={'key': key_id}).text = str(result[attribute].values[0])
#                     except:
#                         pass
#                 else:
#                     # If the attribute is not present, create an empty data element
#                     ET.SubElement(node_element, 'data', attrib={'key': key_id}).text = ""

#         # Add edge elements
#         for edge in G.edges():
#             if str(edge[0]) != str(edge[1]): 
#                 edge_element = ET.SubElement(graph_element, 'edge', attrib={'source': str(edge[0]), 'target': str(edge[1])})
#                 ET.SubElement(edge_element, 'data', attrib={'key': 'd6'}).text = str(G[edge[0]][edge[1]]['distance'])
#                 ET.SubElement(edge_element, 'data', attrib={'key': 'd9'}).text = str(G[edge[0]][edge[1]]['time_duration'])
#                 ET.SubElement(edge_element, 'data', attrib={'key': 'd13'}).text = "0"

#         # Save the GraphML file
#         tree = ET.ElementTree(graphml)
#         tree.write(output_graphml_file_path, encoding='utf-8', xml_declaration=True)
        
# if __name__ == "__main__":
#     input_csv_file_path = "individual_user_dataframe/driver_1300.csv"
#     output_graphml_file_path = "output_graphml_files/updated_1300.graphml"
#     json_file_path = "edges_connetion_json_dir/road_connection_1300.json"
#     csvtograph_obj = CSVTOGRAPH()
#     csvtograph_obj.process(input_csv_file_path, json_file_path, output_graphml_file_path)





import pandas as pd
import networkx as nx
import xml.etree.ElementTree as ET
import json

class CSVTOGRAPH():
    def __init__(self):
        pass

    def process(self, input_csv_file_path, json_file_path, output_graphml_file_path):
        # Load CSV data into a DataFrame
        df = pd.read_csv(input_csv_file_path)
        
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes and edges to the graph
        for index, row in df.iterrows():
            G.add_node(row['unique_node_id'], x=str(row['longitude']), y=str(row['latitude']), osmid=str(row['nid']), speed=str(row['speed']), direction=str(row['direction']))
            if index < len(df):
                next_node_id = df.at[index, 'next_unique_node_id']
                distance = df.at[index, 'distance']  # Assuming you have a 'distance' column in your CSV
                time_duration = df.at[index, 'time_difference']  # Assuming you have a 'time_difference' column in your CSV
                G.add_edge(row['unique_node_id'], next_node_id, time_duration=str(row["time_difference"]), distance=str(distance), time=str(time_duration),
                           traffic_density=str(row["traffic_density"]), bandwidth=str(row["bandwidth"]))  # Adding traffic_density and bandwidth to edge

        # Create the GraphML structure
        graphml = ET.Element('graphml', xmlns="http://graphml.graphdrawing.org/xmlns", xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance", xsi_schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd")
        
        # Add keys
        keys = [
            ('distance', 'string', 'edge', 'd6'),
            ('time_duration', 'string', 'edge', 'd9'),
            ('speed', 'string', 'node', 'd8'),
            ('direction', 'string', 'node', 'd7'),
            ('edge', 'string', 'edge', 'd13'),
            ('unique_node_id', 'string', 'node', 'd5'),
            ('longitude', 'string', 'node', 'd4'),
            ('latitude', 'string', 'node', 'd3'),
            ('streets_per_node', 'string', 'graph', 'd2'),
            ('name', 'string', 'graph', 'd1'),
            ('traffic_density', 'string', 'edge', 'd10'),  # New key for traffic_density
            ('bandwidth', 'string', 'edge', 'd11')  # New key for bandwidth
        ]

        # Add keys to the GraphML structure
        for key in keys:
            key_element = ET.SubElement(graphml, 'key', attrib={'attr.name': key[0], 'attr.type': key[1], 'for': key[2], 'id': key[3]})

        # Add graph element
        graph_element = ET.SubElement(graphml, 'graph', attrib={'edgedefault': 'directed'})
        
        # Add data elements to the graph element
        ET.SubElement(graph_element, 'data', attrib={'key': 'd1'}).text = "graph for 1270"
        
        # Read the JSON file into a dictionary
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        ET.SubElement(graph_element, 'data', attrib={'key': 'd2'}).text = str(data)

        # Add node elements
        for node in G.nodes():
            node_element = ET.SubElement(graph_element, 'node', attrib={'id': str(node)})
            result = df[df['unique_node_id'] == node]

            for key in keys:  # Select relevant keys for nodes
                attribute = key[0]
                key_id = key[3]
                
                # Check if the attribute is in the result columns
                if attribute in result.columns:
                    try:
                        ET.SubElement(node_element, 'data', attrib={'key': key_id}).text = str(result[attribute].values[0])
                    except:
                        pass
                else:
                    # If the attribute is not present, create an empty data element
                    ET.SubElement(node_element, 'data', attrib={'key': key_id}).text = ""

        # Add edge elements
        for edge in G.edges():
            if str(edge[0]) != str(edge[1]): 
                edge_element = ET.SubElement(graph_element, 'edge', attrib={'source': str(edge[0]), 'target': str(edge[1])})
                ET.SubElement(edge_element, 'data', attrib={'key': 'd6'}).text = str(G[edge[0]][edge[1]]['distance'])
                ET.SubElement(edge_element, 'data', attrib={'key': 'd9'}).text = str(G[edge[0]][edge[1]]['time_duration'])
                ET.SubElement(edge_element, 'data', attrib={'key': 'd10'}).text = str(G[edge[0]][edge[1]]['traffic_density'])  # Add traffic_density
                ET.SubElement(edge_element, 'data', attrib={'key': 'd11'}).text = str(G[edge[0]][edge[1]]['bandwidth'])  # Add bandwidth
                ET.SubElement(edge_element, 'data', attrib={'key': 'd13'}).text = "0"

        # Save the GraphML file
        tree = ET.ElementTree(graphml)
        tree.write(output_graphml_file_path, encoding='utf-8', xml_declaration=True)
        
if __name__ == "__main__":
    input_csv_file_path = "individual_user_dataframe/driver_1300.csv"
    output_graphml_file_path = "output_graphml_files/updated_1300.graphml"
    json_file_path = "edges_connetion_json_dir/road_connection_1300.json"
    csvtograph_obj = CSVTOGRAPH()
    csvtograph_obj.process(input_csv_file_path, json_file_path, output_graphml_file_path)

