import math
import random
from scipy.special import erfinv

def sample_point_fn(cb, param_names, param_values):
    tags ={}
    required_inputs = ['META_Vaccination_Threshold', 'META_Fraction_Meeting', 'META_campaign_coverage', 'META_MCV2Frac']
    if not set(required_inputs).issubset(set(param_names)):
        raise ValueError('All of ' + ', '.join(required_inputs) + ' must be inputs to sample_point_fn')

    # Setup some baseline parameters, but allow them to be overwritten afterwards by inputs to this function
    params_dict = Setup_Base_Parameters()

    for name, value in zip(param_names, param_values):
        params_dict[name] = value

    RI_Vacc_Setup(cb, params_dict['META_Vaccination_Threshold'], params_dict['META_Fraction_Meeting'],
                  params_dict['META_MCV2Frac'], tags)
    SIA_Coverage_setup(cb, params_dict['META_campaign_coverage'])

    #Now I am through the required parameters
    for param, value in params_dict.items():
        if param.startswith('META'):
            tags = MetaParameterHandler(cb, param, value, tags)
        else:
            cb.set_param(param, value)
        tags[param] = value
    return tags

def Setup_Base_Parameters():
    # Set some defaults here, but allow them to be overwritten by inputs to the function
    params_dict = dict()
    params_dict['Base_Population_Scale_Factor'] = 0.075
    params_dict['x_Birth'] = 0.98
    params_dict['x_Local_Migration'] = 1.0
    params_dict['x_Air_Migration'] = 1.0
    params_dict['Base_Infectivity'] = 0.6  # R0 of 12 in rural settings
    params_dict['Population_Density_Infectivity_Correction'] = 'URBAN_RURAL_INFECTIVITY'
    params_dict['Rural_Infectivity_Multiplier'] = 1.0
    params_dict['Urban_Infectivity_Multiplier'] = 2.0  # R0 of 24 in urban settings
    params_dict['Relative_Sample_Rate_Immune'] = 0.02
    params_dict['Infectivity_Scale_Type'] = 'ANNUAL_BOXCAR_FUNCTION'
    params_dict['Infectivity_Boxcar_Forcing_Amplitude'] = 0.2
    params_dict['Infectivity_Boxcar_Forcing_Start_Time'] = 30
    params_dict['Infectivity_Boxcar_Forcing_End_Time'] = 120
    params_dict['logLevel_Node'] = "ERROR"
    params_dict['logLevel_default'] = "ERROR"
    params_dict['logLevel_JsonConfigurable'] = "ERROR"
    params_dict['logLevel_StandardEventCoordinator'] = "ERROR"
    params_dict['logLevel_Memory'] = "ERROR"
    params_dict['Enable_Abort_Zero_Infectivity'] = 1
    params_dict['Simulation_Timestep'] = 1.0
    params_dict['Spatial_Output_Days_To_Accumulate'] = 30
    # mAB_prfiles = [(150, 50), (90, 30), (120, 51)]
    params_dict['Maternal_Sigmoid_HalfMaxAge'] = 150
    params_dict['Maternal_Sigmoid_SteepFac'] = 50
    params_dict['Maternal_Sigmoid_SusInit'] = 0.05
    params_dict['Simulation_Duration'] = 9125
    return params_dict


def SIA_Coverage_setup(cb, campaign_coverage):
    demog = cb.demog_overlays['demographics.json']
    LN_sig = 0.1 + 2.4 * (1 - random.random() ** (2.0 / 3.0))
    LN_mu = math.log(campaign_coverage / (1 - campaign_coverage)) - math.sqrt(2) * LN_sig * erfinv(1 - 2 * 0.5)
    tmp = [math.exp(LN_mu + LN_sig*random.gauss(0, 1)) for i in range(len(demog['Nodes']))]
    campaign_coverages = [t/(1+t) for t in tmp]

    for event in cb.campaign.Events:
        if event.Event_Name == 'SIAs - SIAOnly Group':
            event.Event_Coordinator_Config.Coverage_By_Node = []
            for ii in range(len(demog['Nodes'])):
                event.Event_Coordinator_Config.Coverage_By_Node.append(
                    [demog['Nodes'][ii]['NodeID'], campaign_coverages[ii]])


