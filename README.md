_your zenodo badge here_

# ferencz-tidwell_2022_frontiers

**Physical controls on irrigation return flow contributions to stream flow in irrigated alluvial valleys**

Stephen B. Ferencz<sup>1\*</sup> and Vince C. Tidwell<sup>1</sup>

<sup>1 </sup> Sandia National Laboratories, Albuquerque, New Mexico, USA

\* corresponding author:  sbferen @ sandia.gov

## Abstract
Irrigation can be a significant source of groundwater recharge in many agricultural regions, particularly in arid and semi-arid climates. Once infiltrated, irrigation recharge can travel via subsurface flowpaths that return to the river system in a lagged manner, supplementing natural streamflow weeks, months, or even years from when the irrigation was applied. In regions that experience low flows during summer and early fall, return flows can be a significant source of supplementary stream flow. Many water planning and operations models either ignore return flows or roughly approximate them with analytical solutions. Thus, return flows represent an important but often overlooked component of the hydrological exchange and overall water balance in agricultural regions. This study uses groundwater models to explore a wide range of factors that control irrigation return flow timing in irrigated alluvial valleys. Through a sensitivity analysis, we assess how factors such as the extent of irrigated land adjacent to a stream, irrigation recharge rate, aquifer hydraulic conductivity, aquifer thickness, water table configuration, and seasonal fluctuations in stream stage control the timing of subsurface return flows. Modeling is conducted using MODFLOW models representing an irrigated alluvial valley adjacent to a stream. While a simplification of the full complexity in real systems, the models are a significant advancement from the analytical solution and provide new insight into the timescales of return flows over a broad range of possible conditions. To contextualize our results, we compare our modeling results to an analytical solution used for approximating return flows and evaluate its performance. Our findings show what factors and conditions influence return flow timing and control whether they contribute to stream flows over short term (months) or longer term (seasonal) time scales.

## Journal reference
Ferencz, S.B, Tidwell, V.C (2022). Physical controls on irrigation subsurface return flow contributions to stream flow in irrigated alluvial valleys. Frontiers in Water. 10.3389/frwa.2022.828099 

## Code reference

 - `Analytical_return_flow_generator.py` in the `workflows` directory of this repository

## Data reference

### Input data

- Model input data (MODFLOW files and FloPy parameters) for each simulation Group are in Model_Files.zip
- Recharge data from USGS
    - From https://www.sciencebase.gov/catalog/item/58ee3dc7e4b0eed1ab8cf13d we use the 800m_4km_10pc_runoff_monthly_SUMS_m3 model output data
- Irrigation: StateMod
    - From page:  https://cdss.colorado.gov/modeling-data/surface-water-statemod need to download Upper Colorado
- River hydrograph from USGS
    - Retrieved from https://waterdata.usgs.gov/co/nwis/current/?type=dailystagedischarge&group_key=huc_cd on Sept 14, 2021 by author

### Output data
- Output data for each simulation Group is in the Model_Files.zip 

## Contributing modeling software
| Model | Version | Repository Link | DOI |
|-------|---------|-----------------|-----|
| MODFLOW | 6.2.0 | https://www.usgs.gov/software/modflow-6-usgs-modular-hydrologic-model | https://doi.org/10.5066/F76Q1VQV |
| ModelMuse | 4.3 | https://pubs.er.usgs.gov/publication/sir20195036 | https://doi.org/10.3133/sir20195036 |
| Flopy  | 3.3.4 | https://github.com/modflowpy/flopy | https://github.com/modflowpy/flopy/tree/3.3.4 |

## Reproduce my experiment

1. Download inputs noted in Boundary_conditions.zip
2. Run Flopy scripts 'Group_X_flopy_modeling.py' for Scenario Groups 1, 2, and 3. 
3. Use plotting scripts to plot outputs. 

## Reproduce my figures
Use the .py scripts 'Group_X_plotting.py' to generate figures for Scenario Groups 1, 2, and 3. These
scripts use model outputs provided in Model_Files.zip.
