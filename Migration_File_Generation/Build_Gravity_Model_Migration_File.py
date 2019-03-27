##
"""
Build_Demographics_File: Process results from Process_Worldpop.py and a base demographics overlay
to create a new demographics file at ward level in northern Nigeria
"""
#

import numpy as np
import pandas as pd
import scipy.spatial.distance as dist
import json
import math
import os
from dtk.tools.demographics.DemographicsFile import DemographicsFile
from dtk.tools.demographics.Node import Node


# Haversine takes long/lat pairs IN RADIANS and computes the haversine distance between them
from dtk.tools.migration.MigrationFile import MigrationFile
from dtk.tools.migration.MigrationFile import MigrationTypes


def haversine(p1, p2):
    delta = p1 - p2
    return math.fabs(math.asin(
        math.sqrt(math.sin(delta[1] / 2) ** 2 + math.cos(p1[1]) * math.cos(p2[1]) * math.sin(delta[0] / 2) ** 2)))


def migration_outputs_by_channel(Types, nodeIDs, distances, migration_matrix, maxConnections):
    # Dimension 1 refers to source nodes, dimension 2 refers to destination nodes
    outputdict = {}
    nNodes = nodeIDs.size
    for type in Types:
        initmat = np.zeros([nNodes, maxConnections[type]])
        initvec = np.zeros(nNodes)
        outputdict[type] = {'Rates': initmat, 'sourceIDs': initvec, 'destIDs': initmat}

        if type == 'Local':
            indices = distances.argsort()[:,
                      :maxConnections['Local']]  # Indices of the 8 smallest distances in each row
            outputdict[type]['Rates'] = np.array(
                [migration_matrix[ii, indices[ii]] for ii in range(migration_matrix.shape[0])])
            outputdict[type]['destIDs'] = nodeIDs[indices]
            outputdict[type]['sourceIDs'] = nodeIDs


        else:
            indices = migration_matrix.argsort()[:, -1 * maxConnections[
                type]:]  # Indices of the N largest connection rates.  Ignore whether nodes have airports or seaports for now.
            outputdict[type]['Rates'] = np.array(
                [migration_matrix[ii, indices[ii]] for ii in range(migration_matrix.shape[0])])
            outputdict[type]['destIDs'] = nodeIDs[indices]
            outputdict[type]['sourceIDs'] = nodeIDs

        # Zero out corresponding elements to avoid double counting connections if using multiple migration types
        for ii in range(migration_matrix.shape[0]):
            migration_matrix[ii, indices[ii]] = 0.0
    return outputdict


def compute_gravity_matrix(pops, distances, exponents, normalize=True):
    np.fill_diagonal(distances, 1000000)  # Prevent divide by zero errors and self migration

    migration_matrix = np.ones_like(distances)
    pops = pops[:, np.newaxis].T
    pops = np.repeat(pops, pops.size, axis=0)
    migration_matrix = migration_matrix * (pops ** exponents['Destination']) * (pops.T ** (exponents['Source'] - 1))
    migration_matrix = migration_matrix / ((distances + 10) ** exponents[
        'Distance'])  # impose a minimum distance value to prevent excessive migration nearby
    np.fill_diagonal(migration_matrix, 0)

    # Set average outbound migration = 1
    if normalize:
        migration_matrix = migration_matrix / np.mean(np.sum(migration_matrix, axis=1))

    return migration_matrix


def write_outputs_to_textfiles(base_demog_dir, base_demog_file, outputdict):
    for mig_type, outputs in outputdict.items():
        outputfile_name = base_demog_file.replace('demographics.json', mig_type.lower() + '_migration.txt')
        with open(outputfile_name, 'w') as f:
            for d1 in range(outputs['Rates'].shape[0]):
                for d2 in range(outputs['Rates'].shape[1]):
                    f.write(str(outputs['sourceIDs'][d1]) + ' ' + str(outputs['destIDs'][d1, d2]) + ' ' + str(
                        outputs['Rates'][d1, d2]) + '\n')
        os.system(
            'python buildMigrationFiles.py -d ' + base_demog_dir + base_demog_file + ' -r ' + outputfile_name + ' -t ' + mig_type.upper())


if __name__ == "__main__":

    # Basic parameters.  Should these be inputs?
    base_demog_dir = '..\\Demographic_File_Generation\\'
    base_demog_file = 'Nigeria_Ward_smaller_minpop5000_demographics_new.json'
    earth_radius = 6367
    exponents = {'Source': 1, 'Destination': 1, 'Distance': 1}
    maxConnections = {'Local': 8, 'Air': 60, 'Regional': 30, 'Sea': 5}
    Types = ['Local', 'Air']

    if 'Local' in Types:
        Types.insert(0, Types.pop(Types.index('Local')))  # Important to have local up first

    # Load file to DemographicsFile class
    dg = DemographicsFile.from_file(base_demog_dir + base_demog_file)
    nodes = dg.nodes.values()
    lats = np.deg2rad(np.array([n.lat for n in nodes]))
    longs = np.deg2rad(np.array([n.lon for n in nodes]))
    pops = np.array([n.pop for n in nodes])
    nodeIDs = np.array([n.id for n in nodes])

    # Calculate migration matrix
    distances = 2 * earth_radius * dist.squareform(dist.pdist(np.vstack((longs, lats)).T, haversine))
    migration_matrix = compute_gravity_matrix(pops, distances, exponents, normalize=True)
    outputdict = migration_outputs_by_channel(Types, nodeIDs, distances, migration_matrix, maxConnections)

    # Build mig_matrix required in MigrationFile class
    mig_matrix = {}
    for mig_type, outputs in outputdict.items():
        mig_matrix[mig_type] = {}
        tmpt_matrix = {}
        for d1 in range(outputs['Rates'].shape[0]):
            for d2 in range(outputs['Rates'].shape[1]):
                if int(outputs['sourceIDs'][d1]) not in tmpt_matrix:
                    tmpt_matrix[int(outputs['sourceIDs'][d1])] = {
                        int(outputs['destIDs'][d1, d2]): float(outputs['Rates'][d1, d2])}
                else:
                    tmpt_matrix[int(outputs['sourceIDs'][d1])][int(outputs['destIDs'][d1, d2])] = float(
                        outputs['Rates'][d1, d2])
        mig_matrix[mig_type] = tmpt_matrix

    for mig_type, output in mig_matrix.items():
        mf = MigrationFile(dg.idref, output)
        outputfile_name = os.path.splitext(base_demog_file)[0]
        outputfile_name = outputfile_name.replace('demographics', '')
        mf.save_as_txt('{}_{}_migration_new.txt'.format(outputfile_name, mig_type.lower()))
        mig_type = mig_type.lower()
        if mig_type in ['air', 'local', 'sea', 'regional']:
            mig_type_key = MigrationTypes[mig_type]
        else:
            raise (ValueError("Didn't know what mig_type {0} was".format(mig_type)))

        mf.generate_file('{}_{}_migration_new.bin'.format(outputfile_name, mig_type), mig_type_key)
