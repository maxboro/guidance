from abc import ABC, abstractmethod
import math
import numpy as np
from .units import Unit

class Guidance(ABC):

    @abstractmethod
    def __init__(self, interceptor: Unit, target: Unit):
        pass

    @abstractmethod
    def get_angle(self) -> float:
        pass

class PurePursuit(Guidance):
    def __init__(self, interceptor: Unit, target: Unit):
        self.interceptor = interceptor
        self.target = target

    def get_angle(self) -> float:
        direction_vector = self.target.coords - self.interceptor.coords
        direction_vector_angle = math.degrees(np.arctan2(direction_vector[1], direction_vector[0]))
        return direction_vector_angle

def get_guidance(guidance_mode: str) -> Guidance:
    match guidance_mode:
        case "pure_pursuit":
            return PurePursuit
