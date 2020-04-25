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


#stackover flow says its necessary :D  #only if version of tf is above or equal 2
#tf.compat.v1.disable_eager_execution()
#tf.compat.v1.disable_v2_behavior()


env = make_env()
env.reset()
model = Sequential()
model.add(Conv2D(filters=128, kernel_size=3, strides=1, activation="relu", input_shape=(4, 160,112 ),  data_format="channels_first"))
model.add(Conv2D(filters=64, kernel_size=4, strides=2, activation="relu" ))
model.add(GlobalAveragePooling2D())

model.add(Dense(256, activation='relu'))
model.add(Dense(128,activation='relu'))
model.add(Dense(env.action_space.n, activation='linear'))

#policy = EpsGreedyQPolicy()
policy = MaxBoltzmannQPolicy()
memory = SequentialMemory(limit=50000, window_length=1)
print("--------------------------------------")
print(env.action_space.n)
print("---------------------------------------")

player1 = DQNAgent(model=model,
                   nb_actions=env.action_space.n,
                   enable_dueling_network=True,
                   enable_double_dqn=True,
                   memory=memory,
                   target_model_update=1e-2,
                   nb_steps_warmup=2000,
                   policy=policy) #target_model_update=1e-2,

player1.compile(Adam(lr=1e-3), metrics=['mae'])
player1.fit(env, action_repetition=3, nb_steps=10000, visualize=False)
print(model.summary())
player1.save_weights('mk_18.h5f', overwrite=True)

#player1.test(env, nb_episodes=10, visualize=False)
