import csv
import os


max_num = 100000
dir_name = f"sudoku_puzzle_benchmark_{max_num}"
# Create directory if it doesn't exist
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# Open the CSV file
with open("sudoku.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header

    # Loop through the first 1000 rows
    for i, row in enumerate(csv_reader):
        if i == max_num:
            break

        # Write each quiz to a new file
        with open(f"{dir_name}/quiz_{i+1}.txt", "w") as f:
            f.write(row[0])  # Assuming the quiz is in the first column
