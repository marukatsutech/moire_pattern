# Moire pattern 2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from tkinter import ttk


def set_axis():
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_title('Moire pattern 2')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    # ax.grid()
    ax.set_aspect("equal")


def draw_spiral(th, x_center, y_center, width, height, pth, col, size, pitch, a, b):
    if spiral_mode == 0:
        r = theta_space_multi * pitch
    else:
        r = a * np.exp(b* theta_space_multi)
    x = r * np.cos(theta_space_multi)
    y = r * np.sin(theta_space_multi)
    ax.plot(x, y, c=col, linewidth=size)


def draw_ellipses_plot(th, x_center, y_center, width, height, pth, col, size, a_rt, b_rt, th_pth):
    r = 0.
    th = 0.
    while r <= height / 2.:
        a = a_rt * r
        b = b_rt * r
        x = a * np.cos(theta_space)
        y = b * np.sin(theta_space)
        rot = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])  # Matrix of horizontal rotation
        ellipses_rot = np.vstack((x, y))
        ellipses_rotated = np.dot(rot, ellipses_rot)
        # ax.plot(x, y, c=col, linewidth=size)
        ax.plot(ellipses_rotated[0], ellipses_rotated[1], c=col, linewidth=size)
        r = r + pth
        th = th + th_pth


def draw_circles_plot(th, x_center, y_center, width, height, pth, col, size, offset_r_pitch, th_pth):
    r = 0.
    th = 0.
    ofs = 0.
    while r <= height / 2.:
        x = r * np.cos(theta_space) + ofs * np.cos(th)
        y = r * np.sin(theta_space) + ofs * np.sin(th)
        ax.plot(x, y, c=col, linewidth=size)
        r = r + pth
        th = th + th_pth
        ofs = ofs + offset_r_pitch


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


def draw_graph():
    ax.cla()
    set_axis()
    if pattern_number == 0:
        draw_circles_plot(0., 0., 0., 6., 6., pitch_circles, color_pattern, line_width_pattern, circles_offset,
                          circles_offset_theta_pitch)
    elif pattern_number == 1:
        draw_ellipses_plot(0., 0., 0., 6., 6., pitch_circles, color_pattern, line_width_pattern, a_ratio, b_ratio,
                           ellipses_theta_pitch)
    elif pattern_number == 2:
        draw_spiral(0., 0., 0., 6., 6., pitch_circles, color_pattern, line_width_pattern, spiral_pitch, spiral_a,
                    spiral_b)
    if var_overlay.get():
        if var_overlay_pattern.get() == 0:
            draw_parallel_lines(theta, offset_x, offset_y, 6., 6., pitch_stripe, color_overlay, line_width_overlay)
        else:
            draw_parallel_lines(theta, offset_x, offset_y, 6., 6., pitch_stripe, color_overlay, line_width_overlay)
            draw_parallel_lines(theta + np.pi / 2., offset_x, offset_y, 6., 6.,
                                pitch_stripe, color_overlay, line_width_overlay)
    canvas.draw()
    # ax.grid()


def change_line_width_overlay(value):
    global line_width_overlay
    line_width_overlay = int(value)
    draw_graph()


def change_line_width_pattern(value):
    global line_width_pattern
    line_width_pattern = int(value)
    draw_graph()


def change_spiral_b(value):
    global spiral_b
    spiral_b = float(value)
    draw_graph()


def change_spiral_a(value):
    global spiral_a
    spiral_a = float(value)
    draw_graph()


def change_spiral_pitch(value):
    global spiral_pitch
    spiral_pitch = float(value)
    draw_graph()


def change_circles_theta(value):
    global circles_offset_theta_pitch
    circles_offset_theta_pitch = float(value) * np.pi / 180.
    draw_graph()


def change_circles_offset(value):
    global circles_offset
    circles_offset = float(value)
    draw_graph()


def change_ellipses_theta_pitch(value):
    global ellipses_theta_pitch
    ellipses_theta_pitch = float(value) * np.pi / 180.
    draw_graph()


def change_b(value):
    global b_ratio
    b_ratio = float(value)
    draw_graph()


