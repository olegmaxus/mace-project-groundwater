import numpy as np
import pandas as pd
from utils.auxiliaries import *
import matplotlib.pyplot as plt


def main():

    yarr = ['2000', '2010', '2020']

    for year in yarr:
        plot_equilibrium_surface(year=year)

    plot_year_samples(mean_lines=True)
    plot_pie_charts()

    
if __name__ == '__main__':
    main()
