import json
from icecream import ic
from config import *

class COMBINENODES():
    def __init__(self):
        # Dictionary to store combined nodes based on latitude or longitude
        self.combine_nodes_dict = {}
    
    def getLatLonFromNodeId(self, node_id):
        """
        Extract latitude and longitude from a node ID.

        Parameters:
        - node_id (str): Node ID in the format 'lat.lon1lon2'.

        Returns:
        - latitude (str): Latitude part of the node ID.
        - longitude (str): Longitude part of the node ID.
        """
        split_by_dot = node_id.split(".")
        latitude = split_by_dot[0] + "." + split_by_dot[1][:4]
        longitude = split_by_dot[1][-3:] + "." + split_by_dot[2]
        return latitude, longitude
    
    def processSameLatitudeRoad(self, latitude_roads_dict):
        """
        Process roads with the same latitude to combine nodes.

        Parameters:
        - latitude_roads_dict (dict): Dictionary containing information about roads with the same latitude.
        """
        for latitude_road in latitude_roads_dict:
            starting_point_of_road_latitude, starting_point_of_road_longitude = self.getLatLonFromNodeId(latitude_roads_dict[latitude_road]['extreme_starting_point'])
            ending_point_of_road_latitude, ending_point_of_road_longitude = self.getLatLonFromNodeId(latitude_roads_dict[latitude_road]['extreme_ending_point'])

            for latitude_road_2 in latitude_roads_dict:
                if latitude_road != latitude_road_2:
                    starting_point_of_road_latitude_2, starting_point_of_road_longitude_2 = self.getLatLonFromNodeId(latitude_roads_dict[latitude_road_2]['extreme_starting_point'])
                    ending_point_of_road_latitude_2, ending_point_of_road_longitude_2 = self.getLatLonFromNodeId(latitude_roads_dict[latitude_road_2]['extreme_ending_point'])
                    
                    if float(starting_point_of_road_latitude) == float(starting_point_of_road_latitude_2):
                        if (float(starting_point_of_road_longitude) > float(starting_point_of_road_longitude_2) and float(starting_point_of_road_longitude) < float(ending_point_of_road_longitude_2)) or (float(ending_point_of_road_longitude) > float(starting_point_of_road_longitude_2) and float(ending_point_of_road_longitude) < float(ending_point_of_road_longitude_2)):
                            combine_nodes_list_name_list = [latitude_road, latitude_road_2]
                            combine_nodes_list_name_list.sort()
                            combine_nodes_list_name = f"{combine_nodes_list_name_list[0]}_{combine_nodes_list_name_list[1]}"
                            combined_list = latitude_roads_dict[latitude_road]["nodes"] + latitude_roads_dict[latitude_road_2]["nodes"]
                            if combine_nodes_list_name not in self.combine_nodes_dict:
                                self.combine_nodes_dict[combine_nodes_list_name] = list(set(combined_list))
                        else:
                            pass
                        
    def processSameLongitudeRoad(self, longitude_roads_dict):
        """
        Process roads with the same longitude to combine nodes.

        Parameters:
        - longitude_roads_dict (dict): Dictionary containing information about roads with the same longitude.
        """
        for longitude_road in longitude_roads_dict:
            starting_point_of_road_latitude, starting_point_of_road_longitude = self.getLatLonFromNodeId(longitude_roads_dict[longitude_road]['extreme_starting_point'])
            ending_point_of_road_latitude, ending_point_of_road_longitude = self.getLatLonFromNodeId(longitude_roads_dict[longitude_road]['extreme_ending_point'])

            for longitude_road_2 in longitude_roads_dict:
                if longitude_road != longitude_road_2:
                    starting_point_of_road_latitude_2, starting_point_of_road_longitude_2 = self.getLatLonFromNodeId(longitude_roads_dict[longitude_road_2]['extreme_starting_point'])
                    ending_point_of_road_latitude_2, ending_point_of_road_longitude_2 = self.getLatLonFromNodeId(longitude_roads_dict[longitude_road_2]['extreme_ending_point'])
                    
                    if float(starting_point_of_road_longitude) == float(starting_point_of_road_longitude_2):
                        if (float(starting_point_of_road_latitude) > float(starting_point_of_road_latitude_2) and float(starting_point_of_road_latitude) < float(ending_point_of_road_latitude_2)) or (float(ending_point_of_road_latitude) > float(starting_point_of_road_latitude_2) and float(ending_point_of_road_latitude) < float(ending_point_of_road_latitude_2)):
                            combine_nodes_list_name_list = [longitude_road, longitude_road_2]
                            combine_nodes_list_name_list.sort()
                            combine_nodes_list_name = f"{combine_nodes_list_name_list[0]}_{combine_nodes_list_name_list[1]}"
                            combined_list = longitude_roads_dict[longitude_road]["nodes"] + longitude_roads_dict[longitude_road_2]["nodes"]
                            if combine_nodes_list_name not in self.combine_nodes_dict:
                                self.combine_nodes_dict[combine_nodes_list_name] = list(set(combined_list))
                        else:
                            pass
    
    def sorted_by_longitude_list(self, list_of_nodes):
        """
        Sort nodes based on longitude.

        Parameters:
        - list_of_nodes (list): List of node IDs.

        Returns:
        - sorted_nodes_in_list (list): List of sorted node IDs based on longitude.
        """
        longitude_list = []
        sorted_nodes_in_list = []
        latitude_point = list_of_nodes[1].split(".")[0] + "." + list_of_nodes[1].split(".")[1][:4]
        for i in range(0, len(list_of_nodes)):
            longitude_list.append(list_of_nodes[i].split(".")[1][4:] + "." + list_of_nodes[i].split(".")[2])
        longitude_list.sort()
        
        for i in range(0, len(longitude_list)):
            sorted_nodes_in_list.append(f"{latitude_point}{longitude_list[i]}")
        return sorted_nodes_in_list

    def sorted_by_latitude_list(self, list_of_nodes):
        """
        Sort nodes based on latitude.

        Parameters:
        - list_of_nodes (list): List of node IDs.

        Returns:
        - sorted_nodes_in_list (list): List of sorted node IDs based on latitude.
        """
        latitude_list = []
        sorted_nodes_in_list = []
        longitude_point = list_of_nodes[1].split(".")[1][4:] + "." + list_of_nodes[1].split(".")[2]
        for i in range(0, len(list_of_nodes)):
            latitude_list.append(list_of_nodes[i].split(".")[0] + "." + list_of_nodes[i].split(".")[1][:4])
        latitude_list.sort()
        
        for i in range(0, len(latitude_list)):
            sorted_nodes_in_list.append(f"{latitude_list[i]}{longitude_point}")
        return sorted_nodes_in_list
    
    def process(self, streight_roads_json_path):
        """
        Main processing function to combine nodes and save the result in a JSON file.

        Parameters:
        - streight_roads_json_path (str): Path to the JSON file containing road connection information.
        """
        with open(streight_roads_json_path, "r") as file:
            road_connection_dict = json.load(file)
        
        latitude_roads_dict = road_connection_dict["latitude_roads"]
        longitude_roads_dict = road_connection_dict["longitude_roads"]
        
        # Process roads with the same latitude and longitude to combine nodes
        self.processSameLatitudeRoad(latitude_roads_dict)
        self.processSameLongitudeRoad(longitude_roads_dict)
        
        # Sort combined nodes based on latitude or longitude
        for combo_road in self.combine_nodes_dict:
            if combo_road[:3] == "LAT":
                list_of_nodes = self.combine_nodes_dict[combo_road]
                sorted_nodes_in_list = self.sorted_by_longitude_list(list_of_nodes)
                
            elif combo_road[:3] == "LON":
                list_of_nodes = self.combine_nodes_dict[combo_road]
                sorted_nodes_in_list = self.sorted_by_latitude_list(list_of_nodes)
            
            # Update the dictionary with the sorted nodes
            self.combine_nodes_dict[combo_road] = sorted_nodes_in_list
        
        # Save the combined and sorted nodes in the JSON file
        with open(streight_roads_json_path, "w") as file:
            json.dump(self.combine_nodes_dict, file)

if __name__ == "__main__":
    # Create an instance of COMBINENODES
    combine_nodes_obj = COMBINENODES()
    
    # User ID for the current road data
    user_id = 1270
    
    # Path to the JSON file containing road connection information
    streight_roads_json_path = f"{STRAIGHT_ROAD_JSON_DIR_PATH}/road_connection_{user_id}.json"
    
    # Process and combine nodes, then save the result in the JSON file
    combine_nodes_obj.process(streight_roads_json_path)
