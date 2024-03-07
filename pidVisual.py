import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Set initial PID values
P = 1.0
I = 0.5
D = 0.2

# Define target and initial values
target_value = 10
initial_value = 0

# Define time parameters
time_start = 0
time_end = 10
time_step = 0.01

# Create a list of time values
time_values = np.arange(time_start, time_end, time_step)

# Initialize lists for target, system output, and error
target_values = [target_value] * len(time_values)
system_output = [initial_value] * len(time_values)
error_values = [target_value - initial_value] * len(time_values)

# Calculate PID output for a single timestep
def pid_output_single(error, prev_error, p, i, d):
    proportional = p * error
    integral = i * error * time_step  # Note: For simplicity; consider a more accurate integration approach for real applications.
    derivative = 0 if prev_error is None else d * (error - prev_error) / time_step
    return proportional + integral + derivative

prev_error = None  # Initialize prev_error
# Update system output and error based on PID output
for i in range(1, len(time_values)):
    pid_out = pid_output_single(error_values[i-1], prev_error, P, I, D)
    system_output[i] = system_output[i-1] + pid_out * time_step
    error_values[i] = target_value - system_output[i]
    prev_error = error_values[i-1]

# Create Tkinter window
root = tk.Tk()
root.title("PID Illustration")

# Create figure and canvas
fig = Figure(figsize=(8, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add plot to figure
ax = fig.add_subplot(111)
ax.set_title("PID Illustration")
ax.set_xlabel("Time")
ax.set_ylabel("Value")
target_line, = ax.plot(time_values, target_values, label="Target")
system_line, = ax.plot(time_values, system_output, label="System Output")
error_line, = ax.plot(time_values, error_values, label="Error")
ax.legend()

# Function to update plots with new PID values
def update_plots(p, i, d):
    global P, I, D, system_output, error_values, prev_error

    P, I, D = p, i, d
    system_output = [initial_value]
    error_values = [target_value - initial_value]
    prev_error = None

    for i in range(1, len(time_values)):
        pid_out = pid_output_single(error_values[i-1], prev_error, P, I, D)
        system_output.append(system_output[-1] + pid_out * time_step)
        error_values.append(target_value - system_output[i])
        prev_error = error_values[i-1]

    # Update plot data
    system_line.set_ydata(system_output)
    error_line.set_ydata(error_values)

    # Redraw canvas
    canvas.draw()

# Create sliders for P, I, and D and update plots using sliders
p_slider = ttk.Scale(root, from_=0, to=10, value=P, orient=tk.HORIZONTAL,
                     command=lambda x: update_plots(float(x), I, D))
p_slider.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
i_slider = ttk.Scale(root, from_=0, to=10, value=I, orient=tk.HORIZONTAL,
                     command=lambda x: update_plots(P, float(x), D))
i_slider.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
d_slider = ttk.Scale(root, from_=0, to=10, value=D, orient=tk.HORIZONTAL,
                     command=lambda x: update_plots(P, I, float(x)))
d_slider.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# Start Tkinter event loop
root.mainloop()
