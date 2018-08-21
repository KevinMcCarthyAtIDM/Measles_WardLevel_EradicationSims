params1.FilesToRetrieve = {'..\output_stash\output_xb98\SpatialReport_Exposed Population.bin',
    '..\output_stash\output_xb98\SpatialReport_New_Infections.bin',
    '..\output_stash\output_xb98\SpatialReport_Recovered Population.bin',
    '..\output_stash\output_xb98\SpatialReport_Immunized Population.bin',
    '..\output_stash\output_xb98\SpatialReport_Population.bin',
    '..\output_stash\output_xb98\SpatialReport_Susceptible Population.bin',
    '..\output_stash\output_xb98\SpatialReport_Infectious Population.bin',
    '..\output_stash\output_xb98\SpatialReport_Prevalence.bin'};
params1.Name = 'SOP1';

SO = SpatialOutputParser(params1);
SO.ParseFiles(SO.FilesToRetrieve, 1, 1)

SO_node_order = SO.spatialOutput.nodeIDList{1}{1};
demog = loadJson('..\InputFiles\Nigeria_Ward_minpop5000_demographics.json');
demog_dotnames = cellfun(@(x) x.dot_name, demog.Nodes, 'UniformOutput', false);
demog_nodeIDs = cellfun(@(x) x.NodeID, demog.Nodes);
[~, locb] = ismember(SO_node_order, demog_nodeIDs);

SO_dotnames = demog_dotnames(locb);

shapes = shape_get('D:\Shapefiles\Nigeria\July_31_Geopode_Shapes\Boundary_VaccWards_Export\Boundary_VaccWards_Export.shp');
shape_dotnames = {shapes.Attribute.dot_name};
prev = A.spatialOutput.channelTimeSeries{1}{8};
[~, locb] = ismember(shape_dotnames, SO_dotnames);

cmap = flipud(cbrewer('div', 'RdBu', 256));
V = VideoWriter('testsim.avi');
V.FrameRate = 24; %2 year per second;
myfigure_square;
open(V)
for ii = 1:333
    clf;
    shape_plot2(shapes, log10(prev(locb, ii)+.001), log10([.001, 1.001]), cmap);
    colormap(cmap)
    cb = colorbar;
    set(cb, 'YTick', [0, 0.33, 0.66, 1]);
    set(cb, 'YTickLabel', {'0', '1%', '10%', '100%'})
    set(get(cb, 'YLabel'), 'String', 'Prevalence');
    axis square
    axis off
    frame = getframe(gcf);
    writeVideo(V, frame);
end
close(V);