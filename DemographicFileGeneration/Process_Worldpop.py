##
"""
Process_Worldpop: Use STAMP to apply Ward-level shapes from northern Nigeria onto Worldpop maps and generate
a table of populations (and birth rates?), and central lat/longs for each ward.
"""
#

import numpy as np
import pandas as pd
import argparse
import math
import os
from osgeo import gdal, ogr
import sys
import time
sys.path.insert(0, 'D:\\kmccarthy\\GitRepos\\STAMP\\')
from stamp.GDALTools.GDALTools.RasterUtils import extract_admin_level_data
from shutil import copyfile


# import the STAMP utils I need


# def cut_layer(layer):
#
#    for feature in layer:
#        if not feature['StateCode'] in states2keep:
#            layer.DeleteFeature(feature.GetFID())

def process_shapefile(shape_filedir, shape_fileprefix, shape_codefilename):
    shape_codes = pd.read_csv(shape_codefilename)
    shape_file = ogr.Open(shape_filedir + shape_fileprefix + '.shp', update=True)
    layer = shape_file.GetLayerByIndex(0)
    layer.CreateField(ogr.FieldDefn('dot_name', ogr.OFTString))
    i = 0
    states2keep = ['AD', 'BA', 'BR', 'FC', 'JI', 'KB', 'KD', 'KN', 'KT', 'SO', 'YO', 'ZA']
    features2delete = []

    feature = layer.GetNextFeature()
    while feature:
        if 0 == (i % 100):
            print('on shape ', i, ' of ', layer.GetFeatureCount())

        # Find the components of the dot name in the code list
        row = shape_codes[shape_codes['Ward Code'] == feature['WardCode']]

        # Mark shapes for deletion, and fill dot name field for the shapes to keep
        if (feature['StateCode'] not in states2keep) or (feature.geometry() is None) or (len(row) == 0):
            features2delete.append(feature.GetFID())
        else:
            feature.SetField('dot_name', ('Nigeria:' + row.State + ':' + row.Lga + ':' + row.Ward).iloc[0].lower())
            layer.SetFeature(feature)

        feature = layer.GetNextFeature()
        i += 1

    for feat in features2delete:
        layer.DeleteFeature(feat)

    shape_file = None
    return 0


if __name__ == "__main__":

    # Basic parameters.  Should these be inputs?
    shape_filedir = 'D:\\Shapefiles\\Nigeria\\July_31_Geopode_Shapes\\Boundary_VaccWards_Export\\'
    shape_fileprefix = 'Boundary_VaccWards_Export'
    shape_codefilename = 'D:\\Shapefiles\\Nigeria\\July_31_Geopode_Shapes\\Nigeria_Name_Code_Map.csv'
    pop_raster_filename = 'D:\\WorldPop\\Nigeria\\NGA_ppp_v2c_2015_UNadj.tif'
    birth_raster_filename = 'D:\\WorldPop\\Nigeria\\NGA_births_pp_v2_2015.tif'
    output_filename = '.\population_by_ward.csv'
    recompute = False

    if recompute:
        # Copy new base files from the raw original files
        file_names = [fn for fn in os.listdir(shape_filedir) if fn.startswith(shape_fileprefix + '_Raw')]
        for fn in file_names:
            copyfile(shape_filedir + fn, shape_filedir + fn.replace('_Raw', ''))
        process_shapefile(shape_filedir, shape_fileprefix, shape_codefilename)

    shapefile = ogr.Open(shape_filedir + shape_fileprefix + '.shp')
    shapelayer = shapefile.GetLayerByIndex(0)
    pop_raster = gdal.Open(pop_raster_filename)
    method = 'RasterUtils'
    tic = time.clock()
    results = extract_admin_level_data(raster=pop_raster, layer=shapelayer, data_operation=np.ma.sum,
                                       name_field='dot_name', data_field='population', band_number=1,
                                       write_clips=False)

    toc = time.clock()
    results['latitude'] = 0.0
    results['longitude'] = 0.0
    results['area'] = 0.0
    for id in results.index:
        tmpshape = shapelayer.GetFeature(id)
        centroid = tmpshape.geometry().Centroid().GetPoint()
        results.at[id, 'latitude'] = centroid[1]
        results.at[id, 'longitude'] = centroid[0]
        results.at[id, 'area'] = tmpshape.geometry().GetArea()

    results.to_csv(output_filename)
    print('Elapsed time is ' + str(toc - tic))
    del pop_raster
    del shapelayer
    del shapefile

