## Import libraries 

import sys
import os
import platform
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import flopy

# Check versions
print(sys.version)
print('numpy version: {}'.format(np.__version__))
print('matplotlib version: {}'.format(mpl.__version__))
print('flopy version: {}'.format(flopy.__version__))

# Simulation paths
experiment_path = 'C:/Users/xxxxxxx/Documents/Model_Files' # absolute path to Model Files folder
os.chdir(experiment_path + '/Group_3') 
model_path = experiment_path + '/Group_3/MODFLOW_files'

model_name = ['Geom_1000m_rch1_irr1', 'Geom_1000m_rch1_irr2','Geom_1000m_rch1_irr3', \
              'Geom_1000m_rch2_irr1', 'Geom_1000m_rch2_irr2', 'Geom_1000m_rch2_irr3'] # number of models, outer loop of iterative simulation script 
params = pd.read_csv('Group_3_params.csv') # paramater settings file for group of simulations 
baseline_params = pd.read_csv('Group_3_params_baseline.csv')
reset_params = pd.read_csv('Group_3_reset.csv')
return_flow_results = np.zeros([144,12*365+1]) # set rows to number of param combinations, set columns to number of model time steps
baseline_results = np.zeros([48,12*365+1])
combinations = 24 # number of parameter combinations for each model

## Return flow simulations for Group 3 (irrigation recharge = ON)
for i in range(6): # number of MODFLOW models 
    for j in range(combinations): # number of iterations for each model 
        sim_name = model_name[i] #
        sim_path = model_path  + '/' + model_name[i]
        #sim_path = 'C:/Users/sbferen/Documents/Frontiers_Paper/Modflow_scripts/MODFLOW_models/Group_3/' + model_name[i] 
        os.chdir(sim_path)
        sim = flopy.mf6.MFSimulation.load(sim_name=sim_name, version= 'mf6', exe_name = experiment_path + '/mf6.exe', 
                                  sim_ws=sim_path)

        # load model data
        model = sim.get_model()

        # Specific yield - index sy multipliers 
        sy = model.sto.sy
        new_sy = sy.get_data()
        new_sy = new_sy*params.sy_factor[i*combinations+j]
        model.sto.sy.set_data(new_sy)

        # River stage and conductance
        riv = model.riv
        Riv = model.riv.stress_period_data.data
        keys = list(Riv.keys())
        for k in range(np.size(keys)):   
            Riv[keys[k]]['stage'] = Riv[keys[k]]['stage'] * params.river_stage_factor[i*combinations+j] # multiply each key by stage param factor 
            Riv[keys[k]]['cond'] = Riv[keys[k]]['cond'] * params.cond_factor[i*combinations+j] # multiply each key by conductance param factor
        model.riv.stress_period_data.set_data(Riv)
        
        # Irrigation - Same procedure as Riv 
        irr = model.rch.stress_period_data.data
        keys = list(irr.keys())
        for k in range(np.size(keys)):
            irr[keys[k]]['recharge'][1:] = irr[keys[k]]['recharge'][1:] * params.irrigation_factor[i*combinations+j] # multiply each key by conductance param factor
            irr[keys[k]]['recharge'][0] = irr[keys[k]]['recharge'][0] * params.block_recharge_factor[i*combinations+j]
        model.rch.stress_period_data.set_data(irr)
        
        # Hydraulic conductivity  
        hydro = model.npf
        k = hydro.k
        new_k = k.get_data()
        new_k = new_k * params.k_factor[i*combinations+j]
        model.npf.k.set_data(new_k)
        test = model.npf.k.data
        
        # Layer thickness 
        dimensions = model.dis
        b = dimensions.botm
        new_b = b.get_data() # change thickness of bottom layer 
        new_b[0] = new_b[0] * params.b_factor[i*combinations+j]
        model.dis.botm.set_data(new_b)

        # Write and run simulation 
        sim.write_simulation() # save modified scenario 
        sim.run_simulation() 
        
        # load csv with Riv fluxes
        observation_name = model_name[i]+'.rvob_out_riv.csv' # name of observation output csv 
        riv_flux = pd.read_csv(observation_name) # load obs csv
        return_flow_results[i*combinations+j,:] = riv_flux.iloc[:,1] # save observation data to results array 


