# Hidden Markov Model (HMM)

## Overview
This Python script implements the Viterbi algorithm for decoding the most probable sequence of hidden states in a Hidden Markov Model (HMM). Given a set of states, transition probabilities, emission probabilities, and an observation sequence, the algorithm finds the optimal path through the hidden states that best explains the observations.

## Features
- Supports arbitrary transition and emission probabilities.
- Computes the most probable state sequence using the Viterbi dynamic programming approach.
- Outputs the Viterbi table, the best path probability, and the optimal state sequence.

## Conda Environment Setup
To run this script, you can set up a Conda environment as follows:

1. Create a new Conda environment:
   ```bash
   conda create --name hmm_viterbi_env python=3.8 -y
   ```

2. Activate the environment:
   ```bash
   conda activate hmm_viterbi_env
   ```

3. Install NumPy:
   ```bash
   pip install numpy
   ```

## Usage
1. Clone or download the script.
2. Update the HMM parameters (transition matrix `A`, emission probabilities `B`, initial state probabilities `pi`, and the observation sequence `observations`) as needed.
3. Run the script:
   ```bash
   python viterbi_hmm.py
   ```
4. The output will display:
   - The Viterbi table (`V`)
   - The best path probability (`best_path_prob`)
   - The optimal state sequence (`best_path`)

## License

This project is licensed under the MIT License.
