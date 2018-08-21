
# TODO: Generalize this style of CalibAnalyzer as much as possible
#       to minimize repeated code in e.g. PrevalenceByAgeAnalyzer
import logging
from simtools.Utilities.Encoding import NumpyEncoder
import pandas as pd
import numpy as np
import json
import sys
import os
import time
from calibtool import LL_calculators
from mat4py import savemat
from dtk.utils.analyzers.BaseAnalyzer import BaseAnalyzer

logger = logging.getLogger(__name__)


class Output2MatlabAnalyzer(BaseAnalyzer):

    filenames = ['output/InsetChart.json', 'output/AgeAtInfectionHistogramReport.json', 'output/SpatialReport_New_Infections.bin',
                 'output/SpatialReport_Prevalence.bin', 'output/SpatialReport_Population.bin']

    def __init__(self, name):
        super(Output2MatlabAnalyzer, self).__init__()
        self.name = name
        self.metadata = {}
        self.apply_ticker = 0

    def filter(self):
        return True

    def apply(self, parser):
        '''
        Extract data from output data
        '''
        self.apply_ticker += 1
        print('Extracting data from parser ' + str(self.apply_ticker))
        selected_data = dict()

        selected_data['nodeIDs'] = parser.raw_data['output/SpatialReport_New_Infections.bin']['nodeids']
        for datatype in ['New_Infections', 'Prevalence', 'Population']:
            selected_data[datatype] = parser.raw_data['output/SpatialReport_' + datatype + '.bin']['data']
        for name, value in parser.raw_data['output/InsetChart.json']['Channels'].items():
            selected_data['all'+name] = value['Data']
        selected_data['age_bins'] = parser.raw_data['output/AgeAtInfectionHistogramReport.json']['Channels']['Age_Bin_Upper_Edges']['Data']
        selected_data['age_distribution'] = parser.raw_data['output/AgeAtInfectionHistogramReport.json']['Channels']['Accumulated_Binned_Infection_Counts']['Data']
        selected_data['sim_id'] = parser.sim_id
        selected_data['sample'] = parser.sim_data.get('__sample_index__')
        selected_data['metadata'] = parser.sim_data
        self.metadata[parser.sim_data.get('__sample_index__')] = parser.sim_data

        savemat(os.path.join(self.working_dir, 'output_' + str(selected_data['sample']) + '.mat'), selected_data)
        selected_data.clear()

        return selected_data

    def combine(self, parsers):
        '''
        Combine the simulation data into a single table for all analyzed simulations.
        '''
        #self.data = [p.selected_data[id(self)] for p in parsers.values() if id(self) in p.selected_data]

    def compare(self, sample):
        '''
        Assess the result per sample, in this case the likelihood
        comparison between simulation and reference data.
        '''

    def finalize(self):
        '''
        Calculate the output result for each sample.
        '''
        json.dump(self.metadata, open(os.path.join(self.working_dir, 'metadata_output.json'), 'wb'), cls=NumpyEncoder,
                  indent=3)


    def cache(self):
        '''
        Return a cache of the minimal data required for plotting sample comparisons
        to reference comparisons.
        '''
        pass

    def uid(self):
        ''' A unique identifier of site-name and analyzer-name. '''
        return '_'.join([self.site.name, self.name])
