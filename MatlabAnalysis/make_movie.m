exp_id = 'ad51318c-9fa6-e811-a2c0-c4346bcb7275';

metadata = loadJson(['..\Experiments\' exp_id '\metadata_output.json']);
sims = fieldnames(metadata);

sims2movie = cell(1, length(sims));
migration = zeros(1, length(sims));
frac_meeting = zeros(1, length(sims));
threshold = zeros(1, length(sims));
%Later will do some real selection here
for sim = 1:length(sims)
    migration(sim) = metadata.(sims{sim}).META_Migration;
    frac_meeting(sim) = metadata.(sims{sim}).META_Fraction_Meeting;
    threshold(sim) = metadata.(sims{sim}).META_Vaccination_Threshold;
    sims2movie{sim} = strrep(strrep(sims{sim}, 'alpha_', ''), '_', '-');
end

output = load(['..\Experiments\' exp_id '\output_' sims2movie{1} '.mat']);
output_node_order = output.nodeIDs;
demog = loadJson('..\InputFiles\Nigeria_Ward_smaller_minpop5000_demographics.json');
demog_dotnames = cellfun(@(x) x.dot_name, demog.Nodes, 'UniformOutput', false);
demog_nodeIDs = cellfun(@(x) x.NodeID, demog.Nodes);
[~, locb] = ismember(output_node_order, demog_nodeIDs);

output_dotnames = demog_dotnames(locb);

shapes = shape_get('D:\Shapefiles\Nigeria\July_31_Geopode_Shapes\Boundary_VaccWards_Export\Boundary_VaccWards_Export.shp');
shape_dotnames = {shapes.Attribute.dot_name};
[~, locb] = ismember(shape_dotnames, output_dotnames);
cc = locb ~= 0;
shapes.Shape = shapes.Shape(cc);
shapes.Attribute = shapes.Attribute(cc);
locb = locb(cc);


for sim = 1:length(sims2movie)
    output = load(['..\Experiments\' exp_id '\output_' sims2movie{sim} '.mat']);
    prev = output.Prevalence;
    cmap = flipud(cbrewer('div', 'RdBu', 256));
    V = VideoWriter(['testsim_' num2str(sim) '.avi']);
    V.FrameRate = 24; %2 year per second;
    myfigure_square;
    open(V)
    for ii = 1:365
        if size(prev, 1) < 365
            prev(size(prev, 1):365, :) = 0;
        end
        clf;
        shape_plot2(shapes, min(log10(.101), log10(prev(ii, locb)+.001)), log10([.001, .101]), cmap);
        colormap(cmap)
        cb = colorbar;
        set(cb, 'YTick', [0, 0.5, 1]);
        set(cb, 'YTickLabel', {'0', '1%', '>10%'})
        set(get(cb, 'YLabel'), 'String', 'Prevalence');
        title(['Month ' num2str(ii) ', Mig. rate = ' num2str(migration(sim)) ', ' num2str(frac_meeting(sim)*100, '%0.0f') '% of districts over ' num2str(threshold(sim)*100, '%0.0f') '% coverage'], 'FontSize', 24);
        axis square
        axis off
        frame = getframe(gcf);
        writeVideo(V, frame);
    end
    close(V);
end