## RESET models to starting parameters 
for i in range(6):
    sim_name = model_name[i] #
    sim_path = model_path  + '/' + model_name[i]
    #sim_path = 'C:/Users/sbferen/Documents/Frontiers_Paper/Modflow_scripts/MODFLOW_models/Group_3/' + model_name[i] 
    os.chdir(sim_path)
    sim = flopy.mf6.MFSimulation.load(sim_name=sim_name, version= 'mf6', exe_name = experiment_path + '/mf6.exe', 
                                  sim_ws=sim_path)

    # load model data
    model = sim.get_model()

    # Specific yield - index sy multipliers 
    sy = model.sto.sy
    new_sy = sy.get_data()
    new_sy = new_sy*reset_params.sy_factor[i]
    model.sto.sy.set_data(new_sy)

        # River stage and conductance
    riv = model.riv
    Riv = model.riv.stress_period_data.data
    keys = list(Riv.keys())
    for k in range(np.size(keys)):   
        Riv[keys[k]]['stage'] = Riv[keys[k]]['stage'] * reset_params.river_stage_factor[i] # multiply each key by stage param factor 
        Riv[keys[k]]['cond'] = Riv[keys[k]]['cond'] * reset_params.cond_factor[i] # multiply each key by conductance param factor
    model.riv.stress_period_data.set_data(Riv)
        
    # Irrigation - Same procedure as Riv 
    irr = model.rch.stress_period_data.data
    keys = list(irr.keys())
    for k in range(np.size(keys)):
            irr[keys[k]]['recharge'][1:] = irr[keys[k]]['recharge'][1:] * reset_params.irrigation_factor[i] # multiply each key by conductance param factor
            irr[keys[k]]['recharge'][0] = irr[keys[k]]['recharge'][0] * reset_params.block_recharge_factor[i]
    model.rch.stress_period_data.set_data(irr)
        
    # Hydraulic conductivity  
    hydro = model.npf
    k = hydro.k
    new_k = k.get_data()
    new_k = new_k * reset_params.k_factor[i]
    model.npf.k.set_data(new_k)

    # Layer thickness 
    dimensions = model.dis
    b = dimensions.botm
    new_b = b.get_data() # change thickness of bottom layer 
    new_b[0] = new_b[0] * reset_params.b_factor[i]
    model.dis.botm.set_data(new_b)

    sim.write_simulation() # save modified scenario 

## Baseline simulations simulations for Group 3 (irrigation recharge = OFF)
    
model_name = ['Geom_1000m_rch1_baseline', 'Geom_1000m_rch2_baseline'] # number of models, outer loop of iterative simulation script 

for i in range(2): # number of MODFLOW models 
    for j in range(combinations): # number of iterations for each model 
        sim_name = model_name[i] #
        sim_path = model_path  + '/' + model_name[i]
        #sim_path = 'C:/Users/sbferen/Documents/Frontiers_Paper/Modflow_scripts/MODFLOW_models/Group_3/' + model_name[i] 
        os.chdir(sim_path)
        sim = flopy.mf6.MFSimulation.load(sim_name=sim_name, version= 'mf6', exe_name = experiment_path + '/mf6.exe', 
                                  sim_ws=sim_path)

        # load model data
        model = sim.get_model()

        # Specific yield - index sy multipliers 
        sy = model.sto.sy
        new_sy = sy.get_data()
        new_sy = new_sy*baseline_params.sy_factor[i*combinations+j]
        model.sto.sy.set_data(new_sy)

        # River stage and conductance
        riv = model.riv
        Riv = model.riv.stress_period_data.data
        keys = list(Riv.keys())
        for k in range(np.size(keys)):   
            Riv[keys[k]]['stage'] = Riv[keys[k]]['stage'] * baseline_params.river_stage_factor[i*combinations+j] # multiply each key by stage param factor 
            Riv[keys[k]]['cond'] = Riv[keys[k]]['cond'] * baseline_params.cond_factor[i*combinations+j] # multiply each key by conductance param factor
        model.riv.stress_period_data.set_data(Riv)
        
        # Irrigation multiplier  
        irr = model.rch.stress_period_data.data
        keys = list(irr.keys())
        for k in range(np.size(keys)):
            irr[keys[k]]['recharge'][1:] = irr[keys[k]]['recharge'][1:] * baseline_params.irrigation_factor[i*combinations+j] # multiply each key by conductance param factor
            irr[keys[k]]['recharge'][0] = irr[keys[k]]['recharge'][0] * baseline_params.block_recharge_factor[i*combinations+j]
        model.rch.stress_period_data.set_data(irr)
        
        # Hydraulic conductivity  
        hydro = model.npf
        k = hydro.k
        new_k = k.get_data()
        new_k = new_k * baseline_params.k_factor[i*combinations+j]
        model.npf.k.set_data(new_k)

        # Layer thickness 
        dimensions = model.dis
        b = dimensions.botm
        new_b = b.get_data() # change thickness of bottom layer 
        new_b[0] = new_b[0] * baseline_params.b_factor[i*combinations+j]
        model.dis.botm.set_data(new_b)

        # Write and run simulation 
        sim.write_simulation() # save modified scenario 
        sim.run_simulation() # run modified scenario
        
        # load csv with Riv fluxes
        observation_name = model_name[i]+'.rvob_out_riv.csv' # name of observation output csv 
        riv_flux = pd.read_csv(observation_name) # load obs csv
        baseline_results[i*combinations+j,:] = riv_flux.iloc[:,1] # save observation data to results array 

