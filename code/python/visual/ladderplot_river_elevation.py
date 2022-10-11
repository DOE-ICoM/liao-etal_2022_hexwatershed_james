import os, sys, stat
from pathlib import Path
from os.path import realpath
import json

import numpy as np
from osgeo import  osr, gdal, ogr
from shapely.wkt import loads
import matplotlib.pyplot as plt
from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file
import matplotlib as mpl

from pyearth.visual.ladder.ladder_plot_xy_data import ladder_plot_xy_data
from pyearth.visual.color.create_diverge_rgb_color_hex import create_diverge_rgb_color_hex
# getting the data
sPath_parent = str(Path(__file__).parents[3]) # data is located two dir's up
print(sPath_parent)
sPath_data = realpath( sPath_parent +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sPath_data)  /  'input')
sWorkspace_output = '/compyfs/liao313/04model/pyhexwatershed/susquehanna'
nCase  = 14
sDate='20220901'

# we define a dictionnary with months that we'll use later
case_dict = dict()

for i in range(1, nCase +1):
    case_dict[i] = 'Case ' +  "{:0d}".format(i) 

print(case_dict)

#the longest river channel on main

sFilename_site = sPath_parent + '/' + 'data/travel_distance' + '/' + 'site_location.geojson'
pDriver = ogr.GetDriverByName('GeoJSON')
pDataset_site = pDriver.Open(sFilename_site, gdal.GA_ReadOnly)
pLayer_site = pDataset_site.GetLayer(0)
pSrs = osr.SpatialReference()  
pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

nPoint = pLayer_site.GetFeatureCount()
for i in range(nPoint):
    pFeature= pLayer_site.GetFeature(i)
    pGeometry_in = pFeature.GetGeometryRef()
    sGeometry_type = pGeometry_in.GetGeometryName()
    lID =0 
    dDistance_line=0.0
    if sGeometry_type =='POINT':
        site_id = pFeature.GetField("identifier")
        if site_id == "USGS-01497842":
            headwater = loads( pGeometry_in.ExportToWkt() )
            break
#aData = list()
#aPolygon=list()
#aDistance=list()
aX_all=list()
aY_all=list()
aLabel_legend=list()

for iCase_index in range(1, nCase +1):
    aLabel_legend.append(   'Case ' +  "{:0d}".format(iCase_index)   )
    aElevation_case=list()
    aPolygon_case=list()
    aDistance_case=list()
    aCellID_case=list()
    aCellID_downslope_case=list()
    #read data
    sFilename_configuration_in = realpath( sPath_parent +  '/examples/susquehanna/pyhexwatershed_susquehanna_square.json' )
    if os.path.isfile(sFilename_configuration_in):
        pass
    else:
        print('This configuration does not exist: ', sFilename_configuration_in )
    oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
      iCase_index_in=iCase_index,\
          sDate_in= sDate)  
    sWorkspace_output_hexwatershed = oPyhexwatershed.sWorkspace_output_hexwatershed

    aPolygon_case_cellid=list()
    for iWatershed in range(1, 2):#there is only one watershed in this study
        Basin=   oPyhexwatershed.pPyFlowline.aBasin[iWatershed-1]
        sWatershed = "{:04d}".format(iWatershed) 
        sWorkspace_watershed = sWorkspace_watershed =  os.path.join( sWorkspace_output_hexwatershed,  sWatershed )
        sFilename_json = os.path.join(sWorkspace_watershed ,   'watershed.json')
        with open(sFilename_json) as json_file:
            data = json.load(json_file)  
            ncell = len(data)
            lID =0 
            for i in range(ncell):
                pcell = data[i]
                lCellID = int(pcell['lCellID'])
                lCellID_downslope = int(pcell['lCellID_downslope'])
                iSegment = int(pcell['iSegment'])
                dElevation=float(pcell['Elevation'])  
                dDistance=float(pcell['dDistance_to_watershed_outlet'])   
                aCellID_case.append(lCellID)
                aCellID_downslope_case.append(lCellID_downslope)
                aElevation_case.append(dElevation)
                aDistance_case.append(dDistance)

        s = np.array(aCellID_case)
        sort_index = np.argsort(s)
        aCellID_case = list(np.array(aCellID_case)[sort_index])
        aCellID_downslope_case = list(np.array(aCellID_downslope_case)[sort_index])
        aElevation_case = list(np.array(aElevation_case)[sort_index])
        aDistance_case = list(np.array(aDistance_case)[sort_index])
                
        
        sWorkspace_watershed = sWorkspace_watershed =  os.path.join( sWorkspace_output_hexwatershed,  sWatershed )
        sFilename_json = os.path.join(sWorkspace_watershed ,   'travel_distance.geojson')
        pDriver = ogr.GetDriverByName('GeoJSON')
        pDataset = pDriver.Open(sFilename_json, gdal.GA_ReadOnly)
        pLayer = pDataset.GetLayer(0)

        pSrs = osr.SpatialReference()  
        pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon
        

        for pFeature in pLayer:
            pGeometry_in = pFeature.GetGeometryRef()
            sGeometry_type = pGeometry_in.GetGeometryName()
            dummyid= pFeature.GetField("id")
            lID =0 
            if sGeometry_type =='POLYGON':
                dummy0 = loads( pGeometry_in.ExportToWkt() )
                #if iCase_index ==1:
                aPolygon_case.append(dummy0)
                aPolygon_case_cellid.append(dummyid)
                #dTravel = pFeature.GetField("dist")
                #aDistance_case.append(dTravel)
                
                
        
            
    #re-order 
    s = np.array(aPolygon_case_cellid)
    sort_index = np.argsort(s)
    aPolygon_case = list(np.array(aPolygon_case)[sort_index])


    nPolygon = len(aPolygon_case)
    #read nwis info
    
    

    aElevation_main = list()
    aDistance_main =list()
    for j in range(nPolygon):
        poly = aPolygon_case[j]
        if headwater.within(poly):
            #find the cell that is the head
            lCellID = aCellID_case[j]
            dElevation = aElevation_case[j]
            aElevation_main.append(dElevation)
            lCellID_downslope=  aCellID_downslope_case[j]
            aDistance_main.append(aDistance_case[j])
            break
            

    #now get all the elevations
    dummyID = np.array(aCellID_case)
    dummyID_downslope = np.array(aCellID_downslope_case)
    iFlag_found=0
    while lCellID_downslope !=-1:
        
        index0 = np.where(dummyID ==lCellID_downslope )
        index= np.ravel(index0)[0]
        dElevation = aElevation_case[index]
        dDistance = aDistance_case[index]
        aElevation_main.append(dElevation)
        aDistance_main.append(dDistance)
        lCellID_downslope = aCellID_downslope_case[index]
        iFlag_found =1
        pass


    #x is distance
    #y is elevation
    #need reverse
    if iFlag_found ==1:   
        aDistance_main.reverse()
        aX_all.append(aDistance_main)
        aElevation_main.reverse()
        aY_all.append(aElevation_main)
    else:
        print(iCase_index, lCellID)
        #pass

