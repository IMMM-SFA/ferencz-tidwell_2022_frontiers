
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Load data for plots
os.chdir('C:/Users/xxxxxxxx/Documents/Model_Files/Group_3') # absolute path to Group 3 in the Model Files folder
ret_flow = pd.read_csv("Group_3_return_flow_results.csv") # return flow scenario data
baseline = pd.read_csv("Group_3_baseline_results.csv") # baseline scenario data
params = pd.read_csv("Group_3_params.csv") # scenario parameters for Group 2
analytical_returns = pd.read_csv("Superposed_Return_flows.csv") # analytical results for comparison

# Convert daily model output to monthly totals 
bins = pd.read_csv("Modflow_stress_periods.csv")
ret_flow_monthly = pd.DataFrame(np.zeros([144,12*12]))
baseline_monthly = pd.DataFrame(np.zeros([48,12*12]))
ret_flow_monthly_outward = pd.DataFrame(np.zeros([144,12*12]))
baseline_monthly_outward = pd.DataFrame(np.zeros([48,12*12]))

for i in range(144):
    for j in range(144):
        ret_flow_monthly.iloc[i,j] = np.sum(ret_flow.iloc[i,bins.Start[j]+2:bins.End[j]+2])
        if np.sum(ret_flow.iloc[i,bins.Start[j]+2:bins.End[j]+2]) < 0 :
            ret_flow_monthly_outward.iloc[i,j] = np.sum(ret_flow.iloc[i,bins.Start[j]+2:bins.End[j]+2])

for i in range(48):
    for j in range(144):
        baseline_monthly.iloc[i,j] = np.sum(baseline.iloc[i,bins.Start[j]+2:bins.End[j]+2])
        if np.sum(baseline.iloc[i,bins.Start[j]+2:bins.End[j]+2]) < 0 :    
            baseline_monthly_outward.iloc[i,j] = np.sum(baseline.iloc[i,bins.Start[j]+2:bins.End[j]+2])

baseline_monthly_outward_mapped = pd.DataFrame(np.zeros([144,12*12]))            
baseline_monthly_mapped = pd.DataFrame(np.zeros([144,12*12]))         

start = [0, 0, 0, 24, 24, 24]
end = [24, 24, 24, 48, 48, 48]
for i in range(6):
    baseline_monthly_outward_mapped.iloc[i*24:(i+1)*24,:] = baseline_monthly_outward.iloc[start[i]:end[i]]
    baseline_monthly_mapped.iloc[i*24:(i+1)*24,:] = baseline_monthly.iloc[start[i],end[i]]

# # Create irrigation time series to use in plots
irrigation_ts = pd.DataFrame(np.zeros([36,12*12]))
geom_area = np.array([50000, 100000, 200000]).astype('float')
irr_scaling_coef = [1/3, 1/3, 1/3, 1/3, 2/3, 2/3 , 2/3, 2/3, 1, 1, 1, 1]
for i in range(3):
    for k in range(12):
        for j in range(144):
            irrigation_ts.iloc[12*i+k,j] = irr_scaling_coef[k]*geom_area[i] \
            *bins.Irrigation_baseline[j]*(bins.End[j]-bins.Start[j])
            
totals = np.sum(irrigation_ts.iloc[:,9*12:10*12], axis = 1)
        
########################## Plots and Analyis ############################# 


## Figure 9: Additional boundary flux from return flows for year = 10 
mpl.rc('axes', titlesize=14)
plt.rc('font', size= 14)
fig, axs = plt.subplots(nrows=7, ncols=3, figsize=(12, 12))
indexes = [0, 3, 24, 27, 48, 51, 72, 75, 96, 99, 120, 123]
time = np.arange(12)+1
for j in range(3):
    for k in range(4):
        for i in range(12):
            color = ['blue','blue','orange','orange','green','green', \
                     'cyan', 'cyan','red','red', 'lime','lime']
            marker = ['-',':','-',':','-',':','-',':','-',':','-',':']
            axs[k+3,j].plot(time,-1/100*(ret_flow_monthly_outward.iloc[indexes[i]+6*k+j,9*12:10*12] \
                  - baseline_monthly_outward_mapped.iloc[indexes[i]+6*k+j,9*12:10*12]), \
                      color = color[i], linestyle = marker[i])
            axs[k+3,j].set_xbound(1,12)
            axs[k+3,j].set_xticks(np.arange(12)+1)
            axs[k+3,j].set_xlabel('month')
            #print(j*24+k*6+i)

