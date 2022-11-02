import numpy as np
import pandas as pd

def find_value_function(input_file,string,index):
    with open(input_file) as f:
        value = [float(line.split()[index]) for line in f if string in line][0]
    return value

def freq_self_energy_function(input_file,line_num,NBANDSGW,E_f,NKPTS):
    header = ["n", "KS-energy (eV)", "QP-energy (eV)", "sigma(KS)",
              "V_xc(KS)", "V^pw_x(r,r')", "Z", "occ.", "Im(Sigma)"]
    df = pd.DataFrame()
    for count,i in enumerate(line_num,1):
        df_i = pd.read_csv(dat_dir+input_file,delim_whitespace=True,
                         skiprows=i,nrows=NBANDSGW,names=header)
        k_i = [count]*NBANDSGW
        df_i.insert(1, "k", k_i, True)
        df = pd.concat([df,df_i],ignore_index=True)

    #make column for state nk that subtracts KS-energy by the Fermi energy
    E_f_list = [E_f]*NBANDSGW*NKPTS
    df_E_minus_E_f = df['KS-energy (eV)']-E_f_list
    df.insert(3,'KS-EF (eV)',df_E_minus_E_f,True)

    #make column for state nk that subtracts QP-energy by the Fermi energy
    E_f_list = [E_f]*NBANDSGW*NKPTS
    df_E_minus_E_f = df['QP-energy (eV)']-E_f_list
    df.insert(5,'QP-EF (eV)',df_E_minus_E_f,True)

    return df

def get_line_num_function(input_file):
    line_num_list = []
    match_string = " band No.  KS-energies  QP-energies   sigma(KS)   V_xc(KS)     V^pw_x(r,r')   Z   occupation Imag(sigma)"
    with open(input_file) as file:
        [line_num_list.append(count) for count,
                 line in enumerate(file,1) if " ".join(match_string.split()) in " ".join(line.split())]
    return line_num_list

def freq_independent_self_energy_function(input_file):

    NBANDSGW = int(find_value_function(input_file,'NBANDSGW=',1))
    E_f = find_value_function(input_file,'E-fermi',-1)
    NKPTS = int(find_value_function(input_file,'NKPTS',3))

    line_num_list = get_line_num_function(input_file)

    df = freq_self_energy_function(input_file,line_num_list,NBANDSGW)
    return df
