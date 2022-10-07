import sys, os, stat
import numpy as np
from pathlib import Path
import json
from os.path import realpath

from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.visual.color.create_diverge_rgb_color_hex import create_diverge_rgb_color_hex

from pyearth.visual.barplot.barplot_data_with_reference import barplot_data_with_reference
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file

sRegion = 'Susquehanna'

aResolution = ['5km', '40km']
nResolution =len(aResolution)

# getting the data
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


dDrainge_wbd = 71186264342.763/1.0E6

aData = np.full( (2,2,4),0.0, dtype=float )
aData_ref= [dDrainge_wbd]
aData_raw=list()
for iCase_index in range(1, nCase +1):
    
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
        sFilename_txt = os.path.join(sWorkspace_watershed ,   'watershed.txt')
        a = text_reader_string(sFilename_txt,cDelimiter_in=':')
        b= float(a[0,1]) /1.0E6
        aData_raw.append(b)
    pass

aData[0,0,:] = [aData_raw[0], aData_raw[4], aData_raw[8],aData_raw[12]]
aData[0,1,:] = [aData_raw[1], aData_raw[5], aData_raw[9],aData_raw[13]]
aData[1,0,:] = [aData_raw[2], aData_raw[6], aData_raw[10],aData_raw[12]]
aData[1,1,:] = [aData_raw[3], aData_raw[7], aData_raw[11],aData_raw[13]]
iFlag_outlet =1


y_label = r'Drainage area (km2)'
sTitle = r'Susquehanna river basin'
sFilename_out= sPath_parent + '/' + 'figures' + '/' + 'drainage_area_comp.png'



iSize_x = 12
iSize_y =  9
iDPI = 150
nData= 6
aColor= np.array(create_diverge_rgb_color_hex( 5 ))

sWorkspace_output = '/compyfs/liao313/04model/pyflowline/susquehanna/'

aLinestyle = np.array([  'dotted'  , 'solid', 'dashdot','dotted'])
aMarker=  np.array([  '+',  '^'  , 'o', 'p'  ])

aLabel_legend= np.array(['Latlon','Square','Hexagon','MPAS'])



sFormat_x = ''

sFormat_y = '%.1E'


aLabel_legend_reference =['WBD']
aLabel_z = ['Without topology', 'With topology']
aHatch = np.array([ '-',   '*'])

aReference_in= [0]
barplot_data_with_reference(aData, \
             aResolution, \
             aLabel_legend,\
             sFilename_out,\
                aLabel_z_in = aLabel_z,\
                 aData_reference_in = aData_ref,\
                    aLabel_legend_reference_in = aLabel_legend_reference,\
                        iFlag_scientific_notation_in =1,\
             dMax_y_in = np.max(aData)* 1.2,\
             dMin_y_in = 0.0,\
             sFormat_y_in = sFormat_y,
             sLabel_y_in= y_label,\
             ncolumn_in= 3,\
                 aLinestyle_in = aLinestyle,\
             aColor_in= aColor,\
                 aMarker_in = aMarker,\
             aHatch_in = aHatch,\
             sTitle_in = sTitle)

print('finished')
