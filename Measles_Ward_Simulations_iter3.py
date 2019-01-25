##
"""
Measles Ward Simulations: Sample demographic
"""
#
import json
import math
import random

from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.utils.reports import BaseAgeHistReport
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
cb.experiment_files.add_file(path='reporter_plugins\\libReportAgeAtInfectionHistogram_plugin.dll')
cb.add_reports(BaseAgeHistReport(type='ReportPluginAgeAtInfectionHistogram',
                                 age_bins=[x/12 for x in range(1, 180)],
                                 interval_years=1))

if __name__ == "__main__":

    SetupParser.init('HPC')

    #Scenarios to run - 28:
    with open ('MatlabAnalysis\\outputs_iter2.json') as json_data:
        myparams = json.load(json_data)

    basePop = 0.075

    for ind in range(3, len(myparams)):
        theseparams = myparams[ind]
        UrbanMultiplier = theseparams['UrbanR0']/12.0
        RuralMultiplier = theseparams['RuralR0']/12.0
        Migration = theseparams['MigrationRate']
        SIACov = theseparams['CampaignCov']
        Dropout = theseparams['Dropout']
        MCV2Days = theseparams['MCV2Age']
        MCV1Days = theseparams['MCV1Age']
        mAbProfile = theseparams['MaBProfile']
        BirthRateScale = theseparams['BirthRate']
        expID1 = theseparams['expID1']
        expID2 = theseparams['expID2']
        names = ['META_Vaccination_Threshold', 'META_Fraction_Meeting', 'META_campaign_coverage', 'Run_Number',
                 'META_Migration', 'Rural_Infectivity_Multiplier', 'Urban_Infectivity_Multiplier',
                 'META_MCV1Days', 'META_MaB_Profile', 'META_Dropout',
                 'META_MCV2Days', 'x_Birth', 'Base_Population_Scale_Factor', 'META_Timesteps']

        mod_fns = []
        for n_samples in range(512):
            xsamp = -1
            ysamp = -1
            contourind = random.randint(0, len(theseparams['contourx'])-1)
            xs = theseparams['contourx'][contourind]
            ys = theseparams['contoury'][contourind]
            while xsamp<0.4 or xsamp>0.99 or ysamp<0.4 or ysamp>0.99:
                xsamp = xs+random.gauss(0, 0.075)
                ysamp = ys+random.gauss(0, 0.075)

            values = [xsamp, ysamp,
                        SIACov, random.randint(1, 1e6), Migration, RuralMultiplier,
                        UrbanMultiplier, MCV1Days, mAbProfile,
                        Dropout, MCV2Days, BirthRateScale, basePop, 3.0]
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
        exp_manager.experiment_tags['prev_expID1'] = expID1
        exp_manager.experiment_tags['prev_expID2'] = expID2
        for name, value in zip(names, values):
            if name not in ['META_Vaccination_Threshold', 'META_Fraction_Meeting', 'Run_Number']:
                exp_manager.experiment_tags[name] = value
        exp_manager.bypass_missing = True
        exp_manager.run_simulations(**run_sim_args)
#    exp_manager.wait_for_finished(verbose=True)

#    am = AnalyzeManager('latest')
#    am.add_analyzer(Output2MatlabAnalyzer())
#    am.analyze()
