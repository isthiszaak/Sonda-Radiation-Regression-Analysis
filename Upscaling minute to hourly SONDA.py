# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 16:15:26 2023

@author: isaac barros
"""


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapz


# ========================================================================
# ==============  Oppening the dataset from SONDA Base ===================
# ========================================================================

# Feec
#df_original = pd.read_csv("C:/Users/isaac/OneDrive/Área de Trabalho/SONDA - Petrolina/2015/PTR1505ED.csv",sep=";")

# Pessoal
df_original = pd.read_csv("C:/Users/isaac/Desktop/Mestrado/Dados SONDA/Sonda/2012/PTR1204ED.csv",sep=";")

# Headers >= 3.3
#columns = ["id","year","day","min","glo_avg","dir_avg","diff_avg","lw_avg","par_avg","lux_avg","tp_sfc","humid","press","rain","ws_10m","wd_10m"]

# Headers < 3.3
columns = ["id","year","day","min","glo_avg","dir_avg","diff_avg","lw_avg","par_avg","lux_avg","tp_sfc","humid","press","rain","ws_10m","wd_10m"]
df_original = df_original.drop(df_original.columns[3], axis = 1 ) # For years <= 2015, enable this command line


df_original.columns = columns

df = df_original.copy() 

# ========================================================================
# ===================  Upscaling in the Database =========================
# ========================================================================


# =============== Ajusdment in the negative values

df["glo_avg"] = df["glo_avg"].apply(lambda x: max(0, x))
df["par_avg"] = df["par_avg"].apply(lambda x: max(0, x))
df["lux_avg"] = df["lux_avg"].apply(lambda x: max(0, x))

# =============== Converting to 5 minute interval ============================

aux_minute = 0 

df_aux = pd.DataFrame()

#df_aux = df[["day","min","glo_avg"]]


while aux_minute <= (len(df)):
    
    
    #df_aux = df_aux.append((df[aux_minute : aux_minute + 5 ].sum().to_frame().T)/5)
    
    df_aux = pd.concat( [df_aux,(df[aux_minute : aux_minute + 5 ].sum().to_frame().T)/5] ,ignore_index = True)
    
    aux_minute = aux_minute + 5
    
    #print(aux_minute)

df_aux["min"] = df_aux["min"] + 2

# ================ Converting to hourly interval =============================

aux_hora = 0

df_aux_2 = pd.DataFrame()

#while aux_hora <= (len(df)/5):
while aux_hora <= (df_aux.shape[0] - 1):
     
    #list_aux_2.append(sum(list_aux[aux_hora : aux_hora + 12 ])/12)
    
    #df_aux_2 = df_aux_2.append((df_aux[aux_hora : aux_hora + 12 ].sum().to_frame().T)/12)
    df_aux_2 = pd.concat([df_aux_2,(df_aux[aux_hora : aux_hora + 12 ].sum().to_frame().T)/12],ignore_index=True)
    
    aux_hora = aux_hora + 12
    
    
# ========================================================================
# ================== HOURLY DATASET ADJUSMENTS ===========================
# ========================================================================

# ========= Ajusting "Day" column 

num_days = np.linspace(1,df_aux_2.shape[0]/24, int(df_aux_2.shape[0]/24))

df_final_hourly = df_aux_2.reset_index(drop= True)

df_final_hourly["day"] = df_final_hourly["day"].astype(int)


# ======== Inserting "Hour of day" column

count = 1 
    
list_hour = []

while count <= df_aux_2.shape[0]/24 :
    
    list_hour = list_hour + list(np.linspace(0,23,24))
    
    count = count + 1
    
df_final_hourly["day hour"] = list_hour

# ======== Rain ocurrency in that hour (flag) 

df_final_hourly.loc[df_final_hourly['rain'] > 0, 'rain'] = 1  # ajusting the hourly flag of rain occurency

# ========================================================================
# =================== DAILY DATASET ADJUSMENTS ===========================
# ========================================================================

# ============== Creating dataset 

df_final_daily = df_final_hourly.groupby(['id','year','day'], as_index= False).sum()
df_final_daily = df_final_daily.drop(df_final_daily.index[0])



df_final_daily['humid'] = df_final_daily['humid']/24 # ajusting the average daily humid percentage
df_final_daily['tp_sfc'] = df_final_daily['tp_sfc']/24 # ajusting the average daily temperature percentage
df_final_daily['press'] = df_final_daily['press']/24 # ajusting the average daily atmospheric pressure percentage
df_final_daily['ws_10m'] = df_final_daily['ws_10m']/24 # ajusting the average daily wind speed percentage
df_final_daily['wd_10m'] = df_final_daily['wd_10m']/24 # ajusting the average daily wind direction percentage


# ================= Rain Analysis (flag for a raining day)

# list of days that contains rain between 9 and 20

days_with_rain = df_final_hourly[(df_final_hourly['rain'] > 0) & (df_final_hourly['day hour'] >= 9) & (df_final_hourly['day hour'] <= 20) ]['day'].unique()

df_final_daily['rain'] = 0 # cleaning column 

df_final_daily.loc[df_final_daily['day'].isin(days_with_rain), 'rain'] = 1 #assign flag to column

# ========================================================================
# ======================= Saving Files ===================================
# ========================================================================

# FEEC
#df_final_hourly .to_csv("C:/Users/isaac/OneDrive/Área de Trabalho/SONDA - Petrolina/2015/May_hourly.csv")
#df_final_daily .to_csv("C:/Users/isaac/OneDrive/Área de Trabalho/SONDA - Petrolina/2015/May_daily.csv")

# Pessoal
df_final_hourly.to_csv("C:/Users/isaac/Desktop/Data Science/Sonda/2012/April_hourly.csv")
df_final_daily.to_csv("C:/Users/isaac/Desktop/Data Science/Sonda/2012/April_daily.csv")


# ========================================================================
# ====================== Ploting Charts ==================================
# ========================================================================
'''
count = 0

# ========= Hourly irradiance chart

while count < df_final_hourly.shape[0]:
    
    x = df_final_hourly["day hour"][count: count + 24]
    y = df_final_hourly["glo_avg"][count: count + 24]
    
    plt.plot(x,y)
    area = trapz(y, x)
    
 #   print("Area Dia ",str(df_final_hourly["day"][count + 23]),":", round(area,2))
    
       
    count = count + 24
       
plt.title("Hourly Chart Irradiance")
plt.show()

# ======== Daily chart irradiance

plt.plot(df_final_daily["day"],df_final_daily["glo_avg"])

plt.title("Daily Chart Irradiance")
plt.ylim([0, 8000])
plt.show()


# ========= Hourly humidity chart

count = 0

while count <= (df_final_hourly.shape[0]):
    x = df_final_hourly["day hour"][count: count + 24]
    y = df_final_hourly["humid"][count: count + 24]
    
    plt.plot(x,y)
    #plt.legend(loc = 'lower center', ncols = 3)
    
    count = count + 24

plt.title("Hourly Chart Humid ")
plt.ylim([0, 100])
plt.show()

# ========= Original 1 minute step Global Radiation chart

count = 0

while count < (df_original.shape[0]): # - 
    
    x = df_original["min"][count: count + 1540]
    y = df_original["glo_avg"][count: count + 1540]
   
      
    plt.plot(x,y)
    
    count = count + 1540

plt.title("Original 1 minute step Global Radiation - May/2015")
plt.ylim([-10, 10])
plt.xlabel("Day Minute")
plt.ylabel("Global Average Radiation (Wm-2)")
plt.show()
'''