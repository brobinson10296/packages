import numpy as np
import pandas as pd
from scipy.optimize import curve_fit as curve_fit

hbar = 6.582 * (10 ** (-1))  # eV/fs


def model_quad_function(x, a):
    return a * x**2


def get_ee_lifetimes_function(alpha, disc, E_max):
    E_array = np.arange(disc, E_max + disc, disc)
    ee_lifetime = np.array([hbar / (alpha * (E**2)) for E in E_array])
    return E_array, ee_lifetime


def fit_function(df, E_to_fit, E_fit_max, E_max=100):
    df_fit = df[(df[E_to_fit] >= 0) & (df[E_to_fit] <= E_fit_max)]

    x = df_fit[E_to_fit]
    y = -2 * df_fit["Im(Sigma)"]

    alpha = curve_fit(model_quad_function, x, y)[0][0]  # fs*ev^2
    E_fermi_liq, ee_fermi_liq = get_ee_lifetimes_function(alpha, 0.01, E_max)

    return alpha, np.vstack([E_fermi_liq, ee_fermi_liq]).T
