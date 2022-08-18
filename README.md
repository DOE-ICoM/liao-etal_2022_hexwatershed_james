[![DOI](https://zenodo.org/badge/523138410.svg)](https://zenodo.org/badge/latestdoi/523138410)

# Liao. et al. 2022. Journal of Advances in Modeling Earth Systems

**Topological relationships-based flow direction modeling: stream burning and depression filling**

Chang Liao<sup>1\*</sup>, 
Donghui Xu<sup>1</sup>,
Tian Zhou<sup>1</sup>,
Matt Cooper<sup>1</sup>,
Darren Engwirda<sup>2</sup>, 
Hong-Yi Li<sup>3</sup>,
and L. Ruby Leung<sup>1</sup>

<sup>1 </sup> Atmospheric Sciences and Global Change, Pacific Northwest National Laboratory, Richland, WA, USA

<sup>2 </sup> T-3 Fluid Dynamics and Solid Mechanics Group, Los Alamos National Laboratory, Los Alamos, NM, USA

<sup>3 </sup> University of Houston, Houston, TX, USA

\* corresponding author:  chang.liao@pnnl.gov

## Abstract


## Journal reference

Liao. et al. (2022). Topological relationships-based flow direction modeling: stream burning and depression filling

## Code reference

References for each minted software release for all code involved.  

Darren Engwirda: Generalised primal-dual grids for unstructured co-volume schemes, J. Comp. Phys., 375, pp. 155-176, https://doi.org/10.1016/j.jcp.2018.07.025, 2018.

Liao. C. (2022). HexWatershed: a mesh independent flow direction model for hydrologic models (0.1.1). Zenodo. https://doi.org/10.5281/zenodo.6425881

## Data reference

### Input data
Reference for each minted data source for your input data.  For example:

| Data | Source| Download website | Usage |
|-------|---------|-----------------|-----|
| River flowline | USGS National Hydrography Dataset | [USGS national map](https://apps.nationalmap.gov/viewer/) | Raw river flowline | 
| Coastal line | USGS | [USGS national map](https://apps.nationalmap.gov/viewer/) | Coastal for the MPAS mesh | 

### Output data
Reference for each minted data source for your output data.  For example:
| Data | Format| Content | Usage |
|-------|---------|-----------------|-----|
| Mesh | GeoJSON | The mesh file | Hydrology model | 
| Conceptual river flowline | GeoJSON | The modeled river flowline | Hydrology model | 


## Contributing modeling software

| Model | Version | Repository Link | DOI |
|-------|---------|-----------------|-----|
| HexWatershed | version | https://doi.org/10.5281/zenodo.6425881 | 10.5281/zenodo.6425881 |


## Reproduce my experiment

You need to follow two major steps to reproduce this study: 


1. Run the [Mesh generation workflow](https://github.com/DOE-ICoM/liao-etal_2022_hexwatershed_james/blob/main/workflow/mesh_generation.md)
2. Run the [HexWatershed](https://github.com/DOE-ICoM/liao-etal_2022_hexwatershed_james/blob/main/workflow/hexwatershed.md)


## Reproduce my figures

You are recommended to generate the plot using QGIS for all GeoJSON files.

