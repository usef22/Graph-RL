import json
import pandas as pd

class NUMBEROFEDGES():
    def __init__(self):
        pass
    
    def createNoEdgesConnectedToNode(self, df): 
        """
        Count the number of unique edges connected to each node.

        Args:
        - df (DataFrame): Input DataFrame containing the 'edge_pair' column.

        Returns:
        - new_edge_dict (dict): Dictionary with nodes as keys and the number of edges connected to each node as values.
        """
        edges_list = df["edge_pair"].unique().tolist()
        edges_combination_list = []

        # Extract pairs of nodes from the 'edge_pair' column
        for edge in edges_list:
            two_node_list = edge.split("_")
            edges_combination_list.append(two_node_list)    

        edges_dict = {}

        # Create a dictionary with nodes as keys and a list of connected nodes as values
        for two_node_list in edges_combination_list:
            if two_node_list[0] != two_node_list[1]:
                if two_node_list[0] not in edges_dict:
                    edges_dict[two_node_list[0]] = []
                else:
                    pass
                if two_node_list[1] not in edges_dict[two_node_list[0]]:
                    edges_dict[two_node_list[0]].append(two_node_list[1])
            else:
                pass
        
        new_edge_dict = {}
        new_edge_connection_dict = {}

        # Count the number of connected edges for each node
        for key in edges_dict:
            new_edge_dict[key] = len(edges_dict[key])
            last_key, last_value = list(edges_dict.items())[-1]
            new_edge_connection_dict[key] = edges_dict[key]

            # Save the detailed edge connections to a JSON file
            with open("new_edge_connection_dict.json", 'w') as json_file:
                json.dump(new_edge_connection_dict, json_file)

        return new_edge_dict
      
    def process(self, csv_file_path, json_file_path):
        """
        Process the CSV file to count the number of edges connected to each node and save the result in a JSON file.

        Args:
        - csv_file_path (str): Path to the input CSV file.
        - json_file_path (str): Path to save the resulting JSON file.

        Returns:
        - None
        """
        df = pd.read_csv(csv_file_path)
        new_edge_dict = self.createNoEdgesConnectedToNode(df)

        # Save the summary dictionary to a JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(new_edge_dict, json_file)

if __name__ == "__main__":
    csv_file_path = "driver_1290.csv"
    json_file_path = "edges_connection_1290.json"
    numberofedges_obj = NUMBEROFEDGES()
    numberofedges_obj.process(csv_file_path, json_file_path)
