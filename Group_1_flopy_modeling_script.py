## Import libraries 

import sys
import os
import platform
import pandas as pd
import numpy as np
import matplotlib as mpl
import flopy

## Check versions 
print(sys.version)
print('numpy version: {}'.format(np.__version__))
print('matplotlib version: {}'.format(mpl.__version__))
print('flopy version: {}'.format(flopy.__version__))

# Simulation paths 
experiment_path = 'C:/Users/xxxxxx/Documents/Model_Files' # absolute path to Model Files folder
os.chdir(experiment_path + '/Group_1') 
model_path = experiment_path + '/Group_1/MODFLOW_files'


model_name = ['Geom_500m', 'Geom_1000m', 'Geom_2000m'] # number of models, outer loop of iterative simulation script 
params = pd.read_csv('Group_1_params.csv') # paramater settings file for group of simulations 
reset_params = pd.read_csv('Group_1_reset.csv') # parameters to reset MODFLOW models to default parameter values
return_flow_results = np.zeros([72,12*365+1]) # array for saving return flow model outputs set rows to number of param combinations, set columns to number of model time steps
baseline_results = np.zeros([72,12*365+1]) # array for saving baseline model outputs set rows to number of param combinations, set columns to number of model time steps
combinations = 24 # number of parameter combinations for each model in Group 1

## Return flow simulations for Group 1 (irrigation recharge = ON)

for i in range(3): # number of MODFLOW models 
    for j in range(combinations): # number of parameter combinations for each model 
        sim_name = model_name[i] 
        sim_path = model_path  + '/' + model_name[i]
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
            irr[keys[k]]['recharge'][:] = irr[keys[k]]['recharge'][:] * params.irrigation_factor[i*combinations+j] # multiply each key by conductance param factor
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
        sim.run_simulation() # run modified scenario
        
        # load csv with Riv fluxes
        observation_name = model_name[i]+'.rvob_out_riv.csv' # name of observation output csv 
        riv_flux = pd.read_csv(observation_name) # load obs csv
        return_flow_results[i*combinations+j,:] = riv_flux.iloc[:,1] # save observation data to results array 


## RESET models to starting parameters 

for i in range(3):
    sim_name = model_name[i] #
    sim_path = model_path  + '/' + model_name[i]
    os.chdir(sim_path)
    sim = flopy.mf6.MFSimulation.load(sim_name=sim_name, version= 'mf6', exe_name = experiment_path + '/mf6.exe', 
                                  sim_ws=sim_path)

    # load model data
    model = sim.get_model()

    # Specific yield - index sy multipliers 
    sy = model.sto.sy
    new_sy = sy.get_data()
    new_sy = new_sy*reset_params.sy_factor[0]
    model.sto.sy.set_data(new_sy)

    # River stage and conductance
    riv = model.riv
    Riv = model.riv.stress_period_data.data
    keys = list(Riv.keys())
    for k in range(np.size(keys)):   
        Riv[keys[k]]['stage'] = Riv[keys[k]]['stage'] * reset_params.river_stage_factor[0] # multiply each key by stage param factor 
        Riv[keys[k]]['cond'] = Riv[keys[k]]['cond'] * reset_params.cond_factor[0] # multiply each key by conductance param factor
    model.riv.stress_period_data.set_data(Riv)
    test = model.riv.stress_period_data.data
        
    # Irrigation - Same procedure as Riv 
    irr = model.rch.stress_period_data.data
    keys = list(irr.keys())
    for k in range(np.size(keys)):
        irr[keys[k]]['recharge'][:] = irr[keys[k]]['recharge'][:] * \
        reset_params.irrigation_factor[0] # multiply each key by conductance param factor
    model.rch.stress_period_data.set_data(irr)
    test = model.rch.stress_period_data.data
        
    # Hydraulic conductivity  
    hydro = model.npf
    k = hydro.k
    new_k = k.get_data()
    new_k = new_k * reset_params.k_factor[0]
    model.npf.k.set_data(new_k)

    # Layer thickness 
    dimensions = model.dis
    b = dimensions.botm
    new_b = b.get_data() # change thickness of bottom layer 
    new_b[0] = new_b[0] * reset_params.b_factor[0]
    model.dis.botm.set_data(new_b)

    sim.write_simulation() # save modified scenario 

## Baseline simulations simulations for Group 1 (irrigation recharge = OFF)
    
model_name = ['Geom_500m', 'Geom_1000m', 'Geom_2000m'] # number of models, outer loop of iterative simulation script 

