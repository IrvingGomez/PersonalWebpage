import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.datasets import fetch_species_distributions
from sklearn.neighbors import KernelDensity
from scipy.stats import norm
from sklearn.model_selection import GridSearchCV

def make_data(N, f=0.3, rseed=1):
    rand = np.random.RandomState(rseed)
    x = rand.randn(N)    # normal random numbers
    x[int(f * N):] += 5  # sum 5 to the (1-f)*N largest numbers
    return x

N = 1000
x = make_data(N)

plt.figure(figsize=(10,7.5))
hist = plt.hist(x, bins=30, density=True, color='RebeccaPurple', alpha=0.5)

hist

density, bins, patches = hist
widths = bins[1:] - bins[:-1]
(density * widths).sum()

widths

# Estimacion de h optima
h_star = 1.06*np.std(x)/(N**(1/5))
h_star

x_d = np.linspace(-4, 8, 1000)
density = 1/N*sum(norm(xi, h_star).pdf(x_d) for xi in x)

plt.figure(figsize=(10,7.5))
plt.fill_between(x_d, density, alpha=0.5, color='RebeccaPurple')

def kernel(h):
    x_d = np.linspace(-4, 8, 1000)
    density = 1/1000* sum(norm(xi, h).pdf(x_d) for xi in x)

    plt.figure(figsize=(10,7.5))
    plt.fill_between(x_d, density, alpha=0.5, color='RebeccaPurple')

kernel(h_star)

# instantiate and fit the KDE model
kde = KernelDensity(bandwidth=h_star, kernel='gaussian')
kde.fit(x[:, None])

# score_samples returns the log of the probability density
logprob = kde.score_samples(x_d[:, None])

plt.figure(figsize=(10,7.5))
plt.fill_between(x_d, np.exp(logprob), color='RebeccaPurple', alpha=0.5)

params = {'bandwidth': np.logspace(-1.5, 0.5, 100)}
grid = GridSearchCV(KernelDensity(), params)
grid.fit(x[:, None])

grid.best_estimator_

grid.cv_results_.get('mean_test_score')

np.where(grid.cv_results_.get('mean_test_score')==np.amax(grid.cv_results_.get('mean_test_score')))[0][0]

index_best_band = np.where(grid.cv_results_.get('mean_test_score')==np.amax(grid.cv_results_.get('mean_test_score')))[0][0]
params.get('bandwidth')[index_best_band]

plt.figure(figsize=(10,7.5))
plt.plot(params.get('bandwidth'), -1*grid.cv_results_.get('mean_test_score'), color='RebeccaPurple')
plt.axvline(x=params.get('bandwidth')[index_best_band], color='red', linestyle='--')

kernel(params.get('bandwidth')[index_best_band])

plt.figure(figsize=(10,7.5))
sns.histplot(x, color='RebeccaPurple', kde=True)


# sklearn example
try:
    from mpl_toolkits.basemap import Basemap
    basemap = True
except ImportError:
    basemap = False

def construct_grids(batch):
    """Construct the map grid from the batch object

    Parameters
    ----------
    batch : Batch object
        The object returned by :func:`fetch_species_distributions`

    Returns
    -------
    (xgrid, ygrid) : 1-D arrays
        The grid corresponding to the values in batch.coverages
    """
    # x,y coordinates for corner cells
    xmin = batch.x_left_lower_corner + batch.grid_size
    xmax = xmin + (batch.Nx * batch.grid_size)
    ymin = batch.y_left_lower_corner + batch.grid_size
    ymax = ymin + (batch.Ny * batch.grid_size)

    # x coordinates of the grid cells
    xgrid = np.arange(xmin, xmax, batch.grid_size)
    # y coordinates of the grid cells
    ygrid = np.arange(ymin, ymax, batch.grid_size)

    return (xgrid, ygrid)


# Get matrices/arrays of species IDs and locations
data = fetch_species_distributions()
species_names = ['Bradypus Variegatus', 'Microryzomys Minutus']

Xtrain = np.vstack([data['train']['dd lat'],
                    data['train']['dd long']]).T
ytrain = np.array([d.decode('ascii').startswith('micro')
                  for d in data['train']['species']], dtype='int')
Xtrain *= np.pi / 180.  # Convert lat/long to radians

# Set up the data grid for the contour plot
xgrid, ygrid = construct_grids(data)
X, Y = np.meshgrid(xgrid[::5], ygrid[::5][::-1])
land_reference = data.coverages[6][::5, ::5]
land_mask = (land_reference > -9999).ravel()

xy = np.vstack([Y.ravel(), X.ravel()]).T
xy = xy[land_mask]
xy *= np.pi / 180.

# Plot map of South America with distributions of each species
fig = plt.figure(figsize=(10,7.5))
fig.subplots_adjust(left=0.05, right=0.95, wspace=0.05)

for i in range(2):
    plt.subplot(1, 2, i + 1)

    # construct a kernel density estimate of the distribution
    print(" - computing KDE in spherical coordinates")
    kde = KernelDensity(bandwidth=0.04, metric='haversine',
                        kernel='gaussian', algorithm='ball_tree')
    kde.fit(Xtrain[ytrain == i])

    # evaluate only on the land: -9999 indicates ocean
    Z = np.full(land_mask.shape[0], -9999, dtype='int')
    Z[land_mask] = np.exp(kde.score_samples(xy))
    Z = Z.reshape(X.shape)

    # plot contours of the density
    levels = np.linspace(0, Z.max(), 25)
    plt.contourf(X, Y, Z, levels=levels, cmap=plt.cm.Purples)

    if basemap:
        print(" - plot coastlines using basemap")
        m = Basemap(projection='cyl', llcrnrlat=Y.min(),
                    urcrnrlat=Y.max(), llcrnrlon=X.min(),
                    urcrnrlon=X.max(), resolution='c')
        m.drawcoastlines()
        m.drawcountries()
    else:
        print(" - plot coastlines from coverage")
        plt.contour(X, Y, land_reference,
                    levels=[-9998], colors="k",
                    linestyles="solid")
        plt.xticks([])
        plt.yticks([])

    plt.title(species_names[i])
