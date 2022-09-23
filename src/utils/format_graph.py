'''
This helps us read a data file and format a given set of edges so the graph can be displated by https://csacademy.com/app/graph_editor/
'''

import json

if __name__ == '__main__':
    with open('data-82069690-2f52-4d35-b39a-f121af2ac8aa.json', 'r') as f:
        data = json.load(f)
    id = '067c9038-c6a4-4c7c-b626-1a27ffd6ffd0'
    element = [node for node in data if node['uuid'] == id][0]
    for edge in element['edges']:
        print(f'{edge[0]}\t{edge[1]}')
