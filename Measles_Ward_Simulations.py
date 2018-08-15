##
"""
Measles Ward Simulations: Sample demographic
"""
#
import json

from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder

cb = DTKConfigBuilder.from_files(config_name='pathtoconfig\config.json', campaign_name='pathtocampaign\campaign.json')
cb.set_experiment_executable(path='pathtoexecutable\Eradication.exe')
cb.add_demog_overlay(name='demographics.json', content=json.load(open('pathtofile\demograpmics.json')))
cb.experiment_files.add_file(path='migrationFile')

def IndividualPropertiesByNode(cb, threshold, percent_meeting):
    tags ={}
    # Construct vector
    demog = cb.demog_overlays['demographics.json']
    demog['Nodes'][]
    cb.demog_overlays['demographics.json'] = demog
    return tags


if __name__ == "__main__":

    # Basic parameters.  Should these be inputs?
    base_demog_file = '.\\Nigeria_LGA_demographics.json'
    out_demog_file = '.\\Nigeria_Ward_minpop5000_demographics.json'
    node_info_file = '.\\population_by_ward.csv'

    with open(base_demog_file, 'r') as f:
        base_demog = json.load(f)
    out_demog = dict()
    out_demog['Metadata'] = base_demog['Metadata']
    out_demog['Defaults'] = base_demog['Defaults']
    out_demog['Defaults']['NodeAttributes']['Airport'] = 1
    node_info = pd.read_csv(node_info_file)
    out_demog['Nodes'] = fill_nodes(out_demog, node_info, res=out_demog['Metadata']['Resolution']/3600)
    out_demog['Metadata']['NodeCount'] = len(out_demog['Nodes'])

    with open(out_demog_file, 'w') as fp:
        json.dump(out_demog, fp, indent=4)
