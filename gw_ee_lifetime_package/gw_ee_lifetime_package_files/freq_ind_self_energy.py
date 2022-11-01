import numpy as np
import pandas as pd

def get_NBANDSGW_function(input_OUTCAR):
    with open(input_OUTCAR) as f:
        NBANDSGW = np.arange(1,[float(line.split()[1]) for line in f if 'NBANDSGW=' in line][0]+1,1)
    return NBANDSGW

def get_fermi_energy_function(input_OUTCAR):
    with open(input_OUTCAR) as f:
        E_f = [float(line.split()[-1]) for line in f if 'E-fermi' in line][0]
    return E_f

def freq_self_energy_function(input_file,line_num,NBANDSGW):
    header = ["band #", "KS-energy (eV)", "QP-energy (eV)", "sigma(KS)",
              "V_xc(KS)", "V^pw_x(r,r')", "Z", "occ.", "Im(Sigma)"]
    df = pd.DataFrame()
    for count,i in enumerate(line_num,1):
        df_i = pd.read_csv(input_file,delim_whitespace=True,
                         skiprows=i,nrows=len(NBANDSGW),names=header)
        k_i = [count]*len(NBANDSGW)
        df_i.insert(1, "kpoint", k_i, True)
        df = pd.concat([df,df_i],ignore_index=True)
    return df

def get_line_num_function(input_file):
    line_num_list = []
    match_string = " band No.  KS-energies  QP-energies   sigma(KS)   V_xc(KS)     V^pw_x(r,r')   Z   occupation Imag(sigma)"
    with open(input_file) as file:
        [line_num_list.append(count) for count,
                 line in enumerate(file,1) if " ".join(match_string.split()) in " ".join(line.split())]
    return line_num_list

def freq_ind_self_energy_function(input_OUTCAR=None):

    data = []

    E_f = get_fermi_energy_function(input_OUTCAR)
    NBANDSGW = get_NBANDSGW_function(input_OUTCAR)
    line_num_list = get_line_num_function(input_OUTCAR)

    df = freq_self_energy_function(input_OUTCAR,line_num_list,NBANDSGW)
    return df, E_f
