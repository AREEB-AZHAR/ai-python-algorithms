import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 1. Define dataset for NAND gate
# Input combinations (0,0), (0,1), (1,0), (1,1)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) 
# NAND outputs: 1, 1, 1, 0
y_nand = np.array([[1], [1], [1], [0]])

# 2. Build the ANN Model
model = Sequential()
# Single neuron with sigmoid activation for binary output
model.add(Dense(units=1, activation='sigmoid', input_dim=2)) 

# 3. Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 4. Train the model
print("Training NAND Gate ANN...")
model.fit(X, y_nand, epochs=500, verbose=0) # Increased epochs for convergence

# 5. Evaluate and Predict
loss, accuracy = model.evaluate(X, y_nand, verbose=0)
print(f"NAND Gate Accuracy: {accuracy:.2f}")

predictions = np.round(model.predict(X))
print(f"NAND Gate Predictions:\n{predictions}")