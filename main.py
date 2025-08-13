import numpy as np
from src.simulation import run_simulation
from src.units import Unit
from src.utils import load_settings

def main():
    settings = load_settings()

    target = Unit(**settings["target"])
    interceptor = Unit(**settings["inteseptor"])

    run_simulation(target, interceptor, **settings["simulation"])

if __name__ == "__main__":
    main()
