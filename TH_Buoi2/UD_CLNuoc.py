import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier  # Thuật toán KNN
import pandas as pd

# Biến toàn cục để lưu trữ dữ liệu và mô hình
df = None
model = None  # Biến cho mô hình học máy

# Load CSV Data function
def load_data():
    global df
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            # Load file CSV với mã hóa phù hợp
            df = pd.read_csv(file_path, encoding='ISO-8859-1')

            # Kiểm tra xem các cột cần thiết có trong dữ liệu hay không
            required_columns = {'ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate',
                                'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity', 'Potability'}
            if not required_columns.issubset(df.columns):
                raise ValueError("CSV file must contain the required columns.")

            # Chỉ giữ lại các cột có dữ liệu số và thực hiện imputation (xử lý missing values)
            df_numeric = df.select_dtypes(include=[float, int])
            imputer = SimpleImputer(strategy='constant', fill_value=0)
            df_imputed = pd.DataFrame(imputer.fit_transform(df_numeric), columns=df_numeric.columns)

            # Cập nhật DataFrame sau khi xử lý missing values
            df = df_imputed
            messagebox.showinfo("Success", "Data loaded and processed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

# Train function using KNN
def train_model():
    global model
    if df is not None:
        try:
            # Chuẩn bị dữ liệu đầu vào và nhãn
            X = df.drop(columns=['Potability'])  # Đặc trưng
            y = df['Potability']  # Nhãn

            # Khởi tạo và huấn luyện mô hình KNN
            model = KNeighborsClassifier(n_neighbors=5)
            model.fit(X, y)

            messagebox.showinfo("Success", "Model trained successfully with KNN!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to train model: {e}")
    else:
        messagebox.showwarning("Warning", "Please load data first.")

# Predict function
def predict():
    if model is not None:
        try:
            # Lấy dữ liệu từ các entry
            values = [
                float(entry_pH.get()), float(entry_Hardness.get()), float(entry_Solids.get()),
                float(entry_Chloramines.get()), float(entry_Sulfate.get()), float(entry_Conductivity.get()),
                float(entry_Organic_carbon.get()), float(entry_Trihalomethanes.get()), float(entry_Turbidity.get())
            ]

            # Tạo DataFrame với tên cột giống với dữ liệu huấn luyện
            X_new = pd.DataFrame([values], columns=['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate',
                                                    'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity'])
            prediction = model.predict(X_new)[0]

            # Hiển thị kết quả dự đoán
            result = "Uống được" if prediction == 1 else "Không uống được"
            messagebox.showinfo("Prediction", f"Predicted Potability: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to make prediction: {e}")
    else:
        messagebox.showwarning("Warning", "Please train the model first.")

# Khởi tạo tkinter
root = tk.Tk()
root.title("Ứng dụng xác định chất lượng nước")

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

# Thêm các widget vào control_frame
tk.Button(control_frame, text="Train", command=train_model).grid(row=0, column=0, pady=10, sticky="ew")
tk.Button(control_frame, text="Load CSV Data", command=load_data).grid(row=0, column=1, pady=10, sticky="ew")

# Các trường nhập liệu cho các thông số
tk.Label(control_frame, text="pH").grid(row=1, column=0, sticky="e")
entry_pH = tk.Entry(control_frame)
entry_pH.grid(row=1, column=1, sticky="w")

tk.Label(control_frame, text="Hardness").grid(row=2, column=0, sticky="e")
entry_Hardness = tk.Entry(control_frame)
entry_Hardness.grid(row=2, column=1, sticky="w")

tk.Label(control_frame, text="Solids").grid(row=3, column=0, sticky="e")
entry_Solids = tk.Entry(control_frame)
entry_Solids.grid(row=3, column=1, sticky="w")

tk.Label(control_frame, text="Chloramines").grid(row=4, column=0, sticky="e")
entry_Chloramines = tk.Entry(control_frame)
entry_Chloramines.grid(row=4, column=1, sticky="w")

tk.Label(control_frame, text="Sulfate").grid(row=5, column=0, sticky="e")
entry_Sulfate = tk.Entry(control_frame)
entry_Sulfate.grid(row=5, column=1, sticky="w")

tk.Label(control_frame, text="Conductivity").grid(row=6, column=0, sticky="e")
entry_Conductivity = tk.Entry(control_frame)
entry_Conductivity.grid(row=6, column=1, sticky="w")

tk.Label(control_frame, text="Organic_carbon").grid(row=7, column=0, sticky="e")
entry_Organic_carbon = tk.Entry(control_frame)
entry_Organic_carbon.grid(row=7, column=1, sticky="w")

tk.Label(control_frame, text="Trihalomethanes").grid(row=8, column=0, sticky="e")
entry_Trihalomethanes = tk.Entry(control_frame)
entry_Trihalomethanes.grid(row=8, column=1, sticky="w")

tk.Label(control_frame, text="Turbidity").grid(row=9, column=0, sticky="e")
entry_Turbidity = tk.Entry(control_frame)
entry_Turbidity.grid(row=9, column=1, sticky="w")

tk.Button(control_frame, text="Predict", command=predict).grid(row=10, column=0, columnspan=2, pady=10, sticky="ew")

root.mainloop()
