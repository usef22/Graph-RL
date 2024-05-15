import pandas as pd
import json
from config import *

class ROADDETAILS():
    def __init__(self):
        pass

    def get_details_from_latitude_edges(self, list_of_edges):
        """
        Extract details related to latitude edges.

        Parameters:
        - list_of_edges (list): List of edges.

        Returns:
        - Tuple: Tuple containing all nodes in the same road, extreme starting point, and extreme ending point.
        """
        all_nodes_in_same_road = []
        longitude_points = []
        for edge in list_of_edges:
            first_node_of_edge, second_node_of_edge = edge.split("_")
            if first_node_of_edge not in all_nodes_in_same_road:
                split_by_dot = first_node_of_edge.split(".")
                longitude = split_by_dot[1][4:] + "." + split_by_dot[2]
                all_nodes_in_same_road.append(first_node_of_edge)
                longitude_points.append(longitude)

            if second_node_of_edge not in all_nodes_in_same_road:
                split_by_dot = second_node_of_edge.split(".")
                longitude = split_by_dot[1][4:] + "." + split_by_dot[2]
                all_nodes_in_same_road.append(second_node_of_edge)
                longitude_points.append(longitude)
        longitude_points.sort()
        for node in all_nodes_in_same_road:
            if node[-8:] == longitude_points[0]:
                extreme_starting_point = node
            elif node[-8:] == longitude_points[-1]:
                extreme_ending_point = node
        return all_nodes_in_same_road, extreme_starting_point, extreme_ending_point

    def get_details_from_longitude_edges(self, list_of_edges):
        """
        Extract details related to longitude edges.

        Parameters:
        - list_of_edges (list): List of edges.

        Returns:
        - Tuple: Tuple containing all nodes in the same road, extreme starting point, and extreme ending point.
        """
        all_nodes_in_same_road = []
        latitude_points = []
        for edge in list_of_edges:
            first_node_of_edge, second_node_of_edge = edge.split("_")

            if first_node_of_edge not in all_nodes_in_same_road:
                split_by_dot = first_node_of_edge.split(".")
                latitude = split_by_dot[0] + "." + split_by_dot[1][:4]
                all_nodes_in_same_road.append(first_node_of_edge)
                latitude_points.append(latitude)

            if second_node_of_edge not in all_nodes_in_same_road:
                split_by_dot = second_node_of_edge.split(".")
                latitude = split_by_dot[0] + "." + split_by_dot[1][:4]
                all_nodes_in_same_road.append(second_node_of_edge)
                latitude_points.append(latitude)
        latitude_points.sort()

        for node in all_nodes_in_same_road:
            if node[:7] == latitude_points[0]:
                extreme_starting_point = node
            elif node[:7] == latitude_points[-1]:
                extreme_ending_point = node

        return all_nodes_in_same_road, extreme_starting_point, extreme_ending_point

    def get_details_of_latitude_edge(self, all_road_details, straight_roads):
        """
        Extract details of latitude edges.

        Parameters:
        - all_road_details (dict): Dictionary to store road details.
        - straight_roads (dict): Dictionary containing information about straight roads.

        Returns:
        - dict: Updated dictionary containing latitude road details.
        """
        all_road_details["latitude_roads"] = {}
        for latitude_road in straight_roads["latitude_roads"]:
            road_id = f"LAT_{latitude_road.split('_')[-1]}"
            print(road_id)
            list_of_edges = straight_roads["latitude_roads"][latitude_road]

            all_road_details["latitude_roads"][road_id] = {}
            all_road_details["latitude_roads"][road_id]["edges"] = list_of_edges
            all_nodes_in_same_road, extreme_starting_point, extreme_ending_point = self.get_details_from_latitude_edges(
                list_of_edges
            )
            all_road_details["latitude_roads"][road_id]["nodes"] = all_nodes_in_same_road
            all_road_details["latitude_roads"][road_id]["extreme_starting_point"] = extreme_starting_point
            all_road_details["latitude_roads"][road_id]["extreme_ending_point"] = extreme_ending_point

        return all_road_details

    def get_details_of_longitude_edge(self, all_road_details, straight_roads):
        """
        Extract details of longitude edges.

        Parameters:
        - all_road_details (dict): Dictionary to store road details.
        - straight_roads (dict): Dictionary containing information about straight roads.

        Returns:
        - dict: Updated dictionary containing longitude road details.
        """
        all_road_details["longitude_roads"] = {}
        for longitude_road in straight_roads["longitude_roads"]:
            road_id = f"LON_{longitude_road.split('_')[-1]}"
            print(road_id)
            list_of_edges = straight_roads["longitude_roads"][longitude_road]

            all_road_details["longitude_roads"][road_id] = {}
            all_road_details["longitude_roads"][road_id]["edges"] = list_of_edges
            all_nodes_in_same_road, extreme_starting_point, extreme_ending_point = self.get_details_from_longitude_edges(
                list_of_edges
            )
            all_road_details["longitude_roads"][road_id]["nodes"] = all_nodes_in_same_road
            all_road_details["longitude_roads"][road_id]["extreme_starting_point"] = extreme_starting_point
            all_road_details["longitude_roads"][road_id]["extreme_ending_point"] = extreme_ending_point

        return all_road_details

    def process(self, individual_csv_file_path, streight_roads_json_path):
        """
        Main function to process individual CSV file and generate a JSON file with road details.

        Parameters:
        - individual_csv_file_path (str): Path to the individual CSV file.
        - streight_roads_json_path (str): Path to the output JSON file for road details.

        Returns:
        - None
        """
        df = pd.read_csv(individual_csv_file_path)
        straight_roads = {"latitude_roads": {}, "longitude_roads": {}}
        df['next_latitude'] = df['latitude'].shift(-1)
        df['next_longitude'] = df['longitude'].shift(-1)
        df['next_date'] = df['date'].shift(-1)
        df['next_unique_node_id'] = df['unique_node_id'].shift(-1)
        index = 0

        while index < len(df):
            print("index:::::::::::::::", index)
            if df.loc[index, "latitude"] == df.loc[index, "next_latitude"]:
                edges_connected_list = []
                while True:
                    if df.loc[index, "latitude"] == df.loc[index, "next_latitude"]:
                        edges_connected_list.append(df.loc[index, "edge_pair"])
                    else:
                        break
                    index += 1
                    print("SAME LATITUDE ....")
                straight_roads["latitude_roads"][
                    f"road_number_{str(len(straight_roads['latitude_roads'])+1)}"
                ] = edges_connected_list

            elif df.loc[index, "longitude"] == df.loc[index, "next_longitude"]:
                edges_connected_list = []
                while True:
                    if df.loc[index, "longitude"] == df.loc[index, "next_longitude"]:
                        edges_connected_list.append(df.loc[index, "edge_pair"])
                    else:
                        break
                    index += 1
                    print("SAME LONGITUDE ....")
                straight_roads["longitude_roads"][
                    f"road_number_{str(len(straight_roads['longitude_roads'])+1)}"
                ] = edges_connected_list
            else:
                print("NOT IN A STRAIGHT LINE.")
            index += 1
            print("><---" * 20)

        all_road_details = {}
        all_road_details = self.get_details_of_latitude_edge(all_road_details, straight_roads)
        all_road_details = self.get_details_of_longitude_edge(all_road_details, straight_roads)

        with open(streight_roads_json_path, "w") as file:
            json.dump(all_road_details, file)

if __name__ == "__main__":
    csv_file_path = "individual_user_dataframe/driver_1270.csv"
    streight_roads_json_path = f"{STRAIGHT_ROAD_JSON_DIR_PATH}/road_connection_1270.json"
    road_details_obj = ROADDETAILS()
    road_details_obj.process(csv_file_path, streight_roads_json_path)
