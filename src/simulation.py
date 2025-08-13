import time
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from .units import Unit
from .guidance import Guidance

def interception_event_detection(target: Unit, interceptor: Unit):
    distance = np.linalg.norm(target.coords - interceptor.coords)
    if distance < 2:
        return True
    else:
        return False

def run_simulation(target: Unit, interceptor: Unit, guidance: Guidance, target_fps: float, sim_n_steps: int):
    plt.ion()  # interactive on
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title("Trajectory")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.grid(True); ax.set_aspect("equal", adjustable="box")

    (line,) = ax.plot([], [], "-", label="target", color = "tab:blue")
    (head,) = ax.plot([], [], "o", color = "tab:blue")
    (line2,) = ax.plot([], [], "--", label="interceptor", color="tab:orange")
    (head2,) = ax.plot([], [], "o", color="tab:orange")
    ax.legend(loc="upper left")

    target_x_coords, target_y_coords = [], []
    interceptor_x, interceptor_y = [], []

    frame_dt = 1.0 / target_fps
    for n_step in range(sim_n_steps):
        t0 = time.perf_counter()

        # ---- simulation step ----
        target.update(150 + n_step / 1.5)
        proposed_interception_angle = guidance.get_angle()
        interceptor.update(proposed_interception_angle)

        target_x_coords.append(target.coords[0])
        target_y_coords.append(target.coords[1])

        interceptor_x.append(interceptor.coords[0])
        interceptor_y.append(interceptor.coords[1])

        # ---- draw/update artists ----
        line.set_data(target_x_coords, target_y_coords)
        head.set_data([target_x_coords[-1]], [target_y_coords[-1]])

        line2.set_data(interceptor_x, interceptor_y)
        head2.set_data([interceptor_x[-1]], [interceptor_y[-1]])

        ax.relim(); ax.autoscale_view()
        plt.title(f'Trajectory. IC Angle {proposed_interception_angle:,.1f}')

        # This processes GUI events + draws without freezing the window
        plt.pause(0.001)

        if interception_event_detection(target, interceptor):
            print("Intercepted")
            break

        # Pace the loop to ~target_fps
        slept = time.perf_counter() - t0
        if slept < frame_dt:
            time.sleep(frame_dt - slept)

    plt.ioff()
    plt.show()
