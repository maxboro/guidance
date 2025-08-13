from abc import ABC, abstractmethod
import math
import numpy as np
from .units import Unit
from .utils import wrap_deg

class Guidance(ABC):
    def __init__(self, interceptor: Unit, target: Unit):
        self.interceptor = interceptor
        self.target = target

    @abstractmethod
    def get_angle(self) -> float:
        pass

class PurePursuit(Guidance):
    def get_angle(self) -> float:
        los_vector = self.target.coords - self.interceptor.coords
        los_vector_angle = math.degrees(np.arctan2(los_vector[1], los_vector[0]))
        return los_vector_angle

class PropNav(Guidance):
    def __init__(self, interceptor: Unit, target: Unit):
        super().__init__(interceptor, target)
        self._prev_los_vector_angle = None
        self.gain = 5
        self.dt = 1
        self._gamma_deg = None  # internal missile heading

    def get_angle(self) -> float:
        los_vector = self.target.coords - self.interceptor.coords
        los_vector_angle = math.degrees(np.arctan2(los_vector[1], los_vector[0]))

        if self._prev_los_vector_angle is None and self._gamma_deg is None:
            los_rate_deg = 0
            self._gamma_deg = los_vector_angle
        else:
            los_rate_deg = wrap_deg(los_vector_angle - self._prev_los_vector_angle) / self.dt
            gamma_rate_deg = los_rate_deg * self.gain
            self._gamma_deg = wrap_deg(self._gamma_deg + gamma_rate_deg * self.dt)
        self._prev_los_vector_angle = los_vector_angle
        return self._gamma_deg

def get_guidance(guidance_mode: str) -> Guidance:
    match guidance_mode:
        case "pure_pursuit":
            return PurePursuit
        case "prop_nav":
            return PropNav