# Analytical comparions for Sy = 0.2 & b = 20 m
# for j in range(3): 
#     for k in range(4):
#         for i in range(3):
#             color = ['magenta','yellow','lime']
#             axs[k+3,j].plot(time,analytical_returns.iloc[12+k*3+i,9*12+1:10*12+1],color = color[i])

for i in range(3):
    stage_factor = [0.5, 1, 2]
    irr_factor = [1/3,2/3,1,1]
    recharge_factor = 100000*30*np.array([1, 1, 2, 2])
    basin_fill_factor = [2500/12,5000/12,5000/12,10000/12]
    marker = ['-','--','-','--']
    color = ['blue','orange','green','green']
    color_recharge = ['gray', 'gray','black','black']
    for j in range(4):
        axs[0,i].plot(time,stage_factor[i]*bins.iloc[9*12:10*12,3], \
                      color = 'blue', linestyle = marker[j])
        nat_recharge = 1/100*(recharge_factor[j]*bins.Basin_fill_baseline.iloc[0:12])+ \
                      1/100*basin_fill_factor[j]*pd.DataFrame(np.ones([1,12]))
        axs[1,i].plot(time,nat_recharge.iloc[0,:],color = color_recharge[j], linestyle = marker[j])
        axs[2,i].plot(time,1/100*irr_factor[j]*irrigation_ts.iloc[23,9*12:10*12], color = color[j])
        #ax2 = axs[0,i].twinx()             
        #ax2 = axs[0,i].twinx()             
        #ax2.plot(time,irr_factor[j]*irrigation_ts.iloc[1,9*12:10*12], color = 'gray')
        #ax2.set_yticks([])
        #ax2.tick_params(axis = 'y', labelcolor = 'gray')   
        axs[0,i].set_xbound(1,12)
        axs[1,i].set_xbound(1,12)
        axs[2,i].set_xbound(1,12)
        axs[0,i].set_ybound(0,2)
        axs[0,i].set_xticks(np.arange(12)+1)  
        axs[1,i].set_xticks(np.arange(12)+1)  
        axs[2,i].set_xticks(np.arange(12)+1)  
plt.tight_layout()

########## Extra Figures for Group 1 not presented in Paper #########

## Return flow flux for year = 11 (drought)
fig, axs = plt.subplots(nrows=5, ncols=3, figsize=(12, 10))

time = np.arange(12)+1
for j in range(3):
    for k in range(4):
        axs[k+1,j].plot([1,12],[0,0], color = 'r', linestyle = '--')
        for i in range(12):
            color = ['blue','blue','blue','blue','orange','orange', \
                     'orange', 'orange','green','green', 'green','green']
            marker = ['-',':','--','-.','-',':','--','-.','-',':','--','-.']
            axs[k+1,j].plot(time,-1*(ret_flow_monthly_outward.iloc[j*48+k*12+i,10*12:11*12] \
                  - baseline_monthly_outward.iloc[j*48+k*12+i,10*12:11*12]), \
                      color = color[i], linestyle = marker[i])
            axs[k+1,j].set_xbound(1,12)
            axs[k+1,j].set_xticks(np.arange(12)+1)
            axs[k+1,j].set_xlabel('month')
            #print(j*24+k*6+i)
 
