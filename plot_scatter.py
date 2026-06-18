import matplotlib.pyplot as plt

def plot_scatter(dataframe, title):

    fig, ax = plt.subplots(figsize=(12, 4))
    im1 = ax.scatter(dataframe['date'], 
                    dataframe['mags'], 
                    marker='.', 
                    c='yellow', 
                    alpha=0.3,
                    s=0.1,)
    ax.set_ylim(12, 23)
    ax.set_xlabel('Date')
    ax.set_ylabel('Mags / arcsec^2')
    ax.set_title(title)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()

    return None