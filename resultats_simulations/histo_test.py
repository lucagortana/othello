import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)

mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

# the histogram of the data
plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)


plt.xlabel('profondeur')
plt.ylabel('pourcentage de parties gagnées')
plt.title('Performance de alphaBeta selon la profondeur')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.xlim(40, 160)
plt.ylim(0, 0.03)
plt.grid(False)
plt.show()


