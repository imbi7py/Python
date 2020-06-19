# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import geopandas as gpd
import pandas as pd
import glob
from os.path import expanduser
home = expanduser("~")

# INPUT
root = home + '\\Documents\\DATA\\OBServ\\ESYRCE\\PROCESSED\\z30\\filtered\\'

# OUTPUT
outFilename = home + '\\Documents\\DATA\\OBServ\\ESYRCE\\PROCESSED\\z30\\merged.shp'

# Get filtered files
listFiles = glob.glob(root+"*.shp")

# Concat dataframes
data = gpd.read_file(listFiles[0])
print("Read file:", listFiles[0])
frames = [data]
for file in listFiles[1:]:
    data = gpd.read_file(file)
    frames.append(data)
    print("Read file:", file)
result = pd.concat(frames)

# To file 
result.to_file(filename = outFilename, driver="ESRI Shapefile")
print("Saved file:", outFilename)
