
# TODO: Generalize this style of CalibAnalyzer as much as possible
#       to minimize repeated code in e.g. PrevalenceByAgeAnalyzer
import logging

from simtools.Analysis.BaseAnalyzers import BaseAnalyzer
from simtools.Utilities.Encoding import NumpyEncoder
import pandas as pd
import numpy as np
import json
import sys
import os
import time
from calibtool import LL_calculators
from mat4py import savemat

logger = logging.getLogger(__name__)


class Output2MatlabAnalyzer(BaseAnalyzer):

    def __init__(self):
        super().__init__()
        # self.metadata = {}
        # self.apply_ticker = 0

        self.filenames = ['output/InsetChart.json', 'output/AgeAtInfectionHistogramReport.json', 'output/SpatialReport_New_Infections.bin',
                          'output/SpatialReport_Prevalence.bin', 'output/SpatialReport_Population.bin']

    def select_simulation_data(self, data, simulation):
        '''
        Extract data from output data
        '''
        # self.apply_ticker += 1
        # print('Extracting data from parser ' + str(self.apply_ticker))
        selected_data = dict()

        selected_data['nodeIDs'] = data['output/SpatialReport_New_Infections.bin']['nodeids']
        for datatype in ['New_Infections', 'Prevalence', 'Population']:
            selected_data[datatype] = data['output/SpatialReport_' + datatype + '.bin']['data']
        for name, value in data['output/InsetChart.json']['Channels'].items():
            selected_data['all'+name] = value['Data']
        selected_data['age_bins'] = data['output/AgeAtInfectionHistogramReport.json']['Channels']['Age_Bin_Upper_Edges']['Data']
        selected_data['age_distribution'] = data['output/AgeAtInfectionHistogramReport.json']['Channels']['Accumulated_Binned_Infection_Counts']['Data']
        selected_data['sim_id'] = simulation.id
        selected_data['sample'] = simulation.tags.get('__sample_index__')
        selected_data['metadata'] = simulation.tags
        # self.metadata[simulation.tags.get('__sample_index__')] = simulation.tags

        savemat(os.path.join(self.working_dir, 'output_' + str(selected_data['sample']) + '.mat'), selected_data)


        return simulation.tags


    def finalize(self, all_data):
        metadata = {}
        for simulation, selected_data in all_data.items():
            metadata[simulation.id] = selected_data
        json.dump(metadata, open(os.path.join(self.working_dir, 'metadata_output.json'), 'wb'), cls=NumpyEncoder,  indent=3)