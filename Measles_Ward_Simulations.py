##
"""
Measles Ward Simulations: Sample demographic
"""
#
import json
import random

from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.utils.reports import BaseReport
from simtools.Analysis.AnalyzeManager import AnalyzeManager
from simtools.ModBuilder import ModBuilder, ModFn
from simtools.SetupParser import SetupParser
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from PythonAnalysis.Output2MatlabAnalyzer import Output2MatlabAnalyzer
from SetupFunctions import sample_point_fn

#Run on HPC
SetupParser.default_block = "HPC"

cb = DTKConfigBuilder.from_files(config_name='InputFiles\\config.json', campaign_name='InputFiles\\basecampaign.json')
cb.set_experiment_executable(path='Executable\\Eradication.exe')
cb.add_demog_overlay(name='demographics.json', content=json.load(open('InputFiles\\Nigeria_Ward_minpop5000_demographics.json')))
cb.experiment_files.add_file(path='InputFiles\\Nigeria_Ward_minpop5000_air_migration.bin')
cb.experiment_files.add_file(path='InputFiles\\Nigeria_Ward_minpop5000_air_migration.bin.json')
cb.experiment_files.add_file(path='InputFiles\\Nigeria_Ward_minpop5000_local_migration.bin')
cb.experiment_files.add_file(path='InputFiles\\Nigeria_Ward_minpop5000_local_migration.bin.json')
cb.experiment_files.add_file(path='InputFiles\\reports.json')
cb.experiment_files.add_file(path='reporter_plugins\\libReportAgeAtInfectionHistogram_plugin.dll')
cb.add_reports(BaseReport(type='AgeAtInfectionHistogramReport'))

mod_fns = []

for n_samples in range(2):
    names = ['META_Vaccination_Threshold', 'META_Fraction_Meeting', 'META_campaign_coverage', 'Run_Number', 'META_Migration']
    values = [random.uniform(0.5, 0.95), random.uniform(0.5, 0.95), 0.25, random.randint(1, 1e6), 1.0]
    mod_fns.append(ModFn(sample_point_fn, names, values))

builder = ModBuilder.from_combos(mod_fns)

#Name the experiment
exp_name = 'Testing measles eradication pre-condition targets'
run_sim_args = {'config_builder': cb,
                'exp_name': exp_name,
                'exp_builder': builder}
analyzers = [
    Output2MatlabAnalyzer(name='Output2MatlabAnalyzer')
            ]
if __name__ == "__main__":

    SetupParser.init('HPC')
    exp_manager = ExperimentManagerFactory.from_cb(cb)
    exp_manager.bypass_missing = True
    exp_manager.run_simulations(**run_sim_args)
    exp_manager.wait_for_finished(verbose=True)

    am = AnalyzeManager('latest')
    map(am.add_analyzer, analyzers)
    am.analyze()
