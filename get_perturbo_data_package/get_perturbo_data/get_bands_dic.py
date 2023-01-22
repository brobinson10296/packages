import numpy as np

# reads input parameters from pert_run.in file
def pert_input_param(path):
    with open(path + "pert_bands.out", "r") as file:
        for line in file:
            if "band_min:" in line:
                band_min = int(line.split()[1])
                band_max = int(line.split()[-1])
        num_bands = (band_max - band_min) + 1
    return num_bands


def get_k_label(prefix, path, num_points):
    high_sym_kpoints = np.loadtxt(
        path + prefix + "_band.kpt", skiprows=1, usecols=[0, 1, 2]
    )
    kpoints = np.loadtxt(
        path + prefix + ".bands", usecols=[0, 1, 2, 3], max_rows=num_points
    )
    k_xmap_list = []
    for k in kpoints:
        for hsk in high_sym_kpoints:
            if (k[1:4] == hsk).all() == True:
                k_xmap_list.append(k[0])
    # remove duplicates if kpoint appears multiple times
    return sorted(list(set(k_xmap_list)))


def get_bands_dic(prefix, path):
    num_bands = pert_input_param(path)
    flat_E = np.loadtxt(path + prefix + ".bands", usecols=(4))
    E = np.reshape(flat_E, (num_bands, int(len(flat_E) / num_bands)))
    flat_k = np.loadtxt(path + prefix + ".bands", usecols=(0))
    k = np.reshape(flat_k, (num_bands, int(len(flat_k) / num_bands))).T[:, 0]
    k_xmap_list = get_k_label(prefix, path, len(k))
    bands_dic = {"k": k, "n": E, "k_map": k_xmap_list}
    return bands_dic
