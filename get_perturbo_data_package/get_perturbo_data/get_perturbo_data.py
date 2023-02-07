import numpy as np
import h5py
import scipy
from scipy import interpolate


# reads input parameters from pert_run.in file
def pert_input_param(path):
    Ef = None  # set if just a guassian calc
    with open(path + "pert_run.in", "r") as file:
        for line in file:
            if "prefix" in line:
                prefix = line.split()[2].replace("'", "")
            if "boltz_emin" in line:
                E_min = float(line.split()[2])
            if "boltz_emax" in line:
                E_max = float(line.split()[2])
            if "band_min" in line:
                band_min = int(line.split()[2])
            if "band_max" in line:
                band_max = int(line.split()[2])
            if "time_step" in line:
                time_step = float(line.split()[2])
            if "boltz_nstep" in line:
                boltz_nstep = int(line.split()[2])
            if "boltz_init_e0" in line:
                boltz_init_e0 = float(line.split()[2])
            if "E_fermi" in line:
                Ef = float(line.split()[2])
            if "boltz_kdim(1)" in line:
                k_grid = int(line.split()[2])
            if "hole=.true." in line.replace(" ", ""):
                carrier = "Hole"
            else:
                carrier = "Electron"
    band_index = np.arange(int(band_min), int(band_max) + 1, 1)
    num_bands = (band_max - band_min) + 1
    bands_list = [n for n in range(num_bands)]

    return (
        prefix,
        E_min,
        E_max,
        band_index,
        bands_list,
        time_step,
        boltz_nstep,
        boltz_init_e0,
        Ef,
        k_grid,
        carrier,
    )


def get_cc_function(prefix):
    t_cc = np.loadtxt(prefix + "_cdyna.dat", skiprows=1, usecols=(1, 2))
    return t_cc


def get_dos_function(prefix):
    E_dos = np.loadtxt(prefix + ".dos", skiprows=1)
    return E_dos


def read_h5_data_function(
    h5prefix, boltz_nstep, time_step, E_min, E_max, chunk, calc_list=["run", "pp"]
):

    if chunk == None and time_step >= 1:
        chunk = 1
    elif chunk == None and time_step < 1:
        chunk = int(1 / time_step)

    E_dist, E_pop = [], []
    interp_E_dist, interp_E_pop = [], []

    for calc in calc_list:
        if calc == "run":
            h5file = h5py.File(h5prefix + "_cdyna.h5", "r")
            E_dist = []
            energy_ev = np.array(
                h5file["band_structure_ryd"][:]
                * h5file["band_structure_ryd"].attrs["ryd2ev"]
            ).flatten()

            for tb in range(boltz_nstep + 1):
                if tb % chunk == 0:  # implementted for help reduce memory isues
                    dist_func = np.array(
                        h5file["dynamics_run_1"]["snap_t_" + str(tb)][:]
                    ).flatten()

                    E_dist_tb = np.vstack((energy_ev, dist_func)).T
                    E_dist.append(E_dist_tb[E_dist_tb[:, 0].argsort()])

                    disc = 0.001
                    interp_E = np.arange(E_min, E_max + disc, disc)
                    interp_dis_func = interpolate.interp1d(
                        energy_ev, dist_func, fill_value="extrapolate"
                    )
                    interp_dis = interp_dis_func(interp_E)
                    interp_E_tb = np.vstack((interp_E, interp_dis)).T
                    interp_E_dist.append(interp_E_tb)

            h5file.close()

        elif calc == "pp":
            h5file = h5py.File(h5prefix + "_popu.h5", "r")
            for tb in range(boltz_nstep + 1):  # the time is boltz_nstep*time_step
                if tb % chunk == 0:  # implementted for help reduce memory isues
                    E_pop_tb = np.array(
                        (
                            h5file["energy_grid_ev"][()],
                            h5file["energy_distribution"]["popu_t" + str(int(tb))][()],
                        )
                    ).T
                    E_pop.append(E_pop_tb[np.argsort(E_pop_tb[:, 0])])
            h5file.close()

    return np.array(E_dist), np.array(interp_E_dist), np.array(E_pop), chunk


def get_perturbo_data(path, chunk=None):
    (
        prefix,
        E_min,
        E_max,
        band_index,
        band_list,
        time_step,
        boltz_nstep,
        boltz_init_e0,
        Ef,
        k_grid,
        carrier,
    ) = pert_input_param(path)

    calc_dic = {
        "prefix": prefix,
        "E_min": E_min,
        "E_max": E_max,
        "band_index": band_index,
        "band_list": band_list,
        "time_step": time_step,
        "boltz_nstep": boltz_nstep,
        "boltz_init_e0": boltz_init_e0,
        "Ef": Ef,
        "k_grid": k_grid,
        "carrier": carrier,
    }

    E_dos = get_dos_function(path + prefix)
    t_cc = get_cc_function(path + prefix)

    E_dist, interp_E_dist, E_pop, chunk = read_h5_data_function(
        path + calc_dic["prefix"],
        calc_dic["boltz_nstep"],
        calc_dic["time_step"],
        calc_dic["E_min"],
        calc_dic["E_max"],
        chunk=chunk,
        calc_list=["run", "pp"],
    )

    calc_dic.update(
        {
            "E_dist": E_dist,
            "interp_E_dist": interp_E_dist,
            "E_pop": E_pop,
            "t_cc": t_cc,
            "E_dos": E_dos,
            "chunk": chunk,
        }
    )
    return calc_dic