#read obs
#data/elevation_ladder/Channel_dem_travel_distrance.csv
sFilename_obs = sPath_parent + '/' + 'data/elevation_ladder/Channel_dem_travel_distrance.csv'
a = text_reader_string(sFilename_obs,cDelimiter_in=',')
aX_obs= a[:,0].astype(float)
aY_obs= a[:,1].astype(float)

aX_obs = np.reshape(aX_obs, len(aX_obs))
aY_obs = np.reshape(aY_obs, len(aY_obs))


sFilename_out = sPath_parent + '/' + 'figures' + '/' + 'river_ladder.png'
sLabel_x = 'Travel distance from outlet (m)'
sLabel_y = 'Channel elevation (m)'

aColor = np.full(15, None, dtype=object)
aMarker= np.full(15, None, dtype=object)
aSize = np.full(15, None, dtype=object)
aLinestyle = np.full(15, None, dtype=object)
aLinewidth = np.full(15, None, dtype=object)

nmesh=4
aColor0= create_diverge_rgb_color_hex(nmesh)
aMarker0 = [ '.','o','+','x']
for i in range(nCase):
    k= int(np.floor(i/nmesh))
    aColor[i] = aColor0[k]

    j = np.mod(i,nmesh)
    aMarker[i]=aMarker0[j]

    if j < 2:
        aSize[i] = mpl.rcParams['lines.markersize'] ** 2 * 2        
        
        aLinestyle[i] = '-'
    else:
        aSize[i] = mpl.rcParams['lines.markersize'] ** 2 
        
        aLinestyle[i] = 'dotted'

    l = np.mod(i,2)
    if l < 1:
            
        aLinewidth[i] = mpl.rcParams['lines.linewidth'] * 0.5
        
    else:
        
        aLinewidth[i] =mpl.rcParams['lines.linewidth'] * 1
        

aX_all.append(aX_obs)
aY_all.append(aY_obs)
aColor[14] = '#000000'
aMarker[14]= '.'
aSize[14] = mpl.rcParams['lines.markersize'] 
aLinestyle[14] = '-'
aLinewidth[14] = mpl.rcParams['lines.linewidth'] 

aLabel_legend.append('NHD')

sFormat_x =  '%.1E'
ladder_plot_xy_data(aX_all,  aY_all,  \
        sFilename_out,iDPI_in = None, aFlag_trend_in = None,  \
            iReverse_y_in = None,  iSize_x_in = None,  \
                    iFlag_scientific_notation_x_in=1,\
                     # iFlag_scientific_notation_y_in=1,\
                iSize_y_in = None,  ncolumn_in = None,  \
                    dMax_x_in = None,  dMin_x_in = 0,  \
                    dMax_y_in =600, dMin_y_in = None,  \
                        dSpace_y_in = None,  \
                            aColor_in = aColor, aLinestyle_in = aLinestyle,  aLinewidth_in= aLinewidth,\
                                aLabel_point_in = None,  \
                                    aTick_label_x_in = None,  \
                                    aLocation_legend_in = [1.0,0.0], \
                                        sLabel_x_in = sLabel_x, \
                                        sLabel_y_in = sLabel_y,  \
                                            aLabel_legend_in = aLabel_legend, \
        sLocation_legend_in='lower right', sFormat_x_in = sFormat_x, sFormat_y_in =None, 
        sTitle_in = None)



pass

