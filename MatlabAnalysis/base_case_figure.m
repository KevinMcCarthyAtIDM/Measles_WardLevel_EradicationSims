load allouts.mat;
cc1 = allouts.BirthRate == 0.98 & allouts.CampaignCov == 0.5 & ...
allouts.MCV2Frac == 0.75 & allouts.MigrationRate == 0.2 & ...
allouts.MCV1Age == 270 & allouts.RuralR0==12 & ...
cellfun(@length, allouts.eradicated)==512 & strcmpi(allouts.MaBProfile, 'Long');
h1 = myfigure_square;
threshold = [allouts.threshold{cc1}];
fraction = [allouts.fraction{cc1}];
cc = [allouts.eradicated{cc1}];
[~, alpha, x, y] = kde2d([threshold(cc)' fraction(cc)'], 2^8, [0.4 0.4], [0.99, 0.99]);
[~, beta] = kde2d([threshold(~cc)' fraction(~cc)'], 2^8, [0.4 0.4], [0.99, 0.99]);
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
    
    mystr = ['Urban R_{0}: 24; Rural R_{0}: 12' newline ...
             'MCV2 coverage: 75% of MCV1 coverage' newline ...
             'SIAs reach 50% of unvacc' newline ...
             'Migration Rate: High' newline ...
             'Pop growth rate: 2.5%/yr' newline ...
             'MCV1 at 9 months, Long-lived mAb'];
    t = annotation('textbox', [.15, .19, .1, .1], 'String', mystr, 'FitBoxToText', 'on');
    t.BackgroundColor = 'w';
    t.FontSize = 14;
    xlabel('Vaccination Coverage Target')
    ylabel('Fraction of Districts Meeting Target');
    set(gca, 'FontSize', 24);
    myprint('-dpng', ['Images\basecase_heatmap.png']);
    saveas(h1, ['MatFigs\basecase_heatmap.fig']);
    
    hold on
    plot3(C50(1, 2:end), C50(2, 2:end), ones(1, length(C50)-1), 'k-', 'LineWidth', 4);
    myprint('-dpng', ['Images\basecase_heatmap_w1contour.png']);
    saveas(h1, ['MatFigs\basecase_heatmap_w1contour.fig']);
    
        plot3(C75(1, 2:end), C75(2, 2:end), ones(1, length(C75)-1), 'k-', 'LineWidth', 4);
    myprint('-dpng', ['Images\basecase_heatmap_w2contour.png']);
    saveas(h1, ['MatFigs\basecase_heatmap_w2contour.fig']);
        
    plot3(threshold(cc)', fraction(cc)', ones(sum(cc)), 'ko', 'MarkerSize', 12);
    plot3(threshold(~cc)', fraction(~cc)', ones(sum(~cc)), 'kx', 'MarkerSize', 12);
    myprint('-dpng', ['Images\basecase_heatmap_wpts_contour.png']);
    saveas(h1, ['MatFigs\basecase_heatmap_wpts_contour.fig']);