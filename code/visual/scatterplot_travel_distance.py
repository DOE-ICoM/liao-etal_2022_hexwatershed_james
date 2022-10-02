import os, sys, stat
from pathlib import Path
from os.path import realpath
import json
import numpy as np
from osgeo import  osr, gdal, ogr
import matplotlib as mpl
from pyearth.visual.scatter.scatter_plot_data import scatter_plot_data
from pyearth.visual.scatter.scatter_plot_multiple_data import scatter_plot_multiple_data

from pyearth.visual.color.create_diverge_rgb_color_hex import create_diverge_rgb_color_hex
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file
from pyflowline.formats.read_flowline import read_flowline_geojson
from shapely.wkt import loads
from shapely.geometry import Point, Polygon
sPath_parent = str(Path(__file__).parents[2]) # data is located two dir's up
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

aPolygon=list()
aDistance=list()

for iCase_index in range(1, nCase+1):
    aDistance_case=list()
    aPolygon_case=list()
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
    for iWatershed in range(1, 2):#there is only one watershed in this study
        sFilename_mesh=   oPyhexwatershed.pPyFlowline.sFilename_mesh
        sWatershed = "{:04d}".format(iWatershed) 
        sWorkspace_watershed = sWorkspace_watershed =  os.path.join( sWorkspace_output_hexwatershed,  sWatershed )
        sFilename_json = os.path.join(sWorkspace_output_hexwatershed ,   'travel_distance.geojson')
        pDriver = ogr.GetDriverByName('GeoJSON')
        pDataset = pDriver.Open(sFilename_json, gdal.GA_ReadOnly)
        pLayer = pDataset.GetLayer(0)

        pSrs = osr.SpatialReference()  
        pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon
        

        for pFeature in pLayer:
            pGeometry_in = pFeature.GetGeometryRef()
            sGeometry_type = pGeometry_in.GetGeometryName()
            lID =0 
            if sGeometry_type =='POLYGON':
                dummy0 = loads( pGeometry_in.ExportToWkt() )
                #if iCase_index ==1:
                aPolygon_case.append(dummy0)
                dTravel = pFeature.GetField("dist")
                aDistance_case.append(dTravel)
                
        
    aDistance.append(aDistance_case)          
    aPolygon.append(aPolygon_case)  
    


#read geojson

sFilename_site = sPath_parent + '/' + 'data/travel_distance' + '/' + 'site_location.geojson'
pDriver = ogr.GetDriverByName('GeoJSON')
pDataset = pDriver.Open(sFilename_site, gdal.GA_ReadOnly)
pLayer = pDataset.GetLayer(0)
pSrs = osr.SpatialReference()  
pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

nPoint = pLayer.GetFeatureCount()
#aPoint=list()

aDistance_niws =list()
aData_x=list()
aData_y  =list()
aLabel_legend =list()
#for pFeature in pLayer:
#https://autogis-site.readthedocs.io/en/latest/notebooks/L3/02_point-in-polygon.html
for iCase_index in range(1, nCase+1):
    aLabel_legend.append(   'Case ' +  "{:0d}".format(iCase_index)   )
    aIndex0_case=list() #in domain
    aIndex_case=list() #in poly
    aPolygon_case = aPolygon[iCase_index-1]
    nPolygon = len(aPolygon_case)
    for i in range(nPoint):
        pFeature= pLayer.GetFeature(i)

        pGeometry_in = pFeature.GetGeometryRef()
        sGeometry_type = pGeometry_in.GetGeometryName()
        lID =0 
        dDistance_line=0.0
        if sGeometry_type =='POINT':

            #get site name
            if iCase_index ==1:
                dummy0 = loads( pGeometry_in.ExportToWkt() )
                site_id = pFeature.GetField("identifier")
                sFilename_geojson_in = sPath_parent + '/' + 'data/travel_distance' + '/downstreammain' + site_id+ '.geojson'
                aLine,pSpatial_reference  = read_flowline_geojson(sFilename_geojson_in)
                for pLine in aLine:
                    dLength = pLine.dLength
                    dDistance_line = dDistance_line + dLength

                aDistance_niws.append(dDistance_line)
            else:
                dummy0 = loads( pGeometry_in.ExportToWkt() )
            #aPoint.append(dummy0)
            for j in range(nPolygon):
                poly = aPolygon_case[j]
                if dummy0.within(poly):
                    aIndex0_case.append(i)
                    aIndex_case.append(j)
                    

                    break


            pass
    #check now

    aIndex=np.array(aIndex_case)
    aIndex0=np.array(aIndex0_case)
    aDistance_dummy = np.array(aDistance[ iCase_index-1 ])
    aDistance_niws=np.array(aDistance_niws)

    aDistance_obs = aDistance_niws[aIndex0]
    aDistance_site= aDistance_dummy[aIndex]

    aData_x.append(aDistance_obs)
    aData_y.append(aDistance_site)

sFilename_out = sPath_parent + '/' + 'figures' + '/' + 'scatterplot_travel_distance_multiple.png'

#scatter_plot_data(aData_x, \
#                      aData_y,\
#                      sFilename_out, \
#                      iFlag_scientific_notation_x_in=1,\
#                      iFlag_scientific_notation_y_in=1,\
#                      iSize_x_in = None, \
#                      iSize_y_in = None,  \
#                      iDPI_in = None ,\
#                      iFlag_log_x_in = None,\
#                      iFlag_log_y_in = None,\
#                      dMin_x_in = 0, \
#                      dMax_x_in = np.max(aDistance_niws), \
#                      dMin_y_in = 0, \
#                      dMax_y_in = np.max(aDistance_niws), \
#                      dSpace_x_in = None, \
#                      dSpace_y_in = None, \
#                      sFormat_x_in =None,\
#                      sFormat_y_in =None,\
#                      sLabel_x_in ='USGS Gage (Observed)',\
#                      sLabel_y_in = 'HexWatershed (Modeled)' , \
#                      sLabel_legend_in = 'Susquehanna river basin',\
#                      sTitle_in = 'Travel distance')

aColor = np.full(14, None, dtype=object)
aMarker= np.full(14, None, dtype=object)
aSize = np.full(14, None, dtype=object)

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
    else:
        aSize[i] = mpl.rcParams['lines.markersize'] ** 2 



scatter_plot_multiple_data(aData_x, \
                      aData_y,\
                      sFilename_out, \
                      iFlag_miniplot_in = 1,\
                      iFlag_scientific_notation_x_in=1,\
                      iFlag_scientific_notation_y_in=1,\
                      iSize_x_in = None, \
                      iSize_y_in = None,  \
                      iDPI_in = None ,\
                      iFlag_log_x_in = None,\
                      iFlag_log_y_in = None,\
                      dMin_x_in = 0, \
                      dMax_x_in = np.max(aDistance_niws), \
                      dMin_y_in = 0, \
                      dMax_y_in = np.max(aDistance_niws), \
                      dSpace_x_in = None, \
                      dSpace_y_in = None, \
                      sFormat_x_in =None,\
                      sFormat_y_in =None,\
                      sLabel_x_in ='USGS Gage (Observed, m)',\
                      sLabel_y_in = 'HexWatershed (Modeled, m)' , \
                         aColor_in=aColor,\
                        aMarker_in=aMarker,\
                            aSize_in = aSize,\
                      aLabel_legend_in = aLabel_legend,\
                      sTitle_in = 'Travel distance')

print('finished')