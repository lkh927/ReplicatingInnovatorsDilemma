import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy.io import loadmat

def plot_sim(Estate):
    #Labels for the plot
    labels = ['Old-only', 'Both', 'New-only']
    #x-axis is the time period
    x = np.linspace(1981,1998, 18)

    #create the fig
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot data with specified markers and linestyles
    ax.plot(x, Estate['New-only'],  linestyle='--', color='steelblue', marker='^', markerfacecolor='white', linewidth=1,
            zorder=3, label=labels[2], markersize=5)                # New-only
    ax.plot(x, Estate['Both'], linestyle='-', color='steelblue', marker='o', markerfacecolor='white', linewidth=1,    # Both
            label=labels[1], markersize=5, zorder=3)
    ax.plot(x, Estate['Old-only'], 'o-', label=labels[0], color='steelblue', linewidth=1,
            markersize=5, zorder=3) # Old-only

    # Title and axis labels
    ax.set_title('Market Structure', fontsize=12, weight='bold')
    ax.set_ylabel('Number of firms', fontsize=10)

    # Set limits and ticks
    ax.set_ylim(0, 12)
    ax.set_xlim(1980, 1999)
    ax.set_xticks(np.arange(1981, 1999, 2))

    # Set ticks to be inside
    ax.tick_params(axis='both', direction='in', length=4)

    # Only show bottom and left spines (x and y axes)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    # Make x and y axis lines slightly transparent
    ax.spines['bottom'].set_alpha(0.5)
    ax.spines['left'].set_alpha(0.5)

    # Increase z-order to bring markers above the axes
    for line in ax.lines:
        line.set_zorder(3)

    # Show legend
    ax.legend(loc='upper right', frameon=False, fontsize=10)

    plt.show()