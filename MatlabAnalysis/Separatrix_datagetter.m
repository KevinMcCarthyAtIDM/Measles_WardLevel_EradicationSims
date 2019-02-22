basedir = '..\Experiments\';   %Where are the experiments?
experiments = dir(basedir);    %List all files and folders in the base experiment directory

all_experiment_metadata = loadJson([basedir '\experiment_metadata.json']);   %Load all experiment metadata (scenario parameters, ID, etc.)
for expind = 1:length(experiments)  %Loop over experiments
    exp = experiments(expind);    
    if ismember(exp.name, {'.', '..', 'experiment_metadata.json'})   %Skip the metadata file and the "." and ".." folders.
        continue
    end
    %This block deals with annoying matlab-UID difficulties.  Matlab loads
    %json as a struct, and struct field names cannot begin with numbers or 
    %contain '-', so matlab changes the name to match it's conventions. 
    %exp.name is the experiment UID, expfield will be the corresponding
    %field in the experiment metadata struct.
    
    expfield = strrep(exp.name,  '-', '_');         
    if startsWith(expfield, split(num2str(0:9), '  '))
        expfield = ['alpha_' expfield];
    end
    exp_metadata = all_experiment_metadata.(expfield);
    expdir = [basedir exp.name];
    if ~exist([expdir '\condensed_output.mat'], 'file')  %If we have already condensed output, move on.
        sim_metadata = loadJson([expdir '\metadata_output.json']);  %Load all simulation metadata for this experiment.
        sims = dir([expdir '\*.mat']);  %Get the list of simulation .mat files
        %Preallocation of outputs to save
        eradicated = zeros(1, length(sims));
        simlen = zeros(1, length(sims));
        threshold = zeros(1, length(sims));
        fraction = zeros(1, length(sims));
        LN_mu = zeros(1, length(sims));
        LN_sig = zeros(1, length(sims));
        
        for simind = 1:length(sims)  %for each simulation
            sim = sims(simind);
            if strcmpi(sim.name, 'condensed_output.mat') %skip the condensed output file if it exists
                continue
            end
            simouts = load([expdir '\' sim.name]);  %Load the simulation output
            
            %Similar json handling as above to retrieve simulation tags from the metadata json            
            simfield = strrep(strrep(strrep(sim.name, 'output_', ''), '.mat', ''), '-', '_');
            if startsWith(simfield, split(num2str(0:9), '  '))
                simfield = ['alpha_' simfield];
            end
            params = sim_metadata.(simfield);  %Get simulation parameters
            
            %Get outputs of interest - did measles eradicate?
            eradicated(simind) = simouts.allInfected(end) == 0 || length(simouts.allInfected)<3041;
            simlen(simind) = length(simouts.allInfected);  %How long did simulation run?
            threshold(simind) = params.META_Vaccination_Threshold;  %Separatrix parameter 1 - coverage "target"
            fraction(simind) = params.META_Fraction_Meeting;        %Separatrix parameter 2 - fraction of nodes that meet the target
            LN_mu(simind) = params.LN_mu;                           %mean of lognormal distribution of RI coverage by node
            LN_sig(simind) = params.LN_sig;                         %std. dev. of lognormal distribution of RI coverage by node.
        end

        save([expdir '\condensed_output.mat'], 'eradicated', 'threshold', 'fraction', 'exp_metadata', 'LN_mu', 'LN_sig');  %save the condensed output and move on to next experiment.

    end
   
end