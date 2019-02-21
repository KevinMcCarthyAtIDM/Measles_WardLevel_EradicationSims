README on how the code in this folder is structured and how to use it:

Action items:
Bring local dtk-tools into agreement with master and ensure that everything still works.  Push changes to CustomReport.py
Create pull requests for necessary features (Age dependent vaccine take, Spatial report accumulation, and urban rural r0 scaling) into DTK Trunk
Remove all magic numbers - define these in-line as variables somewhere with descriptive names, consider an arg-parser to set them from command line as well.
Suggestions for cleaning up/improving tracking of experiment building?
Suggestions for cleaning up the "sample pt function code"?
Suggestions for cleaning up, removing intermediate files from demographic file building?
Look for opportunities where code should be pulled into dtk-tools or something similar for re-use in other projects.



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


Other input files:
Other Eradication.exe input files can be found in folder "InputFiles". Most were created by hand. These include:
"config.json" - standard config file, many parameters will be overwritten during experiment building.
"basecampaign.json" - a base campaign file that defines the outbreak event, the distribution of routine immunization, and the SIAs.  There are three "individualproperty" groups - called "MCV1", "MCV2", and "SIAOnly".  Routine delivery of a first dose of measles vaccine goes to the MCV1 group and MCV2 group; routine delivery of a second dose goes to the MCV2 group, and the third group is covered only by the SIAs.
In each node, the proportion of children in the three groups will be set in the demographics file during simulation construction.
SIAs are delivered with a CoverageByNode event coordinator, and the coverages by node will be filled in during simulation construction.
"emodules_map.json" and "reports.json" - these files configure Eradication to use a DLL reporter called AgeAtInfectionHistogram reporter, which records the age distribution of new infections.  For space-saving purposes, rather than report all infections individually, they are binned up into a configurable histogram of ages and written out at a configurable reporting interval.  The dll is contained in the folder "reporter_plugins".  This could maybe be moved to InputFiles or into the Executable directory.


Executable: The folder "Executable" contains the version of Eradication.exe used for these simulations.  It should correspond to commitID 5102110386e26ca2a24ad50daf3868f8156a65ff of the branch "KM_working" of DtkTrunk.  
One thing we should consider is pulling in the features that are in this branch but not in master.  Each feature should have it's own commit and a "mothballed" branch associated with it under my account (KevinMcCarthyAtIDM) - these are called "AgeDependentVaccineTake", "Spatial_Report_Accumulation" and "UrbanRuralR0Scaling".


Simulation building - first iteration:
Here we get into the dtk-tools side of things.
The main method to begin experiment construction is "Measles_Ward_Simulations.py"  We can walk through this:
After import statements, the DTKConfigBuilder is set up, with all of the base input files that it will need.  All of this is pretty standard.  
The last line in this block (at line 30) sets up the Age at infection histogram plugin.  This uses code that I added to CustomReport.py in dtk-tools. I committed this code locally but forgot to push to the remote, it can be found in D:\kmccarthy\GitRepos\dtk-tools\dtk\utils\reports\CustomReport.py, from lines 39-55, and should be pushed to the remote.  The local dtk-tools install is a bit out of date now, so I'm wary of just pushing it as is.
In the "main" block, we begin the experiment building.
Each experiment is going to represent a "scenario", with corresponding values for Urban/Rural R0, Migration, SIA coverage, "Dropout", age at which routine immunization is scheduled, maternal antibody profile, birth rate, etc.  These parameters are defined in 28-long lists at the top of the main block.
Loop over each experiment to be built - create an empty list of "mod_fns".  
	Loop over building of simulations (512):
		Create a list of names for each experiment scenario parameter and each simulation parameter (lines 54-57).  
		Create a list of corresponding values.  Run_Number, META_Vaccination_Threshold and META_Fraction_Meeting will vary in each simulation; all other parameters are fixed to the experiment.  The two META parameters will be a mix of 1/3 samples from a uniform distribution  from 0.4-0.99 (lines 58-62), and 2/3 samples from a distribution biased to produce more values near 1 (lines 64-67).
		Append onto the list of mod_fns the ModFn for this simulation - sample_point_fn (from SetupFunctions.py), and the list of names and values.
	Call ModBuilder to build the experiment.  Give it a name and set experiment tags (recording all experiment scenario parameters and excluding the Run Number and the two meta parameters that vary for each simulation).
	Run the experiment






