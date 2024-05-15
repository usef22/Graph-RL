import random
import numpy as np
from icecream import ic
from config import *
import pandas as pd
import math
import wandb
from utility import *

# Set seeds for reproducibility in random and numpy
random.seed(100)
np.random.seed(50) 

###################################################################################################################

def plot_final_graph(min_epochs, min_costs, start_state, end_state, epoch):
    plt.plot(min_epochs, min_costs)
    plt.xlabel('Epoch')
    plt.ylabel('Minimum Time')
    plt.title('Minimum Time vs Epoch (Without any reward)')
    plt.savefig(f"epoch_vs_cost_plots/fastest_path_without_any_reward_{start_state}_{end_state}_{epoch}.png")

def q_learning(df, total_data_to_be_transfer, D, node_indices_with_x_y, num_nodes, start_state, end_state, num_epoch, gamma, epsilon_start, epsilon_end, alpha, save_interval):
    """
    Perform Q-learning to find the shortest path in a graph.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing edge information, including time differences.
    - D (numpy.ndarray): Distance matrix representing the graph.
    - node_indices_with_x_y (dict): Dictionary containing node indices and corresponding x, y coordinates.
    - num_nodes (int): Total number of nodes in the graph.
    - start_state (int): Index of the start state in the graph.
    - end_state (int): Index of the end state in the graph.
    - num_epoch (int): Number of epochs for training the Q-learning agent.
    - gamma (float): Discount factor for future rewards.
    - epsilon_start (float): Initial exploration-exploitation trade-off parameter.
    - epsilon_end (float): Final exploration-exploitation trade-off parameter.
    - alpha (float): Learning rate for updating Q-values.
    - save_interval (int): Interval for saving plots during training.

    Returns:
    - q (numpy.ndarray): Updated Q-values matrix.
    """
    global MIN_COST 

    ic(q_learning)
    # input()
    
    q = np.zeros_like(D)
    shortest_path_len = num_nodes
    final_path = []
    min_costs = []  
    min_epochs = [] 

    node_detail_dict = {v['index']: k for k, v in node_indices_with_x_y.items()}
    
    epsilon = epsilon_start
    stuck_counter = 0
    decay_rate = -math.log(epsilon_end / epsilon_start) / num_epoch
    
    for epoch in range(1, num_epoch + 1):
        
        agent_data = total_data_to_be_transfer
        data_trasfer_flag = True
        
        reward = 0
        s_cur = start_state
        path = [s_cur]

        # Annealing epsilon
        epsilon = epsilon_end + (epsilon_start - epsilon_end) * math.exp(-decay_rate * epoch)

        while s_cur != end_state:
            s_next = epsilon_greedy(s_cur, q, D, epsilon)

            current_node_id = node_detail_dict[s_cur]
            next_node_id = node_detail_dict[s_next]

            filtered_df = df[(df['source'] == current_node_id) & (df['target'] == next_node_id)]

            traffic_density = filtered_df['traffic_density'].tolist()
            bandwidth = filtered_df['bandwidth'].tolist()

            if len(traffic_density) == 1:
                traffic_dens = traffic_density[0]
            else:
                traffic_dens = sum(traffic_density) / len(traffic_density)

            if len(bandwidth) == 1:
                band_width = bandwidth[0]
            else:
                band_width = sum(bandwidth) / len(bandwidth)

            data_transfer = (band_width/traffic_dens) * (D[s_cur][s_next])
            agent_data = agent_data - data_transfer

            if agent_data <= 0 and data_trasfer_flag:
                # ic(">>>>>> All Data is transfered")
                # ic(epoch)
                data_transfer_reward = DATA_TRANSFER_REWARD
                data_trasfer_flag = False
            else:
                data_transfer_reward = 0

            reward = data_transfer_reward
            # reward = -(D[s_cur][s_next]) + data_transfer_reward
            # reward = -2*(D[s_cur][s_next]) + data_transfer_reward



            if s_next == end_state:
                reward = GOAL_REWARD + data_transfer_reward
            elif s_next in path:
                reward = PENALTY_FOR_REVISIT_THE_NODE + data_transfer_reward
                stuck_counter += 1
            else:
                stuck_counter = 0

            if stuck_counter >= MAX_STUCK_LIMIT:
                reward = PENALTY_FOR_STUCK_BETWEEN_NODES + data_transfer_reward
                break

            q[s_cur, s_next] += alpha * (reward + gamma * min(q[s_next]) - q[s_cur, s_next])
            s_cur = s_next
            path.append(s_cur)
                

        cost = calculate_cost(path, D)

        min_costs.append(cost)
        min_epochs.append(epoch)

        # Update minimum cost and shortest path if a better path is found
        if cost < MIN_COST and path[-1] == end_state:
            ic(cost, epoch)
            # min_costs.append(cost)
            # min_epochs.append(epoch)
            MIN_COST = cost
            shortest_path_len = len(path)
            final_path = path

        wandb.log({"cost": cost})  # Log cost directly to wandb

        ic(epoch, " ---> ", len(path))

    if not final_path:
        ic("WITH THE EXISTING DATA AGENT COULD NOT FIND THE SHORTEST PATH.")
        plot_final_graph(min_epochs, min_costs, start_state, end_state, epoch)
    else:
        print("Final Path:", final_path)
        print("Path Length:", len(final_path))
        print("Fastest Path length:", shortest_path_len)
        ic(MIN_COST)

        plot_final_graph(min_epochs, min_costs, start_state, end_state, epoch)

        # Save the final plot
        plot_graph(D, node_indices_with_x_y, start_state, end_state, final_path, epoch, cal_distance)
        return q, min_costs, min_epochs

