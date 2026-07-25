import matplotlib.pyplot as plt

"""Par Curve Visualization"""

def plot_par_curve(par,date):
    row = par.loc[date]
    plt.plot(row.index,row.values,marker='o')
    plt.xlabel("Maturity (years)")
    plt.ylabel("Par yield (%)")
    plt.title(f"Par Curve from {date}")
    plt.show()

def plot_par_heatmap(par):
    plt.imshow(par.T.values , aspect="auto",cmap = "viridis")
    plt.yticks(range(11), par.columns)
    plt.colorbar()
    plt.show()