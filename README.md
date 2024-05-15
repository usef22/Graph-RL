# Find Fastest and Highest bandwidth path

### This code is tested on Python version 3.8.10

### Install the requirement for the project and activate the environment

```
pip install -r requirement.txt
```

## For Preprocessing 

```
cd final/preprocessing
```

### now start preprocessing using below command.

#### change user_id according requirement in the main.py file

```
python main.py
```
## For Training 

```
cd final/training
```

### For Finding the fastest path with giving bandwidth as reward.

```
python fastest_path_with_bandwidth.py
```
### For Finding the fastest path without giving bandwidth as reward.

```
python fastest_path_with_bandwidth.py
```
### For Finding the fastest path without giving any reward.

```
python fastest_path_without_any_reward.py
```

## Notes 

## For Preprocessing.

1] After running main.py file, you will find updated graphml file in updated_graphml_files directory. 

2] You can find the final graph plot in plot_of_a_user_graph directory. 

## For training.

1] In config.py file you will find the static variable that have used during the training. You can change the reward, penalty, plot size in this file. 

2] For training, you can change perameter like start_state, end_state, num_epoch, user_id, total_data_to_be_transfer in the training file. user_id would be the one that you have use during the preprocessing. 

3] After the training, you will find the final plot ( epoch vs minimum time duration) in the epoch_vs_cost_plots directory. 

4] If RL-Agent able to find the fastest path then in the output directory, you will find the path between to nodes in the graph. 
