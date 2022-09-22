import sys, os, stat
import numpy as np
from pathlib import Path


from pyearth.visual.color.create_diverge_rgb_color_hex import create_diverge_rgb_color_hex

from pyearth.visual.barplot.barplot_data_with_reference import barplot_data_with_reference

sRegion = 'Susquehanna'

aResolution = ['50km', '10km', '5km']
nResolution =len(aResolution)

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
dDrainge_wbd = 
aData.append(dDrainge_wbd)
for iCase_index in range(1, nCase +1):
    pass

iFlag_outlet =1


y_label = r'Are of difference (km2)'
sTitle = r'Susquehanna river basin'
sFilename_out= '/people/liao313/data/hexwatershed/susquehanna/area_of_diff_compare.png'



iSize_x = 12
iSize_y =  9
iDPI = 150
nData= 6
aColor= np.array(create_diverge_rgb_color_hex( 8 ))

sWorkspace_output = '/compyfs/liao313/04model/pyflowline/susquehanna/'

aLinestyle = np.array([  'dotted',  'dotted'  , 'solid', 'solid', 'dotted','dotted' 'dashdot','dashdot'])
aMarker=  np.array([  '+',  '^'  , 'o', 'p', 'd', '*', '+',  '^'  ])

aLabel_legend= np.array(['WBD','Latlon','Square','Hexagon','MPAS'])
aHatch = np.array([ '.',   '*', '+', '|', '-', 'o',  '.',   '*',])
aSubset_index = np.arange(4) + 1

sFormat_x = ''

sFormat_y = '%.1f'



aReference_in= [0]
barplot_data_with_reference(aData, \
             aResolution, \
             aLabel_legend[aSubset_index],\
             sFilename_out,\
                 aReference_in,\
             dMax_y_in = 7000,\
             dMin_y_in = 0.0,\
             sFormat_y_in = sFormat_y,
             sLabel_y_in= y_label,\
             ncolumn_in= 2,\
                 aLinestyle_in = aLinestyle[aSubset_index],\
             aColor_in= aColor[aSubset_index],\
                 aMarker_in = aMarker[aSubset_index],\
             aHatch_in = aHatch[aSubset_index],\
             sTitle_in = sTitle)

print('finished')
