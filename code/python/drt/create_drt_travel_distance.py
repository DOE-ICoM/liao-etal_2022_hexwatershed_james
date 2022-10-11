import os, sys, stat
from pathlib import Path
from os.path import realpath
import json

import numpy as np
from osgeo import  osr, gdal, ogr
from shapely.wkt import loads
import matplotlib.pyplot as plt
from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.gis.gdal.read.gdal_read_ascii_file import gdal_read_ascii_file
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file
import matplotlib as mpl
from pyflowline.formats.read_flowline import read_flowline_geojson
from pyearth.visual.ladder.ladder_plot_xy_data import ladder_plot_xy_data
from pyearth.visual.color.create_diverge_rgb_color_hex import create_diverge_rgb_color_hex
# getting the data
sPath_parent = str(Path(__file__).parents[3]) # data is located two dir's up
print(sPath_parent)

#the longest river channel on main

#drt file
sFilename_drt_fd = '/compyfs/liao313/00raw/drt/DRT_16th_FDR_globe.asc'
sFilename_drt_dis = '/compyfs/liao313/00raw/drt/DRT_16th_FDISTANCE_globe.asc'

a = gdal_read_ascii_file(sFilename_drt_fd)
b = gdal_read_ascii_file(sFilename_drt_dis)

aFlow_dir = a[0]
aFlow_dis = b[0]
ymax  = a[3]
xmin=a[2]
ysize =a[1]
xsize =a[1]

sFilename_site = sPath_parent + '/' + 'data/travel_distance' + '/' + 'site_location.geojson'
pDriver = ogr.GetDriverByName('GeoJSON')
pDataset_site = pDriver.Open(sFilename_site, gdal.GA_ReadOnly)
pLayer_site = pDataset_site.GetLayer(0)
pSrs = osr.SpatialReference()  
pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

nPoint = pLayer_site.GetFeatureCount()
aDistance_niws=list()
aTravel_distance= list()
for i in range(nPoint):
    pFeature= pLayer_site.GetFeature(i)
    pGeometry_in = pFeature.GetGeometryRef()
    sGeometry_type = pGeometry_in.GetGeometryName()
    lID =0 
    
    if sGeometry_type =='POINT':
        site_id = pFeature.GetField("identifier")        
        headwater = loads( pGeometry_in.ExportToWkt() )       
        #get the headwater latlon location
        dLon = headwater.coords[0][0]
        dLat = headwater.coords[0][1]
        iRow = int((ymax - dLat) / ysize) + 1
        iColumn = int((dLon - xmin) / xsize) + 1
        #track
        iDownslope =aFlow_dir[iRow-1, iColumn-1]

        #obs
        sFilename_geojson_in = sPath_parent + '/' + 'data/travel_distance' + '/downstreammain' + site_id+ '.geojson'
        
        aLine,pSpatial_reference  = read_flowline_geojson(sFilename_geojson_in)
        dDistance_nwis = 0.0
        for pLine in aLine:
            dLength = pLine.dLength
            dDistance_nwis = dDistance_nwis + dLength

        aDistance_niws.append(dDistance_nwis)

        #drt 
        dDistance_line = aFlow_dis[iRow-1, iColumn-1]               
        while iDownslope !=0:
            if iDownslope == 1:
                iRow= iRow
                iColumn = iColumn + 1
                iDownslope =aFlow_dir[iRow-1, iColumn-1]
                dDistance_line = dDistance_line+ aFlow_dis[iRow-1, iColumn-1]
            else:
                if iDownslope == 2:
                    iRow= iRow + 1
                    iColumn = iColumn + 1
                    iDownslope =aFlow_dir[iRow-1, iColumn-1]
                    dDistance_line = dDistance_line+ aFlow_dis[iRow-1, iColumn-1]
                else:
                    if iDownslope == 4:
                        iRow= iRow + 1
                        iColumn = iColumn 
                        iDownslope =aFlow_dir[iRow-1, iColumn-1]
                        dDistance_line = dDistance_line+ aFlow_dis[iRow-1, iColumn-1]
                    else:
                        if iDownslope == 8:
                            iRow= iRow + 1
                            iColumn = iColumn -1
                            iDownslope =aFlow_dir[iRow-1, iColumn-1]
                            dDistance_line = dDistance_line+ aFlow_dis[iRow-1, iColumn-1]
                            
                        else:
                            if iDownslope == 16:
                                iRow= iRow 
                                iColumn = iColumn - 1
                                iDownslope =aFlow_dir[iRow-1, iColumn-1]
                                dDistance_line = dDistance_line+ aFlow_dis[iRow-1, iColumn-1]
                            else:
                                if iDownslope == 32:
                                    iRow= iRow - 1
                                    iColumn = iColumn -1
                                    iDownslope =aFlow_dir[iRow-1, iColumn-1]
                                    dDistance_line = dDistance_line+ aFlow_dis[iRow-1, iColumn-1]
                                else:
                                    if iDownslope == 64:
                                        iRow= iRow - 1
                                        iColumn = iColumn 
                                        iDownslope =aFlow_dir[iRow-1, iColumn-1]
                                        dDistance_line = dDistance_line+ aFlow_dis[iRow-1, iColumn-1]
                                    else:
                                        if iDownslope == 128:
                                            iRow= iRow - 1
                                            iColumn = iColumn +1
                                            iDownslope =aFlow_dir[iRow-1, iColumn-1]
                                            dDistance_line = dDistance_line+ aFlow_dis[iRow-1, iColumn-1]
                                        else:
                                            print(iDownslope)
                                            pass
            pass
        
        #save 
        aTravel_distance.append(dDistance_line)
print(aDistance_niws)
print(aTravel_distance)

sFilename_out = sPath_parent + '/' + 'data/travel_distance' + '/' + 'drt_travel_distance.csv'
print(sFilename_out)
with open(sFilename_out, 'w') as f:
    for i in range(nPoint):
        sLine = "{:0f}".format(aDistance_niws[i]) + ',' + "{:0f}".format(aTravel_distance[i])  + '\n'
        f.write(sLine)

print('finished')