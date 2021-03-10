# 1099parser

A simple python script for parsing the Robinhood 1099 tax document into CSV format.
Parses the trade information for each trade.

## How to use

1. have python installed
2. clone this repository: `$ git clone https://github.com/liyanghuang/1099-parser.git` or download the `1099parser.py` file in the repository above.
3. run the script: `$ python 1099parser.py`
4. follow the instructions and input what the script asks you to imput

## Options

### Input:
file path to the 1099 pdf file

### Output: 
file path to the output csv file. If left blank `./default.csv` will be used. If full file path is not provided, the file will be created in the directory of the `1099parser.py` file. If a previously existing filename is provided, it will overwrite the existing file.

### Compile Multiple Transactions
If `'Y'` is selected, securities that have multiple transactions will be compiled as one line, with the sum of the transactions used for the cost and proceeds. The acquired dates will be listed as `'various'`. if `'n'` is selected, securities that have multiple transactions will have each transaction listed individually on it's own line.

## Warning

Since I only have short-term trades on my 1099, I am unaware if long term trades have a different structure when listed in the 1099, thus I am unable to guarantee that the script will work with long term trades.


