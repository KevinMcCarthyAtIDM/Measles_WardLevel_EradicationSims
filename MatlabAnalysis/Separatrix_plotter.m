basedir = '..\Experiments\'; %Where are the experiments?
experiments = dir(basedir);
mkdir('Images');             %For output png images
mkdir('MatFigs');            %For output matlab figures
all_experiment_metadata = loadJson([basedir '\experiment_metadata.json']);  %Load metadata
h1 = myfigure_square;        %make my figure object

%initialize outputs to be saved
allouts = table();          %allouts will hold all of the data to save
init_vec = zeros(length(experiments), 1);   %vector of zeros for initializing
init_cell = cell(length(experiments), 1);   %cell of zeros for initializing
allouts.BirthRate = init_vec;               %initialize the columns of allouts to vectors (numeric) or cells (non-numeric/vector) as appropriate.
allouts.CampaignCov = init_vec;
allouts.Dropout = init_vec;
allouts.MCV1Age = init_vec;
allouts.MCV2Age = init_vec;
allouts.MaBProfile = init_cell;
allouts.MigrationRate = init_vec;
allouts.RuralR0 = init_vec;
allouts.UrbanR0 = init_vec;
allouts.threshold = init_cell;
allouts.fraction = init_cell;
allouts.eradicated = init_cell;
allouts.alpha = init_cell;
allouts.beta = init_cell;
allouts.x = init_cell;
allouts.y = init_cell;
allouts.C50 = init_cell;
allouts.C75 = init_cell;
allouts.C80 = init_cell;
allouts.expID = init_cell;

