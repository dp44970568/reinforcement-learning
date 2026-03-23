import numpy as np
import random
import matplotlib.pyplot as plt

# Grid setup
grid_size = 3
num_states = grid_size * grid_size
num_actions = 4  # up, down, left, right

# Actions
actions = ['up', 'down', 'left', 'right']

# Parameters
alpha = 0.1        # learning rate
gamma = 0.9        # discount factor
epsilon = 1.0      # initial exploration
epsilon_decay = 0.995
epsilon_min = 0.01

episodes = 500

# Q-table
Q = np.zeros((num_states, num_actions))

# Define goals and obstacle
goals = [8, 6]        # bottom-right & bottom-left
obstacle = 4          # center cell

# Helper functions
def get_next_state(state, action):
    row, col = divmod(state, grid_size)

    if action == 0 and row > 0:       # up
        row -= 1
    elif action == 1 and row < 2:     # down
        row += 1
    elif action == 2 and col > 0:     # left
        col -= 1
    elif action == 3 and col < 2:     # right
        col += 1

    return row * grid_size + col

def get_reward(state):
    if state in goals:
        return 10
    elif state == obstacle:
        return -10
    else:
        return -1  # step penalty

# Training
rewards_per_episode = []

for ep in range(episodes):
    state = 0  # start from top-left
    total_reward = 0

    done = False

    while not done:
        # Epsilon-greedy
        if random.uniform(0,1) < epsilon:
            action = random.randint(0, num_actions - 1)
        else:
            action = np.argmax(Q[state])

        next_state = get_next_state(state, action)
        reward = get_reward(next_state)

        # Q-learning update
        Q[state, action] = Q[state, action] + alpha * (
            reward + gamma * np.max(Q[next_state]) - Q[state, action]
        )

        state = next_state
        total_reward += reward

        if state in goals or state == obstacle:
            done = True

    # Epsilon decay
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    rewards_per_episode.append(total_reward)

# Print Q-table
print("Final Q-table:\n", Q)

# Plot graph
plt.plot(rewards_per_episode)
plt.xlabel("Episodes")
plt.ylabel("Total Reward")
plt.title("Episode vs Total Reward")
plt.show()