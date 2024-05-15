import networkx as nx
import json
import os

class EDGETIMEDICT():
    def __init__(self):
        # Load existing data from JSON files if they exist, otherwise initialize empty dictionaries.
        if os.path.isfile("all_individual_edge_time.json"):
            with open('all_individual_edge_time.json', 'r') as file:
                self.all_individual_edge_time_dict = json.load(file)
        else:
            self.all_individual_edge_time_dict = {}
        
        if os.path.isfile("all_individual_edge_speed.json"):
            with open('all_individual_edge_speed.json', 'r') as file:
                self.all_individual_edge_speed_dict = json.load(file)
        else:
            self.all_individual_edge_speed_dict = {}
        
    def process(self, graphml_file_path):
        """
        Process the graphml file and update individual edge time and speed dictionaries.

        Parameters:
        - graphml_file_path (str): Path to the input graphml file.

        Returns:
        - None
        """
        G = nx.read_graphml(graphml_file_path)
        for source, target, data in G.edges(data=True):
            time_difference = data.get('time_duration', None)
            speed = data.get('displacement_speed', None)

            if float(time_difference) < 300:
                edge = source + "_" + target
                # Update time dictionary
                if edge in self.all_individual_edge_time_dict:
                    self.all_individual_edge_time_dict[edge].append(time_difference)
                else:
                    self.all_individual_edge_time_dict[edge] = [time_difference]
                
                # Update speed dictionary
                if edge in self.all_individual_edge_speed_dict:
                    self.all_individual_edge_speed_dict[edge].append(speed)
                else:
                    self.all_individual_edge_speed_dict[edge] = [speed]
                        
        # Save the updated dictionaries to JSON files
        with open("all_individual_edge_time.json", 'w') as json_file:
            json.dump(self.all_individual_edge_time_dict, json_file)
        
        with open("all_individual_edge_speed.json", 'w') as json_file:
            json.dump(self.all_individual_edge_speed_dict, json_file)
            
if __name__ == "__main__":
    # Example usage
    edgetimedict_obj = EDGETIMEDICT()
    edgetimedict_obj.process(graphml_file_path='output_graphml_files/output_1270.graphml')
