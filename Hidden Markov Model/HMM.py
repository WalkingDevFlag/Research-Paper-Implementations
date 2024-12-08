import numpy as np

# Define the parameters of the HMM
A = np.array([[0.5, 0.3, 0.2],  # Transition matrix
              [0.4, 0.2, 0.2],
              [0.0, 0.3, 0.7]])
B = np.array([[0.9, 0.1],  # Emission probabilities
              [0.6, 0.4],
              [0.2, 0.8]])
pi = np.array([0.218, 0.273, 0.509])  # Initial state probabilities
observations = [1, 0]  # Observation sequence

# Number of states and length of observation sequence
num_states = A.shape[0]
T = len(observations)

# Initialize Viterbi table and back-pointer table
V = np.zeros((T, num_states))
backpointer = np.zeros((T, num_states), dtype=int)

# Initialization step
V[0, :] = pi * B[:, observations[0]]

# Recursion step
for t in range(1, T):
    for j in range(num_states):
        # Compute the maximum probability and the back-pointer
        prob = V[t - 1] * A[:, j]
        V[t, j] = np.max(prob) * B[j, observations[t]]
        backpointer[t, j] = np.argmax(prob)

# Termination step
best_path_prob = np.max(V[-1, :])
best_last_state = np.argmax(V[-1, :])

# Path backtracking
best_path = [best_last_state]
for t in range(T - 1, 0, -1):
    best_path.insert(0, backpointer[t, best_path[0]])

V, best_path_prob, best_path
print(V)
print(best_path_prob)
print(best_path)
