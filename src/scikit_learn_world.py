# First import necessary libraries
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression

# Generate a dataset for regression problem
X, y = make_regression(n_samples=100, n_features=1, noise=0.1)

# Define the model
model = LinearRegression()

# Train the model on data
model.fit(X, y)

# Use trained model to make predictions
y_pred = model.predict(X)

print(y_pred)
