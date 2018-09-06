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
                '2c1cfe5a-bfad-e811-a2c0-c4346bcb7275', '1d4d8efd-c4ad-e811-a2c0-c4346bcb7275',
                '5e831390-c5ad-e811-a2c0-c4346bcb7275', 'bed13430-c6ad-e811-a2c0-c4346bcb7275',
                'b34657d6-c6ad-e811-a2c0-c4346bcb7275', '81e0fb82-c7ad-e811-a2c0-c4346bcb7275',
                '67c7c029-c8ad-e811-a2c0-c4346bcb7275', '7885fbd6-c8ad-e811-a2c0-c4346bcb7275',
                'af2a0284-c9ad-e811-a2c0-c4346bcb7275', 'ef609e31-caad-e811-a2c0-c4346bcb7275',
                '71cfc7e0-caad-e811-a2c0-c4346bcb7275', 'd3122493-cbad-e811-a2c0-c4346bcb7275',
                '75988d4a-ccad-e811-a2c0-c4346bcb7275', '7b88a9fa-ccad-e811-a2c0-c4346bcb7275',
                'a70ed6b0-cdad-e811-a2c0-c4346bcb7275', '6316e468-cead-e811-a2c0-c4346bcb7275',
                '944e3127-cfad-e811-a2c0-c4346bcb7275', '539b41e3-cfad-e811-a2c0-c4346bcb7275',
                '96bf669e-d0ad-e811-a2c0-c4346bcb7275', 'da60c660-d1ad-e811-a2c0-c4346bcb7275',
                '2417ed1b-d2ad-e811-a2c0-c4346bcb7275', 'bd9abedf-d2ad-e811-a2c0-c4346bcb7275',
                '344891a5-d3ad-e811-a2c0-c4346bcb7275', '86551466-d4ad-e811-a2c0-c4346bcb7275',
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
                'c5bf6431-05af-e811-a2c0-c4346bcb7275', '122b7cf4-05af-e811-a2c0-c4346bcb7275',
                '56a6ed7f-71b0-e811-a2c0-c4346bcb7275', '698d2404-72b0-e811-a2c0-c4346bcb7275',
                '08ce0788-72b0-e811-a2c0-c4346bcb7275', 'bbc5fb07-73b0-e811-a2c0-c4346bcb7275',
                '43a64592-73b0-e811-a2c0-c4346bcb7275', 'fb38ae1f-74b0-e811-a2c0-c4346bcb7275',
                'a8e114aa-74b0-e811-a2c0-c4346bcb7275', '89c9b338-75b0-e811-a2c0-c4346bcb7275',
                'd12f9ec8-75b0-e811-a2c0-c4346bcb7275', '9bcf6360-76b0-e811-a2c0-c4346bcb7275',
                '28282c10-77b0-e811-a2c0-c4346bcb7275', '8cb671c2-77b0-e811-a2c0-c4346bcb7275',
                '16a780d9-78b0-e811-a2c0-c4346bcb7275', 'e4526879-79b0-e811-a2c0-c4346bcb7275',
                'bee39b19-7ab0-e811-a2c0-c4346bcb7275', '7a49a9c0-7ab0-e811-a2c0-c4346bcb7275',
                'dbb4a765-7bb0-e811-a2c0-c4346bcb7275', '0a3e4708-7cb0-e811-a2c0-c4346bcb7275',
                'fe0a50b4-7cb0-e811-a2c0-c4346bcb7275', '7ee4f25d-7db0-e811-a2c0-c4346bcb7275',
                '82bf8608-7eb0-e811-a2c0-c4346bcb7275', 'f9900cb6-7eb0-e811-a2c0-c4346bcb7275',
                'd2b78263-7fb0-e811-a2c0-c4346bcb7275', 'eeda121a-80b0-e811-a2c0-c4346bcb7275',
                '85e1d7cb-80b0-e811-a2c0-c4346bcb7275', 'aa5f9780-81b0-e811-a2c0-c4346bcb7275',
                'bef36933-82b0-e811-a2c0-c4346bcb7275', 'f85e9feb-82b0-e811-a2c0-c4346bcb7275',
                'c89b7ba3-83b0-e811-a2c0-c4346bcb7275', '05f3c561-84b0-e811-a2c0-c4346bcb7275',
                'a8474822-85b0-e811-a2c0-c4346bcb7275', 'ee4410e0-85b0-e811-a2c0-c4346bcb7275',
                '53252da0-86b0-e811-a2c0-c4346bcb7275', 'df2dc263-87b0-e811-a2c0-c4346bcb7275',
                '29cda42b-88b0-e811-a2c0-c4346bcb7275', 'd4d307ef-88b0-e811-a2c0-c4346bcb7275',
                'a68b4c12-9fb1-e811-a2c0-c4346bcb7275', '04f442c6-9fb1-e811-a2c0-c4346bcb7275',
                '2a00b979-a0b1-e811-a2c0-c4346bcb7275', 'dfebd731-a1b1-e811-a2c0-c4346bcb7275',
                '059671eb-a1b1-e811-a2c0-c4346bcb7275', '39deb7a4-a2b1-e811-a2c0-c4346bcb7275',
                'd764f35f-a3b1-e811-a2c0-c4346bcb7275', '6537d21f-a4b1-e811-a2c0-c4346bcb7275',
                '4cbf6fe3-a4b1-e811-a2c0-c4346bcb7275', 'f50505a3-a5b1-e811-a2c0-c4346bcb7275',
                '8d987263-a6b1-e811-a2c0-c4346bcb7275', '4547b435-a7b1-e811-a2c0-c4346bcb7275',
                'be4a4172-a9b1-e811-a2c0-c4346bcb7275', '687b7624-aab1-e811-a2c0-c4346bcb7275',
                'a4f79ad4-aab1-e811-a2c0-c4346bcb7275', '24843684-abb1-e811-a2c0-c4346bcb7275',
                'f5a3a836-acb1-e811-a2c0-c4346bcb7275', '16d398ef-acb1-e811-a2c0-c4346bcb7275',
                '6fa57ba3-adb1-e811-a2c0-c4346bcb7275', '137fec5e-aeb1-e811-a2c0-c4346bcb7275',
                '63547420-afb1-e811-a2c0-c4346bcb7275', '122f1add-afb1-e811-a2c0-c4346bcb7275',
                '254ea69c-b0b1-e811-a2c0-c4346bcb7275', '362e0a63-b1b1-e811-a2c0-c4346bcb7275',
                'd1a75a29-b2b1-e811-a2c0-c4346bcb7275', '815f4ff3-b2b1-e811-a2c0-c4346bcb7275',
                '00066cba-b3b1-e811-a2c0-c4346bcb7275', '67c90b8a-b4b1-e811-a2c0-c4346bcb7275',
                'fd3d2656-b5b1-e811-a2c0-c4346bcb7275', '6456eb2b-b6b1-e811-a2c0-c4346bcb7275',
                'c759c5f5-b6b1-e811-a2c0-c4346bcb7275', 'd0fd3cd1-b7b1-e811-a2c0-c4346bcb7275',
                '6c6e76aa-b8b1-e811-a2c0-c4346bcb7275', 'af580c7e-b9b1-e811-a2c0-c4346bcb7275',
                '42766253-bab1-e811-a2c0-c4346bcb7275', 'c6dddc22-bbb1-e811-a2c0-c4346bcb7275',
                '15852304-bcb1-e811-a2c0-c4346bcb7275', '5a1e0ce4-bcb1-e811-a2c0-c4346bcb7275',
                '4ce584d1-bdb1-e811-a2c0-c4346bcb7275', 'ba44a6ac-beb1-e811-a2c0-c4346bcb7275',
                '2d976692-bfb1-e811-a2c0-c4346bcb7275', 'd8f6ac78-c0b1-e811-a2c0-c4346bcb7275',
                '09cae95e-c1b1-e811-a2c0-c4346bcb7275', '77668448-c2b1-e811-a2c0-c4346bcb7275',
                '33273c40-c3b1-e811-a2c0-c4346bcb7275', '45d7da2a-c4b1-e811-a2c0-c4346bcb7275',
                '8f971917-c5b1-e811-a2c0-c4346bcb7275', 'd4f42403-c6b1-e811-a2c0-c4346bcb7275',
                '2b3e58fa-c6b1-e811-a2c0-c4346bcb7275', '715c74f5-c7b1-e811-a2c0-c4346bcb7275',
                '1cd2a2fb-c8b1-e811-a2c0-c4346bcb7275', 'a5aafaf2-c9b1-e811-a2c0-c4346bcb7275',
                '160b83f5-cab1-e811-a2c0-c4346bcb7275', '367f66f4-cbb1-e811-a2c0-c4346bcb7275',
                'b7f2a5fa-ccb1-e811-a2c0-c4346bcb7275', 'fdd088fb-cdb1-e811-a2c0-c4346bcb7275',
                'ff99de13-cfb1-e811-a2c0-c4346bcb7275', 'db433a21-d0b1-e811-a2c0-c4346bcb7275',
                'acde082e-d1b1-e811-a2c0-c4346bcb7275', 'ef2c7d38-d2b1-e811-a2c0-c4346bcb7275'
                ]
    for exp in exp_list:
        tmp = get_experiment_by_id(exp, query_criteria=QueryCriteria().select_children(["tags"]))
        if (os.path.exists(os.path.join('Experiments', exp))) or (any([sim.state.value != 6 for sim in tmp.get_simulations()])):
            continue

        with open(os.path.join('Experiments', 'experiment_metadata.json'), 'r', encoding='utf8') as jsonfile:
            exp_metadata = json.load(jsonfile)
        exp_metadata[exp] = tmp.tags
        with open(os.path.join('Experiments', 'experiment_metadata.json'), 'w', encoding='utf8') as jsonfile:
            json.dump(exp_metadata, jsonfile, cls=NumpyEncoder, indent=3)

        am = AnalyzeManager(exp)
        am.add_analyzer(Output2MatlabAnalyzer())
        am.analyze()
