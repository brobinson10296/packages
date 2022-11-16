import os
import numpy as np
import h5py
import math
import scipy
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt

#******************************calculation details******************************
#simulation dependent!
def get_carrier_time_step_function(prefix,h5_dir):
    #really do not need these values unless you want to know the max time
    #elec_boltz_nstep = h5py.File('CuI_elec_cdyna.h5', 'r')['dynamics_run_1']['num_steps'][()]
    #hole_boltz_nstep = h5py.File('CuI_hole_cdyna.h5', 'r')['dynamics_run_1']['num_steps'][()]

    elec_time_step = h5py.File(h5_dir+prefix+'_elec_cdyna.h5', 'r')['dynamics_run_1']['time_step_fs'][()]
    hole_time_step = h5py.File(h5_dir+prefix+'_hole_cdyna.h5', 'r')['dynamics_run_1']['time_step_fs'][()]

    return elec_time_step, hole_time_step

simulation_time = [0,1000]#,2000,3000,4000,5000,6000,7000,8000,9000,10000] #fs max = boltz_nstep*time_step
#vasp inputs
NBANDS, NBVALOPT, NBCONOPT = 16, 9, 7
vasp_VBM, vasp_CBM = 4.328192, 5.445130 #eV
#for interpolation
E_min, E_max = -100, 100 #eV

#******************************Extend E range for Transmatrix interpolation******************************
def extend_E(carrier_type_E_occ, num_bands, carrier):
    carrier_E_occ = []

    if carrier == 'elec':
        occ, adjust_bands = 0, (NBANDS-NBCONOPT+1)
    elif carrier == 'hole':
        occ, adjust_bands = 1, (NBVALOPT-num_bands+1)

    for i in range(num_bands):
        carrier_E_occ_min=np.append([[E_min,occ]],carrier_type_E_occ[i],axis=0)
        carrier_E_occ_min_max=np.append(carrier_E_occ_min,[[E_max,occ]],axis=0)
        carrier_E_occ.append(carrier_E_occ_min_max)

    return carrier_E_occ, np.arange(0,num_bands)+adjust_bands

#******************************Get data from h5 pertubro file******************************
def get_E_occ_from_pert(prefix,h5_dir,simulation_step,carrier):
    carrier_type_E_occ = []
    carrier_h5 = h5py.File(h5_dir+prefix+'_'+carrier+'_cdyna.h5', 'r')
    ryd2ev = carrier_h5['band_structure_ryd'].attrs['ryd2ev']
    num_bands = len(carrier_h5['band_structure_ryd'][0])

    for n in range(num_bands):

        perturbo_E = carrier_h5['band_structure_ryd'][:,n] * ryd2ev
        #gets band n occupation
        #simulation step is simulation_time/time_step
        perturbo_occ = carrier_h5['dynamics_run_1']['snap_t_'+str(simulation_step)][0:,n]
        #put in order of energy for each band
        E_occ_i = np.stack((perturbo_E,perturbo_occ),axis=1)[np.stack((perturbo_E,perturbo_occ),axis=1)[:, 0].argsort()]
        carrier_type_E_occ.append(E_occ_i)

    return extend_E(carrier_type_E_occ, num_bands, carrier)

#******************************#linear interpolation with scipy******************************
def linear_interp(interp_E,E,occ):
    interp = interpolate.interp1d(E, occ, kind='linear')
    interp_occ = interp(interp_E)
    return interp_occ

