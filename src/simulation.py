import time
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from .units import Unit

def run_simulation(target: Unit, interceptor: Unit, target_fps: float, sim_n_steps: int, guidance: str):
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
        interceptor.update(90) # placeholder

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

        # This processes GUI events + draws without freezing the window
        plt.pause(0.001)

        # Pace the loop to ~target_fps
        slept = time.perf_counter() - t0
        if slept < frame_dt:
            time.sleep(frame_dt - slept)

    plt.ioff()
    plt.show()
