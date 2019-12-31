# Moneyhub Scripts

This repository will act as a store for my own personal scripts for interacting with Moneyhub export data. I love using the Moneyhub app for aggregating transaction information into one place but the app itself doesn't do everything I want it to, hence this repo and these scripts.


## Installation

Basic git clone for now
```bash
git clone https://github.com/commit-confirm/moneyhub_scripts.git
```

## Usage

```bash
$python3 moneyhub-summary.py -h     

usage: This script will take in moneyhub statements and perform some basic analysis.
       [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Moneyhub file location
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        CSV output location
  -s, --summary         Provides a monthly summary
```

## Sample Output
Below shows some sample output with randomised numbers

```bash
$python3 moneyhub-summary.py -i Transaction-2019.csv  -s
The summary below adds up any transaction within each month provided they are not "transfers".
This will let you see if you spent more than you earned in a month. 

DATE
July        -1234.22
September    -422.22
October      -222.22
April        -111.22
March         -66.22
December      -55.22
May           888.22
February      999.22
January      1111.22
November     1222.22
August       1333.22
June         1444.22
Name: AMOUNT, dtype: float64
```