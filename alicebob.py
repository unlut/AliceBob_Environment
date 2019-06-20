import time
import sys
import os


import pygame
from copy import deepcopy

#  import game object classes
from level import Level
from player import Player
from robot import Robot
from apple import Apple
from key import Key
from door import Door
from light import Light

#  import constant definitions
from macros import *


#  for mathematical operations
import numpy as np


#  openai gym
import gym
import gym.spaces

class Game(gym.Env):
    def __init__(self, game_window_name="Alicebob"):
        #  initialize pygame stuff
        pygame.display.init()
        pygame.mixer.init()

        #wall_width = self.wall.get_width()
        wall_width = 36
        self.wall_width = wall_width
        

        pygame.display.set_caption(game_window_name)
        self.screen = pygame.display.set_mode(game_window_size)
        self.clock = pygame.time.Clock()
        
        #  create a buffer
        #self.gameDisplay = pygame.Surface((display_width, display_height))
        
        

		# Load images, with night versions
        self.wall = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/brick_wall.png').convert(), (wall_width, wall_width))
        self.wall_night = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/brick_wall_night.png').convert(), (wall_width, wall_width))

        self.apple = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/apple.png').convert(), (wall_width, wall_width))
        self.apple_night = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/apple_night.png').convert(), (wall_width, wall_width))
        
        self.floor = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/floor_white.png').convert(), (wall_width, wall_width))
        self.floor_night = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/floor.png').convert(), (wall_width, wall_width))
        
        self.grass = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/grass.png').convert(), (wall_width, wall_width))
        self.grass_night = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/grass_night.png').convert(), (wall_width, wall_width))
        
        self.alice = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/alice.png').convert(), (wall_width, wall_width))
        self.alice_night = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/alice_night.png').convert(), (wall_width, wall_width))

        self.bob = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/bob.png').convert(), (wall_width, wall_width))
        self.bob_night = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/bob_night.png').convert(), (wall_width, wall_width))
       
        self.robot = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/robot_bg.png').convert(), (wall_width, wall_width))

        self.light = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/light_on.png').convert(), (wall_width, wall_width))
        self.light_night = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/light_off.png').convert(), (wall_width, wall_width))

        self.finish_flag = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/finish_flag.png').convert(), (wall_width, wall_width))

        self.door = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/brick_door.png').convert(), (wall_width, wall_width))
        self.door_night = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/brick_door_night.png').convert(), (wall_width, wall_width))

        self.key = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/key.png').convert(), (wall_width, wall_width))
        self.key_night = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/key_night.png').convert(), (wall_width, wall_width))
        

        #  load sounds
        self.win_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '/sounds/tada.wav')
        self.lose_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '/sounds/fail_trombone_4s.wav')

		# Dictionary to map images to characters in level matrix
        self.images = {'W': self.wall, 
                    'P': self.apple, 
                    'F': self.floor, 
                    'G': self.grass, 
                    'A': self.alice,
                    'B': self.bob, 
                    'R': self.robot,
                    'I': self.finish_flag,
                    'L': self.light,
                    'D': self.door,
                    'K': self.key}
        
        #  Night image dictionary
        self.images_night = {'W': self.wall_night, 
                    'P': self.apple_night, 
                    'F': self.floor_night, 
                    'G': self.grass_night, 
                    'A': self.alice_night,
                    'B': self.bob_night, 
                    'R': self.robot,
                    'I': self.finish_flag,
                    'L': self.light_night,
                    'D': self.door_night,
                    'K': self.key_night}

        self.current_level = None
        self.current_level_number = 0

		#  player object
        self.player = None

		#  robots
        self.robots = []

        self.game_finished = False
        self.player_alive = True
        self.light_on = False

        """
        Current level statistics
        """
        #  number of apples player collected so far in curret level
        self.collected_apple_count = 0

        #  number of all apples in the initial level configuration
        self.total_apple_count = 0

        #  key info
        self.collected_key_count = 0
        self.total_key_count = 0
        self.used_key_count = 0

        #  number of time steps elapsed in a level
        self.elapsed_time_step = 0

        #  
        self.distance_to_closest_apple = 0

        self.crashed_into_wall = False



        #  stuff for gym environment
        self.render_env = True
        self.display_env = True
        self.current_player_name = ""
        self.obs_type = "PIXEL"
        self.episode_limit = 0
        self.episode_limit_reached = False

        self._action_set = ["R", "U", "L", "D", "PASS"]
        self.action_space = gym.spaces.Discrete(len(self._action_set))

        #  observation space???
        #???


        #  alicebob stuff
        self.alice_started_state = None
        self.alice_stopped_state = None
        self.alice_stopped = False
    
    def GetGameScreen(self):
        
        return pygame.surfarray.array3d(self.screen)

        #  below function returns a direct reference of screen, but locks
        #return pygame.surfarray.pixels3d(self.screen)



    """
    Taken from openaigym atari_env

    Seed function exists but has no effect
    """
    def seed(self, seed=None):
        self.np_random, seed1 = gym.utils.seeding.np_random(seed)
        
        print("Generated seed:", seed1)
        return seed1

    def step(self, a):
        reward = 0.0
        action = self._action_set[a]

        #print("action:", action)
        reward = self.step_env(action, self.display_env)

        ob = self._get_obs()
        
        info = {}
        pname = self.current_player_name.upper()
        done = self.game_finished
        if (pname == "ALICE"):
            if (self.alice_stopped):
                self.alice_stopped = False
                info["done_reason"] = "Alice decided to stop at timestep {}".format(self.elapsed_time_step)
                done = True
        elif (pname == "BOB"):
            if (self.current_level.get_matrix() == self.alice_stopped_state.get_matrix()):
                done = True
                info["done_reason"] = "Bob reached the last state of Alice at timestep {}".format(self.elapsed_time_step)
                #print("BOB matrix")
                #print(self.current_level.get_matrix())
                #print("ALICE matrix")
                #print(self.alice_stopped_state.get_matrix())
        
        if (self.episode_limit_reached):
            done = True
            info["done_reason_episode_limit"] = "Episode limit {} is reached".format(self.episode_limit)


        reward = 0
        return ob, reward, done, info
    

    @property
    def _n_actions(self):
        return left(self._action_set)


    def _get_obs(self):
        """
        WHAT IS OBSERVATION?
        """
        ob = None
        if (self.obs_type == "PIXEL"):
            ob = self.GetGameScreen()
        elif (self.obs_type == "FEATURE"):
            pass
        return ob
    
    """
    FILL THIS FUNCTION
    """
    def render(self, mode="human"):
        pass


    def reset(self, render_env=True, display_env=True, 
                current_player_name="Alice", obs_type="PIXEL", episode_limit=25, hard_night=True,
                map_width=8, map_height=6, split_point=4,
                prob_light_on=0.5):
        
        self.render_env = render_env
        self.display_env = display_env
        self.current_player_name = current_player_name
        self.obs_type = obs_type
        self.episode_limit = episode_limit

        self.map_width = map_width
        self.map_height = map_height

        self.required_screen_width = self.map_width * self.wall_width
        self.required_screen_height = self.map_height * self.wall_width
        self.game_window_size = (self.required_screen_width, self.required_screen_height)

        if (display_env):
            self.screen = pygame.display.set_mode(self.game_window_size)
        elif (render_env):
            self.screen = pygame.Surface(self.game_window_size)
        else:
            pass

        pname = current_player_name.upper()
        if (pname == "ALICE"):
            #  if current player is alice, generate level normally and save starting grid
            self.init_level(hard_night, current_player_name,
                            map_width, map_height, split_point,
                            prob_light_on)
            self.init_objects()

            self.alice_started_state = deepcopy(self.current_level)
            self.alice_stopped_state = None
            self.alice_stopped = False
        elif (pname == "BOB"):
            #  use same starting state as alice
            if (self.alice_started_state == None):
                print("ALICE MUST PLAY FIRST BEFORE BOB!")
                raise Exception("ALICE MUST PLAY FIRST BEFORE BOB!") 
            self.current_level = self.alice_started_state
            self.init_objects()


        self.elapsed_time_step = 0
        self.episode_limit_reached = False
        self.game_finished = False
        self.alice_stopped = False

        pname = self.current_player_name.upper()
        if (pname == "ALICE"):
            self.images["C"] = self.alice
            self.images_night["C"] = self.alice_night
            self.alice_stopped_state = None
        elif (pname == "BOB"):
            self.images["C"] = self.bob
            self.images_night["C"] = self.bob_night

        ob = self._get_obs()

        return ob
        
        
            

    def set_render_mode(self, render_env, display_env):
        if (display_env):
            self.screen = pygame.display.set_mode(self.game_window_size)
        elif (render_env):
            self.screen = pygame.Surface(self.game_window_size)
        self.render_env = render_env
        self.display_env = display_env


    def draw_level(self, level_matrix):
        # Get image size to print on screen
        #box_size = self.wall.get_width()
        box_size = self.wall_width

        #  what exactly this do
        #self.screen.unlock()
      
        # Print images for matrix
        if (self.light_on):
            for i in range(0, len(level_matrix)):
                for c in range(0, len(level_matrix[i])):
                    self.screen.blit(self.images[level_matrix[i][c]], (c * box_size, i * box_size))
        else:
            if (self.hard_night):
                #  only alice, bob, light, floors and walls are displayed in hard night mode
                for i in range(0, len(level_matrix)):
                    for c in range(0, len(level_matrix[i])):
                        s = level_matrix[i][c]
                        if (s == "A" or s == "B" or s == "W" or s == "L" or s == "C" or s == "F" or s == "D"):
                            self.screen.blit(self.images_night[s], (c * box_size, i * box_size))
                        else:
                            self.screen.blit(self.images_night["F"], (c * box_size, i * box_size))
            else:
                for i in range(0, len(level_matrix)):
                    for c in range(0, len(level_matrix[i])):
                        self.screen.blit(self.images_night[level_matrix[i][c]], (c * box_size, i * box_size))
        
        #pygame.display.update()
        

    def init_objects(self):
        #  create player object
        player_pos = self.current_level.get_character_pos()
        player_current_row = player_pos[0]
        player_current_col = player_pos[1]
        self.player = Player(player_current_row, player_current_col)

        #  create robots
        self.robots = []
        robot_positions = self.current_level.get_robot_positions()
        for pos in robot_positions:
            r = pos[0]
            c = pos[1]
            self.robots.append(Robot(r, c, self.current_level.get_matrix()))

        #  create apples
        self.apples = []
        apple_positions = self.current_level.get_apple_positions()
        for pos in apple_positions:
            r = pos[0]
            c = pos[1]
            self.apples.append(Apple(r, c))

        #  create doors
        self.doors = []
        door_positions = self.current_level.get_door_positions()
        for pos in door_positions:
            r = pos[0]
            c = pos[1]
            self.doors.append(Door(r, c))
        
        #  create keys
        self.keys = []
        key_positions = self.current_level.get_key_positions()
        for pos in key_positions:
            r = pos[0]
            c = pos[1]
            self.keys.append(Key(r, c))
        
        #  create lights
        self.lights = []
        light_positions = self.current_level.get_light_positions()
        for pos in light_positions:
            r = pos[0]
            c = pos[1]
            self.lights.append(Light(r, c))
        
        #  count number of apples
        self.total_apple_count = len(self.apples)
        #print("Number of apples in the level ", self.total_apple_count)
        

        #  count keys and doors
        self.total_key_count = len(self.keys)


    def init_level(self, hard_night=True, current_player_name="Alice",
                    map_width=8, map_height=6, split_point=4,
                    prob_light_on=0.5):
        self.current_level = Level(map_width=map_width, map_height=map_height, split_point=split_point,
                                    hard_night=hard_night, prob_light_on=prob_light_on)
        #self.draw_level(self.current_level.get_matrix())
        self.map_width = self.current_level.map_width
        self.map_height = self.current_level.map_height

        #  mark game as not finished
        self.game_finished = False
        self.player_alive = True
        self.hard_night = hard_night
        self.light_on = self.current_level.is_light_on
        self.current_player_name = current_player_name


        pname = self.current_player_name.upper()
        if (pname == "ALICE"):
            self.images["C"] = self.alice
            self.images_night["C"] = self.alice_night
        elif (pname == "BOB"):
            self.images["C"] = self.bob
            self.images_night["C"] = self.bob_night
        

        #  number of time steps elapsed in a level
        self.elapsed_time_step = 0

        #  initialize number of apples player collected so far in curret level
        self.collected_apple_count = 0

        #  whether played tried to move into wall at last step
        self.crashed_into_wall = False
        


    

    """
    Calculates distance between player and the closest apple to player
    """
    def get_closest_apple_to_player(self):
        player_pos = self.player.get_pos()
        pr = player_pos[0]
        pc = player_pos[1]

        minDist = 1000
        closestApple = None
        for apple in self.apples:
            apple_pos = apple.get_pos()
            rr = apple_pos[0]
            rc = apple_pos[1]
            dist = np.abs(pr - rr) + np.abs(pc - rc)
            if (dist < minDist):
                minDist = dist
                closestApple = apple
        
        return (closestApple, minDist)


    def step_env(self, player_direction, render=True):
        matrix = self.current_level.get_matrix()
        self.current_level.save_history(matrix)

        #Print apples
        #print(self.current_level.get_apple_positions())

        #  robots movement
        for robot in self.robots:
            #robot_old_pos = robot.get_pos()
            #robot_old_row = robot_old_pos[0]
            #robot_old_col = robot_old_pos[1]

            robot_dir = robot.choose_dir()
            robot_new_pos = robot.move(robot_dir)
            robot_next_row = robot_new_pos[0]
            robot_next_col = robot_new_pos[1]
       

		#  save old position of the player
        player_current_pos = self.player.get_pos()
        player_current_row = player_current_pos[0]
        player_current_col = player_current_pos[1]

		#  calculate new position of the player
        player_next_pos = self.player.move(player_direction)
        player_next_row = player_next_pos[0]
        player_next_col = player_next_pos[1]


        #  resolve static collision for robots
        #  NOT USED CURRENTLY
        for robot in self.robots:
            robot_prev_pos = robot.get_prev_pos()
            robot_prev_row = robot_prev_pos[0]
            robot_prev_col = robot_prev_pos[1]

            robot_next_pos = robot.get_pos()
            robot_next_row = robot_next_pos[0]
            robot_next_col = robot_next_pos[1]

            next_cell = matrix[robot_next_row][robot_next_col]
            if next_cell == "F":
                #  next cell is floor
                pass
            elif ((next_cell == "G")
                  or (next_cell == "W")
                  or (next_cell == "A")):
                #  next cell is grass or wall or apple
                #robot cant pass here
                robot.current_pos = robot_prev_pos
            elif (next_cell == "R"):
                #  go into another robot
                pass
            elif (next_cell == "P"):
                #  will resolve later
                pass
        
        
        #  out of bounds check
        if (player_next_row < 0 or player_next_row >= self.current_level.map_height
            or player_next_col < 0 or player_next_col >= self.current_level.map_width):
            self.player.current_pos = self.player.prev_pos
        else:

            #  resolve static collisions for player
            next_cell = matrix[player_next_row][player_next_col]
            if (next_cell == "F"):
                #  next cell is floor
                pass
            elif (next_cell == "W"):
                #  next cell is wall
                #player cant pass here
                self.player.current_pos = self.player.prev_pos
                self.crashed_into_wall = True
            elif (next_cell == "G"):
                #  next cell is grass
                #player removes grass
                matrix[player_next_row][player_next_col] = "C"
            elif (next_cell == 'P'):
                #  next cell is apple
                #player removes apple
                matrix[player_next_row][player_next_col] = "C"
            elif (next_cell == "R"):
                #  next square is robot
                #will resolve later
                pass
            elif (next_cell == "A" or next_cell == "B"):
                #  next cell is alice or bob?
                pass
            elif (next_cell == "I"):
                #  next cell is finish flag
                pass
            elif (next_cell == "L"):
                #  next cell is light switch
                self.light_on = not self.light_on 
            elif (next_cell == "K"):
                #  next cell is key
                #player removes key
                matrix[player_next_row][player_next_col] = "C"
            elif (next_cell == "D"):
                #  next cell is door
                pass

            

        
        #  check if player collected an apple or key
        #  TO DO: create a 2d apple grid for faster check
        new_apples = []
        for apple in self.apples:
            apple_pos = apple.get_pos()
            apple_row = apple_pos[0]
            apple_col = apple_pos[1]
            if (player_next_row == apple_row and player_next_col == apple_col):
                #player removes apple
                #  check if game is finished
                self.collected_apple_count += 1
                if (self.collected_apple_count == self.total_apple_count):
                    self.game_finished = True
            else:
                new_apples.append(apple)
        self.apples = new_apples

        new_keys = []
        for key in self.keys:
            key_pos = key.get_pos()
            key_row = key_pos[0]
            key_col = key_pos[1]
            if (player_next_row == key_row and player_next_col == key_col):
                #player removes key
                self.collected_key_count += 1
                #print("collected a key")
            else:
                new_keys.append(key)
        self.keys = new_keys

        #find if player collide with a door
        for door in self.doors:
            door_pos = door.get_pos()
            door_row = door_pos[0]
            door_col = door_pos[1]
            if (door_row == player_next_row and door_col == player_next_col):
                if (door.is_locked()):
                    #  check if player has a key to unlock the door
                    if (self.collected_key_count > self.used_key_count):
                        #  player can open the door
                        self.used_key_count += 1
                        door.unlock()
                    else:
                        #  player needs a key
                        #bump player back
                        #print("Door is locked")
                        self.player.current_pos = self.player.prev_pos

                else:
                    #  door is already unlocked
                    
                    pass



            

        player_next_row = self.player.current_pos[0]
        player_next_col = self.player.current_pos[1]


        #  resolve dynamic player-robot collisions
        #  NOT USED CURRENTLY
        for robot in self.robots:
            robot_prev_pos = robot.get_prev_pos()
            robot_prev_row = robot_prev_pos[0]
            robot_prev_col = robot_prev_pos[1]

            robot_next_pos = robot.get_pos()
            robot_next_row = robot_next_pos[0]
            robot_next_col = robot_next_pos[1]

            #  CASE 1
            #player and robot moves into same cell
            if (robot_next_row == player_next_row and robot_next_col == player_next_col):
                #print("CASE 1: Player and robot {} moved into same cell!".format(robot.get_id()))
                self.player_alive = False
                self.game_finished = True
            
            #  CASE 2
            #player in cell C1, robot in cell C2
            #player moves from C1 to C2
            #robot moves from C3 to C4
            #C1 == C4 AND C2 == C3
            if (player_current_pos == robot_next_pos and player_next_pos == robot_prev_pos):
                #print("CASE 2: Player and robot {} passed by!".format(robot.get_id()))
                self.player_alive = False
                self.game_finished = True


        #  update game matrix
        level_matrix = self.current_level.get_matrix()
        for robot in self.robots:
            robot_old_pos = robot.get_prev_pos()
            robot_old_row = robot_old_pos[0]
            robot_old_col = robot_old_pos[1]
            robot_new_pos = robot.get_pos()
            robot_next_row = robot_new_pos[0]
            robot_next_col = robot_new_pos[1]

            level_matrix[robot_old_row][robot_old_col] = "F"
            level_matrix[robot_next_row][robot_next_col] = "R"
        player_prev_row = self.player.get_prev_row()
        player_prev_col = self.player.get_prev_col()
        player_next_row = self.player.get_row()
        player_next_col = self.player.get_col()

        #  if there is not a robot in the previous cell of player, clear it
        prev_cell_type = level_matrix[player_prev_row][player_prev_col]
        if (prev_cell_type != "R"):
            level_matrix[player_prev_row][player_prev_col] = "F"
        

        #  apply keys
        for key in self.keys:
            key_pos = key.get_pos()
            key_row = key_pos[0]
            key_col = key_pos[1]
            level_matrix[key_row][key_col] = "K"
        
        #  apply doors
        for door in self.doors:
            door_pos = door.get_pos()
            door_row = door_pos[0]
            door_col = door_pos[1]
            level_matrix[door_row][door_col] = "D"
        
        #  apply lights
        for light in self.lights:
            light_pos = light.get_pos()
            light_row = light_pos[0]
            light_col = light_pos[1]
            level_matrix[light_row][light_col] = "L"
        
        
        level_matrix[player_next_row][player_next_col] = "C"

        #  draw
        if (self.render_env or self.display_env):
            self.draw_level(matrix)
            if (self.display_env):
                pygame.display.update()
    
        self.elapsed_time_step += 1

        #remaining_apple_count = len(self.current_level.get_apple_positions())
        #print("Number of remaining apples: ", remaining_apple_count)


        #  check if character outputs a stop action
        if (player_direction == "PASS"):
            pname = self.current_player_name.upper()
            if (pname == "ALICE"):
                #  alice's pass action finishes the game
                self.game_finished = True
                self.alice_stopped_state = deepcopy(self.current_level)
                self.alice_stopped = True
                #print("ALICE PASSED")
            elif (pname == "BOB"):
                #  bob's pass action does nothing
                pass
        
        #  check if episode limit reached
        if (self.elapsed_time_step == self.episode_limit):
            #  episode limit reached
            self.game_finished = True
            self.episode_limit_reached = True
            pname = self.current_player_name.upper()
            if (pname == "ALICE"):
                self.alice_stopped_state = deepcopy(self.current_level)
        

        #  hack return
        return RESULT_GAME_CONTINUE


    #  function when a human player plays the game
    def start_level_human(self):
        self.init_level()
        self.init_objects()
        self.draw_level(self.current_level.get_matrix())
        pygame.display.update()


		#  number of all apples in the initial level configuration
        self.total_apple_count = len(self.apples)
        
        #  at each time step, distance of player to the closest apple
        apple_distance_rewards = []
        
        #  negative reward if crash into wall
        wall_crash_penalties = []

        #self.distance_to_closest_apple = self.get_closest_apple_to_player()[1]

        #  game loop
        while True:
            result = 0

            #  manual input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #self.craft_features()

                    if event.key == pygame.K_RIGHT:
                        result = self.step_env("R", render=True)
                    elif event.key == pygame.K_UP:
                        result = self.step_env("U", render=True)
                    elif event.key == pygame.K_LEFT:
                        result = self.step_env("L", render=True)
                    elif event.key == pygame.K_DOWN:
                        result = self.step_env("D", render=True)
                    elif event.key == pygame.K_SPACE:
                        result = self.step_env("PASS", render=True)
                    #elif event.key == pygame.K_u:
                    #    self.draw_level(self.current_level.undo())
                    elif event.key == pygame.K_r:
                        self.init_level(self.current_level_number)
                        result = RESULT_GAME_CONTINUE
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    
                    
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if (result == RESULT_PLAYER_WON or result == RESULT_PLAYER_DEAD):
                sound_channel = None
                if (result == RESULT_PLAYER_WON):
                    #print("WON")
                    sound_channel = self.win_sound.play()
                else:
                    #print("LOSE")
                    sound_channel = self.lose_sound.play()

                #  wait for sound to end
                while sound_channel.get_busy() == True:
                    continue
                break
            else:
                #  

                """
                new_closest_apple_dist = self.get_closest_apple_to_player()[1]
                if (new_closest_apple_dist > self.distance_to_closest_apple):
                    apple_distance_rewards.append(MOVING_AWAY_FROM_APPLE)
                elif (new_closest_apple_dist < self.distance_to_closest_apple):
                    apple_distance_rewards.append(GETTING_CLOSER_TO_APPLE_REWARD)
                self.distance_to_closest_apple = new_closest_apple_dist
                """        
                if (self.crashed_into_wall):
                    self.crashed_into_wall = False
                    wall_crash_penalties.append(WALL_CRASH_PENALTY)
    

        #  if killed by robot, give penalty
        robot_death_penalty = 0
        if (result == RESULT_PLAYER_DEAD):
            robot_death_penalty = ROBOT_DEATH_PENALTY

        #  return a tuple of
        #(number of collected apples, elapsed time step)
        return (self.collected_apple_count, apple_distance_rewards, wall_crash_penalties,
                self.elapsed_time_step, robot_death_penalty)



    """
   
    """
    def craft_features(self):
        player_pos = self.player.get_pos()
        pr = player_pos[0]
        pc = player_pos[1]
        matrix = self.current_level.get_matrix()

        #  features showing whether 4 cardinal direction cells blocked or not 
        checked_cell = matrix[pr][pc+1]
        right_blocked = int( (checked_cell == "W") )
        checked_cell = matrix[pr-1][pc]
        up_blocked = int( (checked_cell == "W") )
        checked_cell = matrix[pr][pc-1]
        left_blocked = int( (checked_cell == "W") )
        checked_cell = matrix[pr+1][pc]
        down_blocked = int( (checked_cell == "W") )
        

        #  features showing whether 4 cardinal direction cells contains robot danger or not
        drs = [0, -1, 0, 1]
        dcs = [1, 0, -1, 0]
        matrix_height = len(matrix)
        matrix_width = len(matrix[0])
        robot_vector = np.zeros(4)
        for c in range(4):
            #  calculate cth adjacent cell
            adj_cell_row = pr + drs[c]
            adj_cell_col = pc + dcs[c]

            #  check if there is a robot in the cell
            if (matrix[adj_cell_row][adj_cell_col] == "R"):
                robot_vector[c] = 1.0
                continue
            
            #  check if there is a robot danger in the cell
            for dr in drs:
                for dc in dcs:
                    if (adj_cell_row + dr >= 0 and adj_cell_row + dr < matrix_height
                        and adj_cell_col + dc >= 0 and adj_cell_col + dc < matrix_width
                        and matrix[adj_cell_row + dr][adj_cell_col + dc] == "R"):
                        robot_vector[c] = 1.0
                        break


        #right_robot = int( (checked_cell == "R") )
        #up_robot = int( (checked_cell == "R") )
        #left_robot = int( (checked_cell == "R") )
        #down_robot = int( (checked_cell == "R") )


        #  
        blocked_vector = np.array([right_blocked, up_blocked, left_blocked, down_blocked])
        #robot_vector = np.array([right_robot, up_robot, left_robot, down_robot])

        #  calculate vector that shows the apple direction
        closest_apple = self.get_closest_apple_to_player()[0]
        closest_apple_pos = closest_apple.get_pos()
        closest_apple_row = closest_apple_pos[0]
        closest_apple_col = closest_apple_pos[1]
        closest_apple_vector = np.array([closest_apple_row - pr, closest_apple_col - pc])

        #  normalize direction vector
        closest_apple_vector_norm = np.linalg.norm(closest_apple_vector)
        if (closest_apple_vector_norm == 0):
            closest_apple_vector_norm = len(matrix)
        closest_apple_vector = closest_apple_vector / closest_apple_vector_norm

        #  obtain feature vector by merging blocked and direction vectors
        feature_vector = np.concatenate([blocked_vector, robot_vector, closest_apple_vector])

        #print("--- MATRIX ---")
        #print(matrix)
        #print("--- FEATURES ---")
        #print(feature_vector)

        #  return feature vector
        return feature_vector

    def start_level_computer(self, level_index, agent, 
                             render=False, play_sound=False,
                             max_episode_length=150,
                             use_crafted_features=True,
                             test=False):
        self.init_level(level_index)

        if (render):
            self.draw_level(self.current_level.get_matrix())


		#  number of all apples in the initial level configuration
        self.total_apple_count = len(self.apples)
        
        #  at each time step, distance of player to the closest apple
        apple_distance_rewards = []
        
        #  negative reward if crash into wall
        wall_crash_penalties = []

        self.distance_to_closest_apple = self.get_closest_apple_to_player()[1]
    
        while True:
            result = 0

            #  input source will use matrix to decide
            matrix = self.current_level.get_matrix()

            network_input = None
            if (use_crafted_features):
                network_input = self.craft_features()
            else:
                #  convert grid to network input
                network_input = agent.grid_to_network_input(matrix)
            chosen_action = agent.decide_move(network_input)

            #  apply decided action
            result = self.step_env(chosen_action, render=render)

            #  if we want to render our agent, wait some time 
            if (render):
                self.clock.tick(FPS)

            #  check if game finished
            if (result == RESULT_PLAYER_WON or result == RESULT_PLAYER_DEAD):
                if (play_sound):
                    sound_channel = None
                    if (result == RESULT_PLAYER_WON):
                        sound_channel = self.win_sound.play()
                    else:
                        sound_channel = self.lose_sound.play()

                    #  wait for sound to end
                    while sound_channel.get_busy() == True:
                        continue
                break
            else:
                #  
                new_closest_apple_dist = self.get_closest_apple_to_player()[1]
                if (new_closest_apple_dist > self.distance_to_closest_apple):
                    apple_distance_rewards.append(MOVING_AWAY_FROM_APPLE)
                elif (new_closest_apple_dist < self.distance_to_closest_apple):
                    apple_distance_rewards.append(GETTING_CLOSER_TO_APPLE_REWARD)
                self.distance_to_closest_apple = new_closest_apple_dist
            
                if (self.crashed_into_wall):
                    self.crashed_into_wall = False
                    wall_crash_penalties.append(WALL_CRASH_PENALTY)
            
            #  check if we reached episode length
            if (self.elapsed_time_step >= max_episode_length):
                break
        

        #  if killed by robot, give penalty
        robot_death_penalty = 0
        if (result == RESULT_PLAYER_DEAD):
            robot_death_penalty = ROBOT_DEATH_PENALTY

        #  return a tuple of
        #(number of collected apples, elapsed time step)
        return (self.collected_apple_count, apple_distance_rewards, wall_crash_penalties,
                self.elapsed_time_step, robot_death_penalty)
    
