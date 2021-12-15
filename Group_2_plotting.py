
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# Load data for plots
os.chdir('C:/Users/xxxxxxx/Documents/Model_Files/Group_2') # # absolute path to Group 2 in the Model Files folder
ret_flow = pd.read_csv("Group_2_return_flow_results.csv") # return flow scenario data
baseline = pd.read_csv("Group_2_baseline_results.csv") # baseline scenario data
params = pd.read_csv("Group_2_params.csv") # scenario parameters for Group 2
analytical_returns = pd.read_csv("Superposed_Return_flows.csv") # analytical results for comparison

# Convert daily model output to monthly totals 
bins = pd.read_csv("Modflow_stress_periods.csv")
ret_flow_monthly = pd.DataFrame(np.zeros([144,12*12]))
baseline_monthly = pd.DataFrame(np.zeros([144,12*12]))
ret_flow_monthly_outward = pd.DataFrame(np.zeros([144,12*12]))
baseline_monthly_outward = pd.DataFrame(np.zeros([144,12*12]))
ret_flow_monthly_inward = pd.DataFrame(np.zeros([144,12*12]))
baseline_monthly_inward = pd.DataFrame(np.zeros([144,12*12]))


for i in range(144):
    for j in range(144):
        ret_flow_monthly.iloc[i,j] = np.sum(ret_flow.iloc[i,bins.Start[j]+2:bins.End[j]+2])
        baseline_monthly.iloc[i,j] = np.sum(baseline.iloc[i,bins.Start[j]+2:bins.End[j]+2])
        if np.sum(ret_flow.iloc[i,bins.Start[j]+2:bins.End[j]+2]) < 0 :
            ret_flow_monthly_outward.iloc[i,j] = np.sum(ret_flow.iloc[i,bins.Start[j]+2:bins.End[j]+2])
        if np.sum(baseline.iloc[i,bins.Start[j]+2:bins.End[j]+2]) < 0 :    
            baseline_monthly_outward.iloc[i,j] = np.sum(baseline.iloc[i,bins.Start[j]+2:bins.End[j]+2])
        if np.sum(ret_flow.iloc[i,bins.Start[j]+2:bins.End[j]+2]) > 0 :
            ret_flow_monthly_inward.iloc[i,j] = np.sum(ret_flow.iloc[i,bins.Start[j]+2:bins.End[j]+2])
        if np.sum(baseline.iloc[i,bins.Start[j]+2:bins.End[j]+2]) > 0 :    
            baseline_monthly_inward.iloc[i,j] = np.sum(baseline.iloc[i,bins.Start[j]+2:bins.End[j]+2])
            
# Create irrigation time series to use in plots 
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

mpl.rc('axes', titlesize=10)
plt.rc('font', size= 10) 

# Figure 8: Additional boundary flux from return flows for year = 10 
fig, axs = plt.subplots(nrows=6, ncols=3, figsize=(12, 10))
tick_maj = [10, 20, 20]
tick_min = [5, 10, 10]
time = np.arange(12)+1
for j in range(3):
    for k in range(4):
        for i in range(12):
            color = ['blue','blue','blue','blue','orange','orange', \
                      'orange', 'orange','green','green', 'green','green']
            marker = ['-','',':','--','-','',':','--','-','',':','--']
            axs[k+2,j].plot(time,-1/100*(ret_flow_monthly_outward.iloc[j*48+k*12+i,9*12:10*12] \
                  - baseline_monthly_outward.iloc[j*48+k*12+i,9*12:10*12]), \
                      color = color[i], linestyle = marker[i])
            axs[k+2,j].yaxis.set_major_locator(MultipleLocator(tick_maj[j]))
            axs[k+2,j].yaxis.set_minor_locator(MultipleLocator(tick_min[j]))
            axs[k+2,j].set_xbound(1,12)
            axs[k+2,j].set_xticks(np.arange(12)+1)
            axs[k+2,j].set_xlabel('month')

# Analytical comparions for Sy = 0.2 & b = 20 m
# for j in range(3):
#     for k in range(4):
#         for i in range(3):
#             color = ['magenta','yellow','lime']
#             axs[k+2,j].plot(time,1/100*analytical_returns.iloc[j*12+k*3+i,9*12+1:10*12+1],color = color[i])
            
