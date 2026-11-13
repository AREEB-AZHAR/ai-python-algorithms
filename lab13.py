from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(-1, 28*28).astype('float32') / 255.0
X_test = X_test.reshape(-1, 28*28).astype('float32') / 255.0

model_deep = Sequential([
    Dense(128, activation='relu', input_shape=(28*28,)), 
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(10, activation='softmax')
])

model_deep.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

print("Training Deeper MLP Model...")
model_deep.fit(X_train, y_train, epochs=10, batch_size=64, validation_split=0.2)

loss, accuracy = model_deep.evaluate(X_test, y_test)
print(f"Deep MLP Test Accuracy: {accuracy:.2f}")