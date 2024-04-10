# Sudoku Solver CLI

## Introduction

This repository contains a command-line interface (CLI) tool for solving Sudoku puzzles. It offers robust functionality to solve Sudoku puzzles either individually or in batch mode. The tool supports various input formats and Sudoku board layouts and is designed to be extensible for new formats and solvers.

## Features

- **Single and Batch Processing**: Solve individual puzzles or process multiple files in a directory.
- **Support for Various Formats**: Accepts inputs as file paths or direct Sudoku board strings.
- **Flexible Output Options**: Customise output paths and formats for the solved Sudoku boards.
- **Statistics Generation**: Option to generate and save statistics about the solving process.
- **Extensible**: Easily extendable to incorporate new input formats and Sudoku solving algorithms.

## Installation

To install this Sudoku Solver, clone this repository and navigate to the cloned directory and build the docker image.

```
git clone git@github.com:VishalJ99/sudoku_solver.git
cd sudoku_solver
docker build -t sudoku_solver .
```

## Expected Input Format
This programme can accept text files for sudoku board inputs in two formats: grid and flat.

### Grid Format
The grid format is the standard format specified for the coursework.
A sudoku board specified with a 9x9 grid of numbers with zero representing unknown values and `|`,`+`,`-` separating cells and , i.e.:
```
$ cat grid_input.txt
000|007|000
000|009|504
000|050|169
---+---+---
080|000|305
075|000|290
406|000|080
---+---+---
762|080|000
103|900|000
000|600|000
```
This programme also accepts variants of this grid format that do not require digit alterations. A variant is defined as a grid format which has, after removing white space, empty lines and replacing any dots with zeros, exactly 11 rows. With rows 1-3, 5-7 and 9-11 containing triplets of digits seperated by any non numeric character. It must also have no digits rows 4 and 8 for those
rows to be considered a valid seperator. For example, the following is also an acceptable grid format

```
$ cat correctable_grid_input.txt
,000,007,000,
000,00 9,504
000,050,16 9
--!@#$%^&*(((------
0 80,000,305
075,000,2 90
406,000,08 0
---*&^%$$$$$$$$%^&------
762, 080,000
1 03P9 00P000
000Q6 00,00 0
```

### Flat Format

The flat format is a single line of 81 digits with zeros or .'s representing unknown values. The digits are read from left to right and top to bottom. For example, the following is a valid flat format

```
$ cat flat_input.txt
004300209005009001070060043006002087190007400050083000600000105003508690042910300
```

No corrections are made for invalid flat formats. If the input is not a valid flat format, the programme will throw an error.



## Usage
```
docker run -v $(pwd):/C1_VJ279 sudoku_solver python src/main.py <sudoku_input.txt> [options]
```

### Command Line Arguments
Please see below for what cli arguments are available in `main.py`

```
sudoku_input: Path to the Sudoku input file or directory of files (for batch mode). Can also be a Sudoku board string if `--input_type` is set to `string`.

--batch: Enable batch mode to pass directory of boards as input and process multiple files.

--input_type: Specifies the type of input (filepath or string). filepath is default.

--input_format_type: Format of the Sudoku board in the input (grid or flat). grid is default.

--output_path: Path to save the solved Sudoku board.

--output_format_type: Format of the solved Sudoku board in the output file. grid is default.

--stats_path: Path to save the statistics about the solving process.

--timeout: Maximum time allowed for solving a single board. 60 seconds is default.

--solver: Solver to use for solving the Sudoku board ('bt_basic' or 'bt_easiest_first'), 'bt_basic' is default.
```

### Hello World Example
To run these examples please ensure your working directory is the root directory of the repository.

Example of basic usage for single file
```
docker run sudoku_solver python src/main.py test/sudoku_solver_test_boards/easy_1.txt
```

Example of basic usage for string input

```
docker run sudoku_solver python src/main.py \
  "004300209005009001070060043006002087190007400050083000600000105003508690042910300" \
  --input_type string \
  --input_format_type flat
```

Example of basic usage for batch mode

```
docker run -v $(pwd):/C1_VJ279 sudoku_solver python src/main.py benchmark_board_sets/easy_100 --batch --input_format_type flat
```

Example of advanced usage for single file (may take 2-3 minutes to run)
```
docker run --rm -it \
  -v $(pwd):/C1_VJ279 \
  sudoku_solver python src/main.py benchmark_board_sets/hard_100 \
  --batch \
  --input_format_type flat \
  --output_format_type grid \
  --solver bt_easiest_first \
  --output_path hello_world/hard_100 \
  --stats_path hello_world/hard_100/hard_100_run_stats.txt \
  --timeout 30
```

## Building the autodocumentation
Ensure your working directory is the root directory of the repository
```
docker run -it -v $(pwd):/C1_VJ279 sudoku_solver
# in docker container shell
cd docs
make html
exit
# in local shell
open docs/_build/html/index.html # windows: start docs/_build/html/index.html
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
