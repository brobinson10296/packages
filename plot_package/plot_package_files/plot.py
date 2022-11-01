import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axisartist.axislines import SubplotZero
from cycler import cycler

style_list = ['-','--',':']

plt.style.use(['science','notebook']) #from https://github.com/garrettj403/SciencePlots

def plot_function(ax,x, y, plot_label=None, leg_loc=None, plot_color=None, line_style=None, line_width=None,
                  alpha_value=None, x_label=None, y_label=None, x_bounds=None, y_bounds=None):
    ax.plot(x,y,color=plot_color,linestyle=line_style,alpha=alpha_value,label=plot_label,linewidth=line_width)
    ax.set_xlabel(xlabel=x_label)
    ax.set_ylabel(ylabel=y_label)
    ax.set_xlim(x_bounds)
    ax.set_ylim(y_bounds)
    if plot_label != None:
        ax.legend(loc=leg_loc)
    return ax

def scatter_function(ax, x, y, plot_label=None,leg_loc=None, plot_color=None, marker_style=None, marker_size=None,
                     alpha_value=None, x_label=None, y_label=None, x_bounds=None, y_bounds=None):
    ax.scatter(x,y,color=plot_color,marker=marker_style, s=marker_size, alpha=alpha_value, label=plot_label)
    ax.set_xlabel(xlabel=x_label)
    ax.set_ylabel(ylabel=y_label)
    ax.set_xlim(x_bounds)
    ax.set_ylim(y_bounds)
    if plot_label != None:
        ax.legend(loc=leg_loc)
    return ax
