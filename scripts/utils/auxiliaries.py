import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D, axes3d
from scipy import interpolate
import matplotlib as mpl
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.gridspec as gridspec

data_sets = {
    'model parameters':
        'https://raw.githubusercontent.com/olegmaxus/mace-project-groundwater/master/data/ModelParameters.csv',
    'model parameters new':
        'https://raw.githubusercontent.com/olegmaxus/mace-project-groundwater/master/data/ModelParametersReformatted.csv',
    'springs':
        'https://raw.githubusercontent.com/olegmaxus/mace-project-groundwater/master/data/datasetSptrings.csv',
    'CCM':
        'https://raw.githubusercontent.com/olegmaxus/mace-project-groundwater/master/data/CCM-PCA.csv',
    'CFMF':
        'https://raw.githubusercontent.com/olegmaxus/mace-project-groundwater/master/data/CFMFs.csv'}


def load_data_frames(which: str = 'null'):

    ret_status = {'model parameters': pd.read_csv(data_sets['model parameters']),
                  'model parameters new': pd.read_csv(data_sets['model parameters new']),
                  'springs': pd.read_csv(data_sets['springs']),
                  'CCM': pd.read_csv(data_sets['CCM']),
                  'CFMF': pd.read_csv(data_sets['CFMF'])}

    if which == 'null':
        return ret_status
    else:
        return ret_status[which]


parameters_df = load_data_frames(which='model parameters new')
springs_df = load_data_frames(which='springs')
ccm_df = load_data_frames(which='CCM')
cfmf_df = load_data_frames(which='CFMF')

def gp_roots_evaluator():
    yrs_col = ['2000', '2010', '2020']

    array_ab = np.empty((2,3))
    for idx, yr in enumerate(yrs_col):
        array_ab[0][idx] = parameters_df[yr][0]
        array_ab[1][idx] = parameters_df[yr][1]
    array_ab = array_ab.T

    df = pd.dataframe()
    for idx, yr in enumerate(yrs_col):
        N = springs_df[yr + 'y']
        S = springs_df[yr + 'x']
        temp_arr = np.array([])
        for i, j in zip(N, S):
            GP = [np.max(np.real(np.roots([array_ab[idx][0], 0, array_ab[idx][1] * i, -j])))]
            temp_arr = np.append(temp_arr, GP, axis=idx)
        df[yr] = pd.Series(temp_arr)
    return df

def plot_pie_charts():

    gs = gridspec.GridSpec(2, 3)
    fig = plt.figure()
    colors = ['#c33b2f', '#fda18a', '#e6e5e4', '#a2b1d6', '#436dac']

    ax00 = fig.add_subplot(gs[0, 0])
    ax01 = fig.add_subplot(gs[0, 1])
    ax02 = fig.add_subplot(gs[0, 2])

    ax10 = fig.add_subplot(gs[1, 0])
    ax11 = fig.add_subplot(gs[1, 1])
    ax12 = fig.add_subplot(gs[1, 2])

    ax00.pie(ccm_df['2000 Percentage'], labels=ccm_df['GPS/Year'], explode=(0.05, 0.05, 0.05, 0.05, 0.05),
             colors=colors, autopct='%1.2f%%', textprops={'fontsize': 13})
    ax01.pie(ccm_df['2010 Percentage'], labels=ccm_df['GPS/Year'], explode=(0.05, 0.05, 0.05, 0.05, 0.05),
             colors=colors, autopct='%1.2f%%', textprops={'fontsize': 13})
    ax02.pie(ccm_df['2020 Percentage'], labels=ccm_df['GPS/Year'], explode=(0.05, 0.05, 0.05, 0.05, 0.05),
             colors=colors, autopct='%1.2f%%', textprops={'fontsize': 13})

    ax10.pie(cfmf_df['2000 Percentage'], labels=ccm_df['GPS/Year'], explode=(0.05, 0.05, 0.05, 0.05, 0.05),
             colors=colors, autopct='%1.2f%%', textprops={'fontsize': 13})
    ax11.pie(cfmf_df['2010 Percentage'], labels=ccm_df['GPS/Year'], explode=(0.05, 0.05, 0.05, 0.05, 0.05),
             colors=colors, autopct='%1.2f%%', textprops={'fontsize': 13})
    ax12.pie(cfmf_df['2020 Percentage'], labels=ccm_df['GPS/Year'], explode=(0.05, 0.05, 0.05, 0.05, 0.05),
             colors=colors, autopct='%1.2f%%', textprops={'fontsize': 13})

    ax00.set_ylabel('CCM (New Model)', fontsize=13)
    ax10.set_ylabel('CFMFs (Old Model)', fontsize=13)

    ax00.set_title('2000 yr.')
    ax01.set_title('2010 yr.')
    ax02.set_title('2020 yr.')

    plt.show()
    
    return


def define_equilibrium_surface(year: str = '2000') -> tuple:

    # creating a mash for input N, GP variables  #

    n = np.linspace(-1.2, 1.2, 48)
    gp = np.linspace(-1.2, 1.2, 48)
    N, GP = np.meshgrid(n, gp)

    # getting parameters' values #

    a, b = parameters_df[year][0], parameters_df[year][1]

    S = a * GP ** 3 + b * GP * N

    # bounding the surface by the omitted polygons #

    S[S > 1.5] = np.nan
    S[S < -1.5] = np.nan

    return N, S, GP


