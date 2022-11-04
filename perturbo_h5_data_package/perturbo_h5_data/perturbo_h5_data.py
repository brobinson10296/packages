import numpy as np
import h5py

def read_h5_data_function(h5prefix,num_bands):
    calc_list = ['run','pp']

    boltz_nstep = h5py.File(h5prefix+'_cdyna.h5', 'r')['dynamics_run_1']['num_steps'][()]
    time_step = h5py.File(h5prefix+'_cdyna.h5', 'r')['dynamics_run_1']['time_step_fs'][()]

    for calc in calc_list:
        if calc == 'run':
            E_dist = []
            h5file = h5py.File(h5prefix+'_cdyna.h5', 'r')
            for tb in range(boltz_nstep+1): #the time is boltz_nstep*time_step
                E_dist_tb = []
                for n in range(num_bands):
                    E_dist_n = []
                    E_dist_n.append(np.array([h5file['band_structure_ryd'][:,n] * h5file['band_structure_ryd'].attrs['ryd2ev'],
                            h5file['dynamics_run_1']['snap_t_'+str(int(tb))][:,n]]).T)
                    E_dist_tb.append(E_dist_n)

                E_dist.append(np.array(E_dist_tb).reshape(-1,2)[np.argsort(np.array(E_dist_tb).reshape(-1,2)[:, 0])])

        elif calc == 'pp':
            E_pop = []
            h5file = h5py.File(h5prefix+'_popu.h5', 'r')
            for tb in range(boltz_nstep+1): #the time is boltz_nstep*time_step
                E_pop_tb = np.array((h5file['energy_grid_ev'][()],h5file['energy_distribution']['popu_t'+str(int(tb))][()])).T
                E_pop.append(E_pop_tb[np.argsort(E_pop_tb[:, 0])])
    h5file.close()

    return np.array(E_dist), np.array(E_pop), boltz_nstep, time_step
