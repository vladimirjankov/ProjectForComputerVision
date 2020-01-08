import numpy as np
import retro
import tensorflow as tf
from keras.models import Sequential


from keras.layers import Dense, Activation, Flatten, Conv2D,SimpleRNN,GlobalAveragePooling2D
from keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, GreedyQPolicy, MaxBoltzmannQPolicy
from rl.memory import SequentialMemory
from mortalkombat_env import PlayerOneNetworkControllerWrapper, ObservationWraperMK, make_env


#stackover flow says its necessary :D 
#tf.compat.v1.disable_eager_execution()

env = make_env()

model = Sequential()
model.add(Conv2D(filters=64, kernel_size=8, strides=8, activation="relu", input_shape=(4, 112, 160),
                 data_format="channels_first"))
model.add(Conv2D(filters=32, kernel_size=4, strides=4, activation="relu" ))
model.add(Conv2D(filters=16, kernel_size=3, strides=2, activation="relu"))
model.add(GlobalAveragePooling2D())

model.add(Dense(512, activation='relu'))
model.add(Dense(128,activation='relu'))
model.add(Dense(env.action_space.n, activation='linear'))

policy = EpsGreedyQPolicy()
memory = SequentialMemory(limit=50000, window_length=1)
print("--------------------------------------")
print(env.action_space.n)
print("---------------------------------------")

player1 = DQNAgent(model=model,
                   nb_actions=env.action_space.n,
                   enable_dueling_network=True,
                   enable_double_dqn=True,
                   memory=memory,
                   nb_steps_warmup=500,
                   target_model_update=1e-2,
                   policy=policy)

player1.compile(Adam(lr=1e-3), metrics=['mae'])
player1.fit(env, action_repetition=10, nb_steps=50000, nb_max_episode_steps=1000, visualize=True, verbose=2)
print(model.summary())
player1.save_weights('mk_7.h5f', overwrite=True)

#player1.test(env, nb_episodes=10, visualize=True)