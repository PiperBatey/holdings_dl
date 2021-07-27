#!/usr/bin/env
import argparse
import pandas as pd
from urllib.error import HTTPError
import yfinance as yf

'''
    File name: holdings_dl.py
    Author: Piper Batey
    Date created: 7/13/2021
    Date last modified: 7/13/2021
    Python Version: 3.8
    Description: A simple Python script that downloads 
    the top 25 holdings of one or more ETFs into a .csv file.
'''


class HoldingsDownloader:
    def __init__(self):
        # variables
        self.etf_symbols = []
        self.valid_etfs = []
        self.file_name = ""
        self.num_files = 0
        self.log_mode = False
        self.quiet_mode = False
        self.sort_mode = False
        # init
        self._parse_command_args()
        if self.file_name:
            self._read_input_file()
        if self.sort_mode:
            self.etf_symbols.sort()

    def _parse_command_args(self):
        parser = argparse.ArgumentParser(description="creates a .csv file with the top 25 holdings of an ETF")
        input_type_group = parser.add_mutually_exclusive_group(required=True)
        input_type_group.add_argument("-f", "--file", help="specify a file containing a list of ETF symbols")
        input_type_group.add_argument("-s", "--symbol", action='append', default=[],
                                      help="specify an ETF symbol")
        parser.add_argument("-q", "--quiet", action="store_true", help="suppress verbose terminal output")
        parser.add_argument("-l", "--log", action="store_true",
                            help="create a log of the downloaded ETFs in etf-log.csv")
        parser.add_argument("-a", "--alpha", action="store_true",
                            help="sort the ETF symbols into alphabetical order for output")
        args = parser.parse_args()  # get args from the command line
        self.quiet_mode = args.quiet
        self.log_mode = args.log
        self.sort_mode = args.alpha
        if args.file:
            self.file_name = args.file
        if args.symbol:
            self.etf_symbols = args.symbol

    def _read_input_file(self):
        if not self.quiet_mode:
            print("Reading symbols from {} ...".format(self.file_name), end=" ")
        with open(self.file_name, 'r') as input_file:
            for name in input_file:
                self.etf_symbols.append(name[:-1])  # avoid the newline at the end
        if not self.quiet_mode:
            print("complete")

    def generate_csv_files(self):
        if not self.quiet_mode:
            print("Retrieving holdings information")
        for etf_symbol in self.etf_symbols:
            url = "https://ycharts.com/companies/{}/holdings".format(etf_symbol)
            if not self.quiet_mode:
                print("{} ...".format(etf_symbol), end=" ")
            try:
                dataframe_list = pd.read_html(url, match="Symbol")  # get list of dataframes from website
                dataframe = dataframe_list[0]
                dataframe.columns = ["Symbol", "Name", "% Weight", "Price", "% Change"]  # avoid whitespace issues
                dataframe = dataframe.drop(columns=["% Change", "Price"])  # delete unnecessary columns
                dataframe.to_csv("{}-holdings.csv".format(etf_symbol), index=False)  # create the csv
                self.valid_etfs.append(etf_symbol)
                self.num_files += 1
                if not self.quiet_mode:
                    print("complete")
            except HTTPError:
                if not self.quiet_mode:
                    print("ERROR\n{} is not found as an ETF. Holdings file not generated.".format(etf_symbol))

    def generate_etf_log_file(self):
        etf_full_names = []
        prev_close_prices = []
        if not self.quiet_mode:
            print("Generating etf-log.csv ...", end=" ")

        # Download the full name and previous closing price of each successfully fetched ETF
        for symbol in self.valid_etfs:
            etf_ticker = yf.Ticker(symbol)
            etf_full_names.append(etf_ticker.info["shortName"])
            prev_close_prices.append(etf_ticker.info["previousClose"])

        # use a pandas dataframe to create the csv
        log_dataframe = pd.DataFrame({"Symbol": self.valid_etfs,
                                      "Name": etf_full_names,
                                      "Previous Closing Price": prev_close_prices})
        log_dataframe.to_csv("etf-log.csv", index=False)
        self.num_files += 1
        if not self.quiet_mode:
            print("complete")


def main():
    downloader = HoldingsDownloader()
    downloader.generate_csv_files()
    if downloader.log_mode:
        downloader.generate_etf_log_file()

    if not downloader.quiet_mode:  # verbose output
        print("\n{} file(s) have been generated for {} ETF(s):".format(downloader.num_files,
                                                                       len(downloader.valid_etfs)))
        if downloader.log_mode:
            print("etf-log.csv")
        for symbol in downloader.valid_etfs:
            print("{}-holdings.csv".format(symbol))


if __name__ == "__main__":
    main()
