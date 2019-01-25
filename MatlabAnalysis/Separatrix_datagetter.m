basedir = '..\Experiments\';
experiments = dir(basedir);

all_experiment_metadata = loadJson([basedir '\experiment_metadata.json']);
for expind = 1:length(experiments)
    exp = experiments(expind);
    if ismember(exp.name, {'.', '..', 'experiment_metadata.json'})
        continue
    end
    expfield = strrep(exp.name,  '-', '_');
    if startsWith(expfield, split(num2str(0:9), '  '))
        expfield = ['alpha_' expfield];
    end
    exp_metadata = all_experiment_metadata.(expfield);
    expdir = [basedir exp.name];
    if ~exist([expdir '\condensed_output.mat'], 'file')
        sim_metadata = loadJson([expdir '\metadata_output.json']);
        sims = dir([expdir '\*.mat']);
        eradicated = zeros(1, length(sims));
        simlen = zeros(1, length(sims));
        threshold = zeros(1, length(sims));
        fraction = zeros(1, length(sims));
        LN_mu = zeros(1, length(sims));
        LN_sig = zeros(1, length(sims));
        for simind = 1:length(sims)
            sim = sims(simind);
            if strcmpi(sim.name, 'condensed_output.mat')
                continue
            end
            simouts = load([expdir '\' sim.name]);
            simfield = strrep(strrep(strrep(sim.name, 'output_', ''), '.mat', ''), '-', '_');
            if startsWith(simfield, split(num2str(0:9), '  '))
                simfield = ['alpha_' simfield];
            end
            params = sim_metadata.(simfield);
            eradicated(simind) = simouts.allInfected(end) == 0 || length(simouts.allInfected)<3041;
            simlen(simind) = length(simouts.allInfected);
            threshold(simind) = params.META_Vaccination_Threshold;
            fraction(simind) = params.META_Fraction_Meeting;
            LN_mu(simind) = params.LN_mu;
            LN_sig(simind) = params.LN_sig;
        end

        save([expdir '\condensed_output.mat'], 'eradicated', 'threshold', 'fraction', 'exp_metadata', 'LN_mu', 'LN_sig');

    end
   
end