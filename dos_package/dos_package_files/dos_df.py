import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def dos_function(dos_input_file=None,OUTCAR=None,shift=0):
    with open(OUTCAR) as f:
        NEDOS=[int(line.split()[5]) for line in f if 'NEDOS' in line][0]

    s_df=pd.read_csv(dos_input_file,nrows=NEDOS,skiprows=1,header=None,delim_whitespace=True,names=['Energy (eV)','s-projection'])
    p_df=pd.read_csv(dos_input_file,nrows=NEDOS,skiprows=NEDOS+3,header=None,delim_whitespace=True,names=['Energy (eV)','p-projection'])
    d_df=pd.read_csv(dos_input_file,nrows=NEDOS,skiprows=2*NEDOS+5,header=None,delim_whitespace=True,names=['Energy (eV)','d-projection'])
    tot_df=pd.read_csv(dos_input_file,nrows=NEDOS,skiprows=3*NEDOS+7,header=None,delim_whitespace=True,names=['Energy (eV)','total'])

    dos_df = pd.merge(pd.merge(pd.merge(s_df,p_df,on='Energy (eV)'),d_df,on='Energy (eV)'),tot_df,on='Energy (eV)')
    
    dos_shfited_df=dos_shift_function(dos_df,shift)
    return dos_shfited_df


def dos_shift_function(dos_df,shift):
    dos_shfited_df=dos_df.copy()
    dos_shfited_df['Energy (eV)']=np.where(dos_shfited_df['Energy (eV)']>0,dos_shfited_df['Energy (eV)']+shift,dos_shfited_df['Energy (eV)'])
    return dos_shfited_df
