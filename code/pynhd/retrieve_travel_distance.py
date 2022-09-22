from multiprocessing.connection import deliver_challenge
import os, sys, stat
from pathlib import Path
from os.path import realpath
import json
import numpy as np
from shapely.wkt import loads
from pyflowline.formats.convert_coordinates import convert_gcs_coordinates_to_flowline

from pynhd import NLDI, WaterData, NHDPlusHR
import pynhd as nhd
nldi = NLDI()
sPath_parent = str(Path(__file__).parents[2]) # data is located two dir's up
print(sPath_parent)
sPath_data = realpath( sPath_parent +  '/data/susquehanna' )



#get basin
station_id = '01580570'
basin = nldi.get_basins(station_id)

#get site
site = nldi.getfeature_byid(
    fsource="nwissite",
    fid=f"USGS-{station_id}")
   
#get upstream site

uppoint = nldi.navigate_byid(
    fsource="nwissite",
    fid=f"USGS-{station_id}",
    navigation="upstreamMain",
    source="nwissite",
    distance=1000,
)
#loop all upstream site

sFilename_out = sPath_parent + '/' + 'data/travel_distance' + '/' + 'site_location.geojson'
uppoint.to_file(sFilename_out, driver="GeoJSON")

npoint = len(uppoint)

#for i in range(npoint):
for index,row in uppoint.iterrows(): # Looping over all points
    
    station_id= row.identifier
    flw_main = nldi.navigate_byid(
        fsource="nwissite",
        fid=station_id,
        navigation="downstreamMain",
        source="flowlines",
        distance=1000)

    sFilename_out = sPath_parent + '/' + 'data/travel_distance' + '/' + 'downstreammain' + station_id + '.geojson'
    flw_main.to_file(sFilename_out, driver="GeoJSON")
    

print('finshed')
