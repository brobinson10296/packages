import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_spectrum(df_trans_with_occ,t_list,spec_type='avg',volume=56.27,
                     sigma=0.10,Emax=20.0,Emin=0,Trans_Min=0.0,Trans_Max=20.0,
                     scissor=0,CBM_index=10,VBM_index=9,GRID=10000):
    ######## Constants and Coefficients for Dielectric Function Calc ########
    hr = 27.2116
    bohr = 0.529177249
    pi = 3.14159
    fac = 8.*pi**2*hr**3*bohr**3/volume
    hbareta = 4.*0.69314718/(sigma**2)
    lfac = 2*fac/pi
    KB = 8.61733E-5
    ######## Prep Grids for dielectric function ########
    Energy = np.linspace(Emin,Emax,GRID)
    all_list=[]
    ########################################################
    df=pd.DataFrame()
    for t in t_list:
        tot_curve_x = [0]*len(Energy)
        tot_curve_x_real = [0]*len(Energy)
        tot_curve_y = [0]*len(Energy)
        tot_curve_z = [0]*len(Energy)
        tot_curve_ave = [0]*len(Energy)

        t_zeros = str(t).zfill(len(str(max(t_list))))
        df_t=df_trans_with_occ[df_trans_with_occ['t (fs)']==t_zeros].to_numpy().astype(float)
        for count,trans_i in enumerate(df_t):
            if (trans_i[6] > trans_i[7] and trans_i[6]-trans_i[7] >
                    Trans_Min and trans_i[6]-trans_i[7] < Trans_Max):
                PX = np.sqrt(trans_i[8]**2+trans_i[9]**2)
                PY = np.sqrt(trans_i[10]**2+trans_i[11]**2)
                PZ = np.sqrt(trans_i[12]**2+trans_i[13]**2)
                dE = trans_i[6]-trans_i[7]
                #make fix here!
                #if n_i is valene and n_f is conduction add scissor, else no scissor!
                ddE = dE+scissor
                Fermi_Weight = (1.-trans_i[4])*(trans_i[5])
                if Fermi_Weight > 1.0:
                    print('WARNING!!!!')

                #For Transmatrix_NEW the k-point weight is the last column not the first!
                MX2 = Fermi_Weight*trans_i[14]*((ddE/dE)*(ddE/dE))*(PX/ddE)**2
                MY2 = Fermi_Weight*trans_i[14]*((ddE/dE)*(ddE/dE))*(PY/ddE)**2
                MZ2 = Fermi_Weight*trans_i[14]*((ddE/dE)*(ddE/dE))*(PZ/ddE)**2
                MA2 = (MX2+MY2+MZ2)/3.
                x_real = np.real(MX2*lfac*ddE/(ddE**2-(Energy+1j*sigma)**2))
                x = np.imag(MX2*lfac*ddE/(ddE**2-(Energy+1j*sigma)**2))

                y_real = np.real(MY2*lfac*ddE/(ddE**2-(Energy+1j*sigma)**2))
                y = np.imag(MY2*lfac*ddE/(ddE**2-(Energy+1j*sigma)**2))

                z_real = np.real(MZ2*lfac*ddE/(ddE**2-(Energy+1j*sigma)**2))
                z = np.imag(MZ2*lfac*ddE/(ddE**2-(Energy+1j*sigma)**2))
                av = np.imag(MA2*lfac*ddE/(ddE**2-(Energy+1j*sigma)**2))

                tot_curve_ave += av
                tot_curve_x += x
                tot_curve_y += y
                tot_curve_z += z
                tot_curve_x_real += x_real

        if spec_type.lower()=='avg':
            all_list.append(tot_curve_ave)
        elif spec_type.lower()=='x':
            all_list.append(tot_curve_x)
        elif spec_type=='y':
            all_list.append(tot_curve_y)
        elif spec_type.lower()=='z':
            all_list.append(tot_curve_z)


    df=pd.DataFrame(np.array(all_list).T,columns=t_list)
    df.insert(0,"E (eV)",Energy,True)
    return df
