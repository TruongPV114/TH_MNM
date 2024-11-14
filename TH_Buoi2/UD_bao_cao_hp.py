import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Button

# Load CSV data into a DataFrame
file_path = 'diemPython.csv'  # Đảm bảo file CSV này có trong cùng thư mục với script
df = pd.read_csv(file_path, index_col=0, header=0)

# Convert DataFrame to NumPy array
in_data = df.to_numpy()

# Grade statistics
loai_diem = {
    "A+": in_data[:, 2],
    "A" : in_data[:, 3],
    "B+": in_data[:, 4],
    "B" : in_data[:, 5],
    "C+": in_data[:, 6],
    "C" : in_data[:, 7],
    "D+": in_data[:, 8],
    "D" : in_data[:, 9],
    "F" : in_data[:, 10],
}

# Average scores for L1, L2, TX1, TX2, and final score
l1_avg = np.mean(in_data[:, 11])
l2_avg = np.mean(in_data[:, 12])
tx1_avg = np.mean(in_data[:, 13])
tx2_avg = np.mean(in_data[:, 14])
cuoi_ky_avg = np.mean(in_data[:, 15])

# Create functions to show each plot
def show_grade_distribution():
    plt.figure(figsize=(8, 6))
    labels = list(loai_diem.keys())
    values = [np.sum(diem) for diem in loai_diem.values()]
    plt.bar(labels, values, color='lightblue')
    plt.xlabel('Phân loại điểm')
    plt.ylabel('Số sinh viên')
    plt.title('Số sinh viên đạt từng loại điểm')
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_l1_l2():
    plt.figure(figsize=(6, 4))
    avg_labels_L1_L2 = ['L1', 'L2']
    avg_values_L1_L2 = [l1_avg, l2_avg]
    plt.bar(avg_labels_L1_L2, avg_values_L1_L2, color='orange')
    plt.xlabel('Bài kiểm tra L1, L2')
    plt.ylabel('Số sinh viên')
    plt.title('Điểm trung bình của L1 và L2')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def show_tx1_tx2_final():
    plt.figure(figsize=(6, 4))
    avg_labels_TX1_TX2_CuoiKy = ['TX1', 'TX2', 'Cuối kỳ']
    avg_values_TX1_TX2_CuoiKy = [tx1_avg, tx2_avg, cuoi_ky_avg]
    plt.bar(avg_labels_TX1_TX2_CuoiKy, avg_values_TX1_TX2_CuoiKy, color='green')
    plt.xlabel('Bài kiểm tra')
    plt.ylabel('Số sinh viên')
    plt.title('Điểm trung bình TX1, TX2 và Cuối kỳ')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# Create GUI window
root = Tk()
root.title("Chọn biểu đồ")

# Create buttons
btn_grade_distribution = Button(root, text="Xem biểu đồ phân loại điểm", command=show_grade_distribution)
btn_grade_distribution.pack(pady=10)

btn_l1_l2 = Button(root, text="Xem biểu đồ L1 và L2", command=show_l1_l2)
btn_l1_l2.pack(pady=10)

btn_tx1_tx2_final = Button(root, text="Xem biểu đồ TX1, TX2 và Cuối kỳ", command=show_tx1_tx2_final)
btn_tx1_tx2_final.pack(pady=10)

# Run the GUI loop
root.mainloop()