from abc import ABC, abstractmethod

class TargetMission(ABC):
    """Sets dynamics of angle change for a target."""
    @abstractmethod
    def get_angle(self, n_step: int, sim_n_steps: int) -> float:
        pass

class BallisticAttackFromRight(TargetMission):
    def get_angle(self, n_step: int, sim_n_steps: int) -> float:
        return 150 + ((n_step + 1) / sim_n_steps) * 80

class Pursuit(TargetMission):
    def get_angle(self, n_step: int, sim_n_steps: int) -> float:
        return 0 + ((n_step + 1) / sim_n_steps) * 80

def get_mission(mission_name: str) -> TargetMission:
    match mission_name:
        case "BallisticAttackFromRight":
            return BallisticAttackFromRight
        case "Pursuit":
            return Pursuit
