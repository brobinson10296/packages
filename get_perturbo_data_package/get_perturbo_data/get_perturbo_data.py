import numpy as np
import h5py

# reads input parameters from pert_run.in file
def pert_input_param(path):
    with open(path + "pert_pp.in", "r") as file:
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
    num_bands = (band_max - band_min) + 1
    bands_list = [n for n in range(num_bands)]

    return (
        prefix,
        E_min,
        E_max,
        bands_list,
        time_step,
        boltz_nstep,
        boltz_init_e0,
        Ef,
        k_grid,
        carrier,
    )


def read_h5_data_function(h5prefix, boltz_nstep, num_bands, calc_list=["run", "pp"]):

    E_dist, E_pop = [], []

    for calc in calc_list:
        if calc == "run":
            h5file = h5py.File(h5prefix + "_cdyna.h5", "r")
            for tb in range(boltz_nstep + 1):  # the time is boltz_nstep*time_step
                E_dist_tb = []
                for n in range(num_bands):
                    E_dist_n = []
                    E_dist_n.append(
                        np.array(
                            [
                                h5file["band_structure_ryd"][:, n]
                                * h5file["band_structure_ryd"].attrs["ryd2ev"],
                                h5file["dynamics_run_1"]["snap_t_" + str(int(tb))][
                                    :, n
                                ],
                            ]
                        ).T
                    )
                    E_dist_tb.append(E_dist_n)

                E_dist.append(
                    np.array(E_dist_tb).reshape(-1, 2)[
                        np.argsort(np.array(E_dist_tb).reshape(-1, 2)[:, 0])
                    ]
                )

        elif calc == "pp":
            h5file = h5py.File(h5prefix + "_popu.h5", "r")
            for tb in range(boltz_nstep + 1):  # the time is boltz_nstep*time_step
                E_pop_tb = np.array(
                    (
                        h5file["energy_grid_ev"][()],
                        h5file["energy_distribution"]["popu_t" + str(int(tb))][()],
                    )
                ).T
                E_pop.append(E_pop_tb[np.argsort(E_pop_tb[:, 0])])
    h5file.close()

    return np.array(E_dist), np.array(E_pop)


def get_perturbo_data(path):
    (
        prefix,
        E_min,
        E_max,
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
        "band_list": band_list,
        "time_step": time_step,
        "boltz_nstep": boltz_nstep,
        "boltz_init_e0": boltz_init_e0,
        "Ef": Ef,
        "k_grid": k_grid,
        "carrier": carrier,
    }

    E_dist, E_pop = read_h5_data_function(
        path + calc_dic["prefix"],
        calc_dic["boltz_nstep"],
        len(calc_dic["band_list"]),
        calc_list=["run", "pp"],
    )
    return calc_dic, E_dist, E_pop
