# Moire pattern
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import matplotlib.patches as patches
import tkinter as tk
from tkinter import ttk


def change_pattern():
    global pattern_number
    pattern_number = var_pattern.get()
    draw_graph()


def draw_circles(th, x_center, y_center, width, height, pth, col, size):
    r = 0.
    while r <= height / 2.:
        crl = patches.Circle(xy=(x_center, y_center), radius=r, fill=False, ec=col, linewidth=size)
        ax.add_patch(crl)
        r = r + pth


def draw_dots_hex(th, x_center, y_center, width, height, pth, col, size):
    rot = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])  # Matrix of horizontal rotation
    dots = []
    h = 0.
    cnt = 0
    while h <= height:
        w = 0.
        while w <= width:
            if np.mod(cnt, 2) == 0:
                dot_p = np.array([w - width / 2., h - height / 2.])
            else:
                dot_p = np.array([w - width / 2. + pth / 2., h - height / 2.])
            dots.append(dot_p)
            w = w + pth
        h = h + pth
        cnt = cnt + 1
    for i in range(len(dots)):
        p = dots[i]
        p_rot = np.dot(rot, p)
        crl = patches.Circle(xy=(p_rot[0] + x_center, p_rot[1] + y_center), radius=size, fc=col, ec=col)
        ax.add_patch(crl)


def draw_dots_square(th, x_center, y_center, width, height, pth, col, size):
    rot = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])  # Matrix of horizontal rotation
    dots = []
    h = 0.
    while h <= height:
        w = 0.
        while w <= width:
            dot_p = np.array([w - width / 2., h - height / 2.])
            dots.append(dot_p)
            w = w + pth
        h = h + pth
    for i in range(len(dots)):
        p = dots[i]
        p_rot = np.dot(rot, p)
        crl = patches.Circle(xy=(p_rot[0] + x_center, p_rot[1] + y_center), radius=size, fc=col, ec=col)
        ax.add_patch(crl)


def draw_parallel_lines(th, x_center, y_center, width, height, pth, col, size):
    rot = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])  # Matrix of horizontal rotation
    lines_start = []
    lines_end = []
    h = 0.
    while h <= height:
        line_start = np.array([width / 2., h - height / 2.])
        lines_start.append(line_start)
        line_end = np.array([-width / 2., h - height / 2.])
        lines_end.append(line_end)
        h = h + pth
    for i in range(len(lines_start)):
        p_start = lines_start[i]
        p_end = lines_end[i]
        p_start_rot = np.dot(rot, p_start)
        p_end_rot = np.dot(rot, p_end)
        ax.plot([p_start_rot[0] + x_center, p_end_rot[0] + x_center],
                [p_start_rot[1] + y_center, p_end_rot[1] + y_center], c=col, linewidth=size)


def set_axis():
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_title('Moire pattern')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    # ax.grid()
    ax.set_aspect("equal")


def draw_graph():
    ax.cla()
    set_axis()
    if pattern_number == 0:
        draw_parallel_lines(0., 0., 0., 6., 6., pitch_parallel, 'black', 2)
        draw_parallel_lines(theta, offset_x, offset_y, 6., 6., pitch_parallel * pitch_percent / 100., 'black', 2)
    elif pattern_number == 1:
        draw_dots_square(0., 0., 0., 6., 6., pitch_dots, 'black', 0.1)
        draw_dots_square(theta, offset_x, offset_y, 6., 6., pitch_dots * pitch_percent / 100., 'black', 0.1)
    elif pattern_number == 2:
        draw_dots_hex(0., 0., 0., 6., 6., pitch_dots, 'black', 0.1)
        draw_dots_hex(theta, offset_x, offset_y, 6., 6., pitch_dots * pitch_percent / 100., 'black', 0.1)
    elif pattern_number == 3:
        draw_circles(0., 0., 0., 6., 6., pitch_circles, 'black', 2)
        draw_circles(0., offset_x, offset_y, 6., 6., pitch_circles * pitch_percent / 100., 'black', 2)
    elif pattern_number == 4:
        draw_circles(0., 0., 0., 6., 6., pitch_circles, 'black', 2)
        draw_parallel_lines(theta, offset_x, offset_y, 6., 6., pitch_parallel * pitch_percent / 100., 'black', 2)
    canvas.draw()
    # ax.grid()


