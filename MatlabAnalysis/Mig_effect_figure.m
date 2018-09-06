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
ccMod = allouts.BirthRate == 0.98 & allouts.CampaignCov == 0.5 & ...
allouts.MCV2Frac == 0.75 & allouts.MigrationRate == 0.02 & ...
allouts.MCV1Age == 270 & allouts.RuralR0==12 & ...
cellfun(@length, allouts.eradicated)==512 & strcmpi(allouts.MaBProfile, 'Long');

ccLow = allouts.BirthRate == 0.98 & allouts.CampaignCov == 0.5 & ...
allouts.MCV2Frac == 0.75 & allouts.MigrationRate == 0.002 & ...
allouts.MCV1Age == 270 & allouts.RuralR0==12 & ...
cellfun(@length, allouts.eradicated)==512 & strcmpi(allouts.MaBProfile, 'Long');

ccDisconnect = allouts.BirthRate == 0.98 & allouts.CampaignCov == 0.5 & ...
allouts.MCV2Frac == 0.75 & allouts.MigrationRate == 0.0002 & ...
allouts.MCV1Age == 270 & allouts.RuralR0==12 & ...
cellfun(@length, allouts.eradicated)==512 & strcmpi(allouts.MaBProfile, 'Long');
colors = cbrewer('seq', 'Blues', 9);
hold on
plot3(C50(1, 2:end), C50(2, 2:end), ones(1, length(C50)-1), '-', 'LineWidth', 4, 'Color', colors(9, :));
plot3(allouts.C50{ccMod}(1, 2:end), allouts.C50{ccMod}(2, 2:end), ones(1, length(allouts.C50{ccMod})-1), '-', 'LineWidth', 4, 'Color', colors(7, :));
plot3(allouts.C50{ccLow}(1, 2:end), allouts.C50{ccLow}(2, 2:end), ones(1, length(allouts.C50{ccLow})-1), '-', 'LineWidth', 4, 'Color', colors(5, :));
plot3(allouts.C50{ccDisconnect}(1, 2:end), allouts.C50{ccDisconnect}(2, 2:end), ones(1, length(allouts.C50{ccDisconnect})-1), '-', 'LineWidth', 4, 'Color', colors(3, :));



mystr = ['Urban R_{0}: 24; Rural R_{0}: 12' newline ...
    'MCV2 coverage: 75% of MCV1 coverage' newline ...
    'SIA covers 50% of unvaccinated' newline ...
    'Pop growth rate: 2.5%/yr' newline ...
    'MCV1 at 9 months, Long-lived mAb'];
t = annotation('textbox', [.15, .19, .1, .1], 'String', mystr, 'FitBoxToText', 'on');
t.BackgroundColor = 'w';
t.FontSize = 14;
xlabel('Vaccination Coverage Target')
ylabel('Fraction of Districts Meeting Target');
set(gca, 'FontSize', 24);


xlim([0.5, 0.99]);
ylim([0.5, 0.99]);

text(.51, .74, 'High migration', 'Color', colors(9, :));
text(.51, .71, 'Moderate migration', 'Color', colors(7, :));
text(.51, .68, 'Low migration', 'Color', colors(5, :));
text(.51, .65, 'Disconnected', 'Color', colors(3, :));
title('Effect of Migration Rate: 50% Eradication probability contours');
myprint('-dpng', ['Images\Mig_effect_50contours.png']);
saveas(h1, ['MatFigs\Mig_effect_50contours.fig']);

plot3(C75(1, 2:end), C75(2, 2:end), ones(1, length(C75)-1), '--', 'LineWidth', 4, 'Color', colors(9, :));
plot3(allouts.C75{ccMod}(1, 2:end), allouts.C75{ccMod}(2, 2:end), ones(1, length(allouts.C75{ccMod})-1), '--', 'LineWidth', 4, 'Color', colors(7, :));
plot3(allouts.C75{ccLow}(1, 2:end), allouts.C75{ccLow}(2, 2:end), ones(1, length(allouts.C75{ccLow})-1), '--', 'LineWidth', 4, 'Color', colors(5, :));
plot3(allouts.C75{ccDisconnect}(1, 2:end), allouts.C75{ccDisconnect}(2, 2:end), ones(1, length(allouts.C75{ccDisconnect})-1), '--', 'LineWidth', 4, 'Color', colors(3, :));
title('Effect of Migration Rate: 50% and 75% Eradication probability contours');

myprint('-dpng', ['Images\Mig_effect_bothcontours.png']);
saveas(h1, ['MatFigs\Mig_effect_bothcontours.fig']);

clf;

hold on
plot3(C75(1, 2:end), C75(2, 2:end), ones(1, length(C75)-1), '-', 'LineWidth', 4, 'Color', colors(9, :));
plot3(allouts.C75{ccMod}(1, 2:end), allouts.C75{ccMod}(2, 2:end), ones(1, length(allouts.C75{ccMod})-1), '-', 'LineWidth', 4, 'Color', colors(7, :));
plot3(allouts.C75{ccLow}(1, 2:end), allouts.C75{ccLow}(2, 2:end), ones(1, length(allouts.C75{ccLow})-1), '-', 'LineWidth', 4, 'Color', colors(5, :));
plot3(allouts.C75{ccDisconnect}(1, 2:end), allouts.C75{ccDisconnect}(2, 2:end), ones(1, length(allouts.C75{ccDisconnect})-1), '-', 'LineWidth', 4, 'Color', colors(3, :));
view(2)

text(.51, .74, 'High migration', 'Color', colors(9, :));
text(.51, .71, 'Moderate migration', 'Color', colors(7, :));
text(.51, .68, 'Low migration', 'Color', colors(5, :));
text(.51, .65, 'Disconnected', 'Color', colors(3, :));
t = annotation('textbox', [.15, .19, .1, .1], 'String', mystr, 'FitBoxToText', 'on');
t.BackgroundColor = 'w';
t.FontSize = 14;
xlabel('Vaccination Coverage Target')
ylabel('Fraction of Districts Meeting Target');
set(gca, 'FontSize', 24);


xlim([0.5, 0.99]);
ylim([0.5, 0.99]);
title('Effect of Migration Rate: 75% Eradication Probability Contours')
myprint('-dpng', ['Images\Mig_effect_75contours.png']);
saveas(h1, ['MatFigs\Mig_effect_75contours.fig']);
        