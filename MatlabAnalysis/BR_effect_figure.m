load allouts.mat;
ccHigh = allouts.BirthRate == 0.98 & allouts.CampaignCov == 0.5 & ...
allouts.MCV2Frac == 0.75 & allouts.MigrationRate == 0.2 & ...
allouts.MCV1Age == 270 & allouts.RuralR0==12 & ...
cellfun(@length, allouts.eradicated)==512 & strcmpi(allouts.MaBProfile, 'Long');
h1 = myfigure_square;
threshold = [allouts.threshold{ccHigh}];
fraction = [allouts.fraction{ccHigh}];
cc = [allouts.eradicated{ccHigh}];
[~, alpha, x, y] = kde2d([threshold(cc)' fraction(cc)'], 2^8, [0.4 0.4], [0.99, 0.99]);
[~, beta] = kde2d([threshold(~cc)' fraction(~cc)'], 2^8, [0.4 0.4], [0.99, 0.99]);
alpha = alpha*sum(cc);
beta = beta*sum(~cc);
[C50, ~] = contour(x, y, alpha./(alpha+beta), [.5, .5]);
[C75, ~] = contour(x, y, alpha./(alpha+beta), [.75, .75]);
clf;
ccLow = allouts.BirthRate == 0.85 & allouts.CampaignCov == 0.50 & ...
allouts.MCV2Frac == 0.75 & allouts.MigrationRate == 0.2 & ...
allouts.MCV1Age == 270 & allouts.RuralR0==12 & ...
cellfun(@length, allouts.eradicated)==512 & strcmpi(allouts.MaBProfile, 'Long');

colors = cbrewer('seq', 'Blues', 9);
hold on
plot3(C50(1, 2:end), C50(2, 2:end), ones(1, length(C50)-1), '-', 'LineWidth', 4, 'Color', colors(9, :));
plot3(allouts.C50{ccLow}(1, 2:end), allouts.C50{ccLow}(2, 2:end), ones(1, length(allouts.C50{ccLow})-1), '-', 'LineWidth', 4, 'Color', colors(6, :));



mystr = ['Urban R_{0}: 24; Rural R_{0}: 12' newline ...
    'MCV2 coverage: 75% of MCV1 coverage' newline ...
    'SIA covers 50% of unvaccinated' newline ...
    'Migration Rate: High' newline ...
    'MCV1 at 9 months, Long-lived mAb'];
t = annotation('textbox', [.15, .19, .1, .1], 'String', mystr, 'FitBoxToText', 'on');
t.BackgroundColor = 'w';
t.FontSize = 14;
xlabel('Vaccination Coverage Target')
ylabel('Fraction of Districts Meeting Target');
set(gca, 'FontSize', 24);


xlim([0.5, 0.99]);
ylim([0.5, 0.99]);

text(.7, .64, '2.5% pop growth/yr', 'Color', colors(9, :));
text(.7, .61, '0.5% pop growth/yr', 'Color', colors(6, :));
title('Effect of Birth rate: 50% Eradication probability contours');
myprint('-dpng', ['Images\BirthRate_effect_50contours.png']);
saveas(h1, ['MatFigs\BirthRate_effect_50contours.fig']);

plot3(C75(1, 2:end), C75(2, 2:end), ones(1, length(C75)-1), '--', 'LineWidth', 4, 'Color', colors(9, :));
hold on
plot3(allouts.C75{ccLow}(1, 2:end), allouts.C75{ccLow}(2, 2:end), ones(1, length(allouts.C75{ccLow})-1), '--', 'LineWidth', 4, 'Color', colors(6, :));
title('Effect of Birth Rate: 50% and 75% Eradication probability contours');

myprint('-dpng', ['Images\BirthRate_effect_bothcontours.png']);
saveas(h1, ['MatFigs\BirthRate_effect_bothcontours.fig']);

clf;

plot3(C75(1, 2:end), C75(2, 2:end), ones(1, length(C75)-1), '-', 'LineWidth', 4, 'Color', colors(9, :));
hold on
plot3(allouts.C75{ccLow}(1, 2:end), allouts.C75{ccLow}(2, 2:end), ones(1, length(allouts.C75{ccLow})-1), '-', 'LineWidth', 4, 'Color', colors(6, :));
view(2)

text(.7, .64, '2.5% pop growth/yr', 'Color', colors(9, :));
text(.7, .61, '0.5% pop growth/yr', 'Color', colors(6, :));
t = annotation('textbox', [.15, .19, .1, .1], 'String', mystr, 'FitBoxToText', 'on');
t.BackgroundColor = 'w';
t.FontSize = 14;
xlabel('Vaccination Coverage Target')
ylabel('Fraction of Districts Meeting Target');
set(gca, 'FontSize', 24);


xlim([0.5, 0.99]);
ylim([0.5, 0.99]);
title('Effect of Birth Rate: 75% Eradication Probability Contours')
myprint('-dpng', ['Images\BirthRate_effect_75contours.png']);
saveas(h1, ['MatFigs\BirthRate_effect_75contours.fig']);
        