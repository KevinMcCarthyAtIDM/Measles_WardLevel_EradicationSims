##
"""
Measles Ward Simulations: Sample demographic
"""
#
import json
import math
import os
import random

from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.utils.reports import BaseReport, BaseAgeHistReport
from simtools.Analysis.AnalyzeManager import AnalyzeManager
from simtools.ModBuilder import ModBuilder, ModFn
from simtools.SetupParser import SetupParser
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from PythonAnalysis.Output2MatlabAnalyzer import Output2MatlabAnalyzer
from SetupFunctions import sample_point_fn

#Run on HPC
SetupParser.default_block = "HPC"

cb = DTKConfigBuilder.from_files(config_name='InputFiles\\config.json', campaign_name='InputFiles\\basecampaign.json')
cb.set_param('Num_Cores', 1)
cb.set_experiment_executable(path='Executable\\Eradication.exe')
cb.add_demog_overlay(name='demographics.json', content=json.load(open('InputFiles\\Nigeria_Ward_smaller_minpop5000_demographics.json')))
cb.experiment_files.add_file(path='InputFiles\\Nigeria_Ward_smaller_minpop5000_air_migration.bin')
cb.experiment_files.add_file(path='InputFiles\\Nigeria_Ward_smaller_minpop5000_air_migration.bin.json')
cb.experiment_files.add_file(path='InputFiles\\Nigeria_Ward_smaller_minpop5000_local_migration.bin')
cb.experiment_files.add_file(path='InputFiles\\Nigeria_Ward_smaller_minpop5000_local_migration.bin.json')
cb.experiment_files.add_file(path='InputFiles\\reports.json')
cb.experiment_files.add_file(path='reporter_plugins\\libReportAgeAtInfectionHistogram_plugin.dll')
cb.add_reports(BaseAgeHistReport(type='ReportPluginAgeAtInfectionHistogram',
                                 age_bins=[x/12 for x in range(1, 180)],
                                 interval_years=1))

if __name__ == "__main__":

    SetupParser.init('HPC')

    #camp = [.5, .5, .5, .001, .001, .001, .25, .25, .25, .75, .75, .75]*4
    #Mig = [0.2]*48
    #RIF = [1.0]*48
    #MCV1 = [*[270]*12, *[180]*12]*2
    #MCV2 = [0.25, 0.5, 1.0]*16
    #MaB = [*['Long']*24, *['Short']*24]
    #xB = [0.98]*48
    #Mig = [*[.02]*8, *[.002]*8, *[.0002]*8]
    #camp = [.001, .5, .001, .5, .001, .5, .001, .5]*3
    #RIF = [1.0, 1.0, 1.5, 1.5, 1.0, 1.0, 1.5, 1.5]*3
    #MCV1 = [270]*24
    #MCV2 = [.75]*24
    #MaB = ['Long']*24
    #xB = [.98, .98, .98, .98, .85, .85, .85, .85]*3
    basePop = 0.075

    for ind in range(len(camp)):
        mod_fns = []
        for n_samples in range(512):
            names = ['META_Vaccination_Threshold', 'META_Fraction_Meeting', 'META_campaign_coverage', 'Run_Number',
                     'META_Migration', 'Rural_Infectivity_Multiplier', 'META_MCV1Days', 'META_MaB_Profile', 'META_MCV2Frac',
                     'x_Birth', 'Base_Population_Scale_Factor', 'META_Timesteps']
            if random.uniform(0, 1) < 0.33:
                values = [random.uniform(0.4, 0.99), random.uniform(0.4, 0.99), camp[ind], random.randint(1, 1e6), Mig[ind], RIF[ind],
                          MCV1[ind], MaB[ind], MCV2[ind], xB[ind], basePop, 3.0]
            else:
                values = [0.4 + 0.59 * math.sqrt(random.uniform(0, 1)), 0.4 + 0.59 * math.sqrt(random.uniform(0, 1)), camp[ind],
                          random.randint(1, 1e6), Mig[ind], RIF[ind], MCV1[ind], MaB[ind], MCV2[ind], xB[ind], basePop, 3.0]
            mod_fns.append(ModFn(sample_point_fn, names, values))

        builder = ModBuilder.from_combos(mod_fns)

        # Name the experiment
        exp_name = 'Measles RI targets'
        run_sim_args = {'config_builder': cb,
                        'exp_name': exp_name,
                        'exp_builder': builder}

        exp_manager = ExperimentManagerFactory.from_cb(cb)
        exp_manager.experiment_tags = {}
        for name, value in zip(names, values):
            if name not in ['META_Vaccination_Threshold', 'META_Fraction_Meeting', 'Run_Number']:
                exp_manager.experiment_tags[name] = value
        exp_manager.bypass_missing = True
        exp_manager.run_simulations(**run_sim_args)
#    exp_manager.wait_for_finished(verbose=True)

#    am = AnalyzeManager('latest')
#    am.add_analyzer(Output2MatlabAnalyzer())
#    am.analyze()
