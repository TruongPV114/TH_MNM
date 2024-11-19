import cv2
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, ttk

# Biến lưu trữ ảnh đã xử lý
processed_image = None

# Hàm chọn ảnh
def select_image():
    global img, original_image
    file_path = filedialog.askopenfilename()
    if len(file_path) > 0:
        img = cv2.imread(file_path)
        original_image = img.copy()
        display_image_in_new_window(img, "Original Image")

# Hàm hiển thị ảnh trong cửa sổ mới
def display_image_in_new_window(img, title):
    global processed_image
    processed_image = img  # Cập nhật ảnh đã xử lý
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Chuyển sang RGB

    # Thay đổi kích thước hình ảnh
    height, width = img_rgb.shape[:2]
    max_height = 400  # Chiều cao tối đa cho cửa sổ
    scale = max_height / height
    new_width = int(width * scale)
    new_height = int(height * scale)

    resized_img = cv2.resize(img_rgb, (new_width, new_height))  # Thay đổi kích thước ảnh

    img_pil = Image.fromarray(resized_img)  # Chuyển sang định dạng PIL
    img_tk = ImageTk.PhotoImage(img_pil)

    new_window = Toplevel()  # Tạo cửa sổ mới
    new_window.title(title)
    panel = Label(new_window, image=img_tk)
    panel.image = img_tk  # Giữ tham chiếu ảnh
    panel.pack()

# Hàm tăng chất lượng ảnh
def enhance_image():
    global processed_image, original_image
    if original_image is not None:
        # Điều chỉnh độ sáng và độ tương phản
        alpha = 1.3  # Hệ số độ sáng
        beta = 30    # Độ lệch độ sáng
        processed_image = cv2.convertScaleAbs(original_image, alpha=alpha, beta=beta)
        display_image_in_new_window(processed_image, "Enhanced Image")
    else:
        print("Vui lòng chọn một ảnh trước")

# Hàm lưu ảnh
def save_image():
    if processed_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, processed_image)
            print(f"Image saved at {file_path}")

# Khởi tạo tkinter
root = tk.Tk()
root.title("Ứng dụng tăng chất lượng ảnh thiếu sáng")

# Cấu hình các cột của root để tạo đệm và căn giữa
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

# Tạo các khung
control_frame = ttk.Frame(root, padding="10")
control_frame.grid(row=0, column=1, sticky="nsew")

plot_frame = ttk.Frame(root, padding="10")
plot_frame.grid(row=0, column=2, sticky="nsew")

# Cấu hình cột trong control_frame
control_frame.grid_columnconfigure(0, weight=1)
control_frame.grid_columnconfigure(1, weight=1)

# Các nút
tk.Button(control_frame, text="Select Photo", command=select_image).grid(row=0, column=1, pady=10)
tk.Button(control_frame, text="Tăng chất lượng", command=enhance_image).grid(row=1, column=1, pady=10)
tk.Button(control_frame, text="SAVE", command=save_image).grid(row=2, column=1, pady=10)

# Chạy ứng dụng
root.mainloop()
