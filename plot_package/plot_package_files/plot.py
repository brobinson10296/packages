import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axisartist.axislines import SubplotZero
from cycler import cycler

style_list = ['-','--',':']

plt.style.use(['science','notebook']) #from https://github.com/garrettj403/SciencePlots

def normalized_colormap_function(simulation_time,time_step,cm_style=cm.bwr):
    simulation_time_list=np.arange(0,simulation_time+1, time_step)
    normalize = mcolors.Normalize(vmin=simulation_time_list.min(),
                                    vmax=simulation_time_list.max())
    colormap = cm_style
    return simulation_time_list, normalize, colormap

def plot_function(ax,x, y, plot_label=None, leg_loc=None, plot_color=None,
                  line_style=None,  line_width=None,
                  marker_style=None, marker_size=None,
                  alpha_value=None, z_order=None, x_label=None, y_label=None, x_bounds=None, y_bounds=None):
    ax.plot(x,y,color=plot_color,linestyle=line_style,linewidth=line_width,
            marker=marker_style,markersize=marker_size,alpha=alpha_value,
            label=plot_label,zorder=z_order)
    ax.set_xlabel(xlabel=x_label)
    ax.set_ylabel(ylabel=y_label)
    ax.set_xlim(x_bounds)
    ax.set_ylim(y_bounds)
    if plot_label != None:
        ax.legend(loc=leg_loc)
    return ax

def scatter_function(ax, x, y, plot_label=None,leg_loc=None, plot_color=None, marker_style=None, marker_size=None,
                     alpha_value=None, z_order=None, x_label=None, y_label=None, x_bounds=None, y_bounds=None):
    ax.scatter(x,y,color=plot_color,marker=marker_style, s=marker_size, alpha=alpha_value, label=plot_label,zorder=z_order)
    ax.set_xlabel(xlabel=x_label)
    ax.set_ylabel(ylabel=y_label)
    ax.set_xlim(x_bounds)
    ax.set_ylim(y_bounds)
    if plot_label != None:
        ax.legend(loc=leg_loc)
    return ax

def fill_function(ax,x, y,plot_color=None,alpha_value=None, x_bounds=None, y_bounds=None):
    ax.fill_between(x,y,color=plot_color,alpha=alpha_value)
    ax.set_xlim(x_bounds)
    ax.set_ylim(y_bounds)
    return ax