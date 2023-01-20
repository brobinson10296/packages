import numpy as np
from scipy import interpolate


def get_dos(file, E_cutoff):
    dos = np.loadtxt(file)
    val_dos = dos[[count for count, E in enumerate(dos[:, 0]) if E >= E_cutoff][0] :]
    return dos, val_dos


# takes in list of energies, Fermi energy, T, and units
def get_fermi_function(E_list, Ef=0, T=300, units="K"):
    if units == "K":
        k = 8.617333262 * 10 ** (-5)  # units of eV/K
    elif units == "eV":
        k = 1
    else:
        print("Need to specify units of eV or K")
    kT = k * T
    fermi_func = [1.0 / (np.exp((E - Ef) / kT) + 1) for E in E_list]
    return np.vstack([E_list, fermi_func]).T


def interpolate_function(x, y, x_range, kind="linear"):
    interp = interpolate.interp1d(x, y, kind="linear")
    y_interp = interp(x_range)
    return y_interp
