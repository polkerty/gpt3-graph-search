'''
This helps us read a data file and format a given set of edges so the graph can be displated by https://csacademy.com/app/graph_editor/
'''

import json

if __name__ == '__main__':
    with open('data.json', 'r') as f:
        data = json.load(f)
    id = '74eabbdf-0b33-48ef-82a7-cf2049417cd8'
    element = [node for node in data if node['uuid'] == id][0]
    for edge in element['edges']:
        print(f'{edge[0]}\t{edge[1]}')
