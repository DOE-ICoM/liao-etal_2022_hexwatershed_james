[![DOI](https://zenodo.org/badge/523138410.svg)](https://zenodo.org/badge/latestdoi/523138410)

# Liao. et al. 2022. Journal of Advances in Modeling Earth Systems

**Topological relationships-based flow direction modeling: mesh-independent river networks representation**

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

River networks are important features in surface hydrology. However, accurately representing river networks in spatially distributed hydrologic and Earth system models is often sensitive to the model's spatial resolution. Specifically, river networks are often misrepresented because of the mismatch between the model's spatial resolution and river networks details, resulting in significant uncertainty in projected flow direction. In this study, we developed a topological relationships-based river network representation method for spatially distributed hydrologic models. This novel method uses (1) graph theory algorithms to simplify real-world vector-based river networks and assist in mesh generation; and (2) a topological relationship-based method to reconstruct conceptual river networks. The main advantages of our method are that (1) it combines the strengths of vector-based and DEM raster-based river network extraction methods; and (2) it is mesh-independent and can be applied to both structured and unstructured meshes. This method paves a path for advanced terrain analysis and hydrologic modeling across different scales. 

## Journal reference

Liao. et al. (2022). Topological relationships-based flow direction modeling: river networks representation

## Code reference

References for each minted software release for all code involved.  

Darren Engwirda: Generalised primal-dual grids for unstructured co-volume schemes, J. Comp. Phys., 375, pp. 155-176, https://doi.org/10.1016/j.jcp.2018.07.025, 2018.

Liao, Chang, & Cooper, Matt. (2022). Pyflowline: a mesh-independent river networks generator for hydrologic models (0.1.22). Zenodo. https://doi.org/10.5281/zenodo.6604337

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
| PyFlowline | version | https://doi.org/10.5281/zenodo.6604337 | link to DOI dataset |


## Reproduce my experiment

You need to follow two major steps to reproduce this study: 

1. (Optional, only needed for the `MPAS` mesh) Run the [JIGSAW tool](https://github.com/DOE-ICoM/pyflowline_james/blob/main/workflow/jigsaw.md)
2. Run the [PyFlowline tool](https://github.com/DOE-ICoM/pyflowline_james/blob/main/workflow/pyflowline.md)


## Reproduce my figures

You are recommended to generate the plot using QGIS for all GeoJSON files.

