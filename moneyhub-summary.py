import pandas as pd
import sys
import argparse


"""
TO DO
1) Tidy up three functions for filtering transction type
2) Fix output file argparse flag
3) Validate summary results against moneyhub
"""

# define the program description
description = (
    "This script will take in moneyhub statements and perform some basic analysis."
)

# initiate the parser with a description
parser = argparse.ArgumentParser(description)

# Custom arguements
parser.add_argument("-i", "--input-file", help="Moneyhub file location")
parser.add_argument("-o", "--output-file", help="CSV output location")
parser.add_argument(
    "-s", "--summary", help="Provides a monthly summary", action="store_true"
)

args = parser.parse_args()


transactions = pd.read_csv(args.input_file)

# ---------------------------------------#
def transaction_check(row):
    """
    Check if a transaction is a transfer/outgoing/incoming
    """
    # String comparison on value of column
    if "Transfers" in row["CATEGORY GROUP"]:
        return "Transfer"
    # If negative value then outgoing
    elif row["AMOUNT"] < 0:
        return "Outgoing"
    # If postive value then income
    elif row["AMOUNT"] >= 0:
        return "Income"
    else:
        return "Other"


def ignore_transfers(df):
    """ 
    A simple function to run inverted string contain checks on the master table and return 
    any rows which do not contain TRANCTION TYPE = Trasfer
    """
    return df[~df["TRANSACTION TYPE"].str.contains("Transfer")]

def income_only(df):
    """ 
    A simple function to run inverted string contain checks on the master table and return 
    any rows which do not contain TRANCTION TYPE = Trasfer
    """
    return df[df["TRANSACTION TYPE"].str.contains("Income")]

def expenditure_only(df):
    """ 
    A simple function to run inverted string contain checks on the master table and return 
    any rows which do not contain TRANCTION TYPE = Trasfer
    """
    return df[df["TRANSACTION TYPE"].str.contains("Outgoing")]


def monthly_summary(df):
    """
    A function that will print out the monthly summary excluding transfers
    """
    # Ignore SettingWithCopyWarning for now, not a concern.
    pd.set_option("mode.chained_assignment", None)

    df["DATE"] = pd.to_datetime(df["DATE"])
    # Perform groupby and get sum of the values for each month
    return df.groupby(df["DATE"].dt.strftime("%B"))["AMOUNT"].sum().sort_values()

    # Reset chain assignment warnings
    pd.set_option("mode.chained_assignment", Warning)


# ---------------------------------------#

# Take function return value as transaction type
transactions["TRANSACTION TYPE"] = transactions.apply(transaction_check, axis=1)

# Output to file if requested
if args.output_file is not None:
    transactions.to_csv(args.output_file)


# Print summary if requested
if args.summary is True:
    noTransfers = ignore_transfers(transactions)
    income = income_only(transactions)
    expenditure = expenditure_only(transactions)
    
    income_summary = monthly_summary(income)
    expenditure_summary = monthly_summary(expenditure)
    noTransfers = monthly_summary(noTransfers)

    summary = pd.concat([income_summary, expenditure_summary, noTransfers], axis=1,
                        keys=['Income', 'Expenditure', 'Total'],
                        sort = False )
    #summary = income_summary

    print(
        'The summary below adds up any transaction within each month provided they are not "transfers".'
    )
    print("This will let you see if you spent more than you earned in a month. \n")
    #print(monthly_summary(noTransfers))
    print(summary)

    print("\n")
    print(args)
