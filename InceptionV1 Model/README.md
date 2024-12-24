# Inception v1 (GoogLeNet) Implementation

## Overview
This repository contains a PyTorch implementation of the Inception v1 (GoogLeNet) architecture. Inception v1 was introduced in the paper ["Going Deeper with Convolutions"](https://arxiv.org/abs/1409.4842) by Szegedy et al. It is designed to efficiently capture spatial hierarchies and channel dependencies using modular inception blocks. The model also includes auxiliary classifiers to address the vanishing gradient problem and improve training stability.

### Key Highlights of Inception v1
- **Inception Blocks:** Combines multiple convolutional operations (1x1, 3x3, 5x5) and max-pooling.
- **Auxiliary Classifiers:** Provides intermediate supervision to mitigate vanishing gradients.
- **Parameter Efficiency:** Uses 1x1 convolutions for dimensionality reduction, optimizing computational cost.

## Features
- Modular implementation of Inception Blocks.
- Support for auxiliary classifiers.
- Configurable feature map sizes for each block.
- Implements key layers such as Local Response Normalization (LRN), dropout, and average pooling.
- Outputs include predictions from auxiliary classifiers and the final output.

## Conda Environment Setup
Follow these steps to set up the environment:

1. Clone the repository

2. Create a new Conda environment:
   ```bash
   conda create -n inception_env python=3.9 -y
   conda activate inception_env
   ```

3. Install the required dependencies:
   ```bash
   pip install torch torchvision
   ```

## Usage
The following steps demonstrate how to use the implementation:

1. Import the model and initialize it:
   ```python
   from inception import inceptionV1

   in_channels = [192, 256, 480, 512, 512, 512, 528, 832, 832, 1024]
   feature_maps = [[64, 96, 128, 16, 32, 32],
                   [128, 128, 192, 32, 96, 64],
                   [192, 96, 208, 16, 48, 64],
                   [160, 112, 224, 24, 64, 64],
                   [128, 128, 256, 24, 64, 64],
                   [112, 144, 288, 32, 64, 64],
                   [256, 160, 320, 32, 128, 128],
                   [256, 160, 320, 32, 128, 128],
                   [384, 192, 384, 48, 128, 128]]

   model = inceptionV1(in_channels, feature_maps, classes=1000)
   ```

2. Forward pass with a sample input:
   ```python
   import torch

   input_tensor = torch.rand(16, 3, 224, 224)  # Batch of 16 images
   outputs = model(input_tensor)

   for i, output in enumerate(outputs):
       print(f"Output {i + 1} shape: {output.shape}")
   ```

3. Train or evaluate the model using your custom dataset and training loop.

## License
This project is licensed under the MIT License.
