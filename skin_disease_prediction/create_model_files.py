from keras.layers import Flatten, Dense, Dropout, BatchNormalization, Conv2D, MaxPool2D
from keras.models import Sequential
import numpy as np

# Define the model architecture (this is from your code)
input_shape = (224, 224, 3)
num_classes = 7

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding='Same', input_shape=input_shape))
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding='Same'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.16))

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding='Same'))
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding='Same'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.20))

model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(64, (3, 3), activation='relu', padding='Same'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Save the model architecture to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
print("Model architecture saved to model.json")

# You would normally train the model here with model.fit()
# Since we don't have training data, let's just initialize with random weights
# This is just for testing - in a real scenario, you would train the model

# Save the model weights to HDF5
model.save_weights("model.h5")
print("Model weights saved to model.h5")