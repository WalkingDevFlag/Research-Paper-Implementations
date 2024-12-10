# AlexNet Training Template in TensorFlow 2.x

## Overview
This repository provides a complete pipeline for training the **AlexNet** deep learning model using TensorFlow 2.18.0. AlexNet, a pioneering architecture in deep learning, is adapted here for custom use cases with grayscale or RGB input images. The repository includes the following components:

- **AlexNet Model Definition**: Defined in `Alexnet.py`.
- **Training Script**: Provided in `train.py` to preprocess data, train the model, and save the best-performing model.
- **Dataset Loader**: Example uses `.npy` format for preprocessed data.

## Features
- **Modular Design**: AlexNet model encapsulated in `Alexnet.py` for easy reuse and adaptation.
- **Callback Integration**: Includes early stopping, learning rate scheduling, and checkpointing for robust training.
- **Custom Input Support**: Configurable for different input shapes (e.g., grayscale `(80, 60, 1)` or RGB `(227, 227, 3)`).
- **Model Persistence**: Saves the best model during training and provides a demo to reload it.

## Project Structure
```
your_project/
│
├── Alexnet_Template.py      # AlexNet model definition
├── model.py                 # Model definition
├── train.py                 # Training script
├── dataset.npy              # Sample training data (grayscale images)
├── README.md                # Documentation
```

## Getting Started

### 1. Prerequisites
Ensure the following dependencies are installed:
- Python 3.8+
- TensorFlow 2.17.1
- NumPy
- Scikit-learn

Install the required packages:
```bash
pip install tensorflow==2.17.1 numpy scikit-learn
```

Install the required packages:
```bash
pip install -r requirements.txt
```

### 2. Preparing the Dataset
The script assumes the data is stored in a `.npy` file. The expected format is:
- **Input Features**: Grayscale images stored as 4D arrays, e.g., `(num_samples, 80, 60, 1)`.
- **Labels**: One-hot encoded labels matching the number of output classes.

Modify `train.py` if using a different dataset format.

### 3. Training the Model
1. Clone this repository or copy / download the scripts

2. Run the training script:
    ```bash
    python train.py
    ```

3. Outputs:
    - Best model saved as `best_model.h5`.
    - Final trained model saved as `alexnet.h5`.

4. Training details, including accuracy and loss, will be displayed in the terminal.

### 4. Testing and Evaluation
The script evaluates the trained model on a test set split from the dataset. You can also load the saved model and evaluate it manually:
```python
from tensorflow.keras.models import load_model

model = load_model('alexnet.h5')
test_loss, test_accuracy = model.evaluate(X_test, Y_test)
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")
```

## Configurations

### AlexNet Customization
Modify the `alexnet` function in `model.py` to customize:
- Input shape (default: `(80, 60, 1)` for grayscale or `(227, 227, 3)` for RGB).
- Number of output classes (default: 17).
- Layer parameters such as filter sizes and strides.

### Training Parameters
Adjust the training parameters in `train.py`:
- **Learning Rate**: Controlled by the Adam optimizer (`learning_rate=0.0001`).
- **Batch Size**: Default is `32`.
- **Epochs**: Default is `100`.
- **Validation Split**: Set during train-test split (`test_size=0.2`).

### Callbacks
Preconfigured callbacks include:
- **EarlyStopping**: Stops training when validation loss stagnates for 10 epochs.
- **ReduceLROnPlateau**: Reduces learning rate by 50% if validation loss doesn't improve for 5 epochs.
- **ModelCheckpoint**: Saves the best-performing model based on validation loss.

## Example Output
Upon successful training, you should see output similar to:
```
Training data loaded successfully.
Data shapes - X: (10000, 80, 60, 1), Y: (10000, 17)
Training set: X_train: (8000, 80, 60, 1), Y_train: (8000, 17)
Testing set: X_test: (2000, 80, 60, 1), Y_test: (2000, 17)
Model: "sequential"
...
Epoch 1/100
250/250 [==============================] - 12s 48ms/step - loss: 2.7315 - accuracy: 0.1684 - val_loss: 2.5197 - val_accuracy: 0.2230
...
Epoch 100/100
250/250 [==============================] - 12s 48ms/step - loss: 0.1234 - accuracy: 0.9876 - val_loss: 0.2345 - val_accuracy: 0.9610
Model training completed.
Test Loss: 0.2345
Test Accuracy: 0.9610
```

## License
This project is licensed under the MIT License.

## Acknowledgments
- **AlexNet Architecture**: Adapted from the original 2012 AlexNet paper.
- **TensorFlow Documentation**: For detailed API usage.

Enjoy training your custom AlexNet model! 🚀