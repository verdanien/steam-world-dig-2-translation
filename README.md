# SteamWorldDig2 Utilities

Tool allows to decompress/compress language files.

## Installation

1. install python
    ```commandline
    winget install Python.Python.3.12
    ```
2. install pip
    ```commandline
    python -m pip install --upgrade pip
    ```
3. Setup tool:
    ```commandline
    pip install --editable .
    ```

## Preparation
Please create dir `.private` inside the project. This catalog is excluded from the repository
so you can freely put there all source files.

## Usage

### verification if works
Please type in cmd:
```commandline
swd2
```

it should generate help output as follows:
```commandline
Usage: swd2.exe [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose
  --working-dir PATH  working directory
  --log-level TEXT    Logging level
  --help              Show this message and exit.

Commands:
  translator   Translator group
  working-dir  Displays project location
```

### decompressing all files in dir
Following command will extract all `*.csv.z` files into the `out` directory

```commandline
swd2 --working-dir=.private translator decompress-all --force
```


### compressing all files in dir
Following command will compress all `*.csv` files into the `out` directory

```commandline
swd2 --working-dir=.private translator compress-all --force
```


### more options
To check more available options please type `--help` after each command to read. Examples:

```commandline
swd2 --help
swd2 translator --help
swd2 translator compress-all --help
swd2 translator decompress-all --help
```