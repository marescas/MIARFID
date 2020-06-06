import gym
import numpy as np
def Q_Learning(game,alpha=0.1):
    print("hey")
if __name__ == '__main__':
    env = gym.make('MountainCar-v0')
    env.reset()
    num_states = (env.observation_space.high - env.observation_space.low) * \
                 np.array([10, 100])
    num_states = np.round(num_states, 0).astype(int) + 1
    print(env.observation_space.high)
    print(num_states)
    print((2,) + env.observation_space.shape)
    """for _ in range(1000):
        env.render()
        env.step(env.action_space.sample())  # take a random action
    env.close()"""