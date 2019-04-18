##
"""
Build_Demographics_File: Process results from Process_Worldpop.py and a base demographics overlay
to create a new demographics file at ward level in northern Nigeria
"""
#
from copy import deepcopy
import numpy as np
import pandas as pd
import json
from dtk.tools.demographics.DemographicsFile import DemographicsFile
from dtk.tools.demographics.Node import Node

def node_ID_from_lat_long(lat, long, res=30/3600):
    nodeID = int((np.floor((long+180)/res)*(2**16)).astype(np.uint) + (np.floor((lat+90)/res)+1).astype(np.uint))
    return nodeID


def fill_nodes(node_info, res=30/3600):
    out_nodes = []
    states2keep = ['katsina', 'kano', 'jigawa', 'kaduna', 'bauchi']
    for index, row in node_info.iterrows():
        if row['dot_name'].split(':')[1] in states2keep:
            pop = int(max(5000, 1000*row['population']))
            lat = row['latitude']
            lon = row['longitude']
            extra_attributes = {'Area_deg2': row['area'], 'Area_km2': row['area']*111*111}
            meta = {'dot_name': row['dot_name']}

            if (pop / extra_attributes['Area_deg2']) > 10000000:
                extra_attributes['Urban'] = 1
                extra_attributes['BirthRate'] = 0.00024
            else:
                extra_attributes['Urban'] = 0
                extra_attributes['BirthRate'] = 0.000288

            node = Node(lat=lat, lon=lon, pop=pop, name=int(node_ID_from_lat_long(lat, lon, res)),
                        forced_id=int(node_ID_from_lat_long(lat, lon, res)),
                        extra_attributes=extra_attributes, meta=meta)

            out_nodes.append(node)
    out_nodes = duplicate_nodeID_check(out_nodes)
    return out_nodes


def duplicate_nodeID_check(nodelist):
    nodeIDs = pd.Series([n.id for n in nodelist])
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
        # nodelist[ind2fix]['NodeID'] = int(newNodeID)
        n = deepcopy(nodelist[ind2fix])
        nodelist[ind2fix] = Node(lat=n.lat, lon=n.lon, pop=n.pop,
                        forced_id=int(newNodeID),
                        extra_attributes=n.extra_attributes)
        dups = nodeIDs.duplicated()
    return nodelist


if __name__ == "__main__":

    # Basic parameters.  Should these be inputs?
    base_demog_file = '.\\Nigeria_LGA_demographics.json'
    out_demog_file = '.\\Nigeria_Ward_smaller_minpop5000_demographics.json'
    node_info_file = '.\\population_by_ward.csv'

    node_info = pd.read_csv(node_info_file)

    dg = DemographicsFile.from_file(base_demog_file)
    nodes = fill_nodes(node_info, res=dg.content['Metadata']['Resolution']/3600)
    dg.nodes = {node.name: node for node in nodes}
    dg.content['Defaults']['NodeAttributes']['Airport'] = 1
    dg.content['Defaults']['NodeAttributes']['Urban'] = 0
    dg.content['Defaults']['NodeAttributes']['BirthRate'] = 0.000288

    dg.generate_file(out_demog_file)
