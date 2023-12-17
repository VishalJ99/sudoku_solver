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

```bash
git clone git@gitlab.developers.cam.ac.uk:phy/data-intensive-science-mphil/c1_assessment/vj279.git
cd vj279
docker build -t c1_vj279 .
```

## Usage
```
docker run -v $(pwd):/C1_VJ279 c1_vj279 python src/main.py <sudoku_input.txt> [options]
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
docker run c1_vj279 python src/main.py test/sudoku_solver_test_boards/easy_1.txt
```

Example of basic usage for string input

```
docker run c1_vj279 python src/main.py \
  "004300209005009001070060043006002087190007400050083000600000105003508690042910300" \
  --input_type string \
  --input_format_type flat
```

Example of basic usage for batch mode

```
docker run -v $(pwd):/C1_VJ279 c1_vj279 python src/main.py benchmark_board_sets/easy_100 --batch --input_format_type flat
```

Example of advanced usage for single file (may take 2-3 minutes to run)
```
docker run --rm -it \
  -v $(pwd):/C1_VJ279 \
  c1_vj279 python src/main.py benchmark_board_sets/hard_100 \
  --batch \
  --input_format_type flat \
  --output_format_type grid \
  --solver bt_easiest_first \
  --output_path hello_world/hard_100 \
  --stats_path hello_world/hard_100/hard_100_summary.txt \
  --timeout 30
```

## Building the autodocumentation
Ensure your working directory is the root directory of the repository
```
docker run -it -v $(pwd):/C1_VJ279 c1_vj279
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
