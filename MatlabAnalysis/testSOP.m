params1.FilesToRetrieve = {'..\output_stash\output_xb98\SpatialReport_Exposed Population.bin',
    '..\output_stash\output_xb98\SpatialReport_New_Infections.bin',
    '..\output_stash\output_xb98\SpatialReport_Recovered Population.bin',
    '..\output_stash\output_xb98\SpatialReport_Immunized Population.bin',
    '..\output_stash\output_xb98\SpatialReport_Population.bin',
    '..\output_stash\output_xb98\SpatialReport_Susceptible Population.bin',
    '..\output_stash\output_xb98\SpatialReport_Infectious Population.bin',
    '..\output_stash\output_xb98\SpatialReport_Prevalence.bin'};
params1.Name = 'SOP1';

A = SpatialOutputParser(params1);
A.ParseFiles(A.FilesToRetrieve, 1, 1)
