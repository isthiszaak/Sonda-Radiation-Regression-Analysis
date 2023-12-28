# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 16:12:26 2023

@author: isaac barros
"""


import pandas as pd 
import numpy as np


# =================== Oppening the dataset from SONDA base

df_original = pd.read_csv("C:/Users/isaac/Desktop/Data Science/Sonda/2012/PTR1204ED.csv",sep=";")

df_original = df_original.drop(df_original.columns[3], axis = 1 )

# Headers >= 3.3
#columns = ["id","year","day","min","glo_avg","dir_avg","diff_avg","lw_avg","par_avg","lux_avg","tp_sfc","humid","press","rain","ws_10m","wd_10m"]

# Headers < 3.3
columns = ["id","year","day","min","glo_avg","dir_avg","diff_avg","lw_avg","par_avg","lux_avg","tp_sfc","humid","press","rain","ws_10m","wd_10m"]


df_original.columns = columns

df = df_original 


# =============== Converting to 5 minute interval

aux_minute = 0 

df_aux = pd.DataFrame()

#df_aux = df[["day","min","glo_avg"]]


while aux_minute <= (len(df)/5):
    
    
    df_aux = df_aux.append((df[aux_minute : aux_minute + 5 ].sum().to_frame().T)/5)
    
    aux_minute = aux_minute + 5
    
    
# ================ Converting to hourly interval

aux_hora = 0

df_aux_2 = pd.DataFrame()

while aux_hora <= (len(df)/5):
    
    #list_aux_2.append(sum(list_aux[aux_hora : aux_hora + 12 ])/12)
    
    df_aux_2 = df_aux_2.append((df_aux[aux_hora : aux_hora + 12 ].sum().to_frame().T)/12)

    
    aux_hora = aux_hora + 12
  
# =================

num_days = np.linspace(1,df_aux_2.shape[0]/24, int(df_aux_2.shape[0]/24))

df_final = df_aux_2.reset_index(drop= True)

df_final["day"] = df_final["day"].astype(int)


# ===================== Hour of day column

count = 1 

list_hour = []

while count <= df_aux_2.shape[0]/24 :
    
    list_hour = list_hour + list(np.linspace(0,23,24))
    
    count = count + 1
    
df_final["day hour"] = list_hour

#### SAVING FILE 
df_final.to_csv("C:/Users/isaac/Desktop/Data Science/Sonda/2012/April_hourly.csv")