for expind = 1:length(experiments) %loop over experiment folders
    exper = experiments(expind);   %skip things that aren't experiment folders
    if ismember(exper.name, {'.', '..', 'experiment_metadata.json'})
        continue
    end

    %Do the annoying string handling bit again
    expfield = strrep(exper.name,  '-', '_');
    if startsWith(expfield, split(num2str(0:9), '  '))
        expfield = ['alpha_' expfield];
    end
    exp_metadata = all_experiment_metadata.(expfield);  %Find the metadata for this experiment
    expdir = [basedir exper.name];                      %this experiment's output directory.
    %Make sure that condensed output exists and load it
    assert(exist([expdir '\condensed_output.mat'], 'file')~=0, ['No condensed output for Experiment ' exper.name]);
    outs = load([expdir '\condensed_output.mat']);
    
    figure(h1);
    clf;  %Clear the figure of previous plot data.
    cc = outs.eradicated==1;    %Find the simulations that eradicated
    if ismember(sum(cc), [0, 512])   %If all simulations or no simulations eradicated, skip this experiment
        continue
    end
    
    %Construct a 2D kernel density estimator for the density of successful
    %eliminations (alpha) and failures (beta), on a 256x256 grid from 0.4
    %to 0.99, and save the grid in x and y.
    [~, alpha, x, y] = kde2d([outs.threshold(cc)' outs.fraction(cc)'], 2^8, [0.4 0.4], [0.99, 0.99]);
    [~, beta] = kde2d([outs.threshold(~cc)' outs.fraction(~cc)'], 2^8, [0.4 0.4], [0.99, 0.99]);
    
    %Density will be between 0 and 1, normalize alpha and beta to the total
    %number of successes and failures
    alpha = alpha*sum(cc);
    beta = beta*sum(~cc);
    
    %Construct contour of success/failure probabilities
    %(alpha/(alpha+beta)) at 50%, 75%, and 80% probability
    [C50, ~] = contour(x, y, alpha./(alpha+beta), [.5, .5]);
    [C75, ~] = contour(x, y, alpha./(alpha+beta), [.75, .75]);
    [C80, ~] = contour(x, y, alpha./(alpha+beta), [.80, .80]);
    
    %Plotting a surface plot of the elimination probability.
    surf(x, y, alpha./(alpha+beta), 'EdgeColor', 'none');
    hold on
    caxis([0, 1]);
    xlim([0.5, 0.99]);
    ylim([0.5, 0.99]);
    colormap(cbrewer('div', 'RdYlBu', 256))
    view(2)
    cb = colorbar;
    set(get(cb, 'YLabel'), 'String', 'Elimination Probability');
    
    %The next 25 lines or so handle an annotation text box that puts all of
    %the relevant scenario parameters - migration rate, SIA info, R0, etc. on the figure
    %mig_dict maps the migration rate string (x0p2 = 0.2, x0p002 = 0.002,
    %etc.) to "high", "moderate", "low", etc.
    migdict = struct('x0p2', 'High', 'x0p02', 'Moderate', 'x0p002', 'Low', 'x0p0002', 'Disconnected');                  
    
    %Traslate special values of campaign coverage to annotation strings, 
    if str2double(exp_metadata.META_campaign_coverage) == -1
        campstring = 'No SIAs';
    elseif str2double(exp_metadata.META_campaign_coverage) == 0
        campstring = 'SIAs reach only routine-accessible children';
    else
        campstring = ['SIAs reach ' num2str(100*str2double(exp_metadata.META_campaign_coverage)) '% of RI-missed children'];
    end
    %Translate the maternal antibody profile string to more useful
    %information
    if strcmpi(exp_metadata.META_MaB_Profile, 'Mix')
        mAbstr = 'mixed short and long mAb';
    else
        mAbstr = [exp_metadata.META_MaB_Profile '-lived mAb'];
    end
    %mapping of parameter x_Birth to corresponding population growth rate
    %per yet
    birthdict = struct('x0p98', '2.5%/yr', 'x0p85', '0.5%/yr', 'x0p905', '1.5%/yr', 'x0p81', '0%/yr');
    
    %Finally, construct the annotation string of all scenario parameters
    mystr = ['Urban R_{0}: ' num2str(12*str2double(exp_metadata.Urban_Infectivity_Multiplier)) ...
             '; Rural R_{0}: ' num2str(12*str2double(exp_metadata.Rural_Infectivity_Multiplier)) newline ...
             'MCV1-MCV2 dropout rate: ' num2str(100*str2double(exp_metadata.META_Dropout)) '%' newline ...
             campstring newline ...
             'Migration Rate: ' migdict.(['x' strrep(exp_metadata.META_Migration, '.', 'p')]) newline ...
             'Pop growth rate: ' birthdict.(['x' strrep(exp_metadata.x_Birth, '.', 'p')]) newline ...
             'MCV1 at ' num2str(floor(str2double(exp_metadata.META_MCV1Days)/30)) ' months' newline ...
             'MCV2 at ' num2str(floor(str2double(exp_metadata.META_MCV2Days)/30)) ' months, ' mAbstr];
    %Annotate, label, title, and save the figure to a png and to a matlab
    %figure file.
    t = annotation('textbox', [.15, .17, .1, .1], 'String', mystr, 'FitBoxToText', 'on');
    t.BackgroundColor = 'w';
    t.FontSize = 14;
    xlabel('Vaccination Coverage Target')
    ylabel('Fraction of Districts Meeting Target');
    set(gca, 'FontSize', 24);
    myprint('-dpng', ['Images\' exper.name '_heatmap.png']);
    saveas(h1, ['MatFigs\' exper.name '_heatmap.fig']);
    
    hold on  %Enable further plotting without overwriting figure
    
    %Now we add the 80% contour to the surface plot.  The vector splitting
    %of the contour (C80) into brackets handles the case of multiple
    %contours that are not continuous
    brackets = SplitVec(C80(1, :)==0.8, 'equal', 'bracket');
    for ii = 2:2:size(brackets, 1)
        plot3(C80(1, brackets(ii, 1):brackets(ii, 2)), C80(2, brackets(ii, 1):brackets(ii, 2)), ones(1, brackets(ii, 2)-brackets(ii,1)+1), 'k-', 'LineWidth', 4);
    end
    myprint('-dpng', ['Images\' exper.name '_heatmap_wcontour.png']);
    saveas(h1, ['MatFigs\' exper.name '_heatmap_wcontour.fig']);
    
    %And finally, add the points where eliminations or failures were
    %observed and save again
    plot3(outs.threshold(cc)', outs.fraction(cc)', ones(sum(cc)), 'ko', 'MarkerSize', 12);
    plot3(outs.threshold(~cc)', outs.fraction(~cc)', ones(sum(~cc)), 'kx', 'MarkerSize', 12);
    myprint('-dpng', ['Images\' exper.name '_heatmap_wpts_contour.png']);
    saveas(h1, ['MatFigs\' exper.name '_heatmap_wpts_contour.fig']);
    clf;
  
    %Save the experiment metadata, the vectors of simulation parameters,
    %and the probability surfaces, contours, expID, etc. into allouts.
    allouts.BirthRate(expind) = str2double(exp_metadata.x_Birth);
    allouts.CampaignCov(expind) = str2double(exp_metadata.META_campaign_coverage);
    allouts.Dropout(expind) = str2double(exp_metadata.META_Dropout);
    allouts.MCV1Age(expind) = str2double(exp_metadata.META_MCV1Days);
    allouts.MCV2Age(expind) = str2double(exp_metadata.META_MCV2Days);
    allouts.MaBProfile{expind} = exp_metadata.META_MaB_Profile;
    allouts.MigrationRate(expind) = str2double(exp_metadata.META_Migration);
    allouts.RuralR0(expind) = str2double(exp_metadata.Rural_Infectivity_Multiplier)*12;
    allouts.UrbanR0(expind) = str2double(exp_metadata.Urban_Infectivity_Multiplier)*12;
    allouts.threshold{expind} = outs.threshold;
    allouts.fraction{expind} = outs.fraction;
    allouts.eradicated{expind} = cc;
    allouts.alpha{expind} = alpha;
    allouts.beta{expind} = beta;
    allouts.x{expind} = x;
    allouts.y{expind} = y;
    allouts.C50{expind} = C50;
    allouts.C75{expind} = C75;
    allouts.C80{expind} = C80;
    allouts.expID{expind} = exper.name;
    save('allouts.mat', 'allouts');
    
    %Below code was an attempt to plot in a different x/y space - instead
    %of "coverage threshold" and "fraction of nodes meetind threshold",
    %plot in mean and standard deviation of coverage distribution.  Results
    %were not useful figures, really.
%     if isfield(outs, 'LN_mu')
%         %Invert the quantile distribution for logitnormal to let each sim
%         %inform a full curve in the x-y space
%         quantiles = 0.5:0.01:0.99;
%         cc2 = repmat(cc, [length(quantiles), 1]);
%         fraction = repmat(quantiles',[1, length(outs.LN_sig)]); 
%         sigs = repmat(outs.LN_sig, [length(quantiles), 1]);
%         mus = repmat(outs.LN_mu, [length(quantiles), 1]);
%         tmp = exp(mus + sqrt(2).*sigs.*erfinv(1-2.*fraction));
%         threshold = tmp./(1+tmp);
% 
% %         coverages = 0:0.01:0.99;
% %         cc = repmat(cc, [length(coverages), 1]);
% %         threshold = repmat(coverages',[1, length(sims)]); 
% %         sigs = repmat(outs.LN_sig, [length(coverages), 1]);
% %         mus = repmat(outs.LN_mu, [length(coverages), 1]);
% %         tmp = exp(mus + sqrt(2).*sigs.*erfinv(1-2.*fraction));
% %         fraction = 1/2 - erf( (log( threshold./(1-threshold) ) - mus)./(sqrt(2)*sigs)) /2;
% 
%         [~, alpha, x, y] = kde2d([threshold(cc2) fraction(cc2)], 2^8, [0.5 0.5], [0.99, 0.99]);
%         [~, beta] = kde2d([threshold(~cc2) fraction(~cc2)], 2^8, [0.5 0.5], [0.99, 0.99]);
%         alpha = alpha*sum(cc2(:));
%         beta = beta*sum(~cc2(:));     
%         
%         
%         [C50, ~] = contour(x, y, alpha./(alpha+beta), [.5, .5]);
%         [C75, ~] = contour(x, y, alpha./(alpha+beta), [.75, .75]);
%         surf(x, y, alpha./(alpha+beta), 'EdgeColor', 'none');
%         hold on
%         caxis([0, 1]);
%         xlim([0.5, 0.95]);
%         ylim([0.5, 0.95]);
%         colormap(cbrewer('div', 'RdYlBu', 256))
%         view(2)
%         cb = colorbar;
%         set(get(cb, 'YLabel'), 'String', 'Elim. Prob.');
%         fn = fieldnames(exp_metadata);
%         mystr = [];
%         for ii = 1:length(fn)
%             mystr = [mystr, strrep(strrep(fn{ii}, 'META_', ''), '_', '') ': ' exp_metadata.(fn{ii}) newline];
%         end
%         annotation('textbox', [.15, .17, .1, .1], 'String', mystr, 'FitBoxToText', 'on')
%         xlabel('Vaccination Coverage Target')
%         ylabel('Prop. of Districts Meeting Target');
%         myprint('-dpng', ['Images\' exper.name '_heatmap_extended.png']);
%         saveas(h1, ['MatFigs\' exper.name '_heatmap_extended.fig']);
%         
%         hold on
%         plot3(outs.threshold(cc)', outs.fraction(cc)', ones(sum(cc)), 'ko', 'MarkerSize', 12);
%         plot3(outs.threshold(~cc)', outs.fraction(~cc)', ones(sum(~cc)), 'kx', 'MarkerSize', 12);
%         plot3(C75(1, 2:end), C75(2, 2:end), ones(1, length(C75)-1), 'k-', 'LineWidth', 4);
%         myprint('-dpng', ['Images\' exper.name '_heatmap_extended_wpts_contour.png']);
%         saveas(h1, ['MatFigs\' exper.name '_heatmap__extendedwpts_contour.fig']);
%         
%     end
    
end