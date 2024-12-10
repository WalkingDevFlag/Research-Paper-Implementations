# AlexNet Template in TensorFlow 2.x

## Overview
This repository contains an implementation template of the **AlexNet** architecture using TensorFlow 2.17.1 and Keras. AlexNet is a deep convolutional neural network that revolutionized computer vision tasks by winning the ImageNet Large Scale Visual Recognition Challenge (ILSVRC) in 2012. This template serves as a starting point for creating and training custom models based on AlexNet.

## Features
- **Convolutional Layers**: Five convolutional layers with ReLU activation functions, designed to extract meaningful features from images.
- **Pooling Layers**: MaxPooling layers for spatial downsampling and dimensionality reduction.
- **Batch Normalization**: Used after convolutional and dense layers to stabilize training and improve convergence.
- **Fully Connected Layers**: Three dense layers for high-level reasoning, including dropout for regularization.
- **Customizable Output**: Final softmax layer configured for 17 output classes (can be adjusted).
- **TensorFlow 2.x Compatible**: Built and tested with TensorFlow 2.18.0.

## Conda Environment Setup
Follow these steps to set up the required environment using Conda:

1. Create a new Conda environment:
    ```bash
    conda create -n alexnet-tf python=3.8 -y
    ```

2. Activate the environment:
    ```bash
    conda activate alexnet-tf
    ```

3. Install TensorFlow:
    ```bash
    pip install tensorflow==2.18.0
    ```

## Usage
1.Clone or download the script.

2. Run the script:
    ```bash
    python Alexnet.py
    ```

3. Modify the script:
   - Adjust the input shape (`input_shape=(227,227,3)`) in the first layer to match your dataset.
   - Update the number of classes in the final `Dense` layer (`Dense(17)`) to align with your task.

4. Train the model:
   Add a training loop with your dataset. For example:
    ```python
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_data, train_labels, batch_size=32, epochs=10, validation_split=0.2)
    ```

## MIT License
This project is licensed under the MIT License.