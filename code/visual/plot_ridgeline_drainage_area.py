
import os, sys, stat
from pathlib import Path
from os.path import realpath
import json
import numpy as np
from pyearth.visual.ridgeplot.ridgeplot_data_density import ridgeplot_data_density
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file



# getting the data
sPath_parent = str(Path(__file__).parents[1]) # data is located two dir's up
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

aData = list()
dMax_x=0.0
for iCase_index in range(1, nCase +1):
    aData_case=list()
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
                iSegment = int(pcell['iSegment'])
                dDrainagearea=float(pcell['DrainageArea'])  
                
                aData_case.append(dDrainagearea)
                if dDrainagearea > dMax_x:
                    dMax_x = dDrainagearea
                
    
    aData.append(aData_case)
sFilename_out = sPath_parent + '/' + 'figures' + '/' + 'drainage_area.png'
sLabel_x = r'Drainage area ($m^{2}$)'
ridgeplot_data_density(case_dict, aData, sFilename_out, dMin_x_in =0, dMax_x_in= 0.5*dMax_x,sLabel_x_in =sLabel_x)
pass