def main(user_id, start_state, end_state, graphml_file_path, csv_file_path):
    
    # Read the time duration data from the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Calculate the total number of nodes in the graph
    number_of_total_nodes = calculate_total_number_of_nodes(graphml_file_path)

    ic(number_of_total_nodes)

    if number_of_total_nodes < start_state:
        print("number_of_total_nodes : ",number_of_total_nodes)
        print("start_state : ",start_state," is more than total number of nodes", number_of_total_nodes)
    elif number_of_total_nodes < end_state:
        print("end_state : ",end_state," is more than total number of nodes", number_of_total_nodes)
    else:
        # Convert the GraphML file to an adjacency matrix and obtain node indices with x, y coordinates
        D, node_indices_with_x_y, num_nodes = graph_to_matrix(graphml_file_path, number_of_total_nodes=number_of_total_nodes)

        trained_q_values = q_learning(df, total_data_to_be_transfer, D, node_indices_with_x_y, num_nodes, start_state=start_state, end_state=end_state, num_epoch=num_epoch, gamma=gamma, epsilon_start=epsilon_start, epsilon_end=epsilon_end, alpha=alpha, save_interval=save_interval)

if __name__ == '__main__':
    gamma = 0.8
    epsilon_start = 1
    epsilon_end = 0.01
    alpha = 0.0001
    save_interval = 5000

    ##################################################################################################

    create_directory_if_not_exists("output")
    create_directory_if_not_exists("epoch_vs_cost_plots")

    start_state = 25
    end_state = 50
    num_epoch = 500000
    user_id = 1455
    total_data_to_be_transfer = 100  # In Bits

    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the workspace root directory (parent directory of the current file)
    workspace_dir = os.path.dirname(current_dir)

    # Construct the absolute path to the GraphML file
    graphml_file_path = os.path.join(workspace_dir, "preprocessing", "updated_graphml_files", f"updated_{user_id}.graphml")
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the workspace root directory (parent directory of the current file)
    workspace_dir = os.path.dirname(current_dir)

    # Construct the absolute path to the CSV file
    csv_file_path = os.path.join(workspace_dir, "preprocessing", "time_duration_csv", f"driver_{user_id}.csv")

    # WANDB
    # Loop for multiple runs
    for run in range(2):  # Adjust the number of runs as needed

        wandb.init(project="new_test1")
        config = wandb.config
        config.Agent = "Traffic-Unaware"
        config.Start = start_state
        config.End = end_state
        config.data = total_data_to_be_transfer
        config.epoch = num_epoch

        # Call main and get Q-values and cost tracking
        trained_q_values = main(user_id, start_state, end_state, graphml_file_path, csv_file_path)

        wandb.finish()  # Finish the run before starting a new one

    ##################################################################################################
