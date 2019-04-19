##
"""
Measles Ward Simulations: Sample demographic
"""
#
import os
import json
import math
import random

from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.utils.reports.BaseAgeHistReport import BaseAgeHistReport
from simtools.ModBuilder import ModBuilder, ModFn
from simtools.SetupParser import SetupParser
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
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
cb.add_reports(BaseAgeHistReport(type='ReportPluginAgeAtInfectionHistogram',
                                 age_bins=[x/12 for x in range(1, 180)],
                                 interval_years=1))

current_dir = os.path.dirname(os.path.realpath(__file__))
cb.set_dll_root(os.path.join(current_dir, "inputs", "dll"))


if __name__ == "__main__":

    SetupParser.init('HPC')

    #Scenarios to run - 28:

    UrbanMultiplier = [2, 2, 1.5, *[2]*25]
    RuralMultiplier = [1, 1.5, *[1]*26]
    Migration = [*[0.2]*3, 0.02, 0.002, 0.0002, *[0.2]*22]
    SIACov = [*[0.5]*6, -1, 0, .25, .75, *[0.5]*11, 0, 0.25, 0.75, *[-1]*4]
    Dropout = [*[0.25]*10, 0, 0.5, 0.75, 1.0, *[0.25]*7, *[1.0]*3, 0, 0.5, 0.75, 1.0]
    MCV2Days = [*[365]*14, 455, *[365]*13]
    MCV1Days = [*[270]*15, 180, 270, 180, *[270]*10]
    mAbProfile = [*['Mix']*16, 'Short', 'Short', *['Mix']*10]
    BirthRateScale= [*[0.98]*18, 0.905, 0.85, 0.81, *[0.98]*7]
    basePop = 0.075

    for ind in [2, 3]: #range(len(UrbanMultiplier)):
        mod_fns = []
        for n_samples in range(512):
            names = ['META_Vaccination_Threshold', 'META_Fraction_Meeting', 'META_campaign_coverage', 'Run_Number',
                     'META_Migration', 'Rural_Infectivity_Multiplier', 'Urban_Infectivity_Multiplier',
                     'META_MCV1Days', 'META_MaB_Profile', 'META_Dropout',
                     'META_MCV2Days', 'x_Birth', 'Base_Population_Scale_Factor', 'META_Timesteps']
            if random.uniform(0, 1) < 0.33:
                values = [random.uniform(0.4, 0.99), random.uniform(0.4, 0.99),
                          SIACov[ind], random.randint(1, 1e6), Migration[ind], RuralMultiplier[ind],
                          UrbanMultiplier[ind], MCV1Days[ind], mAbProfile[ind],
                          Dropout[ind], MCV2Days[ind], BirthRateScale[ind], basePop, 3.0]
            else:
                values = [0.4 + 0.59 * math.sqrt(random.uniform(0, 1)), 0.4 + 0.59 * math.sqrt(random.uniform(0, 1)),
                          SIACov[ind], random.randint(1, 1e6), Migration[ind], RuralMultiplier[ind],
                          UrbanMultiplier[ind], MCV1Days[ind], mAbProfile[ind],
                          Dropout[ind], MCV2Days[ind], BirthRateScale[ind], basePop, 3.0]
            mod_fns.append(ModFn(sample_point_fn, names, values))

        builder = ModBuilder.from_combos(mod_fns)

        # Name the experiment
        exp_name = 'Measles RI targets'
        exp_manager = ExperimentManagerFactory.from_cb(cb)
        # suite_id = exp_manager.create_suite("My experiment - Iteration 0")

        run_sim_args = {'config_builder': cb,
                        'exp_name': exp_name,
                        'exp_builder': builder}

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
