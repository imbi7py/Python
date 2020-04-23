# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 16:37:49 2020

@author: angel.gimenez

Calculate the evolution of the following variables using ESYRCE data
# INTENSIFICATION METRICS: 
# - Percentage of semi-natural cover
# - Average of cropfield size
# - Heterogeneity of crops
"""
import geopandas as gpd
import pandas as pd
import numpy as np
import blockCalculator as bc
from os.path import expanduser
home = expanduser("~")

# INPUT
layer = 'z28'
inputESYRCE = home + '\\Documents\\DATA\\OBServ\\LandCover\\ESYRCE\\PROCESSED\\esyrceFiltered_' + layer + '.shp'

# INTENSIFICATION METRICS: 
# Percentage of semi-natural cover
colsSeminatuByYear =  ['blockNr', 'year', 'seminaturalPercentage']
colsSeminatuDiff   =  ['blockNr', 'seminaturalPercentage']
DfSeminatuByYear   = pd.DataFrame(columns = colsSeminatuByYear)
DfSeminatuDiff     = pd.DataFrame(columns = colsSeminatuDiff)

# Average of cropfield size
colsCropSizeByYear =  ['blockNr', 'year', 'avCropfieldSize']
colsCropSizeDiff   =  ['blockNr', 'avCropfieldSize']
DfCropSizeByYear   = pd.DataFrame(columns = colsCropSizeByYear)
DfCropSizeDiff     = pd.DataFrame(columns = colsCropSizeDiff)

# Heterogeneity of crops
colsHeterogByYear =  ['blockNr', 'year', 'heterogeneity']
colsHeterogDiff   =  ['blockNr', 'heterogeneity']
DfHeterogByYear   = pd.DataFrame(columns = colsHeterogByYear)
DfHeterogDiff     = pd.DataFrame(columns = colsHeterogDiff)

# load file from local path
data = gpd.read_file(inputESYRCE)

# Loop plot numbers
blockNrs = np.unique(data.D2_NUM)
for blockNr in blockNrs:
    
    selectedInd = data.D2_NUM == blockNr
    dataBlockNr = [data.iloc[i] for i in range(0,len(selectedInd)) if selectedInd.iloc[i]]
    dataBlockNr = gpd.GeoDataFrame(dataBlockNr)
    
    # Create dataframes with the initial and end years
    years   = np.unique(dataBlockNr.YEA)
    yearIni = years[0]
    yearEnd = years[len(years)-1]    
    if yearIni == yearEnd: continue
    selectedIni  = dataBlockNr.YEA == yearIni
    selectedEnd  = dataBlockNr.YEA == yearEnd
    dataBlockIni = [dataBlockNr.iloc[i] for i in range(0,len(selectedIni)) if selectedIni.iloc[i]]    
    dataBlockEnd = [dataBlockNr.iloc[i] for i in range(0,len(selectedEnd)) if selectedEnd.iloc[i]]
    dataBlockIni = gpd.GeoDataFrame(dataBlockIni)
    dataBlockEnd = gpd.GeoDataFrame(dataBlockEnd)
    
    # Calculate intensification parameters in the initial and end years
    intensParamsIni = bc.calculateIntensificationParameters(dataBlockIni)
    intensParamsEnd = bc.calculateIntensificationParameters(dataBlockEnd)
    
    # SAVE DATAFRAMES
    # Percentage of semi-natural cover
    seminatuPercIni = intensParamsIni['seminaturalPercentage']
    seminatuPercEnd = intensParamsEnd['seminaturalPercentage']
    seminatuDiff    = (seminatuPercEnd - seminatuPercIni) / (yearEnd - yearIni)
    DfSeminatuByYear.loc[len(DfSeminatuByYear)] = [blockNr, yearIni, seminatuPercIni]
    DfSeminatuByYear.loc[len(DfSeminatuByYear)] = [blockNr, yearEnd, seminatuPercEnd]
    DfSeminatuDiff.loc[len(DfSeminatuDiff)]     = [blockNr, seminatuDiff]

    # Average of cropfield size
    avCropfieldSizeIni  = intensParamsIni['avCropfieldSize']
    avCropfieldSizeEnd  = intensParamsEnd['avCropfieldSize']
    avCropfieldSizeDiff = (avCropfieldSizeEnd - avCropfieldSizeIni) / (yearEnd - yearIni)
    DfCropSizeByYear.loc[len(DfCropSizeByYear)] = [blockNr, yearIni, avCropfieldSizeIni]
    DfCropSizeByYear.loc[len(DfCropSizeByYear)] = [blockNr, yearEnd, avCropfieldSizeEnd]
    DfCropSizeDiff.loc[len(DfCropSizeDiff)]     = [blockNr, avCropfieldSizeDiff]

    # Heterogeneity of crops
    heterogeneityIni  = intensParamsIni['heterogeneity']
    heterogeneityEnd  = intensParamsEnd['heterogeneity']
    heterogeneityDiff = (heterogeneityEnd - heterogeneityIni) / (yearEnd - yearIni)
    DfHeterogByYear.loc[len(DfHeterogByYear)] = [blockNr, yearIni, heterogeneityIni]
    DfHeterogByYear.loc[len(DfHeterogByYear)] = [blockNr, yearEnd, heterogeneityEnd]
    DfHeterogDiff.loc[len(DfHeterogDiff)]     = [blockNr, heterogeneityDiff]


    
    