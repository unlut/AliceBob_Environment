import pygame,sys,os
from level import Level
import random
from utils import direction_to_rowcol


class GameObject:
    def __init__(self, row, col, type_string=""):
        self.row = row
        self.col = col

        self.type_string = type_string

        self.current_pos = [self.row, self.col]
    

    def get_pos(self):
        return self.current_pos

    def get_row(self):
        return self.get_pos()[0]

    def get_col(self):
        return self.get_pos()[1]