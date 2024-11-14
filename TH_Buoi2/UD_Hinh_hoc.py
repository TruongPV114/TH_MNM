import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox

# Hàm hiển thị đồ thị matplotlib trong tkinter
def show_plot(fig):
    for widget in plot_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

# Hàm vẽ hình tam giác
def draw_triangle(a, b, c):
    if a + b > c and a + c > b and b + c > a:
        s = (a + b + c) / 2
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        perimeter = a + b + c

        # Kiểm tra loại tam giác
        if a == b == c:
            triangle_type = "Tam giác đều"
        elif a == b or b == c or a == c:
            triangle_type = "Tam giác cân"
        else:
            # Kiểm tra tam giác vuông
            sides = sorted([a, b, c])  # Sắp xếp các cạnh
            if np.isclose(sides[2]**2, sides[0]**2 + sides[1]**2):
                triangle_type = "Tam giác vuông"
            else:
                triangle_type = "Tam giác thường"

        # Vẽ hình tam giác
        fig, ax = plt.subplots()
        # Tính tọa độ cho tam giác
        x = [0, a, (b**2 + a**2 - c**2) / (2 * a)]
        y = [0, 0, np.sqrt(b**2 - ((b**2 + a**2 - c**2) / (2 * a))**2)]
        ax.plot(x + [x[0]], y + [y[0]], 'r')  # Vẽ đường bao
        ax.fill(x + [x[0]], y + [y[0]], 'r', alpha=0.3)  # Vẽ hình

        ax.set_aspect('equal')
        ax.set_title(f"{triangle_type}")
        show_plot(fig)

        result = f"Chu vi: {perimeter:.2f}\nDiện tích: {area:.2f}"
        result_label.config(text=result)
    else:
        messagebox.showerror("Lỗi", "Tam giác không hợp lệ!")


# Hàm vẽ hình bình hành
def draw_parallelogram(a, b, angle):
    # Chuyển angle từ độ sang radian
    angle_rad = np.radians(angle)

    # Tính toán các tọa độ của 4 đỉnh hình bình hành
    x1, y1 = 0, 0  # Đỉnh đầu tiên
    x2, y2 = a, 0  # Đỉnh thứ hai (cạnh a dài)
    x3, y3 = x2 + b * np.cos(angle_rad), b * np.sin(angle_rad)  # Đỉnh thứ ba
    x4, y4 = x3 - a, y3  # Đỉnh thứ tư (cạnh b dài, song song với đỉnh đầu tiên)

    # Các tọa độ của 4 đỉnh
    x = [x1, x2, x3, x4, x1]
    y = [y1, y2, y3, y4, y1]

    # Vẽ hình bình hành
    fig, ax = plt.subplots()
    ax.plot(x, y, 'b')  # Vẽ đường biên
    ax.fill(x, y, 'b', alpha=0.3)  # Vẽ hình với độ mờ
    ax.set_aspect('equal')
    ax.set_title("Hình Bình Hành")

    # Tính chu vi và diện tích
    perimeter = 2 * (a + b)
    area = a * b * np.abs(np.sin(angle_rad))

    # Hiển thị chu vi và diện tích
    result = f"Chu vi: {perimeter:.2f}\nDiện tích: {area:.2f}"
    result_label.config(text=result)

    show_plot(fig)

# Hàm vẽ hình tròn
def draw_circle(radius):
    if radius <= 0:
        messagebox.showerror("Lỗi", "Bán kính phải lớn hơn 0!")
        return

    perimeter = 2 * np.pi * radius
    area = np.pi * radius**2

    fig, ax = plt.subplots()
    circle = plt.Circle((0, 0), radius, fill=None, edgecolor='b')
    ax.add_patch(circle)
    ax.set_xlim([-radius - 1, radius + 1])
    ax.set_ylim([-radius - 1, radius + 1])
    ax.set_aspect('equal')
    ax.set_title("Hình Tròn")
    show_plot(fig)

    result = f"Chu vi: {perimeter:.2f}\nDiện tích: {area:.2f}"
    result_label.config(text=result)

# Hàm vẽ hình vuông
def draw_square(side):
    if side <= 0:
        messagebox.showerror("Lỗi", "Cạnh phải lớn hơn 0!")
        return

    area = side ** 2
    perimeter = 4 * side

    fig, ax = plt.subplots()
    square = plt.Rectangle((0, 0), side, side, fill=None, edgecolor='g')
    ax.add_patch(square)
    ax.set_xlim([-1, side + 1])
    ax.set_ylim([-1, side + 1])
    ax.set_aspect('equal')
    ax.set_title("Hình Vuông")
    show_plot(fig)

    result = f"Chu vi: {perimeter:.2f}\nDiện tích: {area:.2f}"
    result_label.config(text=result)

