import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def mod_exp_function(t, A, tau, t_o, b):
    return A * np.exp(-(t - t_o) / tau) + b


def exp_fit(calc_dic, E_dist, E):

    simulation_time = np.arange(
        0,
        calc_dic["boltz_nstep"] * calc_dic["time_step"] + calc_dic["time_step"],
        calc_dic["time_step"],
    )

    index = np.where(
        E_dist[0][:, 0]
        == (
            E_dist[0][:, 0][
                min(
                    range(len(E_dist[0][:, 0])),
                    key=lambda i: abs(E_dist[0][:, 0][i] - E),
                )
            ]
        )
    )[0][0]
    E_dist_of_interest = E_dist[:, index]
    excitation_index = np.argmax(E_dist_of_interest[:, 1])
    dist_to_fit = E_dist_of_interest[excitation_index:][:, 1]

    t_o_constrain = simulation_time[excitation_index]
    A_constrain = dist_to_fit[0]
    # constrain A to +/- 0.1 and t_o to +/- 1 of value
    bounds = (
        (A_constrain - 1.0, -np.inf, t_o_constrain - 1, 0),
        (A_constrain + 1.0, np.inf, t_o_constrain + 1, np.inf),
    )
    popt, pcov = curve_fit(
        mod_exp_function,
        simulation_time[excitation_index:],
        dist_to_fit,
        p0=[0.05, 30, t_o_constrain, 0],
        bounds=bounds,
    )
    # A,tau,t_o,b=popt[0],popt[1],popt[2],popt[3]
    y_fitted = (
        popt[0] * np.exp(-(simulation_time[excitation_index:] - popt[2]) / popt[1])
        + popt[3]
    )
    r2 = r2_score(dist_to_fit, y_fitted)

    return (
        simulation_time,
        E_dist_of_interest,
        excitation_index,
        dist_to_fit,
        y_fitted,
        popt,
        r2,
    )


def get_tau(calc_dic, E_dist, index):

    simulation_time = np.arange(
        0,
        calc_dic["boltz_nstep"] * calc_dic["time_step"] + calc_dic["time_step"],
        calc_dic["time_step"],
    )

    E_dist_of_interest = E_dist[:, index]
    excitation_index = np.argmax(E_dist_of_interest[:, 1])
    dist_to_fit = E_dist_of_interest[excitation_index:][:, 1]

    t_o_constrain = simulation_time[excitation_index]
    A_constrain = dist_to_fit[0]
    # constrain A to +/- 0.1 and t_o to +/- 1 of value
    bounds = (
        (A_constrain - 1.0, -np.inf, t_o_constrain - 1, 0),
        (A_constrain + 1.0, np.inf, t_o_constrain + 1, np.inf),
    )
    popt, pcov = curve_fit(
        mod_exp_function,
        simulation_time[excitation_index:],
        dist_to_fit,
        p0=[0.05, 30, t_o_constrain, 0],
        bounds=bounds,
    )
    # A,tau,t_o,b=popt[0],popt[1],popt[2],popt[3]
    y_fitted = (
        popt[0] * np.exp(-(simulation_time[excitation_index:] - popt[2]) / popt[1])
        + popt[3]
    )
    r2 = r2_score(dist_to_fit, y_fitted)

    return E_dist_of_interest[0][0], popt[1]