def change_pitch(value):
    global pitch_percent
    pitch_percent = float(value)
    draw_graph()


def slider_offset_y_changed(event):
    global offset_y
    offset_y = float(scl_var_shift_y.get()) / 10.
    draw_graph()


def slider_offset_x_changed(event):
    global offset_x
    offset_x = float(scl_var_shift_x.get()) / 10.
    draw_graph()


def slider_angle_changed(event):
    global angle, theta
    angle = float(scl_var_angle.get())
    theta = angle * np.pi / 180.
    draw_graph()


# Global variables
x_min = -4.
x_max = 4.
y_min = -4.
y_max = 4.

angle = 0.
theta = 0.
pitch_parallel = 0.1
pitch_dots = 0.4
pitch_percent = 100
offset_x = offset_x_init = 0.
offset_y = offset_y_init = 0.
pitch_circles = 0.1

pattern_number = 0

# Generate tkinter
root = tk.Tk()
root.title("Moire pattern")

# Generate figure and axes
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(1, 1, 1)

# Embed Figure in canvas
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

# Draw circles as initial
draw_graph()

# Add toolbar
toolbar = NavigationToolbar2Tk(canvas, root)

# Widgets
frm_pattern = ttk.Labelframe(root, relief="ridge", text="Pattern", labelanchor="n", width=100)
frm_pattern.pack(side='left')
var_pattern = tk.IntVar(value=pattern_number)
rdb0_pattern = tk.Radiobutton(frm_pattern, text="Parallel lines", command=change_pattern,
                              variable=var_pattern, value=0)
rdb1_pattern = tk.Radiobutton(frm_pattern, text="Dots(Square lattice)", command=change_pattern,
                              variable=var_pattern, value=1)
rdb2_pattern = tk.Radiobutton(frm_pattern, text="Dots(hexagonal lattice)", command=change_pattern,
                              variable=var_pattern, value=2)
rdb3_pattern = tk.Radiobutton(frm_pattern, text="2 concentric circles", command=change_pattern,
                              variable=var_pattern, value=3)
rdb4_pattern = tk.Radiobutton(frm_pattern, text="Circles and lines", command=change_pattern,
                              variable=var_pattern, value=4)
rdb0_pattern.pack(anchor=tk.W)
rdb1_pattern.pack(anchor=tk.W)
rdb2_pattern.pack(anchor=tk.W)
rdb3_pattern.pack(anchor=tk.W)
rdb4_pattern.pack(anchor=tk.W)

label_pitch = tk.Label(root, text="Diff. of Pitch(%)")
label_pitch.pack(side='left')
var_pitch = tk.StringVar(root)  # variable for spinbox-value
var_pitch.set(pitch_percent)  # Initial value
s_pitch = tk.Spinbox(
    root, textvariable=var_pitch, format="%.2f", from_=0., to=200, increment=1,
    command=lambda: change_pitch(var_pitch.get()), width=5
    )
s_pitch.pack(side='left')

lbl_position = tk.Label(root, text="Angle")
lbl_position.pack(side='left')
scl_var_angle = tk.StringVar(root)
scl_angle = tk.Scale(root, variable=scl_var_angle, orient='horizontal', length=200, from_=-360, to=360,
                     command=slider_angle_changed)
scl_angle.pack(side='left')
scl_var_angle.set(angle)

lbl_shift_x = tk.Label(root, text="Offset(x/10)")
lbl_shift_x.pack(side='left')
scl_var_shift_x = tk.StringVar(root)
scl_shift_x = tk.Scale(root, variable=scl_var_shift_x, orient='horizontal', length=200, from_=-10, to=10,
                       command=slider_offset_x_changed)
scl_shift_x.pack(side='left')
scl_var_shift_x.set(offset_x)

lbl_shift_y = tk.Label(root, text="Offset(y/10)")
lbl_shift_y.pack(side='left')
scl_var_shift_y = tk.StringVar(root)
scl_shift_y = tk.Scale(root, variable=scl_var_shift_y, orient='horizontal', length=200, from_=-10, to=10,
                       command=slider_offset_y_changed)
scl_shift_y.pack(side='left')
scl_var_shift_x.set(offset_y)

# main loop
set_axis()
root.mainloop()
