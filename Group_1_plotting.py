import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# Load data for plots

os.chdir('C:/Users/xxxxxxx/Documents/Model_Files/Group_1') # absolute path to Group 1 in the Model Files folder

ret_flow = pd.read_csv("Group_1_return_flow_results.csv") # return flow scenario data
baseline = pd.read_csv("Group_1_baseline_results.csv") # baseline scenario data
params = pd.read_csv("Group_1_params.csv") # scenario parameters for Group 1
analytical_returns = pd.read_csv("Superposed_Return_flows.csv") # analytical results for comparison


# Convert daily model output to monthly totals 
bins = pd.read_csv("Modflow_stress_periods.csv") # river and irrigation boundary conditions for Group 1
ret_flow_monthly = pd.DataFrame(np.zeros([72,12*12]))
baseline_monthly = pd.DataFrame(np.zeros([72,12*12]))
ret_flow_monthly_outward = pd.DataFrame(np.zeros([72,12*12]))
baseline_monthly_outward = pd.DataFrame(np.zeros([72,12*12]))
ret_flow_monthly_inward = pd.DataFrame(np.zeros([72,12*12]))
baseline_monthly_inward = pd.DataFrame(np.zeros([72,12*12]))

for i in range(72):
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
irrigation_ts = pd.DataFrame(np.zeros([3,12*12]))
geom_area = np.array([50000, 100000, 200000]).astype('float')
for i in range(3):
    for j in range(144):
        irrigation_ts.iloc[i,j] = 2/3*geom_area[i]*bins.Irrigation_baseline[j]* \
        (bins.End[j]-bins.Start[j])

########################## Plots and Analyis ############################# 


## Figure 5 - superposed analytical return flows for year = 10 

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(9, 3))
time = np.arange(12*1)+1 
for j in range(3):
    axs[j].plot(time,irrigation_ts.iloc[j,9*12:10*12]/100, color = 'black')
    c = ['blue','green','orange','red']
    for k in range(4):
            axs[j].plot(time,analytical_returns.iloc[j*12+k*3+1,9*12+1:10*12+1]/100,color = c[k])
            axs[j].set_xticks(np.linspace(0,12,num = 12, endpoint = False)+1, minor = False)
            axs[j].set_xlabel('month')
    axs[0].legend(['irr','3','10','30','100'], title = 'm/d', loc = 'best')
plt.tight_layout()

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(9, 3))
time = np.arange(12*10)+1 
for j in range(3):
    c = ['blue','green','orange','red']
    for k in range(4):
            axs[j].plot(time,analytical_returns.iloc[j*12+k*3+1,0*12+1:10*12+1]/100,color = c[k])
            axs[j].set_xticks([24,48,72,96,120])
            axs[j].set_yticks([0, 10, 20, 30, 40, 50])
            axs[j].set_xlabel('months')
axs[0].legend(['3','10','30','100'], title = 'm/d', loc = 'best')
plt.tight_layout()

## Figure 6: Return flow flux for year = 10 
fig, axs = plt.subplots(nrows=5, ncols=3, figsize=(12, 10))
time = np.arange(12)+1
for j in range(3):
    for k in range(4):
        for i in range(6):
            color = ['blue','blue','orange','orange','green','green']
            marker = ['-',':','-',':','-',':']
            axs[k+1,j].plot(time,-1/100*(ret_flow_monthly_outward.iloc[j*24+k*6+i,9*12:10*12] \
                  - baseline_monthly_outward.iloc[j*24+k*6+i,9*12:10*12]), \
                      color = color[i], linestyle = marker[i])
            axs[k+1,j].set_xbound(1,12)
            axs[k+1,j].yaxis.set_major_locator(MultipleLocator(10))
            axs[k+1,j].yaxis.set_minor_locator(MultipleLocator(5))
            axs[k+1,j].set_xticks(np.arange(12)+1)
            axs[k+1,j].set_xlabel('month')

for j in range(3):
    for k in range(4):
            axs[k+1,j].plot(time,1/100*analytical_returns.iloc[j*12+k*3+1,9*12+1:10*12+1],color = 'gray')


for i in range(3):
    axs[0,i].plot(time,bins.iloc[9*12:10*12,3], color = 'blue')
    ax2 = axs[0,i].twinx()             
    ax2.plot(time,irrigation_ts.iloc[i,9*12:10*12]/100, color = 'gray')
    ax2.tick_params(axis = 'y', labelcolor = 'gray')   
    axs[0,i].set_xbound(1,12)
    axs[0,i].set_xticks(np.arange(12)+1)    

plt.tight_layout()

## Figure 7 Return flow flux for year = 11
fig, axs = plt.subplots(nrows=5, ncols=3, figsize=(12, 10))
time = np.arange(12)+1
for j in range(3):
    for k in range(4):
        for i in range(6):
            color = ['blue','blue','orange','orange','green','green']
            marker = ['-',':','-',':','-',':']
            axs[k+1,j].plot(time,-1/100*(ret_flow_monthly_outward.iloc[j*24+k*6+i,10*12:11*12] \
                  - baseline_monthly_outward.iloc[j*24+k*6+i,10*12:11*12]), \
                      color = color[i], linestyle = marker[i])
            axs[k+1,j].set_xbound(1,12)
            axs[k+1,j].set_xticks(np.arange(12)+1)
            axs[k+1,j].set_xlabel('month')

