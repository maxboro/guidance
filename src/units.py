import math
import numpy as np

class Unit:
    """
    Movable object.
    
    Has constant speed.
    """
    def __init__(self, start_x: float, start_y: float, speed: float):
        self.coords = np.array([start_x, start_y], dtype=float)
        self.speed = speed

    def update(self, angle_deg: float):
        angle_rad = math.radians(angle_deg)
        unit_vector = np.array([math.cos(angle_rad), math.sin(angle_rad)])
        vector_speed = self.speed * unit_vector
        self.coords += vector_speed
