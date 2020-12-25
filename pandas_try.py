import pandas as pd
import dateutil

# Load data from csv file
data = pd.read_csv('phone_data.csv')
# Convert date from string to date times
data['date'] = data['date'].apply(dateutil.parser.parse, dayfirst=True)
# How many rows the dataset
i1= data['item'].count()


# What was the longest phone call / data entry?
i2= data['duration'].max()

# How many seconds of phone calls are recorded in total?
i3=  data['duration'][data['item'] == 'call'].sum()

# How many entries are there for each month?
i4=  data['month'].value_counts()

# Number of non-null unique network entries
i5=data['network'].nunique()
i=1