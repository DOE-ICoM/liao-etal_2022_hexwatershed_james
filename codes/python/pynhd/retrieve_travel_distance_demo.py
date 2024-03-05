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
#station_id = "01031500"
#
#basin = nldi.get_basins(station_id)
#flw_main = nldi.navigate_byid(
#    fsource="nwissite",
#    fid=f"USGS-{station_id}",
#    navigation="upstreamMain",
#    source="flowlines",
#    distance=1000,
#)
#
#flw_trib = nldi.navigate_byid(
#    fsource="nwissite",
#    fid=f"USGS-{station_id}",
#    navigation="upstreamTributaries",
#    source="flowlines",
#    distance=1000,
#)
#
#st_all = nldi.navigate_byid(
#    fsource="nwissite",
#    fid=f"USGS-{station_id}",
#    navigation="upstreamTributaries",
#    source="nwissite",
#    distance=1000,
#)
#
#st_d20 = nldi.navigate_byid(
#    fsource="nwissite",
#    fid=f"USGS-{station_id}",
#    navigation="upstreamTributaries",
#    source="nwissite",
#    distance=20,
#)

station_id = '01567500'
basin = nldi.get_basins(station_id)

site = nldi.getfeature_byid(
    fsource="nwissite",
    fid=f"USGS-{station_id}")
   

pp = nldi.navigate_byid(
    fsource="nwissite",
    fid=f"USGS-{station_id}",
    navigation="downstreamMain",
    source="huc12pp",
    distance=1000,
)
st_d20 = nldi.navigate_byid(
    fsource="nwissite",
    fid=f"USGS-{station_id}",
    navigation="upstreamTributaries",
    source="nwissite",
    distance=1,
)
flw_main = nldi.navigate_byid(
    fsource="nwissite",
    fid=f"USGS-{station_id}",
    navigation="downstreamMain",
    source="flowlines",
    distance=1000,
)
ax = basin.plot(facecolor="none", edgecolor="k", figsize=(8, 8))
site.plot(ax=ax, label="USGS site", marker="o", markersize=50, color="k", zorder=3)
#pp.plot(ax=ax, label="USGS site", marker="o", markersize=50, color="k", zorder=3)
st_d20.plot(
    ax=ax,
    label="USGS stations up to 1 km",
    marker="v",
    markersize=100,
    zorder=5,
    color="darkorange",
)
#flw_main.plot(ax=ax, lw=3, color="r", zorder=2, label="Main")
sFilename_out = sPath_parent + '/' + 'data' + '/' + 'travel_distance.geojson'
flw_main.to_file(sFilename_out, driver="GeoJSON")

dDistance = 0.0
dLength=0.0
nflowline = len(flw_main)


pJson = flw_main.geometry.to_wkt()
for i in range(nflowline):      
    dummy = loads( pJson[i]     )
    aCoords = dummy.coords 
    dummy1= np.array(aCoords)
    pLine = convert_gcs_coordinates_to_flowline(dummy1)
    dLength = pLine.dLength
    dDistance = dDistance + dLength

ax.legend(loc="best")
ax.set_aspect("auto")
ax.figure.set_dpi(100)
sFilename_out = sPath_parent + '/' + 'figures' + '/' + 'travel_distance.png'
ax.figure.savefig(sFilename_out, bbox_inches="tight", facecolor="w")