def t_dependent_optics(prefix,h5_dir,Trans_dir,elec_step,hole_step,t_zeros):
    if elec_step != hole_step:
        print('ERROR times are not equal!')

    elec_E_occ, cond_bands = get_E_occ_from_pert(prefix,h5_dir,elec_step,'elec')
    hole_E_occ, val_bands = get_E_occ_from_pert(prefix,h5_dir,hole_step,'hole')
    #******************************read in Transmatrix******************************
    transmatrix = np.loadtxt(Trans_dir+'Transmatrix_NEW')
    n_i_occ, n_f_occ = [], []
    transition_index_list = [['n_f', 1, 3, n_f_occ],['n_i', 2, 4, n_i_occ]]
    #******************************shift to match energies******************************
    VBM_shift_to_pert = vasp_VBM - hole_E_occ[0][:,0][-2] # -2 because of 100 tacked onto end
    CBM_shift_to_pert = vasp_CBM - elec_E_occ[0][:,0][1] # 1 because of -100 tacked onto end

    for trans_index in transition_index_list:
        for i in transmatrix:
            #valence bands
            if int(i[trans_index[1]]) <= val_bands[-1]:
                if int(i[trans_index[1]]) in val_bands:
                    n_i = int(i[trans_index[1]])-(NBVALOPT-len(val_bands)+1) #perturbo band
                    E = i[trans_index[2]]-VBM_shift_to_pert
                    occ = linear_interp(E,hole_E_occ[n_i][:,0],hole_E_occ[n_i][:,1])
                else:
                    occ = 1
                trans_index[3].append(float(occ))
            #conduction bands
            if int(i[trans_index[1]]) >= cond_bands[0]:
                if int(i[trans_index[1]]) in cond_bands:
                    n_i = int(i[trans_index[1]])-(NBANDS-NBCONOPT+1) #perturbo band index
                    E  = i[trans_index[2]]-CBM_shift_to_pert
                    occ = linear_interp(E,elec_E_occ[n_i][:,0],elec_E_occ[n_i][:,1])
                else:
                    occ = 0
                trans_index[3].append(float(occ))

    #******************************write Transmatrix with occ******************************
    time_list=[t_zeros]*len(n_f_occ)
    df_t = pd.DataFrame(np.array([transmatrix[:,0],time_list,transmatrix[:,1],transmatrix[:,2],
                                            n_f_occ, n_i_occ,transmatrix[:,3],transmatrix[:,4],
                                            transmatrix[:,5],transmatrix[:,6],transmatrix[:,7],
                                            transmatrix[:,8],transmatrix[:,9],transmatrix[:,10],
                                            transmatrix[:,11]]).T)
    return df_t
    '''
    path = '../dat_files/'
    if not os.path.exists(path):  #check if dir exists
        os.makedirs(path)
    outfile = 'transmatrix_with_occ_'+t_zeros+'fs.dat'
    test = np.savetxt(path+outfile,(np.array([transmatrix[:,0],transmatrix[:,1],transmatrix[:,2],
                                            n_f_occ, n_i_occ,transmatrix[:,3],transmatrix[:,4],
                                            transmatrix[:,5],transmatrix[:,6],transmatrix[:,7],
                                            transmatrix[:,8],transmatrix[:,9],transmatrix[:,10],
                                            transmatrix[:,11]])).T,
                                            fmt='%1.12e %d %d %1.12e %1.12e %1.12e %1.12e %1.12e %1.12e %1.12e %1.12e %1.12e %1.12e %1.12e')
    '''
def get_transmatrix_with_occ_function(prefix,simulation_time,h5_dir,Trans_dir,message='y'):
    elec_time_step, hole_time_step = get_carrier_time_step_function(prefix,h5_dir)
    df=pd.DataFrame()
    for t in simulation_time:
        if message.lower()=='y':
            print('\n*************************************\nLooking at time',t,
                 'fs [elec step ',str(int(t/elec_time_step))+'| hole step ',
                  str(int(t/hole_time_step))+']\n*************************************\n')
        t_zeros = str(t).zfill(len(str(max(simulation_time)))) #gets leading zeros for output file names

        df_t = t_dependent_optics(prefix,h5_dir,Trans_dir,int(t/elec_time_step),
                           int(t/hole_time_step),t_zeros)
        df=pd.concat([df,df_t])

    header=['-','t (fs)','n$_f$','n$_i$','f$_{occ}$','i$_{occ}$','E$_f$','E$_i$',
            'Re(px)','Im(px)','Re(py)','Im(py)',
            'Re(pz)','Im(pz)','weight']
    df.columns = header
    return df
