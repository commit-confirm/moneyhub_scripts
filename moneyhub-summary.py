import pandas as pd
import sys
import argparse

# define the program description
description = 'This script will take in moneyhub statements and perform some basic analysis.'

# initiate the parser with a description
parser = argparse.ArgumentParser(description)

#Custom arguements
parser.add_argument("-i", "--input-file", help="Moneyhub file location")
parser.add_argument("-o", "--output-file", help="CSV output location")
parser.add_argument("-s", "--summary", help="Provides a monthly summary", action="store_true")

args = parser.parse_args()


transactions = pd.read_csv(args.input_file)

#---------------------------------------#
def transaction_check(row):
    """
    Check if a transaction is a transfer/outgoing/incoming
    """
    # String comparison on value of column 
    if 'Transfers' in row['CATEGORY GROUP']:
        return 'Transfer'
    # If negative value then outgoing
    elif row['AMOUNT'] < 0:
        return 'Outgoing'
    # If postive value then income 
    elif row['AMOUNT'] >= 0:
        return 'Income'
    else:
        return 'Other'

def monthly_summary(dataFrame):
    """
    A function that will print out the monthly summary
    """
    
    summary = []
    for index, row in dataFrame.iterrows():
        if 'Transfer' in row['TRANSACTION TYPE']:
            #Skip trasnfers in the count
            continue
        else:
            #Append row items to summary list
            summary.append({'DATE': row['DATE'], 'AMOUNT': row['AMOUNT'], 'TRANSACTION TYPE': row['TRANSACTION TYPE']})
    #Turn summary list into a dataFrame
    summary = pd.DataFrame(summary)
    #Change date column to datetime format
    summary['DATE'] = pd.to_datetime(summary['DATE'])
    #Perform groupby and get sum of the values for each month
    return summary.groupby(summary['DATE'].dt.strftime('%B'))['AMOUNT'].sum().sort_values()

#---------------------------------------#

# Take function return value as transaction type
transactions['TRANSACTION TYPE'] = transactions.apply(transaction_check, axis=1)

# Output to file if requested
if args.output_file is True:
    transactions.to_csv(args.output_file)

#Print summary if requested
if args.summary is True:
    print("The summary below adds up any transaction within each month provided they are not \"transfers\".")
    print("This will let you see if you spent more than you earned in a month. \n")
    print(monthly_summary(transactions))
    print("\n")
