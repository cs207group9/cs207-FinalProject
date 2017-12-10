import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from chemkin_CS207_G9.reaction.ReactionSystem import ReactionSystem



def plot_concentration(reac_sys, time_grid, logscale=False, species=None, ax=None, **options):
    '''plot the concentration evolution of the reaction system

    INPUTS:
        reac_sys:   ReactionSystem object, should be initiated with concs and temp
        time_grid:  list of float, a grid of time with len>2, time should be positive
        logscale:   boolean, whether to plot concentration in log10 scale, defaults False
        species:    list of str, species to plot, if None, all the species get plotted
        ax:         matplotlib axes type, if None, this function will generate one with matplotlib default
        options:    matplotlib plot keywords, optional
    OUTPUTS:
        ax:         the plotted ax
    '''

    time_grid = np.sort(time_grid)
    if len(time_grid) <= 2:
        raise ValueError('time_grid = {}. A valid grid should contain more than 2 elements.'.format(time_grid))
    
    t_start, t_end = time_grid[0], time_grid[-1]
    if t_start < 0:
        raise ValueError('t_start = {}. A valid grid sould start from a positive time.'.format(t_start))

    if species is None:
        species = list(reac_sys.get_species())

    concs_initial = dict(reac_sys.get_concs())
    res_evo = reac_sys.evolute(t_end)
    concs_evo = res_evo(time_grid)

    if ax is None:
        ax = plt.subplot()
    for sp in species:
        concs = concs_evo[sp]
        if logscale:
            concs = np.log10(concs)
        ax.plot(time_grid, concs, label=sp, **options)
    ax.legend(loc='center left', bbox_to_anchor=(1,0.5))
    ax.set_ylabel('concentration'+(' (log10 scale)' if logscale else ''))
    ax.set_xlabel('time')

    reac_sys.set_concs(concs_initial)
    return ax



def plot_reaction_rate(reac_sys, time_grid, logscale=False, species=None, ax=None, **options):
    '''plot the reaction rate evolution of the reaction system

    INPUTS:
        reac_sys:   ReactionSystem object, should be initiated with concs and temp
        time_grid:  list of float, a grid of time with len>2, time should be positive
        logscale:   boolean, whether to plot concentration in log10 scale, defaults False
        species:    list of str, species to plot, if None, all the species get plotted
        ax:         matplotlib axes type, if None, this function will generate one with matplotlib default
        options:    matplotlib plot keywords, optional
    OUTPUTS:
        ax:         the plotted ax
    '''

    time_grid = np.sort(time_grid)
    if len(time_grid) <= 2:
        raise ValueError('time_grid = {}. A valid grid should contain more than 2 elements.'.format(time_grid))
    
    t_start, t_end = time_grid[0], time_grid[-1]
    if t_start < 0:
        raise ValueError('t_start = {}. A valid grid sould start from a positive time.'.format(t_start))

    if species is None:
        species = list(reac_sys.get_species())

    concs_initial = dict(reac_sys.get_concs())
    res_evo = reac_sys.evolute(t_end)
    rates_evo = {sp:[] for sp in reac_sys.get_species()}
    for t in time_grid:
        reac_sys.set_concs(res_evo(t))
        rate = reac_sys.get_reac_rate()
        for sp,r in zip(reac_sys.get_species(), rate):
            rates_evo[sp].append(r)

    if ax is None:
        ax = plt.subplot()
    for sp in species:
        rates = rates_evo[sp]
        if logscale:
            rates = np.log10(rates)
        ax.plot(time_grid, rates, label=sp, **options)
    ax.legend(loc='center left', bbox_to_anchor=(1,0.5))
    ax.set_ylabel('reaction rate'+(' (log10 scale)' if logscale else ''))
    ax.set_xlabel('time')

    reac_sys.set_concs(concs_initial)
    return ax




def plot_modified_arrhenius(RToE_grid, b_grid, ax=None, **options):
    '''plot the trend of the modified arrhenius function over temperature, axis ticks will be scaled

    INPUTS:
        RToE_grid:  list of float, a grid of RT/E, must all be positive
        b_grid:     list of float, a grid of b
        ax:         matplotlib axes type, if None, this function will generate one with matplotlib default
        options:    matplotlib plot keywords, optional
    OUTPUTS:
        ax:         the plotted ax
    '''

    RToE_grid = np.sort(RToE_grid)
    if RToE_grid[0] <= 0:
        raise ValueError('Temperature must be positive.')

    if ax is None:
        ax = plt.subplot()
    for b in list(b_grid):
        ax.plot(RToE_grid, (RToE_grid**b) * np.exp(-1/RToE_grid), label='b = {}'.format(b), **options)
    ax.legend(loc='center left', bbox_to_anchor=(1,0.5))
    ax.set_ylabel('reaction rate coefficient / ' + r'$A \cdot E^b \cdot R^{-b}$')
    ax.set_xlabel('temperature / ' + r'$R \cdot E^{-1}$')

    return ax

