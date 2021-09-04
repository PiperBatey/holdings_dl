# ETF Holdings DL

> A simple Python script that downloads the holdings of one or more ETFs into .csv files


## Table of Contents

- [Dependencies](#dependencies)
- [Description](#description)
- [**How to Use**](#how-to-use)
  * [Simple Example](#simple-example)
  * [Program Usage](#program-usage)
  * [Input Modes](#input-modes)
  * [Data Formats](#data-formats)
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

This script accepts one or more ETF symbols either as command line arguments or from a properly-formatted text file in the local directory.
For every valid ETF, a file named`<ETF_symbol>-holdings.csv` is saved in the local directory and contains the symbol, description, portfolio weight, number of shares held, and market value of each holding in the ETF.

An optional log file can be generated that contains the list of successfully downloaded ETF symbols, descriptions and most recent market prices.
This file will be saved in the local directory as `etf-log.csv`.

## How to Use


### Simple Example

This command downloads the holdings data of the ETF with the symbol `QQQ` :

```
$ python3 holdings_dl.py --symbol QQQ

Opening QQQ database
QQQ: page 1 of 2 ... complete
QQQ: page 2 of 2 ... complete
QQQ: 103 holdings retrieved
  
1 file(s) have been generated for 1 ETF(s):
QQQ-holdings.csv
```

A list of the ETF's holdings is saved in the local directory as `QQQ-holdings.csv`.
Entries are sorted in descending order by portfolio weight.

| Symbol | Description | Portfolio Weight | Shares Held | Market Value |
| --- | --- | --- | --- | --- |
| AAPL | Apple Inc | 11.34% | 142.8M | $21.9B |
| MSFT | Microsoft Corp | 10.15% | 64.5M | $19.6B |
| AMZN | Amazon.com Inc | 7.66% | 4.3M | $14.8B |
| ... | ... | ... | ... | ... |  


### Program Usage

    usage: holdings_dl.py [-h] (--symbol SYM [SYM ...] | --file FILE) [-r] [-l] [-a] [-w] [-q] [-t TIME]

    optional arguments:
      -h, --help              show this help message and exit
      -r, --raw               save raw data without symbols or units
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
The user is required to specify the input mode on the command line.

#### Symbol Input

  Running the program with the `--symbol` flag allows the user to input one or more ETF symbols directly on the command line.

```shell
$ python3 holdings_dl.py --symbol XLK QQQ ARKK
```


#### File Input

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

### Data Formats
In the simple example, the data in the output file is displayed with special characters and units.
In order to generate the holdings files without these charaters, use the `--raw` or `-r` flag on the command line.
In this mode, the portfolio weight is represented as a decimal and the market value is expressed in USD.

Example:
```
$ python3 holdings_dl.py --symbol QQQ -r
```
Raw `QQQ-holdings.csv` :

|Symbol|Description         |Portfolio Weight|Shares Held |Market Value  |
|------|--------------------|----------------|------------|--------------|
|AAPL  |Apple Inc           |0.1134          |1428000000.0|219000000000.0|
|MSFT  |Microsoft Corp      |0.1015          |645000000.0 |196000000000.0|
|AMZN  |Amazon.com Inc      |0.0766          |43000000.0  |148000000000.0|
|...|...|...|...|...|

### Generate Log

Use `--log` or `-l` on the command line to generate a file in the local directory named `etf-log.csv`.
Providing the `--alpha` or `-a` flag sorts the ETF symbols alphabetically before generating the log file.

Example:

```
  $ python3 holdings_dl.py --symbol XLK QQQ ARKK -l -a

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

`etf-log.csv` is saved in the local directory and contains a list of each ETF downloaded.

| Symbol | Name | Last Price | Number of Holdings |
| --- | --- | --- | --- |
| ARKK | ARK Innovation ETF | $124.83 | 50  |
| QQQ | Invesco QQQ Trust | $380.40 | 103 |
| XLK | Technology Select Sector SPDR Fund | $158.73 | 76  |


### Error Handling

#### Invalid ETF Symbols
ETF symbols that cannot be found on the schwab database will not be downloaded and will not appear in `etf-log.csv`.
If such a symbol is encountered, an error message will be printed to the terminal and the program will continue retrieving any remaining ETFs.

Example:
```
$ python3 holdings_dl.py --symbol XLK FAKE QQQ -l

Opening XLK database
XLK: page 1 of 2 ... complete
XLK: page 2 of 2 ... complete
XLK: 76 holdings retrieved

Opening FAKE database
FAKE is not a valid ETF (not found in schwab database)

Opening QQQ database
QQQ: page 1 of 2 ... complete
QQQ: page 2 of 2 ... complete
QQQ: 103 holdings retrieved

Generating log file... complete

3 file(s) have been generated for 2 ETF(s):
etf-log.csv
XLK-holdings.csv
QQQ-holdings.csv
```

#### Invalid Input Files

Only one input file can be accepted at a time.
If a file specified with the `--file` flag does not exist in the local directory, the program will quit with an error message.
If the file exists but is not in the proper format (plain text ETF symbols followed by `\n`), the program will encounter undefined behavior.


## Resources
All data comes  from [Schwab](https://www.schwab.com/research/etfs/tools/compare) via 
[Selenium](https://selenium-python.readthedocs.io/) and 
[Pandas read_html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html)

## Author

Piper Batey (pbatey@umich.edu)

## Version History

* 0.3
  * Supports raw data output
  * Webdriver command line settings added

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
