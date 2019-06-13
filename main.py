import time
import sys
import os


#  import constant definitions
from macros import *

#  import agent classes
from random_agent import RandomAgent


#  for mathematical operations
import numpy as np

#  for saving our agents
import pickle

#  import game class
from alicebob import Game

#  import openai gym
import gym












#First command line argument is player_string
player_string = ""
if (len(sys.argv) >= 2):
    player_string = sys.argv[1]
else:
    #  no argument is provided, assign player_string hardcodedly
    player_string = "HUMAN"
    #player_string = "RL"
    #player_string = "RL_TEST"





#  display player and played level
print("Player {} will be playing".format(player_string))








env = Game()
if (player_string == "HUMAN"):
    (collected_apple_count, apple_distance_rewards, wall_crash_penalties, elapsed_time_step, robot_death_penalty) = env.start_level_human()
    printed_str = "--- Player Statistics ---\n"
    printed_str += "collected apple count:{}\n".format(collected_apple_count)
    printed_str += "total apple distance reward:{}\n".format(np.sum(apple_distance_rewards))
    printed_str += "total wall crash penalty:{}\n".format(np.sum(wall_crash_penalties))
    printed_str += "robot death penalty:{}\n".format(robot_death_penalty)
    printed_str += "total reward:{}\n".format(collected_apple_count*COLLECT_APPLE_REWARD + np.sum(apple_distance_rewards) + np.sum(wall_crash_penalties) + robot_death_penalty)
    printed_str += "elapsed time step:{}\n".format(elapsed_time_step)
    print(printed_str)
elif (player_string == "RL"):

    EPISODES = 100
    MAX_TIMESTEP = 300

    for eps in range(EPISODES):
        s = env.reset(render_env=True, display_env=True, current_player_name="Alice", obs_type="PIXEL")

        for t in range(MAX_TIMESTEP):
            action = np.random.randint(0, 5)
            next_state, reward, done, info = env.step(action)
            time.sleep(0.01)

            if (done):
                break
        
        print("Episode {} finished after {} timesteps".format(eps, t+1))
        print(info)