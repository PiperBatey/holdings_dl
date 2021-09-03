# ETF Holdings DL

> A simple Python script that downloads the holdings of one or more ETFs into .csv files


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
* [Selenium](https://selenium-python.readthedocs.io/)
  * [GeckoDriver](https://github.com/mozilla/geckodriver/releases)

## Description

This program is run from the command line and accepts ETF symbols either as command arguments or from a text file in the local directory.
The holdings of each ETF will be saved in the local directory as `<ETF_symbol>-holdings.csv`.

An optional log file can be generated that contains a list of the successfully downloaded ETFs, their full names, and their previous closing price.


## How to Use

---

### Simple Example

```shell
  $ python3 holdings_dl.py --symbol QQQ
```
This command downloads the holdings data of the ETF designated by the symbol `QQQ` and produces the following terminal output:

```
  Opening QQQ database
  QQQ: page 1 of 2 ... complete
  QQQ: page 2 of 2 ... complete
  QQQ: 103 holdings retrieved
  
  1 file(s) have been generated for 1 ETF(s):
  QQQ-holdings.csv
```

The data is saved in a file in the local directory named `QQQ-holdings.csv` and contains information about each of the ETF's holdings.
The entries are sorted in descending order by portfolio weight in the ETF:

| Symbol | Description | % Portfolio Weight | Shares Held | Market Value |
| --- | --- | --- | --- | --- |
| AAPL | Apple Inc | 11.34% | 142.8M | $21.9B |
| MSFT | Microsoft Corp | 10.15% | 64.5M | $19.6B |
| AMZN | Amazon.com Inc | 7.66% | 4.3M | $14.8B |
| ... | ... | ... | ... | ... |  
  


### Program Usage
    usage: holdings_dl.py [-h] (--symbol SYM [SYM ...] | --file FILE) [-l] [-a] [-w] [-q] [-t TIME]
    
    optional arguments:
      -h, --help              show this help message and exit
      -l, --log               create a log of the downloaded ETFs in etf-log.csv
      -a, --alpha             sort ETF symbols into alphabetical order for output
      -w, --window            run web driver with firefox window visible
      -q, --quiet             suppress verbose terminal output
      -t TIME, --time TIME    set the maximum time in seconds the program will
                              wait for web pages to load (default: 15)
    
    required arguments:
      --symbol SYM [SYM ...]  specify one or more ETF symbols
      --file FILE             specify a file containing a list of ETF symbols
  


### Input Modes

The program supports two ways to input ETF symbols.
The user is required to choose one of the two modes on the command line.

#### 1. Symbol Input

  Running the program with the `--symbol` flag allows the user to input one or more ETF symbols directly on the command line.

```shell
  $ python3 holdings_dl.py --symbol XLK QQQ ARKK
```


#### 2. File Input

Running the program with the `--file` flag allows the user to input the name of a file in the local directory with a list of ETF symbols in the proper format.

```shell
  $ python3 holdings_dl.py --file MyFile.txt
```
A valid input file contains a plain text list of ETF symbols each followed by a newline:
```
 XLK\n
 QQQ\n
 ARKK\n
```

### Generate Log
Use `--log` or `-l` on the command line to 
generate a file in the local directory named `etf-log.csv`:

```shell
  $ python3 holdings_dl.py --symbol XLK QQQ ARKK -l -a
```

Note: providing the `--alpha` or `-a` flag has the program sort the ETF symbols alphabetically before generating the log file.
```
  Opening ARKK database
  ARKK: page 1 of 1 ... complete
  ARKK: 50 holdings retrieved
  
  Opening QQQ database
  QQQ: page 1 of 2 ... complete
  QQQ: page 2 of 2 ... complete
  QQQ: 103 holdings retrieved
  
  Opening XLK database
  XLK: page 1 of 2 ... complete
  XLK: page 2 of 2 ... complete
  XLK: 76 holdings retrieved
  
  Generating log file... complete
  
  4 file(s) have been generated for 3 ETF(s):
  etf-log.csv
  ARKK-holdings.csv
  QQQ-holdings.csv
  XLK-holdings.csv
```

`etf-log.csv` is saved in the local directory and contains a list of each ETF downloaded along with other useful information:

| Symbol | Name | Last Price | Number of Holdings |
| --- | --- | --- | --- |
| ARKK | ARK Innovation ETF | $124.83 | 50  |
| QQQ | Invesco QQQ Trust | $380.40 | 103 |
| XLK | Technology Select Sector SPDR Fund | $158.73 | 76  |



### Error Handling

##### Invalid ETF Symbols
ETF symbols that cannot be found on the database will not be downloaded and will not appear in `etf-log.csv`.
If such a symbol is encountered, an error message will be printed to the terminal and the program will continue retrieving any remaining ETFs.

##### Invalid Input Files

If a file specified with the `--file` flag does not exist in the local directory, the program will quit with an error message.
If the file exists but is not in the proper format (plain text ETF symbols followed by `\n`), the program will encounter undefined behavior.
Only one input file will be accepted at a time.


## Resources
All data comes  from [Schwab](https://www.schwab.com/research/etfs/tools/compare) via 
[Selenium](https://selenium-python.readthedocs.io/) and 
[Pandas read_html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html)

## Author

Piper Batey (pbatey@umich.edu)

## Version History

* 0.2
  * Updated to retrieve all holdings of an ETF
  * Data is now retrieved from [Schwab](https://www.schwab.com/research/etfs/tools/compare)
  * Switched to [Selenium](https://selenium-python.readthedocs.io/) webdriver for speed and reliability

* 0.1
    * Initial Release
    * Retrieves the top 25 holdings of an ETF
    * Holdings data is retrieved from [YCharts.com](https://ycharts.com/stocks)
    * Log file information comes from [yfinance](https://pypi.org/project/yfinance/)

## License

MIT License (see LICENSE file)