for i in range(3): # number of MODFLOW models 
    for j in range(combinations): # number of parameter combinations for each model  
        sim_name = model_name[i] 
        sim_path = model_path  + '/' + model_name[i]
        os.chdir(sim_path)
        sim = flopy.mf6.MFSimulation.load(sim_name=sim_name, version= 'mf6', exe_name = experiment_path + '/mf6.exe', 
                                  sim_ws=sim_path)

        # load model data
        model = sim.get_model()

        # Specific yield - index sy multipliers 
        sy = model.sto.sy
        new_sy = sy.get_data()
        new_sy = new_sy*params.sy_factor[i*combinations+j+3*combinations]
        model.sto.sy.set_data(new_sy)

        # River stage and conductance
        riv = model.riv
        Riv = model.riv.stress_period_data.data
        keys = list(Riv.keys())
        for k in range(np.size(keys)):   
            Riv[keys[k]]['stage'] = Riv[keys[k]]['stage'] * params.river_stage_factor[i*combinations+j+3*combinations] # multiply each key by stage param factor 
            Riv[keys[k]]['cond'] = Riv[keys[k]]['cond'] * params.cond_factor[i*combinations+j+3*combinations] # multiply each key by conductance param factor
        model.riv.stress_period_data.set_data(Riv)
        test = model.riv.stress_period_data.data
        
        # Irrigation multiplier  
        irr = model.rch.stress_period_data.data
        keys = list(irr.keys())
        for k in range(np.size(keys)):
            irr[keys[k]]['recharge'][:] = irr[keys[k]]['recharge'][:] * params.irrigation_factor[i*combinations+j+3*combinations]
        model.rch.stress_period_data.set_data(irr)
        test = model.rch.stress_period_data.data
        
        # Hydraulic conductivity  
        hydro = model.npf
        k = hydro.k
        new_k = k.get_data()
        new_k = new_k * params.k_factor[i*combinations+j+3*combinations]
        model.npf.k.set_data(new_k)

        # Layer thickness 
        dimensions = model.dis
        b = dimensions.botm
        new_b = b.get_data() # change thickness of bottom layer 
        new_b[0] = new_b[0] * params.b_factor[i*combinations+j+3*combinations]
        model.dis.botm.set_data(new_b)

        # Write and run simulation
        sim.write_simulation() # save modified scenario 
        sim.run_simulation() # run modified scenario
        
        # load csv with Riv fluxes
        observation_name = model_name[i]+'.rvob_out_riv.csv' # name of observation output csv 
        riv_flux = pd.read_csv(observation_name) # load obs csv
        baseline_results[i*combinations+j,:] = riv_flux.iloc[:,1] # save observation data to results array 

# RESET models to starting parameters 
for i in range(3):
    sim_name = model_name[i] #
    sim_path = model_path  + '/' + model_name[i]
    os.chdir(sim_path)
    sim = flopy.mf6.MFSimulation.load(sim_name=sim_name, version= 'mf6', exe_name = experiment_path + '/mf6.exe', 
                                  sim_ws=sim_path)

    # load model data
    model = sim.get_model()

    # Specific yield - index sy multipliers 
    sy = model.sto.sy
    new_sy = sy.get_data()
    new_sy = new_sy*reset_params.sy_factor[1]
    model.sto.sy.set_data(new_sy)

    # River stage and conductance
    riv = model.riv
    Riv = model.riv.stress_period_data.data
    keys = list(Riv.keys())
    for k in range(np.size(keys)):   
        Riv[keys[k]]['stage'] = Riv[keys[k]]['stage'] * reset_params.river_stage_factor[1] # multiply each key by stage param factor 
        Riv[keys[k]]['cond'] = Riv[keys[k]]['cond'] * reset_params.cond_factor[1] # multiply each key by conductance param factor
    model.riv.stress_period_data.set_data(Riv)
    test = model.riv.stress_period_data.data
        
    # Irrigation - Same procedure as Riv 
    irr = model.rch.stress_period_data.data
    keys = list(irr.keys())
    for k in range(np.size(keys)):
        irr[keys[k]]['recharge'][:] = irr[keys[k]]['recharge'][:] * \
        reset_params.irrigation_factor[1] # multiply each key by conductance param factor
    model.rch.stress_period_data.set_data(irr)
    test = model.rch.stress_period_data.data
        
    # Hydraulic conductivity  
    hydro = model.npf
    k = hydro.k
    new_k = k.get_data()
    new_k = new_k * reset_params.k_factor[1]
    model.npf.k.set_data(new_k)

    # Layer thickness 
    dimensions = model.dis
    b = dimensions.botm
    new_b = b.get_data() # change thickness of bottom layer 
    new_b[0] = new_b[0] * reset_params.b_factor[1]
    model.dis.botm.set_data(new_b)

    sim.write_simulation() # save modified scenario
    
# save model results as CSVs
os.chdir(experiment_path +'/Group_1')
return_flow_results = pd.DataFrame(return_flow_results)
baseline_results = pd.DataFrame(baseline_results)
return_flow_results.to_csv("Group_1_return_flow_results.csv")
baseline_results.to_csv("Group_1_baseline_results.csv")
