import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

# 1. Load the MNIST dataset
print("Loading MNIST dataset...")
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
print(f"Training samples: {train_images.shape[0]}, Test samples: {test_images.shape[0]}")

# 2. Preprocess the images
print("Preprocessing image data: flattening and normalizing pixel values...")
train_images = train_images.reshape((60000, 28 * 28)).astype('float32') / 255
test_images = test_images.reshape((10000, 28 * 28)).astype('float32') / 255
print(f"Image shape after reshaping: {train_images.shape}")

# 3. Preprocess the labels
print("Converting labels to one-hot encoded format...")
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
print(f"Label shape after encoding: {train_labels.shape}")

# 4. Build the neural network model
print("Building the model...")
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(28 * 28,)))  # Hidden layer
model.add(Dense(10, activation='softmax'))  # Output layer for 10 digit classes

# 5. Compile the model
print("Compiling the model with RMSprop optimizer and categorical crossentropy loss...")
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 6. Train the model
print("Training the model for 5 epochs...")
history = model.fit(train_images, train_labels, epochs=5, batch_size=128, verbose=1)
print("Training complete!")

# 7. Plot the training loss over epochs
print("Plotting training loss...")
loss_values = history.history['loss']
epochs = range(1, len(loss_values) + 1)

plt.figure(figsize=(8, 6))
plt.plot(epochs, loss_values, 'bo-', label='Training Loss')
plt.title('Training Loss Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 8. Evaluate on test data
print("Evaluating model on test data...")
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"Test accuracy: {test_acc:.4f}, Test loss: {test_loss:.4f}")