def change_a(value):
    global a_ratio
    a_ratio = float(value)
    draw_graph()


def change_pitch_stripe(value):
    global pitch_stripe
    pitch_stripe = float(value)
    draw_graph()


def change_pitch_ellipses(value):
    global pitch_circles
    pitch_circles = float(value)
    draw_graph()


def change_pitch_circles(value):
    global pitch_circles
    pitch_circles = float(value)
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


def change_color_overlay():
    global color_overlay
    num = var_color_number_overlay.get()
    if num == 0:
        color_overlay = 'black'
    elif num == 1:
        color_overlay = 'gray'
    elif num == 2:
        color_overlay = 'white'
    draw_graph()


def change_color_pattern():
    global color_pattern
    num = var_color_number_pattern.get()
    print(num)
    if num == 0:
        color_pattern = 'black'
    elif num == 1:
        color_pattern = 'orange'
    draw_graph()


def change_spiral_mode():
    global spiral_mode
    spiral_mode = var_spiral.get()
    draw_graph()


def change_overlay_pattern():
    global overlay_pattern_number
    overlay_pattern_number = var_pattern.get()
    draw_graph()


def change_pattern():
    global pattern_number
    pattern_number = var_pattern.get()
    draw_graph()


def redraw():
    draw_graph()


# Global variables
x_min = -4.
x_max = 4.
y_min = -4.
y_max = 4.

angle = 0.
theta = 0.
pitch_circles = 0.1
offset_x = offset_x_init = 0.
offset_y = offset_y_init = 0.
pitch_circles = 0.1
pitch_stripe = 0.1

pattern_number = 0
overlay_pattern_number = 0

theta_space = np.linspace(0, 2*np.pi, 100)
theta_space_multi = np.linspace(0, 20*np.pi*10, 10000)

circles_offset = 0.
circles_offset_theta_pitch_degree = 0.
circles_offset_theta_pitch = 0.

a_ratio = 1.
b_ratio = 1.2
ellipses_theta_pitch_degree = 0.
ellipses_theta_pitch = 0.

spiral_mode = 0
spiral_pitch = 0.1
spiral_a = 0.1
spiral_b = 0.1

color_number_pattern = 0
color_number_overlay = 0
color_pattern = 'black'
color_overlay = 'black'
line_width_pattern = 2
line_width_overlay = 2

# Generate tkinter
root = tk.Tk()
root.title("Moire pattern")

# Generate figure and axes
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(1, 1, 1)

# Embed Figure in canvas
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')


# Add toolbar
toolbar = NavigationToolbar2Tk(canvas, root)

# Widgets
# Pattern
frm_pattern = ttk.Labelframe(root, relief="ridge", text="Pattern", labelanchor="n", width=100)
frm_pattern.pack(side='left')
var_pattern = tk.IntVar(value=pattern_number)
rdb0_pattern = tk.Radiobutton(frm_pattern, text="Circles", command=change_pattern,
                              variable=var_pattern, value=0)
rdb1_pattern = tk.Radiobutton(frm_pattern, text="Ellipses", command=change_pattern,
                              variable=var_pattern, value=1)
rdb2_pattern = tk.Radiobutton(frm_pattern, text="Spiral", command=change_pattern,
                              variable=var_pattern, value=2)
rdb0_pattern.pack(anchor=tk.W)
rdb1_pattern.pack(anchor=tk.W)
rdb2_pattern.pack(anchor=tk.W)
# Parameter(circles)
frm_parameter_circles = ttk.Labelframe(root, relief="ridge", text="Parameter(circles)", labelanchor="n", width=100)
frm_parameter_circles.pack(side='left')
label_pitch_circles = tk.Label(frm_parameter_circles, text="Pitch:")
label_pitch_circles.pack(anchor=tk.W)
var_pitch_circles = tk.StringVar(root)  # variable for spinbox-value
var_pitch_circles.set(pitch_circles)  # Initial value
s_pitch_circles = tk.Spinbox(
    frm_parameter_circles, textvariable=var_pitch_circles, format="%.2f", from_=0., to=0.5, increment=0.01,
    command=lambda: change_pitch_circles(var_pitch_circles.get()), width=5
    )
