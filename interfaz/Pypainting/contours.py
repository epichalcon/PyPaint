import numpy as np
class Contour:
    coords: set
    leftmost:float 
    rightmost: int
    upmost: float 
    downmost: int
    color: int
    num_color: tuple 
    size: int

    def __init__(self, color):
        self.color = color
        self.coords = set()
        self.leftmost = float('inf')
        self.rightmost = 0
        self.upmost = float('inf')
        self.downmost = 0
        self.size = 0
        self.num_color = (0,0,225)

    def add_cord(self, px, py):
        self.coords.add((px, py))

        self.rightmost = max(self.rightmost, px)
        self.downmost = max(self.downmost, py)
        self.leftmost = min(self.leftmost, px)
        self.upmost = min(self.upmost, py)

        self.size += 1
        assert self.size == len(self.coords)

    def get_center(self):
        return tuple (np.mean(list(self.coords), axis=0, dtype=int))
    
    def __len__(self):
        return self.size
