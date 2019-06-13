import pygame,sys,os
from level import Level
import random
from utils import direction_to_rowcol
from game_object import GameObject


class Door(GameObject):
    def __init__(self, row, col, locked=True):
        super().__init__(row, col, "D")
        self.locked = locked
    
    def unlock(self):
        self.locked = False
    
    def lock(self):
        self.locked = True
    
    def is_locked(self):
        return self.locked
    
    