s_pitch_circles.pack(anchor=tk.W)
label_offset = tk.Label(frm_parameter_circles, text="Offset pitch:")
label_offset.pack(anchor=tk.W)
var_offset = tk.StringVar(root)  # variable for spinbox-value
var_offset.set(circles_offset)  # Initial value
s_offset = tk.Spinbox(
    frm_parameter_circles, textvariable=var_offset, format="%.2f", from_=0., to=1., increment=0.01,
    command=lambda: change_circles_offset(var_offset.get()), width=5
    )
s_offset.pack(anchor=tk.W)
label_offset_rot_pitch = tk.Label(frm_parameter_circles, text="rotation pitch(degree):")
label_offset_rot_pitch.pack(anchor=tk.W)
var_offset_rot_pitch_degree = tk.StringVar(root)  # variable for spinbox-value
var_offset_rot_pitch_degree.set(circles_offset_theta_pitch_degree)  # Initial value
s_rot_pitch = tk.Spinbox(
    frm_parameter_circles, textvariable=var_offset_rot_pitch_degree, format="%.1f", from_=0., to=360., increment=1.,
    command=lambda: change_circles_theta(var_offset_rot_pitch_degree.get()), width=5
    )
s_rot_pitch.pack(anchor=tk.W)
# Parameter(ellipses)
frm_parameter_ellipses = ttk.Labelframe(root, relief="ridge", text="Parameter(ellipses)", labelanchor="n", width=100)
frm_parameter_ellipses.pack(side='left')
label_pitch_ellipses = tk.Label(frm_parameter_ellipses, text="Pitch:")
label_pitch_ellipses.pack(anchor=tk.W)
var_pitch_ellipses = tk.StringVar(root)  # variable for spinbox-value
var_pitch_ellipses.set(pitch_circles)  # Initial value
s_pitch_ellipses = tk.Spinbox(
    frm_parameter_ellipses, textvariable=var_pitch_ellipses, format="%.2f", from_=0., to=0.5, increment=0.01,
    command=lambda: change_pitch_ellipses(var_pitch_ellipses.get()), width=5
)
s_pitch_ellipses.pack(anchor=tk.W)
label_a = tk.Label(frm_parameter_ellipses, text="a(ratio):")
label_a.pack(anchor=tk.W)
var_a = tk.StringVar(root)  # variable for spinbox-value
var_a.set(a_ratio)  # Initial value
s_a = tk.Spinbox(
    frm_parameter_ellipses, textvariable=var_a, format="%.1f", from_=0., to=5., increment=0.1,
    command=lambda: change_a(var_a.get()), width=5
    )
s_a.pack(anchor=tk.W)
label_b = tk.Label(frm_parameter_ellipses, text="b(ratio):")
label_b.pack(anchor=tk.W)
var_b = tk.StringVar(root)  # variable for spinbox-value
var_b.set(b_ratio)  # Initial value
s_b = tk.Spinbox(
    frm_parameter_ellipses, textvariable=var_b, format="%.1f", from_=0., to=5., increment=0.1,
    command=lambda: change_b(var_b.get()), width=5
    )
s_b.pack(anchor=tk.W)
label_rot_pitch = tk.Label(frm_parameter_ellipses, text="rotation pitch(degree):")
label_rot_pitch.pack(anchor=tk.W)
var_rot_pitch_degree = tk.StringVar(root)  # variable for spinbox-value
var_rot_pitch_degree.set(ellipses_theta_pitch_degree)  # Initial value
s_rot_pitch = tk.Spinbox(
    frm_parameter_ellipses, textvariable=var_rot_pitch_degree, format="%.1f", from_=0., to=360., increment=1.,
    command=lambda: change_ellipses_theta_pitch(var_rot_pitch_degree.get()), width=5
    )