# Hàm vẽ hình trụ
def draw_cylinder(radius, height):
    if radius <= 0 or height <= 0:
        messagebox.showerror("Lỗi", "Bán kính và chiều cao phải lớn hơn 0!")
        return

    volume = np.pi * radius**2 * height
    lateral_area = 2 * np.pi * radius * height
    base_area = np.pi * radius**2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    z = np.linspace(0, height, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid)
    y_grid = radius * np.sin(theta_grid)

    ax.plot_surface(x_grid, y_grid, z_grid, color='c', alpha=0.6)
    ax.set_box_aspect([1, 1, height / radius])
    ax.set_title("Hình Trụ")
    show_plot(fig)

    result = f"Thể tích: {volume:.2f}\nDiện tích mặt bên: {lateral_area:.2f}\nDiện tích đáy: {base_area:.2f}"
    result_label.config(text=result)

# Hàm vẽ hình cầu
def draw_sphere(radius):
    if radius <= 0:
        messagebox.showerror("Lỗi", "Bán kính phải lớn hơn 0!")
        return

    volume = (4/3) * np.pi * radius**3
    surface_area = 4 * np.pi * radius**2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x, y, z, color='c', alpha=0.6)
    ax.set_box_aspect([1, 1, 1])
    ax.set_title("Hình Cầu")
    show_plot(fig)

    result = f"Thể tích: {volume:.2f}\nDiện tích bề mặt: {surface_area:.2f}"
    result_label.config(text=result)


# Hàm vẽ hình lập phương
def draw_cube(side_length):
    if side_length <= 0:
        messagebox.showerror("Lỗi", "Chiều dài cạnh phải lớn hơn 0!")
        return

    # Tính toán thể tích và diện tích bề mặt
    volume = side_length ** 3
    surface_area = 6 * (side_length ** 2)

    # Tạo hình lập phương
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Các tọa độ của các đỉnh của hình lập phương
    r = [-side_length / 2, side_length / 2]
    X, Y = np.meshgrid(r, r)

    # Vẽ các mặt của hình lập phương
    ax.plot_surface(X, Y, np.array([[side_length / 2] * 2] * 2), color='c', alpha=0.6)  # Mặt trên
    ax.plot_surface(X, Y, np.array([[-side_length / 2] * 2] * 2), color='c', alpha=0.6)  # Mặt dưới
    ax.plot_surface(X, np.array([[side_length / 2] * 2] * 2), Y, color='c', alpha=0.6)  # Mặt trước
    ax.plot_surface(X, np.array([[-side_length / 2] * 2] * 2), Y, color='c', alpha=0.6)  # Mặt sau
    ax.plot_surface(np.array([[side_length / 2] * 2] * 2), X, Y, color='c', alpha=0.6)  # Mặt phải
    ax.plot_surface(np.array([[-side_length / 2] * 2] * 2), X, Y, color='c', alpha=0.6)  # Mặt trái

    ax.set_box_aspect([1, 1, 1])
    ax.set_title("Hình Lập Phương")
    show_plot(fig)  # Hiển thị hình lập phương

    # Hiển thị kết quả
    result = f"Thể tích: {volume:.2f}\nDiện tích bề mặt: {surface_area:.2f}"
    result_label.config(text=result)

# Hàm vẽ hình nón
def draw_cone(radius, height):
    if radius <= 0 or height <= 0:
        messagebox.showerror("Lỗi", "Bán kính và chiều cao phải lớn hơn 0!")
        return

    # Tính toán thể tích và diện tích xung quanh
    volume = (1/3) * np.pi * radius**2 * height
    lateral_area = np.pi * radius * np.sqrt(radius**2 + height**2)

    # Tạo đồ thị 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Tạo lưới tọa độ cho hình nón
    z = np.linspace(0, height, 50)  # Trục chiều cao từ 0 đến chiều cao
    theta = np.linspace(0, 2 * np.pi, 50)  # Góc quay quanh trục
    theta_grid, z_grid = np.meshgrid(theta, z)

    # Chuyển đổi tọa độ sang hệ trục Descartes
    x_grid = (height - z_grid) / height * radius * np.cos(theta_grid)
    y_grid = (height - z_grid) / height * radius * np.sin(theta_grid)

    # Vẽ mặt bên của hình nón
    ax.plot_surface(x_grid, y_grid, z_grid, color='c', alpha=0.6)

    # Vẽ đường tròn đáy
    theta_circle = np.linspace(0, 2 * np.pi, 50)
    x_circle = radius * np.cos(theta_circle)
    y_circle = radius * np.sin(theta_circle)
    z_circle = np.zeros_like(x_circle)
    ax.plot(x_circle, y_circle, z_circle, color='b')

    # Thiết lập các thông số đồ thị
    ax.set_box_aspect([1, 1, height/radius])
    ax.set_title("Hình Nón")
    show_plot(fig)

    # Hiển thị kết quả tính toán
    result = f"Thể tích: {volume:.2f}\nDiện tích xung quanh: {lateral_area:.2f}"
    result_label.config(text=result)

