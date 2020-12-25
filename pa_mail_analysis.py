import pandas as pd
import dateutil
from datetime import datetime
import collections

# Load data from csv file
filename='2020_Primary_Election_Mail_Ballot_Requests_Department_of_State.csv'
#filename='test.csv'
data = pd.read_csv(filename)
# Convert date from string to date times
#data['Date of Birth'] = data['Date of Birth'].apply(dateutil.parser.parse, dayfirst=True)
# How many rows the dataset
#i1= data['item'].count()

data.index = pd.to_datetime(data["Date of Birth"], format='%m/%d/%Y')
#data.sort_values(by='Date of Birth')
# What was the longest phone call / data entry?
#i2= data['duration'].max()

# How many seconds of phone calls are recorded in total?
#i3=  data['duration'][data['item'] == 'call'].sum()
hash_birth_day={}
for row in data.iterrows():

    birthday = row[1]['Date of Birth']
    ballot_retured = row[1]['Ballot Returned Date']
    if  pd.isnull(ballot_retured):
        continue
    if pd.isnull(birthday):
        date_of_birth = datetime.strptime('01/01/2022', '%m/%d/%Y')
    else:
        date_of_birth = datetime.strptime(birthday, '%m/%d/%Y')
    if date_of_birth not in hash_birth_day:
        hash_birth_day[date_of_birth]=1
    else:
        hash_birth_day[date_of_birth]=hash_birth_day[date_of_birth]+1
od = collections.OrderedDict(sorted(hash_birth_day.items()))
df = pd.DataFrame(list(od.items()),columns = ['birthday','count'])


file_name="birth_day_distribution"

fig = df.plot(    y=["count"],
                  x='birthday',
                  title=f'people distribute by birth date',
                  figsize=(15, 10)).get_figure()
# plt.show()
fig.savefig(f'{file_name}.pdf')
df.to_csv('pa_people_birthday_distribute.csv', index=False)