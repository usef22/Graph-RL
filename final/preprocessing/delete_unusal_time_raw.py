from icecream import ic
import pandas as pd

def delete_raw_where_time_taken_more_than_usual(output_csv_path):

    # Read the CSV file into a DataFrame
    df = pd.read_csv(output_csv_path)

    condition = (df['distance'] < 2) | (df['time_difference'] < 200)
    df_filtered = df[condition]
    
    # Write the filtered data to a new CSV file
    df_filtered.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    delete_raw_where_time_taken_more_than_usual("individual_user_dataframe/driver_2200.csv")