s_rot_pitch.pack(anchor=tk.W)
# Parameter(spiral)
frm_spiral = ttk.Labelframe(root, relief="ridge", text="Parameter(spiral)", labelanchor="n", width=100)
frm_spiral.pack(side='left')
var_spiral = tk.IntVar(value=spiral_mode)
rdb0_spiral = tk.Radiobutton(frm_spiral, text="Arithmetic", command=change_spiral_mode,
                             variable=var_spiral, value=0)
rdb1_spiral = tk.Radiobutton(frm_spiral, text="Logarithmic", command=change_spiral_mode,
                             variable=var_spiral, value=1)
rdb0_spiral.pack(anchor=tk.W)
rdb1_spiral.pack(anchor=tk.W)
label_spiral_pitch = tk.Label(frm_spiral, text="Pitch(arithmetic):")
label_spiral_pitch.pack(anchor=tk.W)
var_spiral_pitch = tk.StringVar(root)  # variable for spinbox-value
var_spiral_pitch.set(spiral_pitch)  # Initial value
s_spiral_pitch = tk.Spinbox(
    frm_spiral, textvariable=var_spiral_pitch, format="%.2f", from_=0., to=5., increment=0.01,
    command=lambda: change_spiral_pitch(var_spiral_pitch.get()), width=5
    )
s_spiral_pitch.pack(anchor=tk.W)
label_spiral_a = tk.Label(frm_spiral, text="a(logarithmic):")
label_spiral_a.pack(anchor=tk.W)
var_spiral_a = tk.StringVar(root)  # variable for spinbox-value
var_spiral_a.set(spiral_a)  # Initial value
s_spiral_a = tk.Spinbox(
    frm_spiral, textvariable=var_spiral_a, format="%.2f", from_=0., to=5., increment=0.01,
    command=lambda: change_spiral_a(var_spiral_a.get()), width=5
    )
s_spiral_a.pack(anchor=tk.W)
label_spiral_b = tk.Label(frm_spiral, text="b(logarithmic):")
label_spiral_b.pack(anchor=tk.W)
var_spiral_b = tk.StringVar(root)  # variable for spinbox-value
var_spiral_b.set(spiral_b)  # Initial value
s_spiral_b = tk.Spinbox(
    frm_spiral, textvariable=var_spiral_b, format="%.2f", from_=0., to=5., increment=0.01,
    command=lambda: change_spiral_b(var_spiral_b.get()), width=5
    )
s_spiral_b.pack(anchor=tk.W)

# Overlay (1)
frm_overlay = ttk.Labelframe(root, relief="ridge", text="Overlay(1)", labelanchor="n", width=100)
frm_overlay.pack(side='left')
var_overlay = tk.BooleanVar(root)    # Variable for checkbutton
check_overlay = tk.Checkbutton(frm_overlay, text="On", variable=var_overlay, command=redraw)
check_overlay.pack(anchor=tk.W)
var_overlay.set(False)
var_overlay_pattern = tk.IntVar(value=overlay_pattern_number)
rdb0_overlay_pattern = tk.Radiobutton(frm_overlay, text="Stripe", command=change_overlay_pattern,
                                      variable=var_overlay_pattern, value=0)
rdb1_overlay_pattern = tk.Radiobutton(frm_overlay, text="Grid", command=change_overlay_pattern,
                                      variable=var_overlay_pattern, value=1)
rdb0_overlay_pattern.pack(anchor=tk.W)
rdb1_overlay_pattern.pack(anchor=tk.W)
label_pitch_stripe = tk.Label(frm_overlay, text="Pitch:")
label_pitch_stripe.pack(anchor=tk.W)
var_pitch_stripe = tk.StringVar(root)  # variable for spinbox-value
var_pitch_stripe.set(pitch_stripe)  # Initial value
s_pitch_stripe = tk.Spinbox(
    frm_overlay, textvariable=var_pitch_stripe, format="%.2f", from_=0., to=0.5, increment=0.01,
    command=lambda: change_pitch_stripe(var_pitch_stripe.get()), width=5
    )
