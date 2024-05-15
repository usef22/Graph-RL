import xml.etree.ElementTree as ET
from icecream import ic
import json
from combine_nodes import COMBINENODES
from road_connections import ROADDETAILS
from config import *
from haversine import haversine, Unit

class UPDATEGRAPHML():

    def __init__(self, output_graphml_file_path):
        self.tree = ET.parse(output_graphml_file_path)
        self.root = self.tree.getroot()
        self.key_d2_element = self.root.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d2']")
        self.d2_value = eval(self.key_d2_element.text)

    def find_traffic_density(self, source, target):
        for edge in self.root.findall(".//{http://graphml.graphdrawing.org/xmlns}edge"):
            source_node = edge.attrib['source']
            target_node = edge.attrib['target']
            if source_node == source and target_node == target:
                for data in edge.findall(".//{http://graphml.graphdrawing.org/xmlns}data"):
                    key = data.attrib['key']
                    if key == 'd10':
                        traffic_density = data.text
                break  # Break the loop once the edge is found and updated
        return traffic_density

    def find_bandwidth(self, source, target):
        for edge in self.root.findall(".//{http://graphml.graphdrawing.org/xmlns}edge"):
            source_node = edge.attrib['source']
            target_node = edge.attrib['target']
            if source_node == source and target_node == target:
                for data in edge.findall(".//{http://graphml.graphdrawing.org/xmlns}data"):
                    key = data.attrib['key']
                    if key == 'd11':
                        bandwidth = data.text
                break  # Break the loop once the edge is found and updated
        return bandwidth
        
    def find_distance(self, source, target):
        for edge in self.root.findall(".//{http://graphml.graphdrawing.org/xmlns}edge"):
            source_node = edge.attrib['source']
            target_node = edge.attrib['target']
            if source_node == source and target_node == target:
                for data in edge.findall(".//{http://graphml.graphdrawing.org/xmlns}data"):
                    key = data.attrib['key']
                    if key == 'd6':
                        distance = data.text
                break  # Break the loop once the edge is found and updated
        return distance

    def find_time_duration(self, source, target):
        for edge in self.root.findall(".//{http://graphml.graphdrawing.org/xmlns}edge"):
            source_node = edge.attrib['source']
            target_node = edge.attrib['target']
            if source_node == source and target_node == target:
                for data in edge.findall(".//{http://graphml.graphdrawing.org/xmlns}data"):
                    key = data.attrib['key']
                    if key == 'd9':
                        time_duration = data.text
                break  # Break the loop once the edge is found and updated
        return time_duration

    def check_if_edge_present_or_not(self, source_node_to_check, target_node_to_check):
    
        # Initialize a flag to track if the edge is found
        edge_found = False

        # Iterate through all edges and check if the specified edge is present
        for edge in self.root.findall(".//{http://graphml.graphdrawing.org/xmlns}edge"):
            
            source_node = edge.attrib['source']
            target_node = edge.attrib['target']

            # Check if the current edge matches the specified source and target nodes
            if source_node == source_node_to_check and target_node == target_node_to_check:
                edge_found = True
                break  # Break the loop once the edge is found
        
        return edge_found
    
    def create_new_edge_with_details(self, new_source, new_target, new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth):
        # Define the namespace
        namespace = "{http://graphml.graphdrawing.org/xmlns}"

        new_edge = ET.Element(f'{namespace}edge', attrib={'source': new_source, 'target': new_target})
        data_d6 = ET.SubElement(new_edge, f'{namespace}data', attrib={'key': 'd6'})
        data_d6.text = new_speed
        data_d9 = ET.SubElement(new_edge, f'{namespace}data', attrib={'key': 'd9'})
        data_d9.text = new_time_duration
        data_d10 = ET.SubElement(new_edge, f'{namespace}data', attrib={'key': 'd10'})
        data_d10.text = new_traffic_density
        data_d11 = ET.SubElement(new_edge, f'{namespace}data', attrib={'key': 'd11'})
        data_d11.text = new_bandwidth
        data_d13 = ET.SubElement(new_edge, f'{namespace}data', attrib={'key': 'd13'})
        data_d13.text = new_data

        # Append the new edge to the graph element
        graph_element = self.root.find(f'{namespace}graph')
        graph_element.append(new_edge)
    
    def delete_edge(self, source_node_to_delete, target_node_to_delete):
    
        for edge in self.root.findall(".//{http://graphml.graphdrawing.org/xmlns}edge"):
            source_node = edge.attrib['source']
            target_node = edge.attrib['target']

            if source_node == source_node_to_delete and target_node == target_node_to_delete:
                edge_to_delete = edge
                break

        # Delete the edge if found
        if edge_to_delete is not None:
            # self.root.remove(edge_to_delete)
            graph_element = self.root.find(".//{http://graphml.graphdrawing.org/xmlns}graph")
            graph_element.remove(edge_to_delete)

    def update_weights_on_edge(self, source_node_to_update, target_node_to_update, new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth):
        # Iterate through all edges and update the specified edge's details

        ic(source_node_to_update, target_node_to_update)
        
        # edge_to_update = None
        for edge in self.root.findall(".//{http://graphml.graphdrawing.org/xmlns}edge"):

            source_node = edge.get('source')
            target_node = edge.get('target')
            
            if source_node == source_node_to_update and target_node == target_node_to_update:
                edge_to_update = edge
                break
            
        # Update the edge weights if the edge is found
        if edge_to_update is not None:
            edge_to_update.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d6']").text = new_speed
            edge_to_update.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d9']").text = new_time_duration
            edge_to_update.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d10']").text = new_traffic_density
            edge_to_update.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d11']").text = new_bandwidth
            edge_to_update.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d13']").text = new_data

            
    def get_details_from_edge(self, source_node_to_get_details, target_node_to_get_details):
        ic(source_node_to_get_details, target_node_to_get_details)
        
        # edge_to_update = None
        for edge in self.root.findall(".//{http://graphml.graphdrawing.org/xmlns}edge"):

            source_node = edge.get('source')
            target_node = edge.get('target')
            
            if source_node == source_node_to_get_details and target_node == target_node_to_get_details:
                edge_to_get_details = edge
                break
            
        # Update the edge weights if the edge is found
        if edge_to_get_details is not None:

            new_speed = edge_to_get_details.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d6']").text
            new_time_duration = edge_to_get_details.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d9']").text
            new_traffic_density = edge_to_get_details.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d10']").text
            new_bandwidth = edge_to_get_details.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d11']").text
            new_data = edge_to_get_details.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d13']").text
            
        return new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth
    
    def get_weights_from_nearest(self, source, target):
        source_nearest_points_list = self.find_all_targets(source)
        for nearest_point in source_nearest_points_list:
            try:
                new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth = self.get_details_from_edge(nearest_point, source)
                if new_speed != "None":
                    return new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth
            except:
                pass
            try:
                new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth = self.get_details_from_edge(source, nearest_point)
                if new_speed != "None":
                    return new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth
            except:
                pass
            
        target_nearest_points_list = self.find_all_targets(target)
        for nearest_point in target_nearest_points_list:
            try:
                new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth = self.get_details_from_edge(nearest_point, target)
                if new_speed != "None":
                    return new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth
            except:
                pass
            try:
                new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth = self.get_details_from_edge(target, nearest_point)
                if new_speed != "None":
                    return new_speed, new_time_duration, new_data, new_traffic_density, new_bandwidth
            except:
                pass

    def calculate_distance(self, latitude, longitude, next_latitude, next_longitude):
        distance = haversine((latitude, longitude),(next_latitude, next_longitude),unit=Unit.KILOMETERS)
        return distance

    def get_latitude_longitude(self, node_id):
        split_by_dot = node_id.split(".")
        longitude = split_by_dot[1][4:]+ "." +split_by_dot[2]
        latitude = split_by_dot[0]+ "." +split_by_dot[1][:4]
        return latitude, longitude
    
    def break_edge(self, source, target, sorted_nodes_in_list):

        source_index = sorted_nodes_in_list.index(source)
        target_index = sorted_nodes_in_list.index(target)
        ic("inside break_edge.")  
        if abs(target_index - source_index) > 1:
            ic({target_index - source_index})
            for i in range(source_index, target_index):
                total_distance = None
                total_distance = self.find_distance(source, target)#edge total distance
                ic(total_distance)
                total_time_duration = self.find_time_duration(source, target)
                ic(total_time_duration, type(total_time_duration))
                total_traffic_density = self.find_traffic_density(source, target)
                total_bandwidth = self.find_bandwidth(source, target)
                
                edge_found_immediate_node = self.check_if_edge_present_or_not(source, target)
                if edge_found_immediate_node:

                    current_node = sorted_nodes_in_list[i]
                    next_node = sorted_nodes_in_list[i+1]
                    ic(current_node, next_node)

                    split_by_dot = sorted_nodes_in_list[i].split(".")
                    longitude = split_by_dot[1][4:]+ "." +split_by_dot[2]

                    # split_by_dot = second_node_of_edge.split(".")
                    latitude = split_by_dot[0]+ "." +split_by_dot[1][:4]
                    ic(latitude)

                    latitude, longitude = self.get_latitude_longitude(current_node)
                    next_latitude, next_longitude = self.get_latitude_longitude(next_node)

                    latitude, longitude = float(latitude), float(longitude)
                    next_latitude, next_longitude = float(next_latitude), float(next_longitude)

                    distance = self.calculate_distance(latitude, longitude, next_latitude, next_longitude)

                    total_time_duration = float(total_time_duration)
                    total_distance = float(total_distance)

                    time_duration = (distance * total_time_duration)/total_distance

                    self.update_weights_on_edge(sorted_nodes_in_list[i], sorted_nodes_in_list[i+1], str(distance), new_time_duration = str(time_duration), new_data = "None", new_traffic_density = total_traffic_density, new_bandwidth = total_bandwidth)
                    self.d2_value[sorted_nodes_in_list[i]] = (self.d2_value[sorted_nodes_in_list[i]]) + 1
                    self.update_weights_on_edge(sorted_nodes_in_list[i+1], sorted_nodes_in_list[i], str(distance), new_time_duration = str(time_duration), new_data = "None", new_traffic_density= total_traffic_density, new_bandwidth = total_bandwidth)
                    self.d2_value[sorted_nodes_in_list[i+1]] = (self.d2_value[sorted_nodes_in_list[i+1]]) + 1                    

            edge_found = self.check_if_edge_present_or_not(source, target)
            if edge_found:
                self.delete_edge(source, target)
                self.d2_value[source] = (self.d2_value[source]) - 1
        else:
            ic("edge already present.")          
                
    def check_if_all_edges_have_weights(self, sorted_nodes_in_list):
        ic("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        for i in range(0, len(sorted_nodes_in_list)-1):    
            speed, time_duration, data, traffic_denstiy, bandwidth = self.get_details_from_edge(sorted_nodes_in_list[i], sorted_nodes_in_list[i+1])
            if speed == "None":
                ic(sorted_nodes_in_list[i], sorted_nodes_in_list[i+1])
                ic("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                get_new_speed_nearest, get_new_time_duration_nearest, get_new_data_nearest, get_new_traffic_density_nearest, get_new_bandwidth_nearest = self.get_weights_from_nearest(sorted_nodes_in_list[i], sorted_nodes_in_list[i+1])
                ic(get_new_speed_nearest, get_new_time_duration_nearest, get_new_data_nearest, get_new_traffic_density_nearest, get_new_bandwidth_nearest)
                self.update_weights_on_edge(sorted_nodes_in_list[i], sorted_nodes_in_list[i+1], get_new_speed_nearest, get_new_time_duration_nearest, get_new_data_nearest, get_new_traffic_density_nearest, get_new_bandwidth_nearest)
        sorted_nodes_in_list= sorted_nodes_in_list[::-1]
        for i in range(0, len(sorted_nodes_in_list)-1):    
            speed, time_duration, data, traffic_denstiy, bandwidth = self.get_details_from_edge(sorted_nodes_in_list[i], sorted_nodes_in_list[i+1])
            if speed == "None":
                ic(sorted_nodes_in_list[i], sorted_nodes_in_list[i+1])
                ic("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                # try:
                get_new_speed_nearest, get_new_time_duration_nearest, get_new_data_nearest, get_new_traffic_density_nearest, get_new_bandwidth_nearest = self.get_weights_from_nearest(sorted_nodes_in_list[i], sorted_nodes_in_list[i+1])
                ic(get_new_speed_nearest, get_new_time_duration_nearest, get_new_data_nearest, get_new_traffic_density_nearest, get_new_bandwidth_nearest)
                self.update_weights_on_edge(sorted_nodes_in_list[i], sorted_nodes_in_list[i+1], get_new_speed_nearest, get_new_time_duration_nearest, get_new_data_nearest, get_new_traffic_density_nearest, get_new_bandwidth_nearest)

            
    def find_all_targets(self, source_node_to_find_targets):
        targets = []
        for edge in self.root.findall(".//{http://graphml.graphdrawing.org/xmlns}edge"):
            source_node = edge.attrib['source']
            target_node = edge.attrib['target']

            if source_node == source_node_to_find_targets:
                targets.append(target_node)
        return targets
    
    def process(self, streight_roads_json_path, updated_graphml_file_path):
        
        with open(streight_roads_json_path, "r") as file:
            combine_nodes_dict = json.load(file)
            
        for combo_road in combine_nodes_dict:
            sorted_nodes_in_list = combine_nodes_dict[combo_road]

            ic(sorted_nodes_in_list)
            for i in range(0, len(sorted_nodes_in_list)-1):
                new_source = sorted_nodes_in_list[i]
                new_target = sorted_nodes_in_list[i+1]
                
                ic(new_source)
                ic(new_target)
                
                edge_present_status = self.check_if_edge_present_or_not(new_source, new_target)
                ic("---", edge_present_status)
                if not edge_present_status:
                    self.create_new_edge_with_details(new_source, new_target, "None", "None", "None", "None", "None")
                    ic(f"created new edge between {new_source} and {new_target}")
                else:
                    ic(f"{new_source} and {new_target} edge already present.")
                # # ic("--") 
                reverse_edge_present_status = self.check_if_edge_present_or_not(new_target, new_source)
                ic(reverse_edge_present_status)
                if not reverse_edge_present_status:
                    self.create_new_edge_with_details(new_target, new_source, "None", "None", "None", "None", "None")
                    ic(f"created new edge between {new_target} and {new_source}  ")
                else:
                    ic(f"{new_target} and {new_source} edge already present.")

            for node in sorted_nodes_in_list:

                targets = self.find_all_targets(node)
                targets.sort()

                if len(targets) == 1:
                    if targets[0] in sorted_nodes_in_list:
                        self.break_edge(node,targets[0], sorted_nodes_in_list)
                elif len(targets) == 0:
                    pass
                else:
                    for individual_target in targets:
                        if individual_target in sorted_nodes_in_list:
                            self.break_edge(node, individual_target, sorted_nodes_in_list)
                        else:
                            pass
            
            ic("reverse sorted loop.")         
            for node in sorted_nodes_in_list[::-1]:
                ic("+++" * 30)
                targets = self.find_all_targets(node)
                targets.sort()
                ic(node)
                ic(targets)
                if len(targets) == 1:
                    ic(targets[0])
                    if targets[0] in sorted_nodes_in_list:
                        ic("targets[0] in sorted_nodes_in_list")
                        self.break_edge(node, targets[0], sorted_nodes_in_list)
                elif len(targets) == 0:
                    pass
                else:
                    for individual_target in targets:
                        ic(individual_target)
                        if individual_target in sorted_nodes_in_list:
                            ic("individual_target in sorted_nodes_in_list")
                            self.break_edge(node, individual_target, sorted_nodes_in_list)
                        else:
                            ic("pass")
                            pass 
            
            print("^^^" * 30)
            print("^^^" * 30)
            print("^^^" * 30)
            self.check_if_all_edges_have_weights(sorted_nodes_in_list)
            key_d2_element = self.root.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d2']")
            key_d2_element.text = str(self.d2_value)
            
            # self.tree.write('modified_graph_updated_new_logic.graphml')
            self.tree.write(updated_graphml_file_path, encoding='utf-8', xml_declaration=True)
            
        # Find the 'd2' key data element
        key_d2_element = self.root.find(".//{http://graphml.graphdrawing.org/xmlns}data[@key='d2']")
        key_d2_element.text = str(self.d2_value)
        
        # self.tree.write('modified_graph_updated_new_logic.graphml')
        self.tree.write(updated_graphml_file_path, encoding='utf-8', xml_declaration=True)
         
if __name__ == "__main__":
    output_graphml_file_path = 'output_graphml_files/output_4242.graphml'
    streight_roads_json_path = 'streight_road_json/road_connection_4242.json'
    updated_graphml_file_path = 'updated_graphml_files/updated_4242.graphml'
    # user_id = 1270
    update_graphml_obj = UPDATEGRAPHML(output_graphml_file_path)
    update_graphml_obj.process(streight_roads_json_path, updated_graphml_file_path)
    print("--")