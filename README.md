# ETF Holdings DL

> A simple Python script that downloads the top 25 holdings of one or more ETFs into a .csv file


## Table of Contents

- [Dependencies](#dependencies)
- [Description](#description)
- [**How to Use**](#how-to-use)
  * [Simple Example](#simple-example)
  * [General Usage](#general-usage)
  * [Input Modes](#input-modes)
  * [Generate Log](#generate-log)
  * [Error Handling](#error-handling)
- [Resources](#resources)
- [Author](#author)
- [Version History](#version-history)
- [License](#license)

## Dependencies

* [Python 3](https://www.python.org/) (tested on 3.6 and 3.8)
* [Pandas](https://pandas.pydata.org/)
  * [NumPy](https://numpy.org/)
  * [lxml](https://pypi.org/project/lxml/)
* [yfinance](https://pypi.org/project/yfinance/)
    * [Requests](https://docs.python-requests.org/en/master/)

## Description

This program is run from the command line and accepts ETF symbols either as command arguments or from a text file in the local directory.
The top 25 holdings of each ETF will be saved in the local directory as `<ETF_symbol>-holdings.csv`.

An optional log file can be generated that contains a list of the successfully downloaded ETFs, their full names, and their previous closing price.


## How to Use

### Simple Example

Generate a file in the local directory named VTI-holdings.csv containing top 25 holdings of the ETF

    $ python3 holdings_dl.py -s VTI

##### Terminal Output
```
Retrieving holdings information
VTI ... complete

1 file(s) have been generated for 1 ETF(s):
VTI-holdings.csv
```

##### VTI-holdings.csv

|Symbol|Name          |% Weight|
|:------:|--------------|--------|
|MSFT  |Microsoft Corp|4.39%   |
|AAPL  |Apple Inc     |4.39%   |
| ... | ...           | ...    |


### General Usage
    holdings_dl.py [-h] (-f FILE | -s SYMBOL) [-q] [-l] [-a]

      -f FILE, --file FILE  specify a file containing a list of ETF symbols
      -s SYMBOL, --symbol SYMBOL
                            specify an ETF symbol
    optional arguments:
      -h, --help            show help message and exit
      -q, --quiet           suppress terminal output
      -l, --log             create a log of the downloaded ETFs in etf-log.csv
      -a, --alpha           sort the ETF symbols into alphabetical order for
                            output


### Input Modes

There are two ways to provide input to the program: either by symbol or by file list. This is specified by the user as a required command line argument.

#### 1. Use `--symbol` or `-s` to input an ETF symbol directly


This was used in the simple example above, however it is worth noting that repeating the flag allows for the input of multiple symbols at a time.

    $ python3 holdings_dl.py --symbol VTI -s SPY -s QQQ  


#### 2. Use `--file` or `-f` to specify a text file

    $ python3 holdings_dl.py -f MyFile.txt

   A valid input file contains a plain text list of ETF symbols, each followed by a newline. 
   Only one file will be accepted at a time.

Ex. `MyFile.txt`

        VTI\n
        SPY\n
        QQQ\n
        

### Generate Log
Specify `--log` or `-l` at the command line in order to 
generate a file named `etf-log.csv` in the local directory. 
This file will contain a log of all the ETFs that were downloaded by the program. 
The full name and previous closing price of each ETF are listed as well.

Using the `--alpha` or `-a` flag will sort the ETFs alphabetically by symbol in the log file.

#### Example:

     $ python3 holdings_dl.py -s VTI -s SPY -s QQQ -l -a

##### Terminal Output
```
Retrieving holdings information
QQQ ... complete
SPY ... complete
VTI ... complete
Generating etf-log.csv ... complete

4 file(s) have been generated for 3 ETF(s):
etf-log.csv
QQQ-holdings.csv
SPY-holdings.csv
VTI-holdings.csv
```

##### etf-log.csv

|Symbol|Name          |Previous Closing Price|
|------|--------------|----------------------|
|QQQ   |Invesco QQQ Trust, Series 1|358.77   |
|SPY   |SPDR S&P 500  |430.92                |
|VTI   |Vanguard Total Stock Market ETF|223.18 |



### Error Handling

##### Invalid ETF Symbols
ETF symbols that cannot be found on the [YCharts.com](https://ycharts.com/stocks) database will not be downloaded and will not appear in `etf-log.csv`.
If such a symbol is encountered, an error message will be printed to the terminal and the program will continue retrieving any remaining ETFs.

##### Invalid Input Files

If a file specified with the `--file` flag does not exist in the local directory, the program will quit with an error message.
If the file exists but is not in the proper format (plain text ETF symbols followed by `\n`), the program will encounter undefined behavior.


## Resources
All holdings data comes  from [YCharts.com](https://ycharts.com/stocks) via the pandas [read_html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html) function.
Information in `etf-log.csv` is retrieved using [yfinance](https://pypi.org/project/yfinance/).

## Author

Piper Batey (pbatey@umich.edu)

## Version History

* 0.1
    * Initial Release

## License

MIT License (see LICENSE file)
