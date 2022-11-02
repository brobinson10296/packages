import numpy as np
import pandas as pd
from itertools import islice

def find_value_function(input_file,string,index):
    with open(input_file) as f:
        value = [float(line.split()[index]) for line in f if string in line][0]
    return value

def kn_line_num_array_function(input_file,NKPTS,NBANDSGW):
    nk_E_line_num_list = []
    with open(input_file) as file:
        [nk_E_line_num_list.append([count,float(line.split()[1])]) for count,
            line in enumerate(file,1) if "selfenergy along real axis" in line]
    kn_line_num_array = np.array(nk_E_line_num_list)[:,0]
    kn_E_array = np.array(nk_E_line_num_list)[:,1]

    return kn_line_num_array,kn_E_array

def freq_self_energy_df_function(input_file,kn_line_num_array,kn_E_array,NBANDSGW,NKPTS,E_f,disc=2001):
    self_energy_list = []
    for line_num in kn_line_num_array:
        with open(input_file) as file:
            lines = islice(file, int(line_num)-1, int(line_num)+disc) # or whatever ranges
            for line in lines:
                [self_energy_list.append([float(i) for i in line.split()]) for line in lines]
    header=['E (eV)','Re(Sigma)','Im(Sigma)']
    df_i = pd.DataFrame(self_energy_list,columns=header)

    #make columns for labeling n and k
    n = np.array([[i]*(disc) for i in range(1,NBANDSGW+1)]*NKPTS).flatten()
    k = np.array([[[i]*(disc)]*NBANDSGW for i in range(1,NKPTS+1)]).flatten()
    df_nk = pd.DataFrame({'n': n, 'k': k}, columns=['n', 'k'])

    #make column for state nk that subtracts freq. by the Fermi energy
    E_f_list = [E_f]*NBANDSGW*NKPTS*disc
    df_E_minus_E_f = df_i['E (eV)']-E_f_list
    df_i.insert(1,'E-EF (eV)',df_E_minus_E_f,True)

    #make column for state nk that subtracts freq. by the state energy
    nk_E = np.array([[i]*disc for i in kn_E_array.tolist()]).flatten()
    df_E_minus_Enk = df_i['E (eV)']-nk_E
    df_i.insert(2,'E-Enk (eV)',df_E_minus_Enk,True)

    df = pd.concat([df_nk,df_i],axis=1)

    return df

def freq_dependent_self_energy_function(input_file):
    NBANDSGW = int(find_value_function(input_file,'NBANDSGW=',1))
    E_f = find_value_function(input_file,'E-fermi',-1)
    NKPTS = int(find_value_function(input_file,'NKPTS',3))
    kn_line_num_array, kn_E_array = kn_line_num_array_function(input_file,NKPTS,NBANDSGW)
    df = freq_self_energy_df_function(input_file,kn_line_num_array,kn_E_array,NBANDSGW,NKPTS,E_f)
    return df
