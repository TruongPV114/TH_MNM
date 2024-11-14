import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# Khởi tạo biến toàn cục
df = None
model = None


# Load CSV Data function
def load_data():
  global df
  file_path = filedialog.askopenfilename()
  if file_path:
    try:
      df = pd.read_csv(file_path, encoding='ISO-8859-1')
      # Chỉ giữ lại các cột có dữ liệu số
      df_numeric = df.select_dtypes(include=[float, int])
      # Xử lý missing values
      imputer = SimpleImputer(strategy='mean')
      df_imputed = pd.DataFrame(imputer.fit_transform(df_numeric), columns=df_numeric.columns)
      df = df_imputed  # Lưu lại dữ liệu đã xử lý
      messagebox.showinfo("Success", "Data loaded and processed successfully!")
    except Exception as e:
      messagebox.showerror("Error", f"Failed to load data: {e}")


# Train function using KNN
def train_model():
  global model
  if df is None:
    messagebox.showwarning("Warning", "Please load data first!")
    return

  try:
    # Xác định các feature và target (giả sử cột cuối là target)
    X = df.iloc[:, :-1]  # Tất cả các cột trừ cột cuối
    y = df.iloc[:, -1]  # Cột cuối làm target
    # Chia tập dữ liệu cho training và testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Huấn luyện mô hình KNN
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    messagebox.showinfo("Success", "Model trained successfully!")
  except Exception as e:
    messagebox.showerror("Error", f"Failed to train model: {e}")


# Predict function
def predict_performance():
  global model
  if model is None:
    messagebox.showwarning("Warning", "Please train the model first!")
    return

  try:
    # Lấy giá trị từ các ô nhập liệu
    input_data = {"Hours Studied": [float(entry_hour_studied.get())],
      "Previous Scores": [float(entry_previous_scores.get())],
      "Extracurricular Activities": [float(entry_extra_activities.get())],
      "Sleep Hours": [float(entry_sleep_hours.get())],
      "Sample Question Papers Practiced": [float(entry_sample_question.get())]}
    # Tạo DataFrame với tên cột
    input_df = pd.DataFrame(input_data)

    # Dự đoán chỉ số "Performance Index" và làm tròn kết quả
    prediction = model.predict(input_df)
    prediction_rounded = round(prediction[0])  # Làm tròn kết quả thành số nguyên

    messagebox.showinfo("Prediction", f"Predicted Performance Index: {int(prediction_rounded)}")
  except ValueError:
    messagebox.showerror("Error", "Please enter valid numerical values in all fields.")
  except Exception as e:
    messagebox.showerror("Error", f"Failed to make prediction: {e}")


# Khởi tạo tkinter
root = tk.Tk()
root.title("Ứng dụng dự đoán kết quả học tập")

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

tk.Label(control_frame, text="Hours Studied").grid(row=1, column=0, sticky="e")
entry_hour_studied = tk.Entry(control_frame)
entry_hour_studied.grid(row=1, column=1, sticky="w")

tk.Label(control_frame, text="Previous Scores").grid(row=2, column=0, sticky="e")
entry_previous_scores = tk.Entry(control_frame)
entry_previous_scores.grid(row=2, column=1, sticky="w")

tk.Label(control_frame, text="Extracurricular Activities").grid(row=3, column=0, sticky="e")
entry_extra_activities = tk.Entry(control_frame)
entry_extra_activities.grid(row=3, column=1, sticky="w")

tk.Label(control_frame, text="Sleep Hours").grid(row=4, column=0, sticky="e")
entry_sleep_hours = tk.Entry(control_frame)
entry_sleep_hours.grid(row=4, column=1, sticky="w")

tk.Label(control_frame, text="Sample Question Papers Practiced").grid(row=5, column=0, sticky="e")
entry_sample_question = tk.Entry(control_frame)
entry_sample_question.grid(row=5, column=1, sticky="w")

tk.Button(control_frame, text="Predict", command=predict_performance).grid(row=6, column=0, columnspan=2, pady=10,
                                                                           sticky="ew")

root.mainloop()
