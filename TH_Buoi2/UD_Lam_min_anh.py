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


def smooth_skin(image):
    # Chuyển đổi sang không gian màu YCrCb để xử lý da tốt hơn
    img_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(img_ycrcb)

    # Áp dụng GaussianBlur trên kênh độ sáng (Y channel)
    y_blurred = cv2.GaussianBlur(y, (15, 15), 0)

    # Ghép lại và chuyển sang BGR
    img_ycrcb_blur = cv2.merge((y_blurred, cr, cb))
    skin_smoothed = cv2.cvtColor(img_ycrcb_blur, cv2.COLOR_YCrCb2BGR)

    # Tăng độ nét của ảnh bằng cách cộng với phần ảnh gốc để giữ lại chi tiết
    sharpened = cv2.addWeighted(image, 0.5, skin_smoothed, 0.5, 0)

    return sharpened


# Trong hàm smooth_image, thay thế bằng hàm mới
def smooth_image():
    global processed_image
    if original_image is not None:
        # Áp dụng chức năng làm mịn da
        processed_image = smooth_skin(original_image)
        display_image_in_new_window(processed_image, "Skin Smoothed Image")


# Hàm lưu ảnh
def save_image():
    if processed_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, processed_image)
            print(f"Image saved at {file_path}")

# Khởi tạo tkinter
root = tk.Tk()
root.title("Ứng dụng xử lý ảnh")

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
tk.Button(control_frame, text="Smooth", command=smooth_image).grid(row=1, column=1, pady=10)
tk.Button(control_frame, text="SAVE", command=save_image).grid(row=2, column=1, pady=10)

# Chạy ứng dụng
root.mainloop()