def define_bifurcation_curve(year: str = '2000') -> tuple:

    a, b = parameters_df[year][0], parameters_df[year][1]
    N = np.linspace(0., 1.3, 100)
    S_1 = a * (np.sqrt(N * (-b)/(3 * a)) ** 3) + b * N * np.sqrt(N * (-b)/(3 * a))  # first bifurcation curve component
    S_2 = a * (- np.sqrt(N * (-b)/(3 * a)) ** 3) - b * N * np.sqrt(N * (-b)/(3 * a)) # second bifurcation curve component

    return N, S_1, S_2


def plot_equilibrium_surface(year: str = '2000'):

    N, S, GP = define_equilibrium_surface(year)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # plotting the equilibrium surface of the catastrophe #

    surface = ax.plot_surface(N, S, GP, linewidth=0, rcount=200, ccount=200, alpha=0.8, cmap=cm.binary)

    # plotting the cusp (bifurcation curves) #

    N, S_1, S_2 = define_bifurcation_curve(year=year)

    _ = ax.plot(N, S_1, color='#000000', label='Bifurcation curve', zdir='z', zs=-1.1)
    _ = ax.plot(N, S_2, color='#000000', zdir='z', zs=-1.1)

    # plotting the spring distribution scatter (according to the article data) #

    scatter_springs = ax.scatter(springs_df[year + 'y'].values, springs_df[year + 'x'].values, label='Springs (Samples)',
                                 color='#ae0001', edgecolor='#000000', linewidths=0.1, zdir='z', zs=-1.1)

    # setting the aesthetics #

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-1.2, 1.2)

    ax.yaxis.set_major_locator(LinearLocator(5))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surface, shrink=0.5, aspect=5).set_label('Equilibrium surface (' + year + ' yr.)')

    ax.set_xlabel('$N\sim n_1$')
    ax.set_ylabel('$S\sim n_2$')
    ax.set_zlabel('$GP\sim m_1$')

    _ = plt.suptitle('Equilibrium surface with fold projection', fontsize=14)
    ax.legend(loc='center left', bbox_to_anchor=(1., .87), fontsize=9)
    plt.show()

    return


def plot_year_samples(mean_lines: bool = False):

    N_00, S_100, S_200 = define_bifurcation_curve('2000')
    N_10, S_110, S_210 = define_bifurcation_curve('2010')
    N_20, S_120, S_220 = define_bifurcation_curve('2020')

    gs = gridspec.GridSpec(1, 3)
    fig = plt.figure()

    ax00 = fig.add_subplot(gs[0, 0])
    ax00.plot(N_00, S_100, color='#d0631b', label='Bifurcation curve')
    ax00.plot(N_00, S_200, color='#d0631b')
    ax00.set_xlabel('Natural composite index $(N)$')
    ax00.set_ylabel('Anthropogenic composite index $(S)$')
    ax00.scatter(springs_df['2000y'].values, springs_df['2000x'].values, label='Springs (Samples)', linewidths=0.5, edgecolor='#000000', color='#5bc3ec')

    if mean_lines:
        mean_line = [springs_df['2000x'].values.mean()] * len(N_00)
        ax00.plot(N_00, mean_line, color='#000000', linestyle='--', linewidth=3, label='Mean line for springs data')

    ax00.legend(title='2000 yr.', loc=2, fontsize=9)

    ax10 = fig.add_subplot(gs[0, 1])
    ax10.plot(N_10, S_110, color='#d0631b', label='Bifurcation curve')
    ax10.plot(N_10, S_210, color='#d0631b')
    ax10.set_xlabel('Natural composite index $(N)$')
    ax10.set_ylabel('Anthropogenic composite index $(S)$')
    ax10.scatter(springs_df['2010y'].values, springs_df['2010x'].values, label='Springs (Samples)', linewidths=0.5, edgecolor='#000000', color='#5bc3ec')

    if mean_lines:
        mean_line = [springs_df['2010x'].values.mean()] * len(N_10)
        ax10.plot(N_10, mean_line, color='#000000', linestyle='--', linewidth=3, label='Mean line for springs data')

    ax10.legend(title='2010 yr.', loc=2, fontsize=9)

    ax20 = fig.add_subplot(gs[0, 2])
    ax20.plot(N_00, S_120, color='#d0631b', label='Bifurcation curve')
    ax20.plot(N_00, S_220, color='#d0631b')
    ax20.set_xlabel('Natural composite index $(N)$')
    ax20.set_ylabel('Anthropogenic composite index $(S)$')
    ax20.scatter(springs_df['2020y'].values, springs_df['2020x'].values, label='Springs (Samples)', linewidths=0.5, edgecolor='#000000', color='#5bc3ec')

    if mean_lines:
        mean_line = [springs_df['2020x'].values.mean()] * len(N_00)
        ax20.plot(N_20, mean_line, color='#000000', linestyle='--', linewidth=3, label='Mean line for springs data')

    ax20.legend(title='2020 yr.', loc=2, fontsize=9)

    _ = plt.suptitle('Samples distribution with respect to bifurcation curve', fontsize=14)

    plt.show()

    return


if __name__ == '__main__':
    plot_year_samples(True)
    plot_equilibrium_surface('2010')
    plot_pie_charts()