## RESET models to starting parameters 

for i in range(2):
    sim_name = model_name[i] #
    sim_path = model_path  + '/' + model_name[i]
    #sim_path = 'C:/Users/sbferen/Documents/Frontiers_Paper/Modflow_scripts/MODFLOW_models/Group_3/' + model_name[i] 
    os.chdir(sim_path)
    sim = flopy.mf6.MFSimulation.load(sim_name=sim_name, version= 'mf6', exe_name = experiment_path + '/mf6.exe', 
                                  sim_ws=sim_path)

    # load model data
    model = sim.get_model()

    # Specific yield - index sy multipliers 
    sy = model.sto.sy
    new_sy = sy.get_data()
    new_sy = new_sy*reset_params.sy_factor[i+6]
    model.sto.sy.set_data(new_sy)

    # River stage and conductance
    riv = model.riv
    Riv = model.riv.stress_period_data.data
    keys = list(Riv.keys())
    for k in range(np.size(keys)):   
        Riv[keys[k]]['stage'] = Riv[keys[k]]['stage'] * reset_params.river_stage_factor[i+6] # multiply each key by stage param factor 
        Riv[keys[k]]['cond'] = Riv[keys[k]]['cond'] * reset_params.cond_factor[i+6] # multiply each key by conductance param factor
    model.riv.stress_period_data.set_data(Riv)
        
    # Irrigation - Same procedure as Riv 
    irr = model.rch.stress_period_data.data
    keys = list(irr.keys())
    for k in range(np.size(keys)):
            irr[keys[k]]['recharge'][1:] = irr[keys[k]]['recharge'][1:] * reset_params.irrigation_factor[i+6] # multiply each key by conductance param factor
            irr[keys[k]]['recharge'][0] = irr[keys[k]]['recharge'][0] * reset_params.block_recharge_factor[i+6]
    model.rch.stress_period_data.set_data(irr)
        
    # Hydraulic conductivity  
    hydro = model.npf
    k = hydro.k
    new_k = k.get_data()
    new_k = new_k * reset_params.k_factor[i+6]
    model.npf.k.set_data(new_k)

    # Layer thickness 
    dimensions = model.dis
    b = dimensions.botm
    new_b = b.get_data() # change thickness of bottom layer 
    new_b[0] = new_b[0] * reset_params.b_factor[i+6]
    model.dis.botm.set_data(new_b)

    sim.write_simulation() # save modified scenario 
    

## save model results as CSVs
os.chdir(experiment_path +'/Group_3')
return_flow_results = pd.DataFrame(return_flow_results)
baseline_results = pd.DataFrame(baseline_results)
return_flow_results.to_csv("Group_3_return_flow_results.csv")
baseline_results.to_csv("Group_3_baseline_results.csv")

