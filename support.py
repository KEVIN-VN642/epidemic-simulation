# -*- coding: utf-8 -*-
"""
This module contain serveral function which support the main module.
This module is separated so that the main module is not too long, which
support code checking easier.
"""
import math
import random
import pandas as pd
import numpy as np

def parameter_check(m,n,r,k,alpha_infected,alpha_recovered,beta_recovered,beta_death,gamma,N):
    """This function check the validity of each parameters for class Simulate"""
    
    if (alpha_infected <0 or alpha_infected >1 or alpha_recovered<0 or alpha_recovered>1 or (alpha_recovered+alpha_infected)>1):
        raise ValueError("alpha_infected, alpha_recovered must be between 0 and 1, and alpha_infected+alpha_recovered must be less than or equal to 1")
    if (beta_recovered <0 or beta_recovered>1 or beta_death<0 or beta_death>1 or (beta_recovered+beta_death>1)):
        raise ValueError("beta_recover, beta_death must be between 0 and 1, beta_recover+beta_death must be less than or equal to 1")
    if (gamma <0 or gamma >1):
        raise ValueError("gamma must be between 0 and 1")
    if (m<=0 or n<=0 or N<=0 or not(isinstance(m,int)) or not(isinstance(n,int)) or not(isinstance(N,int))):
        raise ValueError("m,n,N must be positive integer")

def initilize_state(m,n,alpha_infected,alpha_recovered):
    """This function initialize disease status of each individual in the network"""
    
    initial_state=pd.DataFrame(columns=range(n),index=range(m)) #disease status
    for i in range(m):
        for j in range(n):
            initial_state.iloc[i,j]=np.random.choice(["I","R","S"],1,True,\
                                              [alpha_infected,alpha_recovered,1-alpha_infected-alpha_recovered])[0]
    return initial_state

def contact_graph(m=40,n=25,r=2,k=4):
    """This function initialize the contact graph for simulations"""
    
    #set up sample space S which is a list of mxn elements indicating mxn individuals
    S=[]     
    for i in range(m):
        for j in range(n):
            S.append((i,j))
    connection_count=0
    
    #creating a list graph containing mxnxk/2 random pairs
    graph=[] 
    while (connection_count<math.floor((m * n * k)/2) -1):
        pair=random.sample(S,2)
        p1=pair[0]
        p2=pair[1]
        if math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)<=r:
            if ([p1,p2] not in graph) and ([p2,p1] not in graph):
                graph.append(pair)
                connection_count+=1
    return graph


def Sim_Nday(N_days,df_status,contact_graph,gamma=0.075,beta_recovered=0.05,beta_death=0.005):
    """This function perform N simulations, each simulation indicates a random process which 
    indicates how disease spread in a day.
    Assume that, who have newly infected within day d will remain its infected status for that day
    And people already get infected at the beginning of day just only change their status at the end of day  
    """
    
    sim_nday_data=[df_status.copy()] #sim_nday_data will contain N+1 dataframe, each dataframe present
    #disease status of all individuals in a day (include initial day:0)
    for d in range(N_days):   
        beginning_day_state=df_status #back up status of individual at beginning of days before simulate
        for pair in contact_graph:
            p1=pair[0]
            p2=pair[1]
            # spread disease between two people p1, p2
            if (df_status.iloc[p1[0],p1[1]]=="I") and (df_status.iloc[p2[0],p2[1]]=="S"):
                df_status.iloc[p2[0],p2[1]]=np.random.choice(["I","S"],1,True,[gamma,1-gamma])[0]
            if (df_status.iloc[p1[0],p1[1]]=="S") and (df_status.iloc[p2[0],p2[1]]=="I"):
                df_status.iloc[p1[0],p1[1]]=np.random.choice(["I","S"],1,True,[gamma,1-gamma])[0]

        #update status of individuals who was infected at the beginning of the day
        for i in range(df_status.shape[0]):
            for j in range(df_status.shape[1]):
                if beginning_day_state.iloc[i,j]=="I":
                    df_status.iloc[i,j]=np.random.choice(["R","D","I"],1,True,[beta_recovered,beta_death,1-beta_recovered-beta_death])[0]
        #add status data to sim_nday_data
        sim_nday_data.append(df_status.copy())
    return sim_nday_data





