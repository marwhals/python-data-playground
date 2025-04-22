import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data Generation
np.random.seed(0)
data = pd.DataFrame({
    'A': np.random.randint(0, 100, 1000),
    'B': np.random.randint(0, 100, 1000),
    'C': np.random.normal(size=1000),
    'D': np.random.normal(size=1000),
})

# Create seaborn plot figure
plt.figure(figsize=(8, 6))

# Generate and save Histogram
sns.histplot(data['A'], bins=20)
plt.savefig('pretty-pictures/histogram.png')
plt.clf()

# Generate and save Boxplot
sns.boxplot(data=data[['A', 'B']])
plt.savefig('pretty-pictures/boxplot.png')
plt.clf()

# Generate and save Density plot
sns.kdeplot(data=data[['C', 'D']])
plt.savefig('pretty-pictures/density_plot.png')
plt.clf()

# Generate and save Scatter plot
sns.scatterplot(x='A', y='B', data=data)
plt.savefig('pretty-pictures/scatterplot.png')
plt.clf()