# Analytical comparions for Sy = 0.2 & b = 20 m          
# for j in range(3):
#     for k in range(4):
#         for i in range(3):
#             color = ['magenta','yellow','lime']
#             axs[k+1,j].plot(time,analytical_returns.iloc[j*12+k*3+i,10*12:11*12],color = color[i])
            
   
for i in range(3):
    axs[0,i].plot(time,bins.iloc[9*12:10*12,3], color = 'blue')
    ax2 = axs[0,i].twinx()             
    ax2.plot(time,irrigation_ts.iloc[i,9*12:10*12], color = 'gray')
    ax2.set_yticks([])
    ax2.tick_params(axis = 'y', labelcolor = 'gray')   
    axs[0,i].set_xbound(1,12)
    axs[0,i].set_xticks(np.arange(12)+1)    

plt.tight_layout()

## Stream boundary flux for year = 10 
fig, axs = plt.subplots(nrows=5, ncols=3, figsize=(12, 10))
indexes = [0, 3, 24, 27, 48, 51, 72, 75, 96, 99, 120, 123]
time = np.arange(12)+1
for j in range(3):
    for k in range(4):
        axs[k+1,j].plot([1,12],[0,0], color = 'r', linestyle = '--')
        for i in range(12):
            color = ['blue','blue','orange','orange','green','green', \
                     'cyan', 'cyan','red','red', 'lime','lime']
            marker = ['-',':','-',':','-',':','-',':','-',':','-',':']
            axs[k+1,j].plot(time,-1*ret_flow_monthly_outward.iloc[indexes[i]+6*k+j,9*12:10*12], \
                  color = color[i], linestyle = marker[i])
            axs[k+1,j].set_xbound(1,12)
            #axs[k+1,j].set_ybound(0,np.max((ret_flow_monthly.iloc[j*48+k*12+i,0*12:1*12])))
            axs[k+1,j].set_xticks(np.arange(12)+1)
            axs[k+1,j].set_xlabel('month')
            #print(j*24+k*6+i)
   
for i in range(3):
    axs[0,i].plot(time,bins.iloc[9*12:10*12,3], color = 'blue')
    ax2 = axs[0,i].twinx()             
    ax2.plot(time,irrigation_ts.iloc[i,9*12:10*12], color = 'gray')
    ax2.set_yticks([])
    ax2.tick_params(axis = 'y', labelcolor = 'gray')   
    axs[0,i].set_xbound(1,12)
    axs[0,i].set_xticks(np.arange(12)+1)    

plt.tight_layout()
plt.title("River boundary flux")

## Baseline flow flux for year = 10 
fig, axs = plt.subplots(nrows=5, ncols=3, figsize=(12, 10))
time = np.arange(12)+1
for j in range(3):
    for k in range(4):
        axs[k+1,j].plot([1,12],[0,0], color = 'r', linestyle = '--')
        for i in range(12):
            color = ['blue','blue','blue','blue','orange','orange', \
                     'orange', 'orange','green','green', 'green','green']
            marker = ['-',':','--','-.','-',':','--','-.','-',':','--','-.']
            axs[k+1,j].plot(time,-1* (baseline_monthly.iloc[j*48+k*12+i,0*12:1*12]), \
                      color = color[i], linestyle = marker[i])
            axs[k+1,j].set_xbound(1,12)
            axs[k+1,j].set_xticks(np.arange(12)+1)
            axs[k+1,j].set_xlabel('month')
            #print(j*24+k*6+i)
   
for i in range(3):
    stage_factor = [0.000001, 0.5, 1, 2]
    marker = ['-',':','--','-.']
    for j in range(4):
        axs[0,i].plot(time,stage_factor[j]*bins.iloc[9*12:10*12,3], \
                      color = 'blue', linestyle = marker[j])
        # ax2 = axs[0,i].twinx()             
        # ax2.plot(time,irrigation_ts.iloc[i,9*12:10*12], color = 'gray')
        # ax2.set_yticks([])
        # ax2.tick_params(axis = 'y', labelcolor = 'gray')   
        # axs[0,i].set_xbound(1,12)
        # axs[0,i].set_xticks(np.arange(12)+1)    

plt.tight_layout()
plt.title("Baseline boundary flux")

