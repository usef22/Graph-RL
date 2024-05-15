from convert_one_user_graph_from_csv import INDIVIDUALDATA
from get_edges_connected_to_node import NUMBEROFEDGES
from convert_csv_to_graph import CSVTOGRAPH
from plot_graph import save_graph_plot
import pandas as pd
import os
from config import *
from combine_nodes import COMBINENODES
from road_connections import ROADDETAILS
from update_graphml import UPDATEGRAPHML
from convert_graph_to_csv import graphml_to_csv

def main(original_csv_file_path, user_id):
    """
    Main function to process a user's data and create and analyze the corresponding graph.

    Args:
    - original_csv_file_path (str): Path to the original CSV file containing the user data.
    - user_id (int): ID of the user for whom the processing is to be done.

    Returns:
    - None
    """
    # Create necessary directories if they do not exist
    if not os.path.isdir(INDIVIDUAL_CSV_FILES_DIR_PATH):
        os.mkdir(INDIVIDUAL_CSV_FILES_DIR_PATH)
    if not os.path.isdir(EDGES_CONNECTION_COUNT_JSON_DIR):
        os.mkdir(EDGES_CONNECTION_COUNT_JSON_DIR)
    if not os.path.isdir(INITIAL_GRAPHML_DIR):
        os.mkdir(INITIAL_GRAPHML_DIR)
    if not os.path.isdir(STRAIGHT_ROAD_JSON_DIR_PATH):
        os.mkdir(STRAIGHT_ROAD_JSON_DIR_PATH)
    if not os.path.isdir(UPDATED_GRAPHML_DIR_PATH):
        os.mkdir(UPDATED_GRAPHML_DIR_PATH)
    if not os.path.isdir(PLOT_USER_GRAPH_DIR):
        os.mkdir(PLOT_USER_GRAPH_DIR)
    if not os.path.isdir(TIME_DURATION_CSV):
        os.mkdir(TIME_DURATION_CSV)

    #######################################################################################################################
    # Step 1: Process the individual data of the user
    df = pd.read_csv(original_csv_file_path)
    user_id_list = df["nid"].unique()
    print("--" * 20)
    
    #######################################################################################################################
    # Step 2: Generate individual CSV file for the user
    output_csv_path = f"{INDIVIDUAL_CSV_FILES_DIR_PATH}/driver_{user_id}.csv"
    individualdata_obj = INDIVIDUALDATA()
    individualdata_obj.process(original_csv_file_path, output_csv_path, user_id)
    #######################################################################################################################
    print("--" * 20)
    
    # Step 3: Count the number of edges connected to each node
    input_csv_file_path = output_csv_path
    numberofedges_obj = NUMBEROFEDGES()
    json_file_path = f"{EDGES_CONNECTION_COUNT_JSON_DIR}/edges_connection_{user_id}.json"
    numberofedges_obj.process(input_csv_file_path, json_file_path)
    #######################################################################################################################
    print("--" * 20)
    
    # Step 4: Convert the CSV file to a GraphML file
    input_csv_file_path = output_csv_path
    output_graphml_file_path = f"{INITIAL_GRAPHML_DIR}/output_{user_id}.graphml"
    csvtograph_obj = CSVTOGRAPH()
    csvtograph_obj.process(input_csv_file_path, json_file_path, output_graphml_file_path)
    #######################################################################################################################
    print("--" * 20)
    
    # Step 5: Extract straight road connections
    csv_file_path= f"{INDIVIDUAL_CSV_FILES_DIR_PATH}/driver_{user_id}.csv"
    streight_roads_json_path = f"{STRAIGHT_ROAD_JSON_DIR_PATH}/road_connection_{user_id}.json"
    road_details_obj = ROADDETAILS()
    road_details_obj.process(csv_file_path, streight_roads_json_path)
    #######################################################################################################################
    print("--" * 20)
    
    # Step 6: Combine nodes if needed
    combine_nodes_obj = COMBINENODES()
    combine_nodes_obj.process(streight_roads_json_path)   
    #######################################################################################################################
    print("--" * 20)
    
    # Step 7: Update the GraphML file based on road details
    updated_graphml_file_path = f"{UPDATED_GRAPHML_DIR_PATH}/updated_{user_id}.graphml"
    update_graphml_obj = UPDATEGRAPHML(output_graphml_file_path)
    update_graphml_obj.process(streight_roads_json_path, updated_graphml_file_path)
    #######################################################################################################################
    print("--" * 20)
    
    # Step 8: Save a plot of the user's graph
    save_plot_image_path = f"plot_of_a_user_graph/output_{user_id}.png"
    save_graph_plot(updated_graphml_file_path, save_plot_image_path)
    #######################################################################################################################
    print("--" * 20)
    
    # Step 9: Convert the updated GraphML file to a CSV file with time durations
    input_graphml_file = updated_graphml_file_path
    output_csv_file = f"{TIME_DURATION_CSV}/driver_{user_id}.csv"
    graphml_to_csv(input_graphml_file, output_csv_file)
    #######################################################################################################################

if __name__ == "__main__":
    user_id = 1455 
    original_csv_file_path = "beijing_trace90_2.csv"
    main(original_csv_file_path, user_id)
