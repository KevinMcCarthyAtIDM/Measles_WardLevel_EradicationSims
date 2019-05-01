##
"""
Measles Ward Simulations: Sample demographic
"""
#
import json
import os

from simtools.SetupParser import SetupParser
from simtools.Analysis.AnalyzeManager import AnalyzeManager
from simtools.Utilities.Encoding import NumpyEncoder

from PythonAnalysis.Output2MatlabAnalyzer import Output2MatlabAnalyzer
from simtools.Utilities.COMPSUtilities import get_experiment_by_id
from COMPS.Data import QueryCriteria

SetupParser.default_block = "HPC"


def load_experiments_from_file():
    # load file post_channel_config.json
    ref_exp = json.load(open(os.path.join("Experiments", "experiments.json"), 'rb'))
    return ref_exp


if __name__ == "__main__":
    SetupParser.init()

    exp_list = ["173fa938-40b6-e811-a2c0-c4346bcb7275",
                "eeacb2da-40b6-e811-a2c0-c4346bcb7275",
                "26f0d194-41b6-e811-a2c0-c4346bcb7275",
                "acf5a039-42b6-e811-a2c0-c4346bcb7275",
                "1e7f74eb-42b6-e811-a2c0-c4346bcb7275",
                "28e0b38a-43b6-e811-a2c0-c4346bcb7275",
                "2ffdba43-44b6-e811-a2c0-c4346bcb7275",
                "164a65fc-44b6-e811-a2c0-c4346bcb7275",
                "4acc5eb6-45b6-e811-a2c0-c4346bcb7275",
                "0360df79-46b6-e811-a2c0-c4346bcb7275",
                "f3ad9c4c-47b6-e811-a2c0-c4346bcb7275",
                "7986750d-48b6-e811-a2c0-c4346bcb7275",
                "11afc9ce-48b6-e811-a2c0-c4346bcb7275",
                "e5d30696-49b6-e811-a2c0-c4346bcb7275",
                "19c30858-4ab6-e811-a2c0-c4346bcb7275",
                "a7af2c1b-4bb6-e811-a2c0-c4346bcb7275",
                "9681c9e6-4bb6-e811-a2c0-c4346bcb7275",
                "b81e40b3-4cb6-e811-a2c0-c4346bcb7275",
                "06828780-4db6-e811-a2c0-c4346bcb7275",
                "fc398352-4eb6-e811-a2c0-c4346bcb7275",
                "9923121f-4fb6-e811-a2c0-c4346bcb7275",
                "3d8e8bee-4fb6-e811-a2c0-c4346bcb7275",
                "9e1785ca-50b6-e811-a2c0-c4346bcb7275",
                "e96ff59e-51b6-e811-a2c0-c4346bcb7275",
                "71e24788-52b6-e811-a2c0-c4346bcb7275",
                "8461b95f-53b6-e811-a2c0-c4346bcb7275",
                "1068e93c-54b6-e811-a2c0-c4346bcb7275",
                "79523f2b-55b6-e811-a2c0-c4346bcb7275",
                "07c3b28d-deb7-e811-a2c0-c4346bcb7275",
                "3b4aef1a-dfb7-e811-a2c0-c4346bcb7275",
                'e575f453-7fd9-e811-a2bd-c4346bcb1555', '0cbf770d-0eda-e811-a2bd-c4346bcb1555',
                'e7795791-0eda-e811-a2bd-c4346bcb1555', 'dacee39f-25da-e811-a2bd-c4346bcb1555',
                'd879294b-26da-e811-a2bd-c4346bcb1555', '29af10f0-26da-e811-a2bd-c4346bcb1555',
                'be3dc09c-27da-e811-a2bd-c4346bcb1555', '5603644d-28da-e811-a2bd-c4346bcb1555',
                '969413fc-28da-e811-a2bd-c4346bcb1555', 'a2efdcad-29da-e811-a2bd-c4346bcb1555',
                '71a3845f-2ada-e811-a2bd-c4346bcb1555', 'e3316513-2bda-e811-a2bd-c4346bcb1555',
                'd25705c5-2bda-e811-a2bd-c4346bcb1555', '20007b7a-2cda-e811-a2bd-c4346bcb1555',
                '7632a638-2dda-e811-a2bd-c4346bcb1555', 'da9427f1-2dda-e811-a2bd-c4346bcb1555',
                '66895fac-2eda-e811-a2bd-c4346bcb1555', '5e7a6867-2fda-e811-a2bd-c4346bcb1555',
                'b8d37624-30da-e811-a2bd-c4346bcb1555', '440790e9-30da-e811-a2bd-c4346bcb1555',
                '4337dfa7-31da-e811-a2bd-c4346bcb1555', '2001e07b-32da-e811-a2bd-c4346bcb1555',
                '3c75e943-33da-e811-a2bd-c4346bcb1555', '9ef11c0e-34da-e811-a2bd-c4346bcb1555',
                '3b614bd7-34da-e811-a2bd-c4346bcb1555', '7e065aa6-35da-e811-a2bd-c4346bcb1555',
                '010b9977-36da-e811-a2bd-c4346bcb1555', '5a125a44-37da-e811-a2bd-c4346bcb1555',
                'bfef24ea-cee2-e811-a2bd-c4346bcb1555', '61404201-cee2-e811-a2bd-c4346bcb1555',
                '866a3a20-cde2-e811-a2bd-c4346bcb1555', '0d84e743-cce2-e811-a2bd-c4346bcb1555',
                '747f3f63-cbe2-e811-a2bd-c4346bcb1555', '9a61be8c-cae2-e811-a2bd-c4346bcb1555',
                '52ce22b5-c9e2-e811-a2bd-c4346bcb1555', '6117dcd9-c8e2-e811-a2bd-c4346bcb1555',
                '81bebc0b-c8e2-e811-a2bd-c4346bcb1555', '501bb73a-c7e2-e811-a2bd-c4346bcb1555',
                '87f0236a-c6e2-e811-a2bd-c4346bcb1555', 'af15e496-c5e2-e811-a2bd-c4346bcb1555',
                'e63697c0-c4e2-e811-a2bd-c4346bcb1555', 'b80b63ec-c3e2-e811-a2bd-c4346bcb1555',
                '7e386d0d-c3e2-e811-a2bd-c4346bcb1555', 'b24b5e48-c2e2-e811-a2bd-c4346bcb1555',
                'fa4be499-c1e2-e811-a2bd-c4346bcb1555', '1afdafd8-c0e2-e811-a2bd-c4346bcb1555',
                'ad7d4128-c0e2-e811-a2bd-c4346bcb1555', 'c44c307d-bfe2-e811-a2bd-c4346bcb1555',
                'e7c26a6a-b7e2-e811-a2bd-c4346bcb1555', '604d5bc8-b6e2-e811-a2bd-c4346bcb1555',
                'f8394f29-b6e2-e811-a2bd-c4346bcb1555', 'cd70a86e-b5e2-e811-a2bd-c4346bcb1555',
                'c47d78b3-b4e2-e811-a2bd-c4346bcb1555', 'c6cbf126-59dd-e811-a2bd-c4346bcb1555',
                'c9eef583-58dd-e811-a2bd-c4346bcb1555', '50a088ee-57dd-e811-a2bd-c4346bcb1555'
                ]

    ref_exp = load_experiments_from_file()
    for exp in exp_list:

        tmp = get_experiment_by_id(exp, query_criteria=QueryCriteria().select_children(["tags"]))
        if (exp in ref_exp) or (any([sim.state.value != 6 for sim in tmp.get_simulations()])):
            continue

        with open(os.path.join('Experiments', 'experiment_metadata.json'), 'r', encoding='utf8') as jsonfile:
            exp_metadata = json.load(jsonfile)
        exp_metadata[exp] = tmp.tags
        with open(os.path.join('Experiments', 'experiment_metadata.json'), 'w', encoding='utf8') as jsonfile:
            json.dump(exp_metadata, jsonfile, cls=NumpyEncoder, indent=3)

        am = AnalyzeManager(exp)
        am.add_analyzer(Output2MatlabAnalyzer())
        am.analyze()
