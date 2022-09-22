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


station_id = '01580570'
basin = nldi.get_basins(station_id)

ax = basin.plot(facecolor="none", edgecolor="k", figsize=(8, 8))


dDistance = 0.0
dLength=0.0
dArea =0.0
sFilename_out = sPath_parent + '/' + 'data' + '/' + 'watershed_boundary.geojson'
basin.to_file(sFilename_out, driver="GeoJSON")


ax.legend(loc="best")
ax.set_aspect("auto")
ax.figure.set_dpi(100)
sFilename_out = sPath_parent + '/' + 'figures' + '/' + 'watershed_boundary.png'
ax.figure.savefig(sFilename_out, bbox_inches="tight", facecolor="w")