import pandas as pd
import sys
import argparse

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
if args.output_file is True:
    transactions.to_csv(args.output_file)

# Print summary if requested
if args.summary is True:
    noTrasnfers = ignore_transfers(transactions)
    print(
        'The summary below adds up any transaction within each month provided they are not "transfers".'
    )
    print("This will let you see if you spent more than you earned in a month. \n")
    print(monthly_summary(noTrasnfers))
    print("\n")
