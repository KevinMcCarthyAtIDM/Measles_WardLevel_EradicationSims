basedir = '..\Experiments\';
experiments = dir(basedir);
mkdir('Images');
mkdir('MatFigs');
all_experiment_metadata = loadJson([basedir '\experiment_metadata.json']);
h1 = myfigure_square;

%initialize outputs to be saved
allouts = table();
init_vec = zeros(length(experiments), 1);
init_cell = cell(length(experiments), 1);
allouts.BirthRate = init_vec;
allouts.CampaignCov = init_vec;
allouts.MCV2Frac = init_vec;
allouts.MCV1Age = init_vec;
allouts.MaBProfile = init_cell;
allouts.MigrationRate = init_vec;
allouts.RuralR0 = init_vec;
allouts.threshold = init_cell;
allouts.fraction = init_cell;
allouts.eradicated = init_cell;
allouts.alpha = init_cell;
allouts.beta = init_cell;
allouts.x = init_cell;
allouts.y = init_cell;
allouts.C50 = init_cell;
allouts.C75 = init_cell;
allouts.expID = init_cell;

for expind = 1:length(experiments)
    exper = experiments(expind);
    if ismember(exper.name, {'.', '..', 'experiment_metadata.json'})
        continue
    end
    %if ~ismember(exper.name, {'539b41e3-cfad-e811-a2c0-c4346bcb7275'})
    %    continue
    %end
    expfield = strrep(exper.name,  '-', '_');
    if startsWith(expfield, split(num2str(0:9), '  '))
        expfield = ['alpha_' expfield];
    end
    exp_metadata = all_experiment_metadata.(expfield);
    expdir = [basedir exper.name];
    assert(exist([expdir '\condensed_output.mat'], 'file')~=0, ['No condensed output for Experiment ' exper.name]);
    outs = load([expdir '\condensed_output.mat']);
    if ~isfield(exp_metadata, 'x_Birth')
        exp_metadata.x_Birth = '0.98';
        exp_metadata.META_MCV2Frac = '0.75';
        exp_metadata.META_MaB_Profile = 'Long';
        exp_metadata.Base_Population_Scale_Factor = '0.075';
    end
    if isfield(exp_metadata, 'META_Campaign_Coverage')
        exp_metadata.META_campaign_coverage = exp_metadata.META_Campaign_Coverage;
    end
    if isfield(exp_metadata, 'MCV1_Dose_Days')
        exp_metadata.META_MCV1Days = exp_metadata.MCV1_Dose_Days;
    end
        
    
    figure(h1);
    clf;
    cc = outs.outcomes==1;
    if ismember(sum(cc), [0, 512])
        continue
    end
    [~, alpha, x, y] = kde2d([outs.threshold(cc)' outs.fraction(cc)'], 2^8, [0.4 0.4], [0.99, 0.99]);
    [~, beta] = kde2d([outs.threshold(~cc)' outs.fraction(~cc)'], 2^8, [0.4 0.4], [0.99, 0.99]);
    alpha = alpha*sum(cc);
    beta = beta*sum(~cc);
    [C50, ~] = contour(x, y, alpha./(alpha+beta), [.5, .5]);
    [C75, ~] = contour(x, y, alpha./(alpha+beta), [.75, .75]);
    surf(x, y, alpha./(alpha+beta), 'EdgeColor', 'none');
    hold on
    caxis([0, 1]);
    xlim([0.5, 0.99]);
    ylim([0.5, 0.99]);
    colormap(cbrewer('div', 'RdYlBu', 256))
    view(2)
    cb = colorbar;
    set(get(cb, 'YLabel'), 'String', 'Elimination Probability');
    
    migdict = struct('x0p2', 'High', 'x0p02', 'Moderate', 'x0p002', 'Low', 'x0p0002', 'Disconnected');                  
    birthdict = struct('x0p98', '2.5%/yr', 'x0p85', '0.5%/yr');
    mystr = ['Urban R_{0}: 24; Rural R_{0}: ' num2str(12*str2double(exp_metadata.Rural_Infectivity_Multiplier)) newline ...
             'MCV2 coverage: ' num2str(100*str2double(exp_metadata.META_MCV2Frac)) '% of MCV1 coverage' newline ...
             'SIAs reach ' num2str(100*str2double(exp_metadata.META_campaign_coverage)) '% of unvacc' newline ...
             'Migration Rate: ' migdict.(['x' strrep(exp_metadata.META_Migration, '.', 'p')]) newline ...
             'Pop growth rate: ' birthdict.(['x' strrep(exp_metadata.x_Birth, '.', 'p')]) newline ...
             'MCV1 at ' num2str(floor(str2double(exp_metadata.META_MCV1Days)/30)) ' months, ' exp_metadata.META_MaB_Profile '-lived mAb'];
    t = annotation('textbox', [.15, .17, .1, .1], 'String', mystr, 'FitBoxToText', 'on');
    t.BackgroundColor = 'w';
    t.FontSize = 14;
    xlabel('Vaccination Coverage Target')
    ylabel('Fraction of Districts Meeting Target');
    set(gca, 'FontSize', 24);
    myprint('-dpng', ['Images\' exper.name '_heatmap.png']);
    saveas(h1, ['MatFigs\' exper.name '_heatmap.fig']);
    
    hold on
    plot3(C50(1, 2:end), C50(2, 2:end), ones(1, length(C50)-1), 'k-', 'LineWidth', 4);
    myprint('-dpng', ['Images\' exper.name '_heatmap_wcontour.png']);
    saveas(h1, ['MatFigs\' exper.name '_heatmap_wcontour.fig']);
    
    plot3(outs.threshold(cc)', outs.fraction(cc)', ones(sum(cc)), 'ko', 'MarkerSize', 12);
    plot3(outs.threshold(~cc)', outs.fraction(~cc)', ones(sum(~cc)), 'kx', 'MarkerSize', 12);
    myprint('-dpng', ['Images\' exper.name '_heatmap_wpts_contour.png']);
    saveas(h1, ['MatFigs\' exper.name '_heatmap_wpts_contour.fig']);
    clf;
  
%     allouts.BirthRate(expind) = str2double(exp_metadata.x_Birth);
%     allouts.CampaignCov(expind) = str2double(exp_metadata.META_campaign_coverage);
%     allouts.MCV2Frac(expind) = str2double(exp_metadata.META_MCV2Frac);
%     allouts.MCV1Age(expind) = str2double(exp_metadata.META_MCV1Days);
%     allouts.MaBProfile{expind} = exp_metadata.META_MaB_Profile;
%     allouts.MigrationRate(expind) = str2double(exp_metadata.META_Migration);
%     allouts.RuralR0(expind) = str2double(exp_metadata.Rural_Infectivity_Multiplier)*12;
%     allouts.threshold{expind} = outs.threshold;
%     allouts.fraction{expind} = outs.fraction;
%     allouts.eradicated{expind} = cc;
%     allouts.alpha{expind} = alpha;
%     allouts.beta{expind} = beta;
%     allouts.x{expind} = x;
%     allouts.y{expind} = y;
%     allouts.C50{expind} = C50;
%     allouts.C75{expind} = C75;
%     allouts.expID{expind} = exper.name;
%     save('allouts.mat', 'allouts');
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