import math
import numpy as np 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import os 

mpl.rc('axes', titlesize=14)
plt.rc('font', size= 16)

os.chdir('C:/Users/sbferen/Documents/Frontiers_Paper/Analytical_solution_comparison')

data = pd.read_csv("Modflow_statemod_comparison.csv")
params = pd.read_csv("Analytical_params.csv")
bins = np.asarray([np.arange(0,390,30)])

monthly_ret_fraction = np.zeros([12,2])

for i in range(2):
    for j in range(12):
        monthly_ret_fraction[j,i] = 1/(8640*30) * \
        np.sum(data.iloc[bins[0,j]:bins[0,j]+31, i+2]) 

frac_slow = np.sum(monthly_ret_fraction[0:11,1])
frac_fast = np.sum(monthly_ret_fraction[0:11,0])

#### Analytical Solution Script ####
mpl.rc('axes', titlesize=14)
plt.rc('font', size= 14)
length = 20 

# Parameters 
t = np.arange(360*length)+1
base = np.zeros([12,360*length])
term_1 = np.zeros([12,360*length])
term_2 = np.zeros([12,360*length])
term_3 = np.zeros([12,360*length])
term_4 = np.zeros([12,360*length])
term_5 = np.zeros([12,360*length])
term_6 = np.zeros([12,360*length])

for j in range(12):
    for i in range(360*length):
        base[j,i] = math.erfc(params.a[j]/(2*(params.D[j]*t[i])**.5))
        term_1[j,i] = (-1)**2*(math.erfc((2*1*params.c[j]-params.a[j])/(2*(params.D[j]*t[i])**0.5))- \
                             math.erfc((2*1*params.c[j]+params.a[j])/(2*(params.D[j]*t[i])**0.5)))
        term_2[j,i] = (-1)**3*(math.erfc((2*2*params.c[j]-params.a[j])/(2*(params.D[j]*t[i])**0.5)) - \
                             math.erfc((2*2*params.c[j]+params.a[j])/(2*(params.D[j]*t[i])**0.5))) 
        term_3[j,i] = (-1)**4*(math.erfc((2*3*params.c[j]-params.a[j])/(2*(params.D[j]*t[i])**0.5)) - \
                             math.erfc((2*3*params.c[j]+params.a[j])/(2*(params.D[j]*t[i])**0.5)))  
        term_4[j,i] = (-1)**5*(math.erfc((2*4*params.c[j]-params.a[j])/(2*(params.D[j]*t[i])**0.5)) - \
                             math.erfc((2*4*params.c[j]+params.a[j])/(2*(params.D[j]*t[i])**0.5))) 
        term_5[j,i] = (-1)**6*(math.erfc((2*5*params.c[j]-params.a[j])/(2*(params.D[j]*t[i])**0.5)) - \
                             math.erfc((2*5*params.c[j]+params.a[j])/(2*(params.D[j]*t[i])**0.5))) 
        term_6[j,i] = (-1)**7*(math.erfc((2*6*params.c[j]-params.a[j])/(2*(params.D[j]*t[i])**0.5)) - \
                             math.erfc((2*6*params.c[j]+params.a[j])/(2*(params.D[j]*t[i])**0.5))) 
   
            
total = -1*(base+term_1+term_2+term_3+term_4+term_5+term_6)
return_flow = np.copy(total)
return_flow[:,31:] = return_flow[:,31:]-return_flow[:,0:360*length-31]       

bins = np.asarray([np.arange(0,360*length+30,30)])
monthly_return_flow = np.zeros([12,12*length])        
for i in range(12):
    for j in range(12*length):
        monthly_return_flow[i,j] = np.sum(return_flow[i,bins[0,j]:bins[0,j+1]])/30 

five_yr_return_frac= np.sum(monthly_return_flow, axis = 1)

# Figures for analytical solutions 
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12, 10))
c = ['blue','green','orange','red']
for i in range(3):
    for j in range(4):
        axs[i].plot(-1*return_flow[i*4+j,:], color = c[j])
    axs[i].grid(axis = 'y',color = 'grey')
    axs[i].set_xbound(0,365)
    axs[i].set_xticks([0,30,60,90,120,150,180,210,240,270,300,330, \
                       360]) #,390,420,450,480,510,540,570,600,630,660, \
                       #690,720])
#axs[0].legend(['3','10','30','100'], title = 'm/d', loc = 'right')

# Return flow with valley boundary 
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12, 10))
c = ['blue','green','orange','red']
for i in range(3):
    for j in range(4):
        axs[i].plot(-1*total[i*4+j,:], color = c[j])
    axs[i].grid(axis = 'y',color = 'grey')

# Return flow without valley boundary 
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12, 10))
c = ['blue','green','orange','red']
for i in range(3):
    for j in range(4):
        axs[i].plot(base[i*4+j,:], color = c[j])
    axs[i].grid(axis = 'y',color = 'grey')
    axs[i].set_xbound(0,length*12*30)
    #axs[i].set_xticks([0,30,60,90,120,150,180,210,240,270,300,330, \
                       # 360,390,420,450,480,510,540,570,600,630,660, \
                       # 690,720])

# Monthly lag function 
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12, 10))
c = ['black','green','orange','red']
for i in range(3):
    for j in range(1):
        axs[i].plot(np.arange(240)+1,-1*monthly_return_flow[i*4+j+1,:], color = c[j])
    axs[i].grid(axis = 'y',color = 'grey')
    axs[i].set_xbound(1,12*1)
    axs[i].set_xticks([1,2,3,4,5,6,7,8,9,10,11,12]) #, \
                       # 360,390,420,450,480,510,540,570,600,630,660, \
                       # 690,720])
     
# Lag function example 
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12, 10))
c = ['blue','gold','orange','purple','cyan']
coef = [500,1000, 2000, 1000, 500,]

axs[0].plot(np.arange(24)+1, [0,0,0,500,1000,2000,1000,500,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], color = 'k')
axs[0].set_xticks([2,4,6,8,10,12,14,16,18,20,22,24]) 
axs[0].set_xticks([1,3,5,7,9,11,13,15,17,19,21,23], minor = True) 
axs[0].set_xbound(1,24*1)
axs[0].grid(axis = 'y',color = 'grey')

ret_sum = np.zeros([1,240])
for j in range(5):
    axs[1].plot(np.arange(240)+j+4,-1*coef[j]*monthly_return_flow[1,0:240], color = c[j])
    axs[1].grid(axis = 'y',color = 'grey')
    axs[1].set_xbound(1,24*1)
    axs[1].set_xticks([2,4,6,8,10,12,14,16,18,20,22,24])  
    axs[1].set_xticks([1,3,5,7,9,11,13,15,17,19,21,23], minor = True) 
    ret_sum[0,j+4:] += -1*coef[j]*monthly_return_flow[1,0:240-4-j]

axs[2].plot(np.arange(240),ret_sum[0,:], color = 'k')
axs[2].set_xticks([2,4,6,8,10,12,14,16,18,20,22,24]) 
axs[2].set_xticks([1,3,5,7,9,11,13,15,17,19,21,23], minor = True) 
axs[2].set_xbound(1,24*1)
axs[2].grid(axis = 'y',color = 'grey')
                    
########## Analytical return flows calculations using superposition #########

a = np.zeros([36,144+120]) # empty array to populate of dimensions unused_V data (minus field headers)
ret_pattern = np.array([1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8, \
                        9,9,9,10,10,10,11,11,11,12,12,12])-1 # return flow pattern code # for each DIV, from dds


# Define fractional return patterns - 12 patterns from 'return_flow' array 

bins = pd.read_csv("Modflow_stress_periods.csv")
irrigation_ts = pd.DataFrame(np.zeros([9,12*12]))
geom_area = np.array([50000, 100000, 200000]).astype('float')
irr_scaling_coef = [1/3, 2/3, 1]
for i in range(3):
    for k in range(3):
        for j in range(144):
            irrigation_ts.iloc[3*i+k,j] = irr_scaling_coef[k]*geom_area[i] \
            *bins.Irrigation_baseline[j]*(bins.End[j]-bins.Start[j])
annual_irr_total = np.sum(irrigation_ts.iloc[:,9*12:10*12], axis = 1)

irr_pattern = np.array([1,2,3,1,2,3,1,2,3,1,2,3,4,5,6,4,5,6,4,5,6,4,5,6,7,8,9, \
               7,8,9,7,8,9,7,8,9])-1

for i in range (36): # iterate across scenarios (rows)
    for j in range(144): # iterate through time (columns) # rows of unused_V array
        b = np.zeros([1,144+120]) # number of columns in irrigation array 
        ret = (irrigation_ts.iloc[irr_pattern[i],j] * -1 * \
               monthly_return_flow[ret_pattern[i],:]) # return time series for month j 
        ret.shape = (1,120)
        b[0,j:(j+120)] = ret # assign returns from month j to correct indexes in time
        c = np.copy(a[i,:]) # copy current DIV to add new returns to 
        c.shape = (1,144+120)
        c = c + b # add returns to temp return time series c
        c = c.flatten()
        a[i,:] = c # add c to master array of return flows
        
        
superposed_returns = pd.DataFrame(np.copy(a))
superposed_returns.to_csv("Superposed_return_flows.csv")
        
        
        
        