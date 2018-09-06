strs = {'105', '102', '1', '98', '95', '9'};
xbs = [1.05, 1.02, 1.0, .98, .95, .9];
for ii = 1:length(strs)
    A = loadJson(['output_xb' strs{ii} '\InsetChart.json']);
    pop = [A.ChannelData{15}{:}];    
    x = (0:4000)/365;
    ps = polyfit(x, log(pop(6000:end)), 1);
    GR(ii) = exp(ps(1))-1;
end