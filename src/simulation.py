import time
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from .units import Unit
from .guidance import Guidance
from .missions import TargetMission

def interception_event_detection(target: Unit, interceptor: Unit,  blast_radius: float):
    distance = np.linalg.norm(target.coords - interceptor.coords)
    if distance < blast_radius:
        return True
    else:
        return False

def wait_till_window_visible(fig):
    # --- make sure the GUI is created and visible before starting the sim ---
    fig.canvas.draw_idle()           # schedule a draw
    plt.show(block=False)            # create and show the window without blocking

    # Wait until the underlying Qt window is visible
    win = getattr(fig.canvas.manager, "window", None)
    while win is None or not win.isVisible():
        plt.pause(1)              # lets Qt process events & show the window
        win = getattr(fig.canvas.manager, "window", None)


def run_simulation(target: Unit, interceptor: Unit, guidance: Guidance, mission: TargetMission,
                   target_fps: float, sim_n_steps: int, blast_radius: float):
    plt.ion()  # interactive on
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title("Trajectory")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.grid(True); ax.set_aspect("equal", adjustable="box")

    (line,) = ax.plot([], [], "-", label="target", color = "tab:blue")
    (head,) = ax.plot([], [], "o", color = "tab:blue")
    (line2,) = ax.plot([], [], "--", label="interceptor", color="tab:orange")
    (head2,) = ax.plot([], [], "o", color="tab:orange")
    ax.legend(loc="lower right")

    target_x_coords, target_y_coords = [], []
    interceptor_x, interceptor_y = [], []

    frame_dt = 1.0 / target_fps
    intercepted = False
    wait_till_window_visible(fig)
    gif_path = "./output/trajectory.gif"                 # choose your path/name
    writer = PillowWriter(fps=target_fps)
    with writer.saving(fig, gif_path, dpi=100):
        for n_step in range(sim_n_steps):
            t0 = time.perf_counter()

            # ---- simulation step ----
            angle_for_target = mission.get_angle(n_step, sim_n_steps)
            target.update(angle_for_target)
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

            fig.canvas.draw()       # ensure the latest frame is rendered
            writer.grab_frame()     # <-- record this frame into the GIF
            plt.pause(0.001)  # This processes GUI events + draws without freezing the window

            if interception_event_detection(target, interceptor, blast_radius):
                intercepted = True
                break

            # Pace the loop to ~target_fps
            slept = time.perf_counter() - t0
            if slept < frame_dt:
                time.sleep(frame_dt - slept)
    
    if intercepted:
        result = "Intercepted"
    else:
        result = "Not Intercepted"
    print(result)
    plt.title(result)


    plt.ioff()
    plt.show()

   