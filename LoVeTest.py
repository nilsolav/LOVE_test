#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from pydap.client import open_url
import requests
import xmltodict
from datetime import datetime
import pandas as pd


url0 = 'https://opendap1.nodc.no'

catalog = url0+'/opendap/hyrax/projects/LoVeOcean/'

# List the nodes
response = requests.get(catalog+'catalog.xml')
_LoVeCatalog = xmltodict.parse(response.content)['thredds:catalog'][
    'thredds:dataset']['thredds:catalogRef']
LoVeNodes = [catalog+__LoVeCatalog['@xlink:href'] for __LoVeCatalog in _LoVeCatalog]
ncfiles = []
# Loop over nodes
for LoVeNode in LoVeNodes:
    dataset = [url0+_node['@ID'] for _node in xmltodict.parse(requests.get(LoVeNode).content)['thredds:catalog'][
        'thredds:dataset']['thredds:catalogRef']]
    # Loop over data sets
    for _dataset in dataset:
        ncfiles.extend([url0+_ncfile['@ID'] for _ncfile in xmltodict.parse(requests.get(_dataset+'catalog.xml').content)['thredds:catalog']['thredds:dataset']['thredds:dataset']])
len(ncfiles)

node = [_ncfiles.split('/')[-3] for _ncfiles in ncfiles]
var = [_ncfiles.split('/')[-1].split('_')[-2] for _ncfiles in ncfiles]
t = [datetime.strptime(_ncfiles.split('/')[-1].split('_')[-1].split('.')[0].
                       split('-')[0],'%Y%m%dT%H%M%S') for _ncfiles in ncfiles]

# Put data into a pandas data frame
data = {'Node': node, 'Variable': var, 'Time': t}
df = pd.DataFrame(data)
grouped_data = df.groupby(['Node', 'Variable'])

#df['Value'] = grouped_data.cumcount()

df['Value'] = df.groupby(['Node', 'Variable']).ngroup()

plt.figure(figsize=(10, 6))

for (node, variable), group in grouped_data:
    plt.plot(group['Time'], group['Value'], marker='o', linestyle='', label=f"{node}-{variable}")

plt.title('Data status from LoVe production server')
plt.xlabel('Time')
plt.yticks([])  # Hide y-axis ticks since they are constant
plt.legend()
plt.savefig('DataStatus.png')
plt.show()
