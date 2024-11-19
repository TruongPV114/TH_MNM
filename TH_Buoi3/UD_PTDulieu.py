import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt


# Load CSV Data function
def load_data():
  global df
  file_path = filedialog.askopenfilename()
  if file_path:
    try:
      df = pd.read_csv(file_path, encoding='ISO-8859-1')
      df_numeric = df.select_dtypes(include=[float, int])
      imputer = SimpleImputer(strategy='mean')
      df_imputed = pd.DataFrame(imputer.fit_transform(df_numeric), columns=df_numeric.columns)
      df = df_imputed
      messagebox.showinfo("Success", "Data loaded and processed successfully!")
    except Exception as e:
      messagebox.showerror("Error", f"Failed to load data: {e}")


# Display Statistics
def show_statistics():
  selected_data = data_var.get()
  if selected_data not in df.columns:
    messagebox.showerror("Error", f"Column '{selected_data}' not found in data!")
    return

  max_value = df[selected_data].max()
  min_value = df[selected_data].min()
  mean_value = df[selected_data].mean()

  stats_window = tk.Toplevel(root)
  stats_window.title(f"Statistics for {selected_data}")
  stats_window.geometry("300x150")

  tk.Label(stats_window, text=f"Max: {max_value:.2f}").pack(pady=5)
  tk.Label(stats_window, text=f"Min: {min_value:.2f}").pack(pady=5)
  tk.Label(stats_window, text=f"Mean: {mean_value:.2f}").pack(pady=5)


# Plot Data Distribution
def plot_distribution():
  selected_data = data_var.get()
  if selected_data not in df.columns:
    messagebox.showerror("Error", f"Column '{selected_data}' not found in data!")
    return

  plt.figure(figsize=(8, 5))
  plt.hist(df[selected_data], bins=20, color='skyblue', edgecolor='black')
  plt.title(f"Distribution of {selected_data}")
  plt.xlabel(selected_data)
  plt.ylabel("Frequency")
  plt.show()


# Analyze data function
def analyze_data():
  if 'df' not in globals():
    messagebox.showerror("Error", "Please load data first!")
    return

  show_statistics()
  plot_distribution()


# Initialize tkinter
root = tk.Tk()
root.title("Ứng dụng Phân tích Dữ liệu Học Tập")
root.geometry("400x300")

# Configure root columns and rows for center alignment
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a main frame to hold all widgets and center them
main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=1, column=0, sticky="nsew")
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Load Data button
load_button = ttk.Button(main_frame, text="Load CSV Data", command=load_data)
load_button.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

# Data selection dropdown
ttk.Label(main_frame, text="Choose Data:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
data_var = tk.StringVar(value="Hours Studied")
data_dropdown = ttk.OptionMenu(main_frame, data_var, "Hours Studied", "Previous Scores", "Extracurricular Activities",
                               "Sleep Hours", "Sample Question Papers Practiced", "Performance Index")
data_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Analysis button
analysis_button = ttk.Button(main_frame, text="Analysis", command=analyze_data)
analysis_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

root.mainloop()
