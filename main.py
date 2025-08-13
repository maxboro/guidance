import numpy as np
from src.simulation import run_simulation
from src.units import Unit

def main():
    coords_target = np.array([100, 100])
    coords_interceptor = np.array([0, 0])

    target = Unit(coords_target, speed=2)
    interceptor = Unit(coords_interceptor, speed = 3)

    run_simulation(target, interceptor)

if __name__ == "__main__":
    main()
