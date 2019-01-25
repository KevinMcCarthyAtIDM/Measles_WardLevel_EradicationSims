
%Code to plot population density for the wards of Nigeria on a map

%Load population, area, and names from demographics file
demog = loadJson('..\InputFiles\Nigeria_Ward_smaller_minpop5000_demographics.json');
demog_dotnames = cellfun(@(x) x.dot_name, demog.Nodes, 'UniformOutput', false);
pops = cellfun(@(x) x.NodeAttributes.InitialPopulation, demog.Nodes);
area = cellfun(@(x) x.NodeAttributes.Area_km2, demog.Nodes);

%Load shapes and names from shapefile
shapes = shape_get('D:\Shapefiles\Nigeria\July_31_Geopode_Shapes\Boundary_VaccWards_Export\Boundary_VaccWards_Export.shp');
shape_dotnames = {shapes.Attribute.dot_name};

%Link the shapes, population, and areas using the dotname field.
%Ignore any unmatched names (though there should be none, hopefully)
[~, locb] = ismember(shape_dotnames, demog_dotnames);
cc = locb ~= 0;
shapes.Shape = shapes.Shape(cc);
shapes.Attribute = shapes.Attribute(cc);
locb = locb(cc);  %Locb reorders pops and area to match the shapes.

%Plotting - define color map, color axis limits
cmap = flipud(cbrewer('div', 'RdBu', 256));
myfigure_square;
clf;
minC = floor(min(log10(pops./area)));
maxC = ceil(max(log10(pops./area)));
rangeC = maxC - minC;

%Plot LGA shapes and color according to log10(pop density)
shape_plot2(shapes, log10(pops(locb)./area(locb)), [minC, maxC], cmap);

%For visual purposes, map the state boundaries as well.
%Just plot the boundaries as lines - highlights state boundaries, but
%doesn't fill the area like "shape_plot" does, so the wards are still
%visible.
shapes2 = shape_get('D:\Shapefiles\Nigeria\July_31_Geopode_Shapes\Boundary_VaccStates_Export\Boundary_VaccStates_Export.shp');
cc = ismember({shapes2.Attribute.StateName}, {'Kano', 'Katsina', 'Jigawa', 'Kaduna', 'Bauchi'});
myshapes = shapes2.Shape(cc);
hold on
for ii = 1:5
    plot(myshapes(ii).x, myshapes(ii).y, 'k-')
end

%Label the colorbar and print
cb = colorbar();
colormap(cmap)
set(cb, 'YTick', linspace(0, 1, rangeC+1));
cInts = linspace(minC, maxC, rangeC+1); 
Clabs = {};
for ii = 1:(rangeC+1)
    Clabs{ii} = ['10^' num2str(cInts(ii))];
end
set(cb, 'YTickLabel', Clabs);
axis equal
axis off
set(get(cb, 'YLabel'), 'String', 'Pop. Density (ppl/km^2)')
myprint('-dpng', '..\Images\Density.png');
