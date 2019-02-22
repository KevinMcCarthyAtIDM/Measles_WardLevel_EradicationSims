README on how the code in this folder is structured and how to use it:
This is an example of how I did a Separatrix by hand, so Zhaowei, as you look through this, it should hopefully serve a bit to inform how we might translate the old matlab separatrix code into dtk-tools.  A key difference is that in this implementation, I ran batches of experiments, each representing a scenario, and then iterated by creating new experiments as iterations on those scenarios.  I did a lot of bookkeeping in json files to link new experiments to old ones.  The ideal implementation of Separatrix would spawn a suite, and each iteration would be an experiment within that suite instead of how I did it here.

Action items:
Bring local dtk-tools into agreement with master and ensure that everything still works.  Push changes to CustomReport.py
Create pull requests for necessary features (Age dependent vaccine take, Spatial report accumulation, and urban rural r0 scaling) into DTK Trunk
Remove all magic numbers - define these in-line as variables somewhere with descriptive names, consider an arg-parser to set them from command line as well.
Send simulation outputs and all intermediate files to a Dropbox folder instead of keeping them located in the repository.
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

I think it makes sense briefly describe here the setup for building later iterations as well. The Measles_Ward_Simulations_iterx.py files proceed very similarly to the process described above.  However, after the first round of analysis, we will end up with a file "MatlabAnalysis\outputs.json" (or "outputs_iter2.json, ...) that guides the next set of simulations as follows:
Set up the configBuilder as in iteration 0.  
	Load "outputs.json".  It contains a list of dicts, and each element of this list describes one of the experiments run in the previous iteration, recording all of the "scenario parameters", the experiment ID, and a contour of interest where the next set of simulations should be located.
For each dict in the list:
	Set up all of the "scenario parameters" so that this experiment is consistent with the previous experiment we are iterating on.
	Record the last experiment ID.
	Loop to build the simulations:
		Get a random point from "contourx" and "contoury", the recorded contour of interest from the previous iteration.
		Place a sample near that point, with random Gaussian nose.  If the point is outside of 0.4, 0.99 in either x or y, try again.
From here, experiment building proceeds as in the first iteration.

The last bit of code necessary for experiment building should be the setup functions in SetupFunctions.py.  The first function in this file defines "sample_point_fn", which is the mod_fn used in the builder.  The behavior of the functions in here are as follows:
sample_point_fn is the main function that will be called by the builder.  

sample_point_fn()
Initialize an empty set of simulation tags.  
Check for required inputs.
Setup "Base parameters" - default parameter setup for the configuration file (could also just change the base configuration to reflect all of these)
Call RI_Vacc_Setup to set up the routine vaccination configuration.  This requires the metaparameters "vaccination threshold" and "fraction of nodes meeting that threshold", which are the main parameters varied by simulation.  It also takes a metaparameter called "Dropout", which sets the ratio of first and second-dose routine coverage with measles vaccine.  
Call SIA_Coverage_Setup to set up the campaign coverage by node.
Loop over all other parameters.  If parameter is a meta parameter, call "MetaParameterHandler", which defines special behavior when I need to vary multiple config/campaign parameters at once.  If parameter is not a meta parameter, just call the standard config_builder.set_param.  
Save all parameters in tags, and return the tags.

RI_Vacc_Setup():
This is a tricky one.  The vaccination threshold and fraction of nodes meeting that threshold do not actually completely define a distribution.  However, making some assumptions - the distribution is normal in logit space (a transform of probability), I can draw a random value for the variance and solve for the mean, and then draw a distribution consistent with the threshold/fraction meeting constraint.  A second complication is that the operational threshold is generally defined in terms of districts, but the nodes are smaller than districts, so we need to apply this constraint at district level but allow some extra variance on the nodes in a district. The code proceeds as follows: 
Draw a random number from 0 to 4, which will be the standard deviation of the distribution.
Solve for the mean, given the standard deviation, the threshold, and the fraction of districts above that threshold.
Find all unique district names - each node has an associated dot_name in it's metadata - country:province:district:ward.  Split this string for all nodes and find the unique country:province:district tuplets.  
Draw a random value of coverage for each district as follows:
    for name in unique_district_names:
        tmp = math.exp(LN_mu + LN_sig * random.gauss(0, 1))
        district_coverages[name] = tmp / (1 + tmp)

The math here relates the coverages in probability space to the random numbers in logit-space (p = e^x/(1+e^x) ). 
Now, loop over each node.
Find which district it is in and get the corresponding district-level coverage.
Add a little bit of extra noise:
        tmp = math.log(distcov / (1 - distcov))  #transform back to logit space
        tmp2 = math.exp(tmp + 0.2 * random.gauss(0, 1)) #add a bit of noise here, 0.2 (magic number, should fix this!)
        wardcov = tmp2 / (1 + tmp2)  #convert back to probability space

Now, since routine immunization is governed by IndividualProperties, we'll be setting the distribution of individual properties for this node as follows:
        node['IndividualProperties'][0]['Initial_Distribution'] = [(1-Dropout)*wardcov, (Dropout)*wardcov, 1-wardcov]

	Dropout defines the probability of somebody getting 1 dose instead of 2, so in the above, the first group gets 2 doses (coverage*(1-Dropout)), the second group gets only 1 dose (coverage * Dropout), and the last get no doses: (1-coverage).
	After we've covered all nodes, put the new demographic file as an overlay for config-builder.

SIA_Coverage_setup:
A little simpler than the RI coverage setup, but very similar.  Note that the "campaign coverage" parameter, as implemented, is the campaign coverage only for children who are in the "SIAOnly" group - children in the "MCV1" or "MCV2" groups will always be covered.

First, if campaign coverage is <=0, this is a signal for no campaigns at all -> demographic Coverage = 0.
Otherwise, we set demographic Coverage = 1, and use the coverage by node coordinator to change coverage on a node by node basis.
Similar to above, draw a random variance of the campaign coverage distribution, and draw random numbers in logit-space to set campaign coverages for each node.  

Loop over events in the campaign file:
if the event is an SIA, set demographic Coverage to 0 or 1 as determined above.
if the event is the SIAs targeted to the SIAonly group, additionally fill the "Coverage_By_Node" property with the random campaign coverages drawn above.

The last piece of code in SetupFunctions.py is the MetaParameterHandler.  In short, this function lets me use "metaparameters" to set multiple config/campaign parameters at once.  
So for example, if the parameter passed in is "META_MaB_Profile", I want to set the maternal antibody profile, which is governed by two config parameters - Maternal_Sigmoid_HalfMaxAge, and Maternal_Sigmoid_SteepFac.  In MetaParameterHandler, the appropriate code to do this is implemented.  
Or another example - META_Timesteps.  If I change the Simulation_Timestep from a value of 1 to a value of T, I need to change other parameters (i.e., Timesteps_Between_Repetitions for all campaign events needs to be changed to 1/T.)  This is handled here.  



Experiment Analysis:
The function "Measles_Ward_Simulations_Analyze.py" pulls down simulation results for analysis, though most of the real analysis is done in matlab.  The function is fairly simple:
Create a list of all experiments that should be analyzed.  
Loop over this list:
	If there already exists a folder for this experiment in the "Experiments" folder, or if any simulations have not completed, skip.
	Otherwise, get tags for the experiment and record them in the file "Experiments\experiment_metadata.json"
	Use the analyzer Output2MatlabAnalyzer to analyze the experiments.

Output2MatlabAnalyzer is contained in the folder "Python Analysis.  In brief, here is what it does:
Make an output directory for the experiment
Retrieve the InsetChart, Age at infection histogram report, and spatial reports (defined in self.filenames) for each simulation.
Shorten insetChart channel names, because if they are too long it cannot save the output.
Get simID, ExpId, and save all of the data for this simulation to a matlab file in the experiment directory.
Finally, after all simulations are saved, write a metadata file in the experiment directory ("experiments\[ExpId]\metadata_output.json"), that records all simulation tags.



Matlab Analysis:
The matlab analysis folder is a very poorly organized folder of scripts to analyze simulation outputs, generate some figures, and store results to enable further iteration of the experiments.
The first piece of code to be run is called "Separatrix_datagetter.m".  This file loops over all of the experiments, load all simulations for each experiment, and condenses the outputs of interest into a single file, which helps speed up downstream analysis.  Rather than describe in detail here, I've commented extensively in the m-file to help readability.

The next code of interest is in Separatrix_plotter.m.  Due to poor code architecting, this piece of code both performs the separatrix analysis and produces a set of figures; it is also copied three times into "Separatrix_plotter_2exps" and "..._3exps" to handle the analysis and plotting after the second and third iteration.  It's a bit of a beast, and I'll describe it a bit here and try to comment extensively in the file itself.  Note that the _2exps and _3exps versions follow much the same path, but have some additional bookkeeping to do the analysis on the results from multiple experiments.  I'll describe the initial version first.  

In Separatrix_plotter - 
First, initialize a structure that will hold experiment metadata, simulation parameters, and analysis results for all experiments.
Loop over the experiments, and construct a probability surface of successful eradication vs. failure to eradicate.  Find the 50, 75, and 80% contours of this probability surface.  Make some figures and cache the metadata, sim parameters, and analysis results.  After looping over all experiments, save all of the cached data.
More extensive comments are embedded in the code.
Separatrix_plotter_iter2 and _iter3 do much the same thing as separatrix_plotter, but with extra bookkeeping to combine results from multiple experiments that represent iterations of a particular scenario.
Also unfortunately, the code for Separatrix_pltter doesn't really check whether the experiment belongs to the appropriate iteration, and so if I re-run Separatrix_plotter, it will probably plot results for all experiments independently, including the later iterations, when it should really only plot results from the first iteration.  Separatrix_plotter_iter2 and _iter3 do have version checking - they look for whether the experiment metadata contains a field called "prev_expID" (iter2) or "prev_expID1", "prev_expID2" in iter3.  Similar checking would be good for the first iteration.  

The last piece of code of interest here is "output_table_to_jsondict", which loads the output matlab file produced by Separatrix_plotter, and converts the outputs of interest and experiment scenario parameters/IDs to a json file that can be read by the experiment builders for the second and third iterations of simulations.  Again, comments embedded in the code

Remaining code in this folder generates specific figures that combine results from multiple experiment scenarios (i.e., I define a baseline scenario, and compare the three iterations of that scenario with other scenarios that vary one of the parameters - e.g., lower birth rate, or different migration, or different vaccine schedules, etc.)