# Giao diện tkinter
def draw_2d_shapes():
    for widget in control_frame.winfo_children():
        widget.destroy()

    title_label = ttk.Label(control_frame, text="Chọn hình 2D:", font=("Arial", 14))
    title_label.grid(row=0, column=0, pady=10)

    # Vẽ tam giác
    triangle_label = ttk.Label(control_frame, text="Tam giác: Nhập 3 cạnh")
    triangle_label.grid(row=1, column=0)
    triangle_entry_a = ttk.Entry(control_frame)
    triangle_entry_a.grid(row=2, column=0)
    triangle_entry_b = ttk.Entry(control_frame)
    triangle_entry_b.grid(row=3, column=0)
    triangle_entry_c = ttk.Entry(control_frame)
    triangle_entry_c.grid(row=4, column=0)

    def draw_triangle_button():
        a = float(triangle_entry_a.get())
        b = float(triangle_entry_b.get())
        c = float(triangle_entry_c.get())
        draw_triangle(a, b, c)

    triangle_button = ttk.Button(control_frame, text="Vẽ Tam Giác", command=draw_triangle_button)
    triangle_button.grid(row=5, column=0, pady=10)

    # Vẽ hình tròn
    circle_label = ttk.Label(control_frame, text="Hình tròn: Nhập bán kính")
    circle_label.grid(row=6, column=0)
    circle_entry = ttk.Entry(control_frame)
    circle_entry.grid(row=7, column=0)

    def draw_circle_button():
        radius = float(circle_entry.get())
        draw_circle(radius)

    circle_button = ttk.Button(control_frame, text="Vẽ Hình Tròn", command=draw_circle_button)
    circle_button.grid(row=8, column=0, pady=10)

    # Vẽ hình vuông
    square_label = ttk.Label(control_frame, text="Hình vuông: Nhập cạnh")
    square_label.grid(row=9, column=0)
    square_entry = ttk.Entry(control_frame)
    square_entry.grid(row=10, column=0)

    def draw_square_button():
        side = float(square_entry.get())
        draw_square(side)

    square_button = ttk.Button(control_frame, text="Vẽ Hình Vuông", command=draw_square_button)
    square_button.grid(row=11, column=0, pady=10)

    # Vẽ hình tứ giác
    quadrilateral_label = ttk.Label(control_frame, text="Hình Bình Hành: Nhập 2 cạnh và góc")
    quadrilateral_label.grid(row=12, column=0)
    parallelogram_entry_a = ttk.Entry(control_frame)
    parallelogram_entry_a.grid(row=13, column=0)
    parallelogram_entry_b = ttk.Entry(control_frame)
    parallelogram_entry_b.grid(row=14, column=0)
    parallelogram_entry_angle = ttk.Entry(control_frame)
    parallelogram_entry_angle.grid(row=15, column=0)

    def draw_parallelogram_button():
        a = float(parallelogram_entry_a.get())
        b = float(parallelogram_entry_b.get())
        angle = float(parallelogram_entry_angle.get())
        draw_parallelogram(a, b, angle)

    parallelogram_button = ttk.Button(control_frame, text="Vẽ Hình Bình Hành", command=draw_parallelogram_button)
    parallelogram_button.grid(row=16, column=0, pady=10)

    # Hiển thị kết quả chu vi, diện tích
    global result_label
    result_label = ttk.Label(control_frame, text="", font=("Arial", 12), foreground="blue")
    result_label.grid(row=18, column=0, pady=10)

    return1_button = ttk.Button(control_frame, text="Trở về", command=go_back_to_main_menu)
    return1_button.grid(row=20, column=0, pady=10)


