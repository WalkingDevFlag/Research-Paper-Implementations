# train.py

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

# Import the AlexNet model
from model import alexnet

def main():
    # Load the training data
    try:
        train_data = np.load('training_data_v7.2.npy', allow_pickle=True)
        print("Training data loaded successfully.")
    except FileNotFoundError:
        print("Error: 'training_data_v7.2.npy' not found.")
        return

    # Prepare the data
    X = np.array([i[0] for i in train_data]).reshape(-1, 80, 60, 1)  # 80x60 grayscale images
    Y = np.array([i[1] for i in train_data])  # Labels (one-hot encoded)
    print(f"Data shapes - X: {X.shape}, Y: {Y.shape}")

    # Split into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    print(f"Training set: X_train: {X_train.shape}, Y_train: {Y_train.shape}")
    print(f"Testing set: X_test: {X_test.shape}, Y_test: {Y_test.shape}")

    # Initialize the model
    input_shape = (80, 60, 1)  # Adjusted to match the data
    num_classes = Y.shape[1]   # Assuming Y is one-hot encoded
    model = alexnet(input_shape=input_shape, num_classes=num_classes)
    model.summary()

    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, verbose=1),
        ModelCheckpoint(filepath='best_model.h5', save_best_only=True, monitor='val_loss', verbose=1)
    ]

    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=0.0001),  # Optimizer with a learning rate
        loss='categorical_crossentropy',        # Loss function for multi-class classification
        metrics=['accuracy']                    # Metric to evaluate during training
    )
    print("Model compiled successfully.")

    # Train the model
    history = model.fit(
        X_train, Y_train,
        epochs=100,
        batch_size=32,
        validation_data=(X_test, Y_test),
        callbacks=callbacks,
        verbose=1
    )
    print("Model training completed.")

    # Save the trained model
    model.save('Alexnet.h5')
    print("Model saved to 'Alexnet.h5'.")

    # Evaluate the model on the test set
    test_loss, test_accuracy = model.evaluate(X_test, Y_test, verbose=0)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")

    # Load the saved model (optional)
    loaded_model = load_model('Alexnet.h5')
    print("Loaded model summary:")
    loaded_model.summary()

if __name__ == "__main__":
    main()
