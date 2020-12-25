import json
import time
#import archiveis
from archivenow import archivenow
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


#filename = write_file.replace("GeneralConcatenator-", "_")
input_name = 'input.txt'
archive_name = input_name.replace('input','Archive')
filename = f"archive/{archive_name}"

with open(input_name) as f,open(archive_name,'a+') as wf:
    for url in f:
        url=url.rstrip("\r\n")
        if (not url) or url.startswith('#'):
            continue
        archive_url = archivenow.push(url, "ia")
        print(url+"\n")
        if len(archive_url) > 0:
            result= archive_url[0]
            if ('Exceeded 30 redirects') in result or  ('HTTPSConnectionPoo' in result):
                time.sleep(10)
                archive_url = archivenow.push(url, "ia")
                if len(archive_url) > 0:
                    result = archive_url[0]

            wf.write(f"{result}\n")



