from simtools.Utilities.COMPSUtilities import get_experiment_by_id
from COMPS import Client
from COMPS.Data import QueryCriteria

Client.login('https://comps.idmod.org')

exp_list = ['ea1e506d-25a7-e811-a2c0-c4346bcb7275', '96583fdd-27a7-e811-a2c0-c4346bcb7275',
                'cb60414a-fda7-e811-a2c0-c4346bcb7275', '7e7edfb2-fda7-e811-a2c0-c4346bcb7275',
                '30c13b96-9ba8-e811-a2c0-c4346bcb7275', 'f626a243-9ca8-e811-a2c0-c4346bcb7275',
                'b95874b8-9ca8-e811-a2c0-c4346bcb7275', '64ef6572-9da8-e811-a2c0-c4346bcb7275',
                'b9314306-9fa8-e811-a2c0-c4346bcb7275', '7bf00e89-44a9-e811-a2c0-c4346bcb7275',
                '521a5f3f-5faa-e811-a2c0-c4346bcb7275', 'f5ffd5d3-5faa-e811-a2c0-c4346bcb7275']
rural_mult = [1.0, 1.0, 1.5, 1.5, 1.0, 1.0, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0]
coverage = [0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5]
migration = [.2, .2, .2, .2, .2, .2, .2, .2, .02, .02, .002, .002]
AgeAtVacc = [270, 270, 270, 270, 180, 180, 180, 180, 270, 270, 270, 270]

for ii in range(len(exp_list)):
    exp = get_experiment_by_id(exp_list[ii], query_criteria=QueryCriteria().select_children(["tags"]))
    exp.merge_tags({'Rural_Infectivity_Multiplier': rural_mult[ii], 'META_Campaign_Coverage': coverage[ii], 'META_Migration': migration[ii], 'MCV1_Dose_Days': AgeAtVacc[ii]})