for i in range(3):
    stage_factor = [0.000001, 0.5, 1, 2]
    irr_factor = [1/3,2/3,1,1]
    irr_loc = [11, 27, 35]
    marker = ['-',':','--','-.']
    color = ['blue','orange','green','green']
    for j in range(4):
        axs[0,i].plot(time,stage_factor[j]*bins.iloc[9*12:10*12,3], \
                      color = 'blue', linestyle = marker[j])
        axs[1,i].plot(time,1/100*irr_factor[j]*irrigation_ts.iloc[irr_loc[i],9*12:10*12], color = color[j])
        #ax2 = axs[0,i].twinx()             
        #ax2.plot(time,irr_factor[j]*irrigation_ts.iloc[1,9*12:10*12], color = 'gray')
        #ax2.set_yticks([])
        #ax2.tick_params(axis = 'y', labelcolor = 'gray')   
        axs[0,i].set_xbound(1,12)
        axs[0,i].set_xticks(np.arange(12)+1)    
        axs[1,i].set_xticks(np.arange(12)+1) 
        axs[0,i].yaxis.set_major_locator(MultipleLocator(1))
        axs[0,i].yaxis.set_minor_locator(MultipleLocator(0.5))
        
plt.tight_layout()


# Return flow years 10, 11, 12
total_rf_yr10 = np.sum(-1*(ret_flow_monthly_outward.iloc[:,9*12:10*12] \
                  - baseline_monthly_outward.iloc[:,9*12:10*12]), axis = 1)


## FIGURE 10: MODFLOW Baseflow and stream exchange amplitude in Feb year = 10 
additional_outward = -1*(ret_flow_monthly_outward
                  - baseline_monthly_outward)

limit = np.array([40, 60, 80])
tick_maj = [10, 10, 20]
tick_min = [5, 5, 10]
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(9, 3))
for j in range(3):
    axs[j].plot([0 ,limit[j]],[0,limit[j]], color = 'k')
    for k in range(4):
        color = ['blue','blue','blue', 'blue', \
                 'gold','gold','gold','gold',\
                     'red','red' ,'red','red']
        for i in range(12):
            marker = ['P','>','x','o','P','>','x','o','P','>','x','o']
            axs[j].scatter(1/100*additional_outward.iloc[j*48+k*12+i,9*12+2], \
                1/100*np.max(additional_outward.iloc[j*48+k*12+i,9*12:10*12]), \
                      color = color[i], marker = marker[i])
            axs[j].set_xlabel('Feb Return Flow')
            axs[j].set_ylabel('Max Monthly Return Flow')
            axs[j].yaxis.set_major_locator(MultipleLocator(tick_maj[j]))
            axs[j].yaxis.set_minor_locator(MultipleLocator(tick_min[j]))
            axs[j].xaxis.set_major_locator(MultipleLocator(tick_maj[j]))
            axs[j].xaxis.set_minor_locator(MultipleLocator(tick_min[j]))


plt.tight_layout()            

# Figure 11: Analytical - MODFLOW absolute and % difference in year = 10, late summer period = July, Aug, Sept 
late_sum_analytical = pd.DataFrame(np.zeros([1,36]))
for j in range(3):
    for k in range(3):
        for i in range(4):
            late_sum_analytical.iloc[0,4*k+i+j*12] = 1/100*np.sum(analytical_returns.iloc[j*12+i*3+k,9*12+7+1:9*12+9+1])

late_sum_modflow = pd.DataFrame(np.zeros([1,36]))
for j in range(3):
    for k in range(4):
        for i in range(3):
            late_sum_modflow.iloc[0,k+i*4+j*12] = 1/100*np.sum(additional_outward.iloc[j*48+k*12+i*4,9*12+7:9*12+9])
 
plt.tight_layout()

ticks = [1, 4, 5]
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
for j in range(3):
    color = ['blue','blue','blue', 'blue', \
                 'gold','gold','gold','gold',\
                     'red','red' ,'red','red']
    for i in range(12):
        axs[j].scatter(i, (late_sum_analytical.iloc[0,j*12+i]-late_sum_modflow.iloc[0,j*12+i]) \
                      , color = color[i], marker = 'o')
        axs[j].set_ylabel('Late summer absolute difference')
        axs[j].xaxis.set_minor_locator(MultipleLocator(1))
        axs[j].xaxis.set_major_locator(MultipleLocator(12))
        axs[j].yaxis.set_major_locator(MultipleLocator(ticks[j]))
        axs[j].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
        axs[j].set_xticklabels(['3','10','30','100','3','10','30','100','3','10','30','100'])
