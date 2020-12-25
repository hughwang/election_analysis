import json
import datetime
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import os
import io
import re
import urllib.request
"""

...
url = 'http://example.com/'
response = urllib.request.urlopen(url)
data = response.read()      # a `bytes` object
text = data.decode('utf-8') # 
"""

#filename = write_file.replace("GeneralConcatenator-", "_")
filename = "AZ_all.csv"
csv_file =  open(f'{filename}', mode='w')
fieldnames = ['last_updated','poll_time','Biden_votes', 'Biden_percent', 'Biden_electoral_votes',
              'Biden_absentee_votes', 'Biden_absentee_percent', 
               'Trump_votes', 'Trump_percent', 'Trump_electoral_votes',
              'Trump_absentee_votes', 'Trump_absentee_percent', 
               'Jorgensen_votes', 'Jorgensen_percent', 'Jorgensen_electoral_votes',
              'Jorgensen_absentee_votes', 'Jorgensen_absentee_percent', 
              'absentee_counties', 'votes','absentee_votes','electoral_votes'
              ]
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

filename = "AZ_counties.csv"
csv_county_file =  open(f'{filename}', mode='w')
fieldnames = ['county_name', 'precincts', 'votes','absentee_votes','tot_exp_vote','eevp_value',
              'absentee_max_ballots',
              'results_bidenj', 'resultes_trumpd', 'results_jorgensenj',
              'results_absentee_bidenj', 'results_absentee_trumpd', 'results_absentee_jorgensenj',
              'last_updated','votes2016','votes2012'
              ]
writer_counties = csv.DictWriter(csv_county_file, fieldnames=fieldnames)
writer_counties.writeheader()

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
overall_set=set()
county_set=set()
with open(f'input.txt') as f:
    for url in f:
        url=url.rstrip("\r\n")
        if url.startswith('#'):
            continue

        file_name=url
        write_file = f'json_data/{file_name}'
        #filename = write_file[0:2]
        timestamp=url
        if os.path.exists(write_file):
            with open(write_file) as json_file:
                data = json.load(json_file)
        else:
            #req = urllib2.Request(url, headers=hdr)
            #print(url)
            try:
                response = urllib.request.urlopen(f"https://web.archive.org/web/{url}if_/https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/arizona/president.json")
                data = response.read()
                content = data.decode('utf-8')
                data=json.loads(content)
                fjson = open(write_file, 'w')
                fjson.write(content)
                fjson.close()
            except:
                print(f"failed: {url}")
                continue

        for item in data['data']['races']:
            lastupdate = item['last_updated'][0:10]

            if lastupdate in overall_set:
                continue
            else:
                overall_set.add(lastupdate)
            for candidate in item['candidates']:
                if candidate['last_name'] =='Biden':
                    Biden_votes=candidate['votes']
                    Biden_percent=candidate['percent']
                    Biden_electoral_votes=candidate['electoral_votes']
                    Biden_absentee_votes=candidate['absentee_votes']
                    Biden_absentee_percent=candidate['absentee_percent']
                elif candidate['last_name'] =='Trump':
                    Trump_votes=candidate['votes']
                    Trump_percent=candidate['percent']
                    Trump_electoral_votes=candidate['electoral_votes']
                    Trump_absentee_votes=candidate['absentee_votes']
                    Trump_absentee_percent=candidate['absentee_percent']
                elif candidate['last_name'] == 'Jorgensen':
                    Jorgensen_votes = candidate['votes']
                    Jorgensen_percent = candidate['percent']
                    Jorgensen_electoral_votes = candidate['electoral_votes']
                    Jorgensen_absentee_votes = candidate['absentee_votes']
                    Jorgensen_absentee_percent = candidate['absentee_percent']
            writer.writerow({
                'last_updated': item['last_updated'],
                'poll_time': item['poll_time'],
                'votes':item['votes'],
                'electoral_votes':item['electoral_votes'],
                'absentee_votes':item['absentee_votes'],
                'Biden_votes': Biden_votes,
                'Biden_percent': Biden_percent,
                'Biden_electoral_votes': Biden_electoral_votes,
                'Biden_absentee_votes': Biden_absentee_votes,
                'Biden_absentee_percent': Biden_absentee_percent,
                'Trump_votes': Trump_votes,
                'Trump_percent': Trump_percent,
                'Trump_electoral_votes': Trump_electoral_votes,
                'Trump_absentee_votes': Trump_absentee_votes,
                'Trump_absentee_percent': Trump_absentee_percent,
                'Jorgensen_votes': Jorgensen_votes,
                'Jorgensen_percent': Jorgensen_percent,
                'Jorgensen_electoral_votes': Jorgensen_electoral_votes,
                'Jorgensen_absentee_votes': Jorgensen_absentee_votes,
                'Jorgensen_absentee_percent': Jorgensen_absentee_percent,
                'absentee_counties':item['absentee_counties']
            })
        for county in data['data']['races'][0]['counties']:
            lastupdate = county['last_updated'][0:10]
            key= county['name']+ lastupdate
            if key in county_set:
                continue
            else:
                county_set.add(key)
            writer_counties.writerow({
                'county_name': county['name'],
                'precincts': county['precincts'],
                'votes': county['votes'],
                'absentee_votes': county['absentee_votes'],
                'tot_exp_vote': county['tot_exp_vote'],
                'eevp_value': county['eevp_value'],
                'tot_exp_vote': county['tot_exp_vote'],
                'absentee_max_ballots': county['absentee_max_ballots'],
                'results_bidenj': county['results']['bidenj'],
                'resultes_trumpd': county['results']['trumpd'],
                'results_jorgensenj': county['results']['jorgensenj'],
                'results_absentee_bidenj': county['results_absentee']['bidenj'],
                'results_absentee_trumpd': county['results_absentee']['trumpd'],
                'results_absentee_jorgensenj': county['results_absentee']['jorgensenj'],
                'last_updated' : county['last_updated'],
                'votes2016' : county['votes2016'],
                'votes2012' : county['votes2012'],
            })
csv_file.close()
csv_county_file.close()