def draw_3d_shapes():
    for widget in control_frame.winfo_children():
        widget.destroy()

    title_label = ttk.Label(control_frame, text="Chọn hình 3D:", font=("Arial", 14))
    title_label.grid(row=0, column=0, pady=10)

    # Vẽ hình trụ
    cylinder_label = ttk.Label(control_frame, text="Hình trụ: Nhập bán kính và chiều cao")
    cylinder_label.grid(row=1, column=0)
    cylinder_radius_entry = ttk.Entry(control_frame)
    cylinder_radius_entry.grid(row=2, column=0)
    cylinder_height_entry = ttk.Entry(control_frame)
    cylinder_height_entry.grid(row=3, column=0)

    cylinder_button = ttk.Button(control_frame, text="Vẽ Hình Trụ", command=lambda: draw_cylinder(float(cylinder_radius_entry.get()), float(cylinder_height_entry.get())))
    cylinder_button.grid(row=4, column=0, pady=10)

    # Vẽ hình cầu
    sphere_label = ttk.Label(control_frame, text="Hình cầu: Nhập bán kính")
    sphere_label.grid(row=5, column=0)
    sphere_entry = ttk.Entry(control_frame)
    sphere_entry.grid(row=6, column=0)

    sphere_button = ttk.Button(control_frame, text="Vẽ Hình Cầu", command=lambda: draw_sphere(float(sphere_entry.get())))
    sphere_button.grid(row=7, column=0, pady=10)

    # Vẽ hình lập phương
    cube_label = ttk.Label(control_frame, text="Hình lập phương: Nhập độ dài cạnh")
    cube_label.grid(row=8, column=0)
    cube_side_entry = ttk.Entry(control_frame)
    cube_side_entry.grid(row=9, column=0)

    cube_button = ttk.Button(control_frame, text="Vẽ Hình Lập Phương",
                             command=lambda: draw_cube(float(cube_side_entry.get())))
    cube_button.grid(row=10, column=0, pady=10)

    # Vẽ hình nón
    cone_label = ttk.Label(control_frame, text="Hình nón: Nhập bán kính và chiều cao")
    cone_label.grid(row=11, column=0)
    cone_radius_entry = ttk.Entry(control_frame)
    cone_radius_entry.grid(row=12, column=0)
    cone_height_entry = ttk.Entry(control_frame)
    cone_height_entry.grid(row=13, column=0)

    cone_button = ttk.Button(control_frame, text="Vẽ Hình Nón",
                             command=lambda: draw_cone(float(cone_radius_entry.get()), float(cone_height_entry.get())))
    cone_button.grid(row=14, column=0, pady=10)

    # Hiển thị kết quả thể tích, diện tích
    global result_label
    result_label = ttk.Label(control_frame, text="", font=("Arial", 12), foreground="blue")
    result_label.grid(row=15, column=0, pady=10)

    return2_button = ttk.Button(control_frame, text="Trở về", command=go_back_to_main_menu)
    return2_button.grid(row=17, column=0, pady=10)


def go_back_to_main_menu():

    # Xóa tất cả widget trong control_frame
    for widget in control_frame.winfo_children():
        widget.destroy()

    # Thêm lại các widget của menu chính
    main_menu_label = ttk.Label(control_frame, text="Chọn kiểu hình:", font=("Arial", 14))
    main_menu_label.grid(row=0, column=0, pady=10)

    button_2d = ttk.Button(control_frame, text="Chọn Hình 2D", command=draw_2d_shapes)
    button_2d.grid(row=1, column=0, pady=5)

    button_3d = ttk.Button(control_frame, text="Chọn Hình 3D", command=draw_3d_shapes)
    button_3d.grid(row=2, column=0, pady=5)


# Khởi tạo tkinter
root = tk.Tk()
root.title("Ứng Dụng Hỗ Trợ Học Hình Học")

# Cấu hình các cột của root để tạo đệm và căn giữa
root.grid_columnconfigure(0, weight=1)  # Cột đệm bên trái
root.grid_columnconfigure(1, weight=0)  # Cột chứa control_frame (không mở rộng)
root.grid_columnconfigure(2, weight=0)  # Cột chứa plot_frame (không mở rộng)
root.grid_columnconfigure(3, weight=1)  # Cột đệm bên phải

# Cấu hình hàng cho căn giữa theo chiều dọc nếu cần
root.grid_rowconfigure(0, weight=1)

# Tạo các khung
control_frame = ttk.Frame(root, padding="10")
control_frame.grid(row=0, column=1)  # Loại bỏ sticky='nsew'

plot_frame = ttk.Frame(root, padding="10")
plot_frame.grid(row=0, column=2)     # Loại bỏ sticky='nsew'

# Các nút để chọn hình
shape_selection_label = ttk.Label(control_frame, text="Chọn kiểu hình:", font=("Arial", 14))
shape_selection_label.grid(row=0, column=0)

draw_2d_button = ttk.Button(control_frame, text="Hình 2D", command=draw_2d_shapes)
draw_2d_button.grid(row=1, column=0, pady=10)

draw_3d_button = ttk.Button(control_frame, text="Hình 3D", command=draw_3d_shapes)
draw_3d_button.grid(row=2, column=0, pady=10)

# Khởi động ứng dụng
root.mainloop()
