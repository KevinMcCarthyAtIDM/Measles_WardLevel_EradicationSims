README on how the code in this folder is structured and how to use it:

Input file generation
First step - build demographics and migration files.


Demographics file creation:
In folder "DemographicFileGeneration"
The first item to run is Process_Worldpop.py.  This function reads a shapefile and worldpop population and birth rasters, aggregates the rasters according to the shapes in the shapefile, and spits out the file "population_by_ward.csv" containing ward names, corresponding populations, latitude, longitude, and areas.  I don't believe that the births actually get used here.
The shapefiles and worldpop rasters paths are hardcoded to their location on IDMPPTSS03 (D:\Shapefiles\..., D:\Worldpop\...), and this should be replaced so that they resolve to the corresponding files in Dropbox(IDM)\Measles Team Folder\Data\(Shapefiles, Worldpop).

Once Process_Worldpop.py is run, Build_Demographics_File.py builds the actual Json grabbed by Eradication.exe.  It begins from a base demographics file (Nigeria_LGA_demographics, co-located in this directory), and creates a set of nodes corresponding to the information in "population_by_ward.csv", cuttin git to only 5 states so that the simulations are manageable.  Pretty straightforward.  NodeIDs are constructed from a numbering convention where nodeID also encodes information about the latitude and longtiude.


Migration file creation:
In folder "Migration File Generation"
The main piece of code here is Gravity_Model_Migration.py.  Beginning from the base demographics file constructed in the last step, read in the set of nodes, and define some parameters (maximum number of connections set by DTK, the 3 exponents of the gravity model). Then compute the "gravity matrix": for each node i, the connection strength to any other node j is proportional to 
(node i population)^('source' exponent) * (node j population)^('destination' exponent) / (distance from i to j, + magic number to avoid div by zero)^('distance' exponent).  All of the exponents are set to 1 by my default.

Normalize the migration matrix so that on average, rows sum to 1 (i.e., on average, each person migrates daily).  This sets a meaningful scale for the configuration params x_[type]_Migration.

Then, build the local migration file first - for each node, get the elements of the mgiration matrix corresponding to the 8 closest nodes.  
After grabbing, set the corresponding elements of the migration matrix to 0 so they don't get double counted in later steps
Next, loop through other migration components.  Here, for each node, I grab the strongest remaining connections up to "maxConnections" for the corresponding migration type.  Again, set them to 0 in the migration matrix so that they don't get grabbed again if we are using many migration types.

The results are written out to migration text files, formatted as "source node ID	destination node ID	connection strength".  
Finally, we call "buildMigrationFiles.py" to construct the migration binaries from the demographics file and the migration text files.