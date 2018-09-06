
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

    def __init__(self, working_dir=None):
        super().__init__(working_dir=working_dir)
        # self.metadata = {}
        # self.apply_ticker = 0

        self.filenames = ['output/InsetChart.json', 'output/AgeAtInfectionHistogramReport.json', 'output/SpatialReport_New_Infections.bin',
                          'output/SpatialReport_Prevalence.bin', 'output/SpatialReport_Population.bin']


    def per_experiment(self, experiment):
        outdir = os.path.join(self.working_dir, 'Experiments', experiment.exp_id)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    def select_simulation_data(self, data, simulation):
        '''
        Extract data from output data
        '''
        # self.apply_ticker += 1
        # print('Extracting data from parser ' + str(self.apply_ticker))
        selected_data = dict()

        selected_data['nodeIDs'] = data['output/SpatialReport_New_Infections.bin']['nodeids'].tolist()
        for datatype in ['New_Infections', 'Prevalence', 'Population']:
            selected_data[datatype] = data['output/SpatialReport_' + datatype + '.bin']['data'].tolist()
        for name, value in data['output/InsetChart.json']['Channels'].items():
            selected_data[(('all'+name).replace(' ', '').replace('_', '').replace('(', '').replace(')', ''))[0:20]] = value['Data']
        selected_data['age_bins'] = data['output/AgeAtInfectionHistogramReport.json']['Channels']['Age_Bin_Upper_Edges']['Data']
        selected_data['age_distribution'] = data['output/AgeAtInfectionHistogramReport.json']['Channels']['Accumulated_Binned_Infection_Counts']['Data']
        selected_data['sim_id'] = simulation.id
        selected_data['exp_id'] = simulation.experiment_id

        outdir = os.path.join(self.working_dir, 'Experiments', selected_data['exp_id'])

        savemat(os.path.join(outdir, 'output_' + str(selected_data['sim_id']) + '.mat'), selected_data)

        return simulation.tags


    def finalize(self, all_data):
        metadata = {}
        for simulation, selected_data in all_data.items():
            metadata[simulation.id] = selected_data
        json.dump(metadata, open(os.path.join(self.working_dir, 'Experiments', simulation.experiment_id, 'metadata_output.json'), 'w', encoding='utf8'), cls=NumpyEncoder,  indent=3)