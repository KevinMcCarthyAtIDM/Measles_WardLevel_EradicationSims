load allouts.mat;
cc50 = allouts.BirthRate == 0.98 & allouts.CampaignCov == 0.5 & ...
allouts.MCV2Frac == 0.75 & allouts.MigrationRate == 0.2 & ...
allouts.MCV1Age == 270 & allouts.RuralR0==12 & ...
cellfun(@length, allouts.eradicated)==512 & strcmpi(allouts.MaBProfile, 'Long');
h1 = myfigure_square;
threshold = [allouts.threshold{cc50}];
fraction = [allouts.fraction{cc50}];
cc = [allouts.eradicated{cc50}];
[~, alpha, x, y] = kde2d([threshold(cc)' fraction(cc)'], 2^8, [0.4 0.4], [0.99, 0.99]);
[~, beta] = kde2d([threshold(~cc)' fraction(~cc)'], 2^8, [0.4 0.4], [0.99, 0.99]);
alpha = alpha*sum(cc);
beta = beta*sum(~cc);
[C50, ~] = contour(x, y, alpha./(alpha+beta), [.5, .5]);
[C75, ~] = contour(x, y, alpha./(alpha+beta), [.75, .75]);
clf;
cc0 = allouts.BirthRate == 0.98 & allouts.CampaignCov == 0.001 & ...
allouts.MCV2Frac == 0.75 & allouts.MigrationRate == 0.2 & ...
allouts.MCV1Age == 270 & allouts.RuralR0==12 & ...
cellfun(@length, allouts.eradicated)==512 & strcmpi(allouts.MaBProfile, 'Long');
%Looks like I ran this scenario twice as well?
inds = find(cc0);
cc0(inds(2:end))=false;

cc25 = allouts.BirthRate == 0.98 & allouts.CampaignCov == 0.25 & ...
allouts.MCV2Frac == 0.75 & allouts.MigrationRate == 0.2 & ...
allouts.MCV1Age == 270 & allouts.RuralR0==12 & ...
cellfun(@length, allouts.eradicated)==512 & strcmpi(allouts.MaBProfile, 'Long');

cc75 = allouts.BirthRate == 0.98 & allouts.CampaignCov == 0.75 & ...
allouts.MCV2Frac == 0.75 & allouts.MigrationRate == 0.2 & ...
allouts.MCV1Age == 270 & allouts.RuralR0==12 & ...
cellfun(@length, allouts.eradicated)==512 & strcmpi(allouts.MaBProfile, 'Long');

colors = cbrewer('seq', 'Blues', 9);
hold on
plot3(allouts.C50{cc0}(1, 2:end), allouts.C50{cc0}(2, 2:end), ones(1, length(allouts.C50{cc0})-1), '-', 'LineWidth', 4, 'Color', colors(9, :));
plot3(allouts.C50{cc25}(1, 2:end), allouts.C50{cc25}(2, 2:end), ones(1, length(allouts.C50{cc25})-1), '-', 'LineWidth', 4, 'Color', colors(7, :));
plot3(C50(1, 2:end), C50(2, 2:end), ones(1, length(C50)-1), '-', 'LineWidth', 4, 'Color', colors(5, :));
plot3(allouts.C50{cc75}(1, 2:end), allouts.C50{cc75}(2, 2:end), ones(1, length(allouts.C50{cc75})-1), '-', 'LineWidth', 4, 'Color', colors(3, :));



mystr = ['Urban R_{0}: 24; Rural R_{0}: 12' newline ...
    'MCV2 coverage: 75% of MCV1 coverage' newline ...
    'Migration Rate: High' newline ...
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

text(.7, .64, '0% SIA Coverage', 'Color', colors(9, :));
text(.7, .61, '25% SIA Coverage', 'Color', colors(7, :));
text(.7, .58, '50% SIA Coverage', 'Color', colors(5, :));
text(.7, .55, '75% SIA Coverage', 'Color', colors(3, :));
title('Effect of SIAs: 50% Eradication probability contours');
myprint('-dpng', ['Images\SIA_effect_50contours.png']);
saveas(h1, ['MatFigs\SIA_effect_50contours.fig']);

plot3(allouts.C75{cc0}(1, 2:end), allouts.C75{cc0}(2, 2:end), ones(1, length(allouts.C75{cc0})-1), '--', 'LineWidth', 4, 'Color', colors(9, :));
plot3(allouts.C75{cc25}(1, 2:end), allouts.C75{cc25}(2, 2:end), ones(1, length(allouts.C75{cc25})-1), '--', 'LineWidth', 4, 'Color', colors(7, :));
plot3(C75(1, 2:end), C75(2, 2:end), ones(1, length(C75)-1), '--', 'LineWidth', 4, 'Color', colors(5, :));
plot3(allouts.C75{cc75}(1, 2:end), allouts.C75{cc75}(2, 2:end), ones(1, length(allouts.C75{cc75})-1), '--', 'LineWidth', 4, 'Color', colors(3, :));
title('Effect of SIAs: 50% and 75% Eradication probability contours');

myprint('-dpng', ['Images\SIA_effect_bothcontours.png']);
saveas(h1, ['MatFigs\SIA_effect_bothcontours.fig']);

clf;
plot3(allouts.C75{cc0}(1, 2:end), allouts.C75{cc0}(2, 2:end), ones(1, length(allouts.C75{cc0})-1), '-', 'LineWidth', 4, 'Color', colors(9, :));
hold on
plot3(allouts.C75{cc25}(1, 2:end), allouts.C75{cc25}(2, 2:end), ones(1, length(allouts.C75{cc25})-1), '-', 'LineWidth', 4, 'Color', colors(7, :));
plot3(C75(1, 2:end), C75(2, 2:end), ones(1, length(C75)-1), '-', 'LineWidth', 4, 'Color', colors(5, :));
plot3(allouts.C75{cc75}(1, 2:end), allouts.C75{cc75}(2, 2:end), ones(1, length(allouts.C75{cc75})-1), '-', 'LineWidth', 4, 'Color', colors(3, :));
view(2)
text(.51, .74, '0% SIA Coverage', 'Color', colors(9, :));
text(.51, .71, '25% SIA Coverage', 'Color', colors(7, :));
text(.51, .68, '50% SIA Coverage', 'Color', colors(5, :));
text(.51, .65, '75% SIA Coverage', 'Color', colors(3, :));
mystr = ['Urban R_{0}: 24; Rural R_{0}: 12' newline ...
    'MCV2 coverage: 75% of MCV1 coverage' newline ...
    'Migration Rate: High' newline ...
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
title('Effect of SIAs: 75% Eradication Probability Contours')
myprint('-dpng', ['Images\SIA_effect_75contours.png']);
saveas(h1, ['MatFigs\SIA_effect_75contours.fig']);
        