import pandas as pd

def delete_edge_between_two_users_from_csv(csv_path, output_csv_path):
    """
    Delete edges between consecutive nodes of each unique 'nid' in the CSV file.

    Args:
    - csv_path (str): Path to the input CSV file.
    - output_csv_path (str): Path to save the modified CSV file.

    Returns:
    - None
    """
    df = pd.read_csv(csv_path)
    rows_to_delete = []
    
    # Identify the indices of rows to be deleted
    for nid in df['nid'].unique():
        index_to_delete = df[df['nid'] == nid].index[0]
        rows_to_delete.append(index_to_delete)
        
    # Remove the identified rows
    df = df.drop(rows_to_delete[1:])
    df = df.reset_index(drop=True)
    
    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    csv_path = 'driver_1300.csv'
    output_csv_path = 'modified_file.csv'
    delete_edge_between_two_users_from_csv(csv_path, output_csv_path)
