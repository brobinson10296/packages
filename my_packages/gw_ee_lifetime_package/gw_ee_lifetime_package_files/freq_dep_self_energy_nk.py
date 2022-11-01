import pandas as pd
import numpy as np

E_disc = 2001

#--------------------------------------------------------------------------------

def get_NBANDSGW_function(OUTCAR_file):
    with open(OUTCAR_file) as f:
        NBANDSGW = np.arange(1,[float(line.split()[1]) for line in f if 'NBANDSGW=' in line][0]+1,1)
    return NBANDSGW

#--------------------------------------------------------------------------------

def get_E_fermi_function(OUTCAR_file):
    with open(OUTCAR_file) as f:
        E_f = [float(line.split()[-1]) for line in f if 'E-fermi' in line][0]
    return E_f

#--------------------------------------------------------------------------------

def get_NKPTS_function(OUTCAR_file):
    with open(OUTCAR_file) as f:
        NKPTS = int([float(line.split()[3]) for line in f if 'NKPTS' in line][0])
    return NKPTS

#--------------------------------------------------------------------------------

def get_E_shift_function(input_file,line_num,E_f,fermi):
    if fermi == False:
        file = open(input_file)
        E_shift,E_shift_label = float(file.readlines()[line_num-1].split()[1]),'E$_{nk}$'
    elif fermi == True:
        E_shift,E_shift_label = E_f, 'E$_F$'
    return E_shift,E_shift_label

#--------------------------------------------------------------------------------

def freq_self_energy_function(input_file=None,line_num=None,E_f=None,fermi_shift=True):
    df = pd.read_csv(input_file,header=None,delim_whitespace=True,
                     skiprows=line_num,nrows=E_disc,names=['E (eV)-E$_{shift}$','Re(Sigma)','Im(Sigma)'])
    E_shift,E_shift_label = get_E_shift_function(input_file,line_num,E_f,fermi_shift)
    df_shift = df - [E_shift,0,0]
    return df_shift

#--------------------------------------------------------------------------------

def k_n_line_num_function(OUTCAR_file=None):
    line_num_band_E_list = []

    NBANDSGW = get_NBANDSGW_function(OUTCAR_file)
    E_f =  get_E_fermi_function(OUTCAR_file)
    NKPTS = get_NKPTS_function(OUTCAR_file)

    with open(OUTCAR_file) as file:
        [line_num_band_E_list.append(count) for count,
                 line in enumerate(file,1) if "selfenergy along real axis" in line]

    k_n_line_num_array = np.array(line_num_band_E_list).reshape(NKPTS,len(NBANDSGW))
    return k_n_line_num_array, E_f

#--------------------------------------------------------------------------------

def pick_k_n_function(k=None,n=None,E_max=None,OUTCAR=None,k_n_line_num_array=None,
                      E_f=None,fermi_shift=True):
    df = freq_self_energy_function(input_file=OUTCAR+'TRUE',
                              line_num=k_n_line_num_array[k-1][n-1],E_f=E_f,fermi_shift=fermi_shift)
    df_fit = df[df['E (eV)-E$_{shift}$'].between(0,E_max)]
    x = df_fit['E (eV)-E$_{shift}$']
    y = -2*df_fit['Im(Sigma)']
    return x,y
