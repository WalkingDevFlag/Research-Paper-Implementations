# **Attention Is All You Need**


## Overview

This project implements a Transformer model from scratch using PyTorch. The Transformer architecture is a foundational model for Natural Language Processing (NLP) tasks such as machine translation, summarization, and text generation. This implementation includes all core components like self-attention, encoder, and decoder layers, and provides flexibility to adjust hyperparameters like embedding size, number of layers, and attention heads.

## Features

- **Multi-Head Self-Attention**: Efficient attention mechanism to capture relationships between words in a sequence.
- **Transformer Blocks**: Layered encoder and decoder structures with normalization and feedforward networks.
- **Custom Masking**: Source and target masking for sequence alignment and autoregressive behavior.
- **Positional Embedding**: Encodes positional information in sequence data.
- **Scalable Architecture**: Adjustable parameters for embedding size, number of layers, attention heads, and expansion factor.
- **GPU Support**: Compatible with CUDA for accelerated training.

## Requirements

- Python 3.8+
- PyTorch 1.11.0+

## Conda Environment Setup

1. **Create the Environment**  
   ```bash
   conda create -n transformer-env python=3.8 -y
   ```

2. **Activate the Environment**  
   ```bash
   conda activate transformer-env
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Running the Script**  
   The script initializes a Transformer model and tests it with toy data. To run the code:
   ```bash
   python transformer_model.py
   ```

2. **Customizing Parameters**  
   Update the model parameters such as `embed_size`, `num_layers`, `heads`, and `max_length` in the `Transformer` class initialization.

3. **Integrate with Your Data**  
   Replace the dummy tensors `x` and `target` in the `__main__` section with your dataset, ensuring appropriate preprocessing.

## MIT License

This project is licensed under the MIT License.
