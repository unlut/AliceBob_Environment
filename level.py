import os,copy
import random
import numpy as np

class Level:


    def profonksiyon(self, start_column, end_column,
                     start_row, end_row, letter):
        #  find somewhere random which is floor
        object_row = -1
        object_col = -1
        while True:
            rand_row = random.randint(start_row, end_row)
            rand_col = random.randint(start_column, end_column)
            if (self.matrix[rand_row][rand_col] == "F"):
                object_row = rand_row
                object_col = rand_col
                self.matrix[object_row][object_col] = letter
                break
        return object_row, object_col
   
    def __init__(self, map_width=8, map_height=6, split_point=4, hard_night=True, prob_light_on=0.5):
        self.map_width = map_width
        self.map_height = map_height
        self.split_point = split_point
        
        
        self.matrix = []
        self.hist_matrix = []

        #  create a widthXheight matrix filled with FLOOR
        for r in range(map_height):
            self.matrix.append([])
            for c in range(map_width):
                self.matrix[r].append("F")
        
        #  fill split_pointth column with brick wall
        for r in range(map_height):
            self.matrix[r][split_point] = "W"
        

        #  put a door to a random row in split_pointth column
        door_pos_height = random.randint(0, map_height-1)
        self.matrix[door_pos_height][split_point] = "D"

        left_side_start_column = 0
        left_side_end_column = split_point-1
        left_side_start_row = 0
        left_side_end_row = map_height-1

        right_side_start_column = split_point+1
        right_side_end_column = map_width-1
        right_side_start_row = 0
        right_side_end_row = map_height-1

        
        #  put the character and key to a random location of left side of the map
        #  put the character
        self.character_row, self.character_col = self.profonksiyon(left_side_start_column, left_side_end_column,
                     left_side_start_row, left_side_end_row, "C")
        
        #  put the key
        self.key_row, self.key_col = self.profonksiyon(left_side_start_column, left_side_end_column,
                     left_side_start_row, left_side_end_row, "K")
        

        #  put the light
        #if light is on, put it to right side, else to left side
        prob = np.random.uniform(low=0, high=1.0)
        self.light_row, self.light_col = -1, -1
        if (prob >= prob_light_on):
            self.is_light_on = True
            self.light_row, self.light_col = self.profonksiyon(right_side_start_column, right_side_end_column,
                         right_side_start_row, right_side_end_row, "L")
            #print("LIGHT ON RIGHT")
        else:
            self.is_light_on = False
            self.light_row, self.light_col = self.profonksiyon(left_side_start_column, left_side_end_column,
                         left_side_start_row, left_side_end_row, "L")
            #print("LIGHT ON LEFT")


    


    def get_matrix(self):
        return self.matrix

    def save_history(self, matrix):
        pass#self.hist_matrix.append(copy.deepcopy(matrix))

    def undo(self):
        if len(self.hist_matrix) > 0:
            last_matrix = self.hist_matrix.pop()
            self.matrix = last_matrix
            return last_matrix
        else:
            return self.matrix

    def get_character_pos(self):
        # Iterate all Rows
        for r in range(0, len(self.matrix)):
            # Iterate all columns
            for c in range(0, len(self.matrix[r])):
                cell_type = self.matrix[r][c]
                if (cell_type == "C" or cell_type == "A" or cell_type == "B"):
                    return [r, c]

    def get_apple_positions(self):
        apples = []
        for r in range(0, len(self.matrix)):
            for c in range(0, len(self.matrix[r])):
                if self.matrix[r][c] == "P":
                    apples.append([r, c])
        return apples

    def get_robot_positions(self):
        robots = []
        for r in range(0, len(self.matrix)):
            for c in range(0, len(self.matrix[r])):
                if self.matrix[r][c] == "R":
                    robots.append([r, c])
        return robots
    
    def get_key_positions(self):
        keys = []
        for r in range(0, len(self.matrix)):
            for c in range(0, len(self.matrix[r])):
                if self.matrix[r][c] == "K":
                    keys.append([r, c])
        return keys

    def get_light_positions(self):
        lights = []
        for r in range(0, len(self.matrix)):
            for c in range(0, len(self.matrix[r])):
                if self.matrix[r][c] == "L":
                    lights.append([r, c])
        return lights
    
    def get_door_positions(self):
        doors = []
        for r in range(0, len(self.matrix)):
            for c in range(0, len(self.matrix[r])):
                if self.matrix[r][c] == "D":
                    doors.append([r, c])
        return doors

    def get_size(self):
        max_row_length = 0
        for i in range(0, len(self.matrix)):
            row_length = len(self.matrix[i])
            if row_length > max_row_length:
                max_row_length = row_length
        return [len(self.matrix), max_row_length]
