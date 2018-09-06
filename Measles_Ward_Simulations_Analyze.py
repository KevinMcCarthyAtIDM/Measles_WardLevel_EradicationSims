##
"""
Measles Ward Simulations: Sample demographic
"""
#
import json
import os

from simtools.Analysis.AnalyzeManager import AnalyzeManager
from simtools.Utilities.Encoding import NumpyEncoder

from PythonAnalysis.Output2MatlabAnalyzer import Output2MatlabAnalyzer
from simtools.Utilities.COMPSUtilities import get_experiment_by_id
from COMPS import Client
from COMPS.Data import QueryCriteria

Client.login('https://comps.idmod.org')

if __name__ == "__main__":
    exp_list = ['ea1e506d-25a7-e811-a2c0-c4346bcb7275', '96583fdd-27a7-e811-a2c0-c4346bcb7275',
                'cb60414a-fda7-e811-a2c0-c4346bcb7275', '7e7edfb2-fda7-e811-a2c0-c4346bcb7275',
                '30c13b96-9ba8-e811-a2c0-c4346bcb7275', 'f626a243-9ca8-e811-a2c0-c4346bcb7275',
                'b95874b8-9ca8-e811-a2c0-c4346bcb7275', '64ef6572-9da8-e811-a2c0-c4346bcb7275',
                'b9314306-9fa8-e811-a2c0-c4346bcb7275', '7bf00e89-44a9-e811-a2c0-c4346bcb7275',
                '521a5f3f-5faa-e811-a2c0-c4346bcb7275', 'f5ffd5d3-5faa-e811-a2c0-c4346bcb7275',
                '0d1d0b11-f8ab-e811-a2c0-c4346bcb7275', 'e522c5a5-f8ab-e811-a2c0-c4346bcb7275',
                '132fb72a-faab-e811-a2c0-c4346bcb7275',
                '357bb128-fcab-e811-a2c0-c4346bcb7275', '2de90287-a4ac-e811-a2c0-c4346bcb7275',
                '2c1cfe5a-bfad-e811-a2c0-c4346bcb7275',  '1d4d8efd-c4ad-e811-a2c0-c4346bcb7275',
                '5e831390-c5ad-e811-a2c0-c4346bcb7275',  'bed13430-c6ad-e811-a2c0-c4346bcb7275',
                'b34657d6-c6ad-e811-a2c0-c4346bcb7275',  '81e0fb82-c7ad-e811-a2c0-c4346bcb7275',
                '67c7c029-c8ad-e811-a2c0-c4346bcb7275',  '7885fbd6-c8ad-e811-a2c0-c4346bcb7275',
                'af2a0284-c9ad-e811-a2c0-c4346bcb7275',  'ef609e31-caad-e811-a2c0-c4346bcb7275',
                '71cfc7e0-caad-e811-a2c0-c4346bcb7275',  'd3122493-cbad-e811-a2c0-c4346bcb7275',
                '75988d4a-ccad-e811-a2c0-c4346bcb7275',  '7b88a9fa-ccad-e811-a2c0-c4346bcb7275',
                'a70ed6b0-cdad-e811-a2c0-c4346bcb7275',  '6316e468-cead-e811-a2c0-c4346bcb7275',
                '944e3127-cfad-e811-a2c0-c4346bcb7275',  '539b41e3-cfad-e811-a2c0-c4346bcb7275',
                '96bf669e-d0ad-e811-a2c0-c4346bcb7275',  'da60c660-d1ad-e811-a2c0-c4346bcb7275',
                '2417ed1b-d2ad-e811-a2c0-c4346bcb7275',  'bd9abedf-d2ad-e811-a2c0-c4346bcb7275',
                '344891a5-d3ad-e811-a2c0-c4346bcb7275',  '86551466-d4ad-e811-a2c0-c4346bcb7275',
                '467268eb-f6ae-e811-a2c0-c4346bcb7275', '05de6868-f7ae-e811-a2c0-c4346bcb7275',
                'ca2656ea-f7ae-e811-a2c0-c4346bcb7275', 'df8e9b69-f8ae-e811-a2c0-c4346bcb7275',
                'ff73a1ee-f8ae-e811-a2c0-c4346bcb7275', 'd899cb6f-f9ae-e811-a2c0-c4346bcb7275',
                '523f440a-faae-e811-a2c0-c4346bcb7275', '627a50ab-faae-e811-a2c0-c4346bcb7275',
                '2ed76556-fbae-e811-a2c0-c4346bcb7275', '0e9282fb-fbae-e811-a2c0-c4346bcb7275',
                'b96ae7a5-fcae-e811-a2c0-c4346bcb7275', 'e533db53-fdae-e811-a2c0-c4346bcb7275',
                '42e59d03-feae-e811-a2c0-c4346bcb7275', '5bc6d9af-feae-e811-a2c0-c4346bcb7275',
                'a31ebe61-ffae-e811-a2c0-c4346bcb7275', '3c5b821a-00af-e811-a2c0-c4346bcb7275',
                'a59301cc-00af-e811-a2c0-c4346bcb7275', '02b38283-01af-e811-a2c0-c4346bcb7275',
                '5a0dd13f-02af-e811-a2c0-c4346bcb7275', 'bc7978f6-02af-e811-a2c0-c4346bcb7275',
                'cdfc10b3-03af-e811-a2c0-c4346bcb7275', '8d7bb174-04af-e811-a2c0-c4346bcb7275',
                'c5bf6431-05af-e811-a2c0-c4346bcb7275', '122b7cf4-05af-e811-a2c0-c4346bcb7275'
                ]
    for exp in exp_list:
        tmp = get_experiment_by_id(exp, query_criteria=QueryCriteria().select_children(["tags"]))
        with open(os.path.join('Experiments', 'experiment_metadata.json'), 'r', encoding='utf8') as jsonfile:
            exp_metadata = json.load(jsonfile)
        exp_metadata[exp] = tmp.tags
        with open(os.path.join('Experiments', 'experiment_metadata.json'), 'w', encoding='utf8') as jsonfile:
            json.dump(exp_metadata, jsonfile, cls=NumpyEncoder, indent=3)

        am = AnalyzeManager(exp)
        am.add_analyzer(Output2MatlabAnalyzer())
        am.analyze()