s_pitch_stripe.pack(anchor=tk.W)
# Overlay (2)
frm_overlay2 = ttk.Labelframe(root, relief="ridge", text="Overlay(2)", labelanchor="n", width=100)
frm_overlay2.pack(side='left')
lbl_position = tk.Label(frm_overlay2, text="Angle:")
lbl_position.pack(anchor=tk.W)
scl_var_angle = tk.StringVar(root)
scl_angle = tk.Scale(frm_overlay2, variable=scl_var_angle, orient='horizontal', length=200, from_=-360, to=360,
                     command=slider_angle_changed)
scl_angle.pack(anchor=tk.W)
scl_var_angle.set(angle)

lbl_shift_x = tk.Label(frm_overlay2, text="Offset(x/10):")
lbl_shift_x.pack(anchor=tk.W)
scl_var_shift_x = tk.StringVar(root)
scl_shift_x = tk.Scale(frm_overlay2, variable=scl_var_shift_x, orient='horizontal', length=200, from_=x_min, to=x_max,
                       command=slider_offset_x_changed)
scl_shift_x.pack(anchor=tk.W)
scl_var_shift_x.set(offset_x)

lbl_shift_y = tk.Label(frm_overlay2, text="Offset(y/10):")
lbl_shift_y.pack(anchor=tk.W)
scl_var_shift_y = tk.StringVar(root)
scl_shift_y = tk.Scale(frm_overlay2, variable=scl_var_shift_y, orient='horizontal', length=200, from_=y_min, to=y_max,
                       command=slider_offset_y_changed)
scl_shift_y.pack(anchor=tk.W)
scl_var_shift_x.set(offset_y)
# Color and line width
frm_color = ttk.Labelframe(root, relief="ridge", text="Color and line with", labelanchor="n", width=100)
frm_color.pack(side='left')
label_col_pattern = tk.Label(frm_color, text="Pattern:")
label_col_pattern.pack(anchor=tk.W)
var_color_number_pattern = tk.IntVar(color_number_pattern)
rdb0_color_pattern = tk.Radiobutton(frm_color, text="Black", command=change_color_pattern,
                                    variable=var_color_number_pattern, value=0)
rdb1_color_pattern = tk.Radiobutton(frm_color, text="Orange", command=change_color_pattern,
                                    variable=var_color_number_pattern, value=1)
rdb0_color_pattern.pack(anchor=tk.W)
rdb1_color_pattern.pack(anchor=tk.W)
var_line_width_pattern = tk.IntVar(root)  # variable for spinbox-value
var_line_width_pattern.set(line_width_pattern)  # Initial value
s_line_width_pattern = tk.Spinbox(
    frm_color, textvariable=var_line_width_pattern, from_=1, to=10, increment=1,
    command=lambda: change_line_width_pattern(var_line_width_pattern.get()), width=5
    )
s_line_width_pattern.pack(anchor=tk.W)
label_col_overlay = tk.Label(frm_color, text="Overlay:")
label_col_overlay.pack(anchor=tk.W)
var_color_number_overlay = tk.IntVar(color_number_overlay)
rdb0_color_overlay = tk.Radiobutton(frm_color, text="Black", command=change_color_overlay,
                                    variable=var_color_number_overlay, value=0)
rdb1_color_overlay = tk.Radiobutton(frm_color, text="Gray", command=change_color_overlay,
                                    variable=var_color_number_overlay, value=1)
rdb2_color_overlay = tk.Radiobutton(frm_color, text="White", command=change_color_overlay,
                                    variable=var_color_number_overlay, value=2)
rdb0_color_overlay.pack(anchor=tk.W)
rdb1_color_overlay.pack(anchor=tk.W)
rdb2_color_overlay.pack(anchor=tk.W)
var_line_width_overlay = tk.IntVar(root)  # variable for spinbox-value
var_line_width_overlay.set(line_width_overlay)  # Initial value
s_line_width_overlay = tk.Spinbox(
    frm_color, textvariable=var_line_width_overlay, from_=1, to=10, increment=1,
    command=lambda: change_line_width_overlay(var_line_width_overlay.get()), width=5
    )
s_line_width_overlay.pack(anchor=tk.W)
# Draw circles as initial
draw_graph()

# main loop
set_axis()
root.mainloop()
