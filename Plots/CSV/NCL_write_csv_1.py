"""
NCL_write_csv_1.py
===============
This script illustrates the following concepts:
   - Writing a CSV file
   - Using python tools 'csv' and 'pandas' to write integers to a CSV file
   
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/write_csv_1.ncl
"""

###############################################################################
# Import packages:

import csv
from itertools import zip_longest
import pandas as pd

###############################################################################
# Create data in column format 

x1 = [34, 36, 31, 29, 54, 42]
x2 = [67, 87, 56, 67, 71, 65]
x3 = [56, 78, 88, 92, 68, 82]

###############################################################################
# Create CSV file using 'csv'

# Put data into one list so it can be manipulated together
col = [x1, x2, x3]

# Transpose data lists so they are read column by column not row by row
export_cols = zip_longest(*col, fillvalue='')

# Create a new CSV file and write data to it
with open('example1a.csv', mode='w') as myfile:
    example_writer = csv.writer(myfile, delimiter=',')
    example_writer.writerows(export_cols)
myfile.close()

###############################################################################
# Creat CSV file using 'pandas'

# Create a data frame to contain all data
df = pd.DataFrame([x1, x2, x3])

# Transpose data frame so that it will be read in column by column not row by row
df = df.T

# Export data frame to csv file
df.to_csv('example1b.csv', header=False, index=False)