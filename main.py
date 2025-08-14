from src.simulation import run_simulation
from src.units import Unit
from src.utils import load_settings
from src.guidance import get_guidance
from src.missions import get_mission

def main():
    settings = load_settings()

    mission = get_mission(settings["mission"])()
    target = Unit(**settings["target"])
    interceptor = Unit(**settings["inteseptor"])
    guidance = get_guidance(settings["guidance"])(interceptor, target)

    run_simulation(target, interceptor, guidance, mission, **settings["simulation"])

if __name__ == "__main__":
    main()
