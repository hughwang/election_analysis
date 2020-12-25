import json
import datetime
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
arr = os.listdir('EdisonAndScript')
print(arr)
for file in arr:
    print(file)
    file_name= file.replace(".json","")
    with open(f'EdisonAndScript/{file}') as f:
      data = json.load(f)

    result_hash={}
    for record in data['data']['races'][0]['timeseries']:
         #print record['timestamp']
         date_time_obj = datetime.datetime.strptime(record['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
         print(date_time_obj)
         result_hash[date_time_obj]=record
         record['bidenj_votes'] = int(record['votes']*record['vote_shares']['bidenj'])
         record['trumpd_votes'] = int(record['votes']*record['vote_shares']['trumpd'])

    od = collections.OrderedDict(sorted(result_hash.items()))
    list_result=[]
    trumpd_vote_previous=0
    bidenj_vote_previous=0
    for k, v in od.items():
      #print(k, v)
      v['time']=k
      v['trumpd_vote_diff'] = v['trumpd_votes'] - trumpd_vote_previous
      v['bidenj_vote_diff'] = v['bidenj_votes'] - bidenj_vote_previous
      # remove the abnormal data
      if (v['trumpd_vote_diff'] < -300000) or (v['bidenj_vote_diff']<-300000):
          continue
      trumpd_vote_previous= v['trumpd_votes']
      bidenj_vote_previous= v['bidenj_votes']

      list_result.append(v)

    for item in list_result:
      #print(item['trumpd_vote_diff'], item['time'])
      pass

    for item in list_result:
      pass
      #print(item['bidenj_vote_diff'], item['time'])

    with open(f'csv_files/{file_name}.csv', mode='w') as csv_file:
        fieldnames = ['id', 'timestamp', 'trumpd_votes_diff','bidenj_votes_diff','trumpd_votes','bidenj_votes','trumpd_votes_share','bidenj_votes_share','total_votes']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        id=1
        for item in list_result:
            writer.writerow({'id': id,
                             'timestamp': item['timestamp'],
                             'trumpd_votes_diff': item['trumpd_vote_diff'],
                             'bidenj_votes_diff': item['bidenj_vote_diff'],
                             'bidenj_votes': item['bidenj_votes'],
                             'trumpd_votes': item['trumpd_votes'],
                             'total_votes': item['votes'],
                             'trumpd_votes_share' :item['vote_shares']['trumpd'],
                             'bidenj_votes_share' :item['vote_shares']['bidenj'],
                             })
            id=id+1

    # draw the chart
    df = pd.read_csv(f'csv_files/{file_name}.csv',
                     usecols=[1, 4, 5],
                     header=0,
                     names=["timestamp", "trumpd_votes", "bidenj_votes"])
    df.index = pd.to_datetime(df["timestamp"], format='%Y-%m-%dT%H:%M:%SZ')
    nov_5th=datetime.datetime(2020,11,6,15)
    new_df = df[df.index < nov_5th]
    fig = new_df.plot(y=["bidenj_votes","trumpd_votes", ],
                      title=f'{file_name} votes count chart',
                      figsize=(15,10)).get_figure()
    fig.savefig(f'chart/{file_name}.pdf')

    # draw the diff chart
    df = pd.read_csv(f'csv_files/{file_name}.csv',
                     usecols=[1, 2, 3],
                     header=0,
                     names=["timestamp", "trumpd_votes_diff", "bidenj_votes_diff"])
    df.index = pd.to_datetime(df["timestamp"], format='%Y-%m-%dT%H:%M:%SZ')
    nov_5th=datetime.datetime(2020,11,6,15)
    new_df = df[df.index < nov_5th]
    fig = new_df.plot(y=["bidenj_votes_diff","trumpd_votes_diff", ],
                      title=f'{file_name} vote difference between time stamp chart',
                      figsize=(15,10)).get_figure()
    #plt.show()
    fig.savefig(f'diff_chart/{file_name}.pdf')

    # draw the share chart
    df = pd.read_csv(f'csv_files/{file_name}.csv',
                     usecols=[1, 6, 7],
                     header=0,
                     names=["timestamp", "trumpd_votes_share", "bidenj_votes_share"])
    df.index = pd.to_datetime(df["timestamp"], format='%Y-%m-%dT%H:%M:%SZ')
    nov_5th=datetime.datetime(2020,11,6,15)
    new_df = df[df.index < nov_5th]
    fig = new_df.plot(y=["bidenj_votes_share","trumpd_votes_share", ],
                      title = f'{file_name} vote rate share chart',
                      figsize=(15,10)).get_figure()
    #plt.show()
    fig.savefig(f'share_chart/{file_name}.pdf')
