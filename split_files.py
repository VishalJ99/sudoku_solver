input_file = input("Enter the path of the input text file: ")

with open(input_file, "r") as file:
    lines = file.readlines()

for i, line in enumerate(lines):
    output_file = f"challenging_sudoku_{i}.txt"
    with open(output_file, "w") as file:
        file.write(line)