plt.tight_layout()

ticks = [5, 10, 10]
ticks_m = [2.5, 5, 5]
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
for j in range(3):
    color = ['blue','blue','blue', 'blue', \
                 'gold','gold','gold','gold',\
                     'red','red' ,'red','red']
    for i in range(12):
        axs[j].scatter(i,100 * (late_sum_analytical.iloc[0,j*12+i]-late_sum_modflow.iloc[0,j*12+i])/ \
                      late_sum_modflow.iloc[0,j*12+i] \
                       , color = color[i], marker = 'o')
        axs[j].set_ylabel('Late summer percent difference')
        axs[j].xaxis.set_minor_locator(MultipleLocator(1))
        axs[j].yaxis.set_major_locator(MultipleLocator(ticks[j]))
        axs[j].yaxis.set_minor_locator(MultipleLocator(ticks_m[j]))
        axs[j].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
        axs[j].set_xticklabels(['3','10','30','100','3','10','30','100','3','10','30','100'])

        
plt.tight_layout()

    
## Figure 11 Analytical - MODFLOW absolute and % difference in winter year = 10, winter = December, Jan, Feb
winter_analytical = pd.DataFrame(np.zeros([1,36]))
for j in range(3):
    for k in range(3):
        for i in range(4):
            winter_analytical.iloc[0,4*k+i+j*12] = 1/100*np.sum(analytical_returns.iloc[j*12+i*3+k,9*12+12+1:10*12+2+1]) 

winter_modflow = pd.DataFrame(np.zeros([1,36]))
for j in range(3):
    for k in range(4):
        for i in range(3):
            winter_modflow.iloc[0,k+i*4+j*12] = 1/100*np.sum(additional_outward.iloc[j*48+k*12+i*4,9*12+12:10*12+2])

 
ticks = [2, 2, 4]
ticks_m= [10, 1, 2]
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
for j in range(3):
    color = ['blue','blue','blue', 'blue', \
                 'gold','gold','gold','gold',\
                     'red','red' ,'red','red']
    for i in range(12):
        axs[j].scatter(i, (winter_analytical.iloc[0,j*12+i]-winter_modflow.iloc[0,j*12+i]) \
                      , color = color[i], marker = 'o')
        axs[j].set_ylabel('Winter absolute difference')
        axs[j].xaxis.set_minor_locator(MultipleLocator(1))
        axs[j].xaxis.set_major_locator(MultipleLocator(12))
        axs[j].yaxis.set_major_locator(MultipleLocator(ticks[j]))
        axs[j].yaxis.set_minor_locator(MultipleLocator(ticks_m[j]))
        axs[j].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
        axs[j].set_xticklabels(['3','10','30','100','3','10','30','100','3','10','30','100'])
        
plt.tight_layout() 

ticks = [5, 5, 10]
ticks_m = [5, 10, 5]
y_bnd = [0, 30, 30]
y_start = [30, 0, -10]
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
for j in range(3):
    color = ['blue','blue','blue', 'blue', \
                 'gold','gold','gold','gold',\
                     'red','red' ,'red','red']
    for i in range(12):
        axs[j].scatter(i, 100*(winter_analytical.iloc[0,j*12+i]-winter_modflow.iloc[0,j*12+i])/
                       winter_modflow.iloc[0,j*12+i],\
                      color = color[i], marker = 'o')
        axs[j].set_ylabel('Winter percent difference')
        axs[j].xaxis.set_minor_locator(MultipleLocator(1))
        axs[j].xaxis.set_major_locator(MultipleLocator(12))
        axs[j].yaxis.set_major_locator(MultipleLocator(ticks[j]))
        axs[j].yaxis.set_minor_locator(MultipleLocator(ticks_m[j]))
        axs[j].set_ybound([y_start[j],y_bnd[j]])
        axs[j].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
        axs[j].set_xticklabels(['3','10','30','100','3','10','30','100','3','10','30','100'])
            
plt.tight_layout()  

