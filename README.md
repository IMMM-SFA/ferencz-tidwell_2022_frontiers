_your zenodo badge here_

# ferencz-tidwell_2022_frontiers

**Physical controls on irrigation return flow contributions to stream flow in irrigated alluvial valleys**

Stephen B. Ferencz<sup>1\*</sup> and Vince C. Tidwell<sup>1</sup>

<sup>1 </sup> Sandia National Laboratories, Albuquerque, New Mexico, USA

\* corresponding author:  sbferen @ sandia.gov

## Abstract
Irrigation can be a significant source of groundwater recharge in many agricultural regions, particularly in arid and semi-arid climates. Once infiltrated, irrigation recharge can travel via subsurface flowpaths that return to the river system in a lagged manner, supplementing natural streamflow weeks, months, or even years from when the irrigation was applied. In regions that experience low flows during summer and early fall, return flows can be a significant source of supplementary stream flow. Many water planning and operations models either ignore return flows or roughly approximate them with analytical solutions. Thus, return flows represent an important but often overlooked component of the hydrological exchange and overall water balance in agricultural regions. This study uses groundwater models to explore a wide range of factors that control irrigation return flow timing in irrigated alluvial valleys. Through a sensitivity analysis, we assess how factors such as the extent of irrigated land adjacent to a stream, irrigation recharge rate, aquifer hydraulic conductivity, aquifer thickness, water table configuration, and seasonal fluctuations in stream stage control the timing of subsurface return flows. Modeling is conducted using MODFLOW models representing an irrigated alluvial valley adjacent to a stream. While a simplification of the full complexity in real systems, the models are a significant advancement from the analytical solution and provide new insight into the timescales of return flows over a broad range of possible conditions. To contextualize our results, we compare our modeling results to an analytical solution used for approximating return flows and evaluate its performance. Our findings show what factors and conditions influence return flow timing and control whether they contribute to stream flows over short term (months) or longer term (seasonal) time scales.

## Journal reference
TBD

## Code reference

 - `Analytical_return_flow_generator.py` in the `workflows` directory of this repository
 - **TODO**:  modify above script to be generalized
 - **TODO**:  need scripts for transforming recharge, irrigation, and hydrographs  

## Data reference

### Input data

**TODO**:  Need compressed data from author for all categories

- Recharge data from USGS
    - asdf
- Irrigation: StateMod
    - From page:  https://cdss.colorado.gov/modeling-data/surface-water-statemod need to download Upper Colorado
- River hydrograph from USGS
    - Retrieved from https://waterdata.usgs.gov/co/nwis/current/?type=dailystagedischarge&group_key=huc_cd on Sept 14, 2021 by author

### Output data

- CSVs for 3 different simulations as a time series of boundary fluxes
- **TODO**:  Add descriptive headers, and output units


## Contributing modeling software
| Model | Version | Repository Link | DOI |
|-------|---------|-----------------|-----|
| MODFLOW | 6.2.0 | https://www.usgs.gov/software/modflow-6-usgs-modular-hydrologic-model | https://doi.org/10.5066/F76Q1VQV |
| ModelMuse | 4.3 | https://pubs.er.usgs.gov/publication/sir20195036 | https://doi.org/10.3133/sir20195036 |
| Flopy  | 3.3.4 | https://github.com/modflowpy/flopy | https://github.com/modflowpy/flopy/tree/3.3.4 |

## Reproduce my experiment
Fill in detailed info here or link to other documentation that is a thorough walkthrough of how to use what is in this repository to reproduce your experiment.

1. Download inputs noted in [Input data](#input-data)
2. Run script [**TODO**] to create boundary conditions recharge, irrigation, and hydrograph datasets
3. Run MODFLOW and Flopy **TODO**
4. Download and unzip the output data from my experiment [Output data](#output-data)

## Reproduce my figures
Use the scripts found in the `figures` directory to reproduce the figures used in this publication.

**TODO**:  get code to make figures

| Script Name | Description | How to Run |
| --- | --- | --- |
| `generate_figures.py` | Script to generate my figures | `python3 generate_figures.py -i /path/to/inputs -o /path/to/outuptdir` |