for i in range(3):
    axs[0,i].plot(time,bins.iloc[10*12:11*12,3], color = 'blue')
    axs[0,i].plot(time,irrigation_ts.iloc[i,10*12:11*12], color = 'gray')
    axs[0,i].set_xbound(1,12)
    axs[0,i].set_yticks([0.25, 0.5])
    axs[0,i].set_xticks(np.arange(12)+1)    

plt.tight_layout()

## Figure 7 model difference in amplitude in Sep year = 10 and Sep year 11 (drought)
amp_analytical = pd.DataFrame(np.zeros([1,36]))
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(9, 4))
for j in range(3):
    for k in range(4):
        color = ['blue','blue','orange','orange','green','green']
        for i in range(6):
            marker = ['o','+','o','+','o','+']
            axs[j].scatter(k,100*((ret_flow_monthly_outward.iloc[j*24+k*6+i,10*12+8] \
                  - baseline_monthly_outward.iloc[j*24+k*6+i,10*12+8])/(ret_flow_monthly_outward.iloc[j*24+k*6+i,9*12+8] \
                  - baseline_monthly_outward.iloc[j*24+k*6+i,9*12+8])), \
                      color = color[i], marker = marker[i])
            axs[j].set_xlabel('K')
            axs[j].set_xticks([0,1,2,3])
            axs[j].set_xticklabels(['3','10','30','100'])
            axs[j].set_ylabel('% of previous August return flow')
            axs[j].yaxis.set_major_locator(MultipleLocator(20))
            axs[j].yaxis.set_minor_locator(MultipleLocator(10))
            
      
plt.tight_layout() 

########## Extra Figures for Group 1 not presented in Paper #########

# Stream boundary flux for year = 10 
mpl.rc('axes', titlesize=14)
plt.rc('font', size= 14)

fig, axs = plt.subplots(nrows=5, ncols=3, figsize=(12,10))
time = np.arange(12)+1
for j in range(3):
    for k in range(4):
        axs[k+1,j].plot([1,12],[0,0], color = 'r', linestyle = '--')
        for i in range(6):
            color = ['blue','blue','orange','orange','green','green']
            marker = ['-',':','-',':','-',':']
            axs[k+1,j].plot(time,-1/100*ret_flow_monthly.iloc[j*24+k*6+i,10*12:11*12], \
                  color = color[i], linestyle = marker[i])
            axs[k+1,j].set_xbound(1,12)
            axs[k+1,j].set_xticks(np.arange(12)+1)
            axs[k+1,j].set_xlabel('month')

for i in range(3):
    axs[0,i].plot(time,bins.iloc[9*12:10*12,3], color = 'blue')
    ax2 = axs[0,i].twinx()             
    ax2.plot(time,irrigation_ts.iloc[i,9*12:10*12], color = 'gray')
    ax2.tick_params(axis = 'y', labelcolor = 'gray')   
    axs[0,i].set_xbound(1,12)
    axs[0,i].set_xticks(np.arange(12)+1)    

plt.tight_layout()

# Baseline flow flux for year = 10 
fig, axs = plt.subplots(nrows=5, ncols=3, figsize=(12, 10))
time = np.arange(12)+1
for j in range(3):
    for k in range(4):
        axs[k+1,j].plot([1,12],[0,0], color = 'r', linestyle = '--')
        for i in range(6):
            color = ['blue','blue','orange','orange','green','green']
            marker = ['-',':','-',':','-',':']
            axs[k+1,j].plot(time,-1/100 * (baseline_monthly.iloc[j*24+k*6+i,9*12:10*12]), \
                      color = color[i], linestyle = marker[i])
            axs[k+1,j].set_xbound(1,12)
            axs[k+1,j].set_xticks(np.arange(12)+1)
            axs[k+1,j].set_xlabel('month')

for i in range(3):
    axs[0,i].plot(time,bins.iloc[9*12:10*12,3], color = 'blue') 
    axs[0,i].set_xbound(1,12)
    axs[0,i].set_xticks(np.arange(12)+1) 

plt.tight_layout()

# Reduced river-aquifer exchange in year = 10 
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 3))
time = np.arange(12)+1
recharge = [0.2*50000, 0.2*100000, 0.2*200000]
for j in range(3):
    for k in range(4):
        for i in range(6):
            color = ['blue','blue','orange','orange','green','green']
            marker = ['o','x','o','x','o','x']
            axs[j].plot(k+1,(np.sum(ret_flow_monthly_inward.iloc[j*24+k*6+i,9*12:10*12]) \
                  - np.sum(baseline_monthly_inward.iloc[j*24+k*6+i,9*12:10*12]))/100, \
                      color = color[i], marker = '.', markersize = 10)
            axs[j].set_xbound(0.5,4.5)
            axs[j].set_ybound(0,-100)
            axs[j].set_yticks([0,-20, -40, -60, -80, -100])  
plt.tight_layout()

# Additional flow to aquifer in year = 10 
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 3))
time = np.arange(12)+1
for j in range(3):
    for k in range(4):
        for i in range(6):
            color = ['blue','blue','orange','orange','green','green']
            marker = ['o','x','o','x','o','x']
            axs[j].plot(k+1,-1*(np.sum(ret_flow_monthly_outward.iloc[j*24+k*6+i,9*12:10*12]) \
                  - np.sum(baseline_monthly_outward.iloc[j*24+k*6+i,9*12:10*12]))/100, \
                      color = color[i], marker = '.', markersize = 10)
            axs[j].plot([0,5],[recharge[j]/100,recharge[j]/100], color = 'r', linestyle = '--')
            axs[j].set_xbound(0.5,4.5)
            axs[j].set_yticks([0, 50, 100, 150, 200, 250, 300, 350, 400])   
plt.tight_layout()


