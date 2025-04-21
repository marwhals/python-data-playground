import tensorflow as tf  # Needs specific python version
import numpy as np
import matplotlib.pyplot as plt

# Create data
X = np.linspace(0, 2, 100)
Y = 3 * X + np.random.randn(*X.shape) * 0.33


# Create a linear model
class Model:
    def __init__(self):
        self.W = tf.Variable(10.0)
        self.b = tf.Variable(-5.0)

    def __call__(self, x):
        return self.W * x + self.b


# Instantiate the model
model = Model()


# Define loss
def loss(predicted_y, target_y):
    return tf.reduce_mean(tf.square(predicted_y - target_y))


# Define train
def train(model, inputs, outputs, learning_rate):
    with tf.GradientTape() as t:
        current_loss = loss(model(inputs), outputs)
    dW, db = t.gradient(current_loss, [model.W, model.b])
    model.W.assign_sub(learning_rate * dW)
    model.b.assign_sub(learning_rate * db)


# Train the model
for epoch in range(10):
    train(model, X, Y, 0.425)

# Predict Y
Y_pred = model(X)

# Plot
plt.scatter(X, Y, label='original data')
plt.scatter(X, Y_pred, label='fitted line')
plt.legend()
plt.show()
