##
"""
Build_Demographics_File: Process results from Process_Worldpop.py and a base demographics overlay
to create a new demographics file at ward level in northern Nigeria
"""
#

import numpy as np
import pandas as pd
import json

def node_ID_from_node_coordinates(node, res=30/3600):
    lat = node['NodeAttributes']['Latitude']
    long = node['NodeAttributes']['Longitude']
    nodeID = int((np.floor((long+180)/res)*(2**16)).astype(np.uint) + (np.floor((lat+90)/res)+1).astype(np.uint))
    return nodeID


def fill_nodes(out_demog, node_info, res=30/3600):
    out_nodes = []
    states2keep = ['katsina', 'kano', 'jigawa', 'kaduna', 'bauchi']
    for index, row in node_info.iterrows():
        if row['dot_name'].split(':')[1] in states2keep:
            curr_node = {}
            curr_node['dot_name'] = row['dot_name']
            curr_node['NodeAttributes'] = {}
            curr_node['NodeAttributes']['InitialPopulation'] = int(max(5000, 1000*row['population']))
            curr_node['NodeAttributes']['Latitude'] = row['latitude']
            curr_node['NodeAttributes']['Longitude'] = row['longitude']
            curr_node['NodeAttributes']['Area_deg2'] = row['area']
            curr_node['NodeAttributes']['Area_km2'] = row['area']*111*111
            curr_node['NodeID'] = int(node_ID_from_node_coordinates(curr_node, res))
            if (curr_node['NodeAttributes']['InitialPopulation'] / curr_node['NodeAttributes']['Area_deg2']) > 10000000:
                curr_node['NodeAttributes']['Urban'] = 1
                curr_node['NodeAttributes']['BirthRate'] = 0.00024
            else:
                curr_node['NodeAttributes']['Urban'] = 0
                curr_node['NodeAttributes']['BirthRate'] = 0.000288

            out_nodes.append(curr_node)
    out_nodes = duplicate_nodeID_check(out_nodes)
    return out_nodes


def duplicate_nodeID_check(nodelist):
    nodeIDs = pd.Series([n['NodeID'] for n in nodelist])
    dups = nodeIDs.duplicated()
    while any(dups):
        # In lieu of something more clever, find the first non-unique, find a nearby unused ID,
        # and loop until all IDs are unique
        ind2fix = dups[dups].index[0]
        oldNodeID = nodeIDs[ind2fix]
        newNodeID = oldNodeID
        shift = 0
        while newNodeID == oldNodeID:
            shift += 1
            for xs in range(-1*shift, shift):
                for ys in range(-1*shift, shift):
                    testId = oldNodeID + xs*2**16 + ys
                    if not any(nodeIDs.isin([testId])):
                        newNodeID = testId
        nodeIDs[ind2fix] = newNodeID
        nodelist[ind2fix]['NodeID'] = int(newNodeID)
        dups = nodeIDs.duplicated()
    return nodelist


if __name__ == "__main__":

    # Basic parameters.  Should these be inputs?
    base_demog_file = '.\\Nigeria_LGA_demographics.json'
    out_demog_file = '.\\Nigeria_Ward_smaller_minpop5000_demographics_test.json'
    node_info_file = '.\\population_by_ward_test.csv'

    with open(base_demog_file, 'r') as f:
        base_demog = json.load(f)
    out_demog = dict()
    out_demog['Metadata'] = base_demog['Metadata']
    out_demog['Defaults'] = base_demog['Defaults']
    out_demog['Defaults']['NodeAttributes']['Airport'] = 1
    out_demog['Defaults']['NodeAttributes']['Urban'] = 0
    out_demog['Defaults']['NodeAttributes']['BirthRate'] = 0.000288
    node_info = pd.read_csv(node_info_file)
    out_demog['Nodes'] = fill_nodes(out_demog, node_info, res=out_demog['Metadata']['Resolution']/3600)
    out_demog['Metadata']['NodeCount'] = len(out_demog['Nodes'])

    with open(out_demog_file, 'w') as fp:
        json.dump(out_demog, fp, indent=4)
