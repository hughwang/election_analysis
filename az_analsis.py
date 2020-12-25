import json
import datetime
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import pytz
import os
from dateutil import parser
file="AZ_counties.csv"
df = pd.read_csv(file)
counties= ['Coconino','Maricopa','Pima','Pinal']

est = pytz.timezone('US/Eastern')
ph_tz = pytz.timezone('America/Phoenix')
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

for county in counties:
    Coconino = df[df['county_name']==county]

    Coconino = Coconino.drop_duplicates(subset=['absentee_votes',
                                                'results_absentee_bidenj',
                                                'results_absentee_trumpd'])
    Coconino=Coconino.sort_values(by='last_updated', ascending=True)

    Coconino['absentee_votes_diff'] = Coconino['absentee_votes'].diff(1)
    Coconino['absentee_bidenj_diff'] = Coconino['results_absentee_bidenj'].diff(1)
    Coconino['absentee_trumpd_diff'] = Coconino['results_absentee_trumpd'].diff(1)
    Coconino['absentee_votes_diff'] = Coconino['absentee_votes'].diff(1)
    Coconino['last_updated'] = \
        pd.to_datetime(Coconino['last_updated'],format='%Y-%m-%dT%H:%M:%SZ')\
            .dt.tz_localize('UTC').dt.tz_convert('America/Phoenix')
    #Coconino['last_updated'] = Coconino['last_updated'].map(lambda x: parser.parse(x).astimezone(ph_tz).strftime(fmt))
    Coconino['absentee_biden_rate'] = (Coconino['absentee_bidenj_diff'] / Coconino['absentee_votes_diff'] )
    Coconino['absentee_trump_rate'] = (Coconino['absentee_trumpd_diff'] / Coconino['absentee_votes_diff'] )
    Coconino.iloc[0, Coconino.columns.get_loc('absentee_trump_rate')] = \
        (Coconino.iloc[0,Coconino.columns.get_loc('results_absentee_trumpd')]
         / Coconino.iloc[0,Coconino.columns.get_loc('absentee_votes')] )
    Coconino.iloc[0, Coconino.columns.get_loc('absentee_biden_rate')] = \
        (Coconino.iloc[0,Coconino.columns.get_loc('results_absentee_bidenj')]
         / Coconino.iloc[0,Coconino.columns.get_loc('absentee_votes')] )

    #Coconino['absentee_biden_rate'] = Coconino['absentee_biden_rate'].map(lambda x: "{0:.2f}%".format(x*100))
    #Coconino['absentee_trump_rate'] = Coconino['absentee_trump_rate'].map(lambda x: "{0:.2f}%".format(x*100))

    Coconino.to_csv(path_or_buf=f"{county}.csv",index=False)

    fig = Coconino.plot.bar(y=["absentee_biden_rate","absentee_trump_rate"],
                        x="last_updated",
                      title=f'{county} absentee vote rate',
                       rot = 20,
                      figsize=(10,7)).get_figure()
    fig.set_size_inches(10, 8)
    #plt.show()
    fig.savefig(f'{county}.pdf')

