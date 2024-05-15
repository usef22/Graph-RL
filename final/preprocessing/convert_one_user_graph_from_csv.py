import pandas as pd
from haversine import haversine, Unit
from datetime import datetime
from icecream import ic
from delete_edge_between_two_user import delete_edge_between_two_users_from_csv
from config import *
import numpy as np

class INDIVIDUALDATA():
    
    def __init__(self):
        self.first_entry_status = True

    def add_traffic_density_and_bandwidth_in_csv(self, output_csv_path):
        # Load the CSV file into a DataFrame
        data = pd.read_csv(output_csv_path)

        traffic_dens = (data['time_difference'] / 3600) / data['distance']
        
        # Calculate traffic density
        data['traffic_density'] = traffic_dens

        data['bandwidth'] = np.random.uniform(0.25, 1, size=len(data)) + traffic_dens
        
        # Save the updated DataFrame to another CSV file
        data.to_csv(output_csv_path, index=False)

    def remove_last_row_of_nid(self, output_csv_path):
        """
        Remove the last row of each unique 'nid' in the DataFrame.

        Args:
        - output_csv_path (str): Path to the CSV file.

        Returns:
        - None
        """
        df = pd.read_csv(output_csv_path)
        last_nid = None
        for index, row in df.iterrows():
            current_nid = row['nid']
            if current_nid != last_nid:
                if last_nid is not None:
                    df = df.drop(last_index)
            last_nid = current_nid
            last_index = index
        df.to_csv(output_csv_path, index=False)

    def timeTakenToCoverEdge(self, time_1, time_2):
        """
        Calculate the time taken to cover an edge.

        Args:
        - time_1 (str): Timestamp of the first point.
        - time_2 (str): Timestamp of the second point.

        Returns:
        - float: Time difference in seconds.
        """
        datetime_obj1 = datetime.strptime(time_1, '%Y-%m-%d %H:%M:%S')
        datetime_obj2 = datetime.strptime(time_2, '%Y-%m-%d %H:%M:%S')
        time_difference = abs((datetime_obj1 - datetime_obj2).total_seconds())
        return time_difference
    
    def addZerosIfNeeded(self, float_number):
        """
        Add zeros to the decimal part of a float number if needed.

        Args:
        - float_number (float): Input float number.

        Returns:
        - str: Float as a string with added zeros.
        """
        length_of_digits_after_decimal = len(str(float_number).split(".")[-1])
        if length_of_digits_after_decimal < 4:
            float_string = str(float_number) + ("0" *(4-length_of_digits_after_decimal))
        if length_of_digits_after_decimal >= 4:
            rounded_number = round(float_number, 4)
            float_string = str(rounded_number)
        return float_string
    
    def createUniqueNodeIdColumnInsideDataframe(self, df):
        """
        Create a new column 'unique_node_id' in the DataFrame.

        Args:
        - df (pd.DataFrame): Input DataFrame.

        Returns:
        - pd.DataFrame: DataFrame with the new 'unique_node_id' column.
        """
        df['latitude_new'] = df['latitude'].apply(self.addZerosIfNeeded)
        df['longitude_new'] = df['longitude'].apply(self.addZerosIfNeeded)
        df.loc[:, "unique_node_id"] = df["latitude_new"] + df["longitude_new"]
        df.loc[:, 'unique_node_id'] = df['unique_node_id']
        return df

    def calculateDisplacementSpeed(self, point_1, point_2, time_1, time_2):
        """
        Calculate displacement speed between two points.

        Args:
        - point_1 (tuple): Latitude and longitude of the first point.
        - point_2 (tuple): Latitude and longitude of the second point.
        - time_1 (str): Timestamp of the first point.
        - time_2 (str): Timestamp of the second point.

        Returns:
        - float: Displacement speed in kilometers per hour.
        """
        distance = haversine(point_1, point_2, unit=Unit.KILOMETERS)
        datetime_obj1 = datetime.strptime(time_1, '%Y-%m-%d %H:%M:%S')
        datetime_obj2 = datetime.strptime(time_2, '%Y-%m-%d %H:%M:%S')

        # Calculate the time difference in seconds
        time_difference = abs((datetime_obj1 - datetime_obj2).total_seconds())
        if time_difference > 0:
            displacement_speed_kmph = distance / (time_difference / 3600)
        else:
            displacement_speed_kmph = 0
        return displacement_speed_kmph

    def removeZeroDisplacementRows(self, output_csv_path):
        """
        Remove rows with zero displacement speed from the DataFrame.

        Args:
        - output_csv_path (str): Path to the CSV file.

        Returns:
        - None
        """
        df = pd.read_csv(output_csv_path)
        df = df[df['displacement_speed'] != 0.0]
        df.to_csv(output_csv_path, index=False)

    def calculateTimeDifference(self, output_csv_path):
        """
        Calculate time difference and displacement speed for each edge in the DataFrame.

        Args:
        - output_csv_path (str): Path to the CSV file.

        Returns:
        - None
        """
        df = pd.read_csv(output_csv_path)
        self.first_entry_status = True
        initial_index = 0
        for index, row in df.iterrows():
            if self.first_entry_status:
                self.first_entry_status = False
                initial_index = index
            new_index = index - initial_index
            if new_index + 1 < len(df):
                row = df.iloc[new_index]
                next_row = df.iloc[new_index + 1] 

                # Extract relevant columns
                lat1, lon1 = row['latitude'], row['longitude']
                lat2, lon2 = next_row['latitude'], next_row['longitude']
                unique_node_id_1, unique_node_id_2 = row["unique_node_id"], next_row['unique_node_id']

                # Calculate displacement_speed
                displacement_speed = self.calculateDisplacementSpeed(
                    (lat1, lon1),
                    (lat2, lon2),
                    row['date'],
                    next_row['date']
                )
                df.at[index, 'displacement_speed'] = displacement_speed
                time_difference = self.timeTakenToCoverEdge(row['date'], next_row['date'])
                df.at[new_index, 'time_difference'] = time_difference
        df = df.dropna()       
        df.to_csv(output_csv_path, index=False)
        
    def is_float_in_range(self, value, lower_limit, upper_limit):
        """
        Check if a float value is within a specified range.

        Args:
        - value (float): Float value to be checked.
        - lower_limit (float): Lower limit of the range.
        - upper_limit (float): Upper limit of the range.

        Returns:
        - bool: True if the value is within the range, False otherwise.
        """  
        return lower_limit <= value <= upper_limit  
    
    def move_node_if_needed(self, filtered_rows):
        """
        Move nodes in the DataFrame if needed based on a specified range.

        Args:
        - filtered_rows (pd.DataFrame): DataFrame containing rows to be filtered.

        Returns:
        - pd.DataFrame: DataFrame with nodes moved if needed.
        """
        # NEARBY_NODE_LIMIT = 0.0049
        initial_index = 0
        for index, row in filtered_rows.iterrows():
            if self.first_entry_status:
                self.first_entry_status = False
                initial_index = index
            new_index = index - initial_index

            if new_index + 1 < len(filtered_rows):
                # Get the next row
                row = filtered_rows.iloc[new_index]
                next_row = filtered_rows.iloc[new_index + 1]
                primary_node_id_latitude, primary_node_id_longitude = row['latitude'], row['longitude']
                secondary_node_id_latitude, secondary_node_id_longitude = next_row['latitude'], next_row['longitude']
        
                latitude_range_check_status = self.is_float_in_range(
                    secondary_node_id_latitude,
                    primary_node_id_latitude - NEARBY_NODE_LIMIT,
                    primary_node_id_latitude + NEARBY_NODE_LIMIT
                )
                longitude_range_check_status = self.is_float_in_range(
                    secondary_node_id_longitude,
                    primary_node_id_longitude - NEARBY_NODE_LIMIT,
                    primary_node_id_longitude + NEARBY_NODE_LIMIT
                )
                
                if latitude_range_check_status:
                    filtered_rows.at[index + 1, 'latitude'] = primary_node_id_latitude
                elif longitude_range_check_status:
                    filtered_rows.at[index + 1, 'longitude'] = primary_node_id_longitude
                elif longitude_range_check_status and latitude_range_check_status:
                    filtered_rows.at[index + 1, 'latitude'] = primary_node_id_latitude
                    filtered_rows.at[index + 1, 'longitude'] = primary_node_id_longitude
                else:
                    pass
        return filtered_rows

    def changeInLastElemet(self, df_group):
        """
        Modify the last element of each group based on specific criteria.

        Args:
        - df_group (pd.DataFrame): Grouped DataFrame.

        Returns:
        - pd.DataFrame: Modified DataFrame.
        """
        # print(df_group[-5:])
        # if len(df_group) <= 1:
        #     ic(df_group.index)
        #     ic(df_group)
        #     a = input()
        if len(df_group) >= 2:
            unique_node_last = df_group.at[df_group.index[-1], "unique_node_id"]
            ic(unique_node_last)
            unique_node_2nd_last = df_group.at[df_group.index[-2], "unique_node_id"]
            ic(unique_node_2nd_last)
            displacement_speed_2nd_last = df_group.at[df_group.index[-2], "displacement_speed"]
            ic(displacement_speed_2nd_last)
            distance_2nd_last = df_group.at[df_group.index[-2], "distance"]
        
            ic(df_group.at[df_group.index[-1], "edge_pair"])
            ic(df_group.at[df_group.index[-1], "displacement_speed"])
            df_group.at[df_group.index[-1], "edge_pair"] = f"{unique_node_last}_{unique_node_2nd_last}"
            df_group.at[df_group.index[-1], "displacement_speed"] = displacement_speed_2nd_last
            df_group.at[df_group.index[-1], "distance"] = distance_2nd_last
            df_group.at[df_group.index[-1], "next_unique_node_id"] = unique_node_2nd_last
            return df_group
    
    def apply_function_to_groups(self, df, group_column):
        """
        Apply a function to each group of a DataFrame based on a specified column.

        Args:
        - df (pd.DataFrame): Input DataFrame.
        - group_column (str): Column used for grouping.

        Returns:
        - pd.DataFrame: Modified DataFrame.
        """
        grouped_df = df.groupby(group_column)
        modified_df = grouped_df.apply(self.changeInLastElemet)
        modified_df.reset_index(drop=True, inplace=True)
        return modified_df
            
    def process(self, csv_file_path: str, output_csv_path: str, user_id: int):
        """
        Process the input CSV file, perform various operations, and save the output.

        Args:
        - csv_file_path (str): Path to the input CSV file.
        - output_csv_path (str): Path to save the processed CSV file.
        - user_id (int): User ID for filtering data.

        Returns:
        - None
        """
        df = pd.read_csv(csv_file_path)
        filtered_rows = df[df['nid'] <= user_id]
        filtered_rows = self.move_node_if_needed(filtered_rows)
        filtered_rows = self.createUniqueNodeIdColumnInsideDataframe(filtered_rows)        
        filtered_rows = filtered_rows.reset_index()
        
        filtered_rows['next_latitude'] = filtered_rows['latitude'].shift(-1)
        filtered_rows['next_longitude'] = filtered_rows['longitude'].shift(-1)
        filtered_rows['next_date'] = filtered_rows['date'].shift(-1)
        filtered_rows['next_unique_node_id'] = filtered_rows['unique_node_id'].shift(-1)
        
        filtered_rows = filtered_rows.dropna()
        # Apply the function to create a new column
        filtered_rows['displacement_speed'] = filtered_rows.apply(
            lambda row: self.calculateDisplacementSpeed(
                (row['latitude'], row['longitude']),
                (row['next_latitude'], row['next_longitude']),
                row['date'],
                row['next_date']
            ),
            axis=1
        )
        filtered_rows['edge_pair'] = filtered_rows['unique_node_id'] + "_" + filtered_rows['next_unique_node_id']

        filtered_rows['distance'] = filtered_rows.apply(
            lambda row: haversine((row['latitude'], row['longitude']),
                                  (row['next_latitude'], row['next_longitude']),
                                  unit=Unit.KILOMETERS),
            axis=1
        )

        filtered_rows = filtered_rows.drop('next_latitude', axis=1)
        filtered_rows = filtered_rows.drop('next_longitude', axis=1)
        filtered_rows = filtered_rows.drop('next_date', axis=1)
        filtered_rows = filtered_rows.drop("index", axis=1)
        filtered_rows = filtered_rows.drop("latitude_new", axis = 1)
        filtered_rows = filtered_rows.drop("longitude_new", axis = 1)

        filtered_rows.to_csv(output_csv_path, index=False)
        filtered_rows = filtered_rows.dropna()

        self.calculateTimeDifference(output_csv_path)
        self.removeZeroDisplacementRows(output_csv_path)
        self.remove_last_row_of_nid(output_csv_path)
        # delete_edge_between_two_users_from_csv(output_csv_path, output_csv_path)
        
        df = pd.read_csv(output_csv_path)
        modified_df = self.apply_function_to_groups(df, 'nid')
        modified_df.to_csv(output_csv_path, index=False)
        self.add_traffic_density_and_bandwidth_in_csv(output_csv_path)

if __name__ == "__main__":
    csv_file_path = "beijing_trace90_2.csv"
    output_csv_path = "individual_user_dataframe/1.csv"
    user_id = 1280
    individualdata_obj = INDIVIDUALDATA()
    individualdata_obj.process(csv_file_path, output_csv_path,  user_id)
