# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import dill
import geopandas as gpd
import numpy as np

from os.path import expanduser
home = expanduser("~")

# INPUT
dissolve = True
layer = "z30"
#inputFile = home + '\\Documents\\DATA\\OBServ\\LandCover\\ESYRCE\\PROCESSED\\esyrceProcessed_' + layer + '.shp'
inputFile = home + '\\Documents\\DATA\\Observ\\LandCover\\ESYRCE\\PROCESSED\\session_esyrceFiltered_z30_epsg23030_selectedCols_addIntenMetrics_addDemand.pkl'

if layer == 'z28':
    crs = "EPSG:23028"

if layer == 'z30':
    crs = "EPSG:23030"
    
# Read file
#processedData = gpd.read_file(inputFile)
dill.load_session(inputFile) # data in dataSel
processedData = dataSel
    
# To files, by year
years = np.unique(processedData.YEA)
for year in years:
    selectedInd   = processedData.YEA == year
    validDataYear = [processedData.iloc[i] for i in range(0,len(selectedInd)) if selectedInd.iloc[i]]
    validDataYear = gpd.GeoDataFrame(validDataYear)
    if (dissolve):
        try:
            validDataYear = validDataYear.dissolve(by='D2_NUM')
        except:
            print("Warning: dissolve in year "+str(year)+" failed...")
        shapefile = home + '\\Documents\\DATA\\OBServ\\LandCover\\ESYRCE\\PROCESSED\\'+layer+'\\dissolved\\'+str(year)+".shp"
    else:
        shapefile = home + '\\Documents\\DATA\\OBServ\\LandCover\\ESYRCE\\PROCESSED\\'+layer+'\\full\\'+str(year)+".shp"
    validDataYear.crs = crs;
    validDataYear.to_file(filename = shapefile, driver="ESRI Shapefile")
    
