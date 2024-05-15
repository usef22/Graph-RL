import csv

def get_csv_rows_count(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        # Use len() to get the total number of rows
        row_count = len(list(csv_reader))
    return row_count

# Replace 'your_file.csv' with the actual path to your CSV file
file_path = 'individual_user_dataframe/driver_1400.csv'
total_rows = get_csv_rows_count(file_path)

print(f'Total number of rows in the CSV file: {total_rows}')