def RI_Vacc_Setup(cb, threshold, fraction_meeting, MCV2, tags):
    # RI Vaccination is all set up in the demographics file using individual properties
    # Draw a random variance and construct the coverages from a logitnormal distribution
    #LN_sig = 0.1 + 1.4 * (1 - random.random() ** (2.0 / 3.0))  # slightly bias variance down relative to uniform
    LN_sig = 4*random.random()
    LN_mu = math.log(threshold / (1 - threshold)) - math.sqrt(2) * LN_sig * erfinv(1 - 2 * fraction_meeting)

    # I need to make sure that this is writing correctly - assigning dictionaries in this way in a loop may be tricky.
    demog = cb.demog_overlays['demographics.json']

    district_names = [node['dot_name'].split(':')[2] for node in demog['Nodes']]
    unique_district_names = set(district_names)
    district_coverages = {}
    for name in unique_district_names:
        tmp = math.exp(LN_mu + LN_sig * random.gauss(0, 1))
        district_coverages[name] = tmp / (1 + tmp)

    tags['LN_sig'] = LN_sig
    tags['LN_mu'] = LN_mu
    for node in demog['Nodes']:
        distcov = district_coverages[node['dot_name'].split(':')[2]]
        # Add a little ward-level noise around the district mean
        tmp = math.log(distcov / (1 - distcov))
        tmp2 = math.exp(tmp + 0.2 * random.gauss(0, 1))
        wardcov = tmp2 / (1 + tmp2)
        node['IndividualProperties'] = []
        node['IndividualProperties'].append(demog['Defaults']['IndividualProperties'][0].copy())
        node['IndividualProperties'][0]['Initial_Distribution'] = [MCV2*wardcov, (1-MCV2)*wardcov, 1-wardcov]

    cb.demog_overlays['demographics.json'] = demog


def MetaParameterHandler(cb, param, value, tags):
    #A place to handle all of the various metaparameters that may arise
    if param == 'META_Migration':
        cb.set_param('x_Local_Migration', value)
        cb.set_param('x_Air_Migration', value)
        tags['x_Local_Migration'] = value
        tags['x_Air_Migration'] = value
    if param == 'META_MCV1Days':
        for event in cb.campaign.Events:
            if event.Event_Name == 'MCV1':
                event.Event_Coordinator_Config.Intervention_Config.Actual_IndividualIntervention_Config.Delay_Period_Mean = value
                event.Event_Coordinator_Config.Intervention_Config.Actual_IndividualIntervention_Config.Delay_Period_Std_Dev = value/6.0
        tags['MCV1_Dose_Days'] = value
    if param == 'META_MaB_Profile':
        mAb_profiles = {'Long': [150, 50], 'Short': [90, 30], 'Mix': [120, 51]}
        cb.set_param('Maternal_Sigmoid_HalfMaxAge', mAb_profiles[value][0])
        cb.set_param('Maternal_Sigmoid_SteepFac', mAb_profiles[value][1])
        tags['Maternal_Antibody_Profile'] = value
        tags['Maternal_Sigmoid_HalfMaxAge'] = mAb_profiles[value][0]
        tags['Maternal_Sigmoid_SteepFac'] = mAb_profiles[value][1]
    if param == 'META_Timesteps':
        cb.set_param('Simulation_Timestep', int(value))
        cb.set_param('Spatial_Output_Days_To_Accumulate', int(30/value))
        for event in cb.campaign.Events:
                event.Event_Coordinator_Config.Timesteps_Between_Repetitions = max(int(1), int(
                    event.Event_Coordinator_Config.Timesteps_Between_Repetitions/value))
        tags['Simulation_Timestep'] = value
        tags['Spatial_Output_Days_To_Accumulate'] = 30/value
    return tags
