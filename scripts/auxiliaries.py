import numpy as np
import matplotlib.pyplot as plt
import plotly
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as subplt
from mpl_toolkits.mplot3d import Axes3D, axes3d
from scipy import interpolate
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

data_sets = {
    'model parameters':
        'https://raw.githubusercontent.com/olegmaxus/mace-project-groundwater/master/data/ModelParameters.csv',
    'model parameters new':
        'https://raw.githubusercontent.com/olegmaxus/mace-project-groundwater/master/data/ModelParametersReformatted.csv',
    'springs':
        'https://raw.githubusercontent.com/olegmaxus/mace-project-groundwater/master/data/datasetSptrings.csv'}


def load_data_frames(which: str = 'null'):

    ret_status = {'model parameters': pd.read_csv(data_sets['model parameters']),
                  'model parameters new': pd.read_csv(data_sets['model parameters new']),
                  'springs': pd.read_csv(data_sets['springs'])}

    if which == 'null':
        return ret_status
    else:
        return ret_status[which]


df = load_data_frames('model parameters new')
print(df['2020'][0])


def define_equilibrium_surface(year: str) -> tuple:

    # loading a data frame #

    df = load_data_frames(which='model parameters new')

    n = np.linspace(-1.2, 1.2, 48)
    gp = np.linspace(-1.2, 1.2, 48)
    N, GP = np.meshgrid(n, gp)
    a, b = df[year][0], df[year][1]
    S = a * GP ** 3 + b * GP * N
    S[S > 1.5] = np.nan
    S[S < -1.5] = np.nan
    return N, S, GP


def plot_equilibrium_surface(year: str):

    N, S, GP = define_equilibrium_surface(year)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # plotting the equilibrium surface of the catastrophe #

    surface = ax.plot_surface(N, S, GP, linewidth=0, rcount=200, ccount=200, alpha=0.8, cmap=cm.binary)

    # plotting the cusp (bifurcation curves) #

    N = np.linspace(0., 1.3, 100)

    S_1 = -2.61 * (np.sqrt(N * 32 / 261) ** 3) + 0.96 * N * np.sqrt(N * 32 / 261)  # first bifurcation curve component
    S_2 = 2.61 * (np.sqrt(N * 32 / 261) ** 3) - 0.96 * N * np.sqrt(N * 32 / 261)  # second bifurcation curve component

    _ = ax.plot(N, S_1, color='#000000', label='Bifurcation curve', zdir='z', zs=-1.1)
    _ = ax.plot(N, S_2, color='#000000', zdir='z', zs=-1.1)

    # plotting the spring distribution scatter (according to the article data) #

    springs_df = load_data_frames(which='springs')
    scatter_springs = ax.scatter(springs_df[year + 'y'].values, springs_df[year + 'x'].values, label='Springs (Samples)',
                                 color='#a60707', alpha=0.7, zdir='z', zs=-1.1)

    # setting the aesthetics #

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-1.2, 1.2)

    ax.yaxis.set_major_locator(LinearLocator(5))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surface, shrink=0.5, aspect=5).set_label('Equilibrium surface (' + year + ')')

    ax.set_xlabel('$N\sim n_1$')
    ax.set_ylabel('$S\sim n_2$')
    ax.set_zlabel('$GP\sim m_1$')

    ax.legend(loc='center left', bbox_to_anchor=(1., .87), fontsize=9)
    plt.show()

