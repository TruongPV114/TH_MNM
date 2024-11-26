import pygame
import random
import csv
import time
import tkinter as tk
from tkinter import messagebox

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game bắn chim")

# Tải và điều chỉnh kích thước ảnh nền để vừa với cửa sổ
background_img = pygame.image.load("bg1.jpg")
background_img = pygame.transform.scale(background_img, (width, height))

# Tải và điều chỉnh kích thước tâm ngắm
crosshair_img = pygame.image.load("tam_ngam.png")
crosshair_img = pygame.transform.scale(crosshair_img, (70, 70))

# Tải và thu nhỏ các ảnh nút
start_img = pygame.image.load("start.png")
start_img = pygame.transform.scale(start_img, (150, 75))  # Kích thước mong muốn

high_score_img = pygame.image.load("high_score.png")
high_score_img = pygame.transform.scale(high_score_img, (150, 75))  # Kích thước mong muốn

# Tạo rect cho mỗi ảnh và căn giữa
start_img_rect = start_img.get_rect(center=(width // 2, height // 2 - 50))
high_score_img_rect = high_score_img.get_rect(center=(width // 2, height // 2 + 50))

# Ẩn con trỏ chuột
pygame.mouse.set_visible(False)

# Tải và thu nhỏ các ảnh chim
bird_imgs = [pygame.image.load(f"chim{i}.png") for i in range(1, 8)]
bird_imgs = [pygame.transform.scale(img, (50, 50)) for img in bird_imgs]

# Cài đặt cơ bản
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)
game_duration = 60
start_time = None
birds = []
show_main_menu = True


# Tạo chim ngẫu nhiên từ ba hướng khác nhau
def spawn_bird():
  img = random.choice(bird_imgs)
  direction = random.choice(["left", "right", "bottom"])

  if direction == "left":
    x = -50
    y = random.randint(50, height - 50)
  elif direction == "right":
    x = width + 50
    y = random.randint(50, height - 50)
  else:
    x = random.randint(50, width - 50)
    y = height + 50

  speed_x = random.uniform(1.5, 3.5) * random.choice([-1, 1])
  speed_y = random.uniform(1.5, 3.5) * random.choice([-1, 1])
  birds.append([img, x, y, speed_x, speed_y])


# Hàm hiển thị điểm và thời gian
def display_info():
  score_text = font.render(f"Score: {score}", True, (255, 255, 255))
  screen.blit(score_text, (10, 10))

  elapsed_time = time.time() - start_time
  remaining_time = max(0, game_duration - int(elapsed_time))
  timer_text = font.render(f"Time: {remaining_time}s", True, (255, 255, 255))
  screen.blit(timer_text, (width - 150, 10))


# Lưu điểm vào file CSV
def save_score():
  with open("scores.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), score])


# Hiển thị danh sách điểm từ file CSV
def show_scores():
  try:
    with open("scores.csv", "r") as csvfile:
      reader = csv.reader(csvfile)
      scores = [row for row in reader]
  except FileNotFoundError:
    scores = []

  # Tạo cửa sổ mới với tkinter để hiển thị điểm
  score_window = tk.Tk()
  score_window.title("High Scores")

  # Thêm tiêu đề
  title_label = tk.Label(score_window, text="Top 5 High Scores", font=("Arial", 16))
  title_label.pack(pady=10)

  # Hiển thị điểm trong cửa sổ
  for i, score_row in enumerate(scores[-5:]):  # Hiển thị 5 điểm gần nhất
    score_label = tk.Label(score_window, text=f"{score_row[0]} - {score_row[1]}", font=("Arial", 12))
    score_label.pack()

  # Nút để đóng cửa sổ điểm
  close_button = tk.Button(score_window, text="Close", command=score_window.destroy)
  close_button.pack(pady=10)

  # Mở cửa sổ điểm
  score_window.mainloop()


# Vòng lặp chính
running = True
while running:
  screen.blit(background_img, (0, 0))

  if show_main_menu:
    # Hiển thị lại con trỏ chuột khi ở màn hình chờ
    pygame.mouse.set_visible(True)

    # Hiển thị menu chính
    screen.blit(start_img, start_img_rect)
    screen.blit(high_score_img, high_score_img_rect)

    # Kiểm tra các sự kiện trong menu chính
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if start_img_rect.collidepoint(event.pos):
          # Bắt đầu trò chơi
          score = 0
          birds = []
          start_time = time.time()
          for _ in range(5):
            spawn_bird()
          show_main_menu = False
        elif high_score_img_rect.collidepoint(event.pos):
          # Mở cửa sổ điểm cao
          show_scores()

  else:
    # Chạy trò chơi
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for bird in birds[:]:
          img, bird_x, bird_y, _, _ = bird
          if bird_x < mouse_x < bird_x + img.get_width() and bird_y < mouse_y < bird_y + img.get_height():
            birds.remove(bird)
            score += 1
            spawn_bird()

    for bird in birds:
      img, bird[1], bird[2], bird[3], bird[4] = bird
      bird[1] += bird[3]
      bird[2] += bird[4]

      bird[3] += random.uniform(-0.5, 0.5)
      bird[4] += random.uniform(-0.5, 0.5)
      bird[3] = max(min(bird[3], 4), -4)
      bird[4] = max(min(bird[4], 4), -4)

      if bird[1] < -50 or bird[1] > width + 50 or bird[2] < -50 or bird[2] > height + 50:
        birds.remove(bird)
        spawn_bird()
      screen.blit(img, (bird[1], bird[2]))

    while len(birds) < 5:
      spawn_bird()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(crosshair_img, (mouse_x - crosshair_img.get_width() // 2, mouse_y - crosshair_img.get_height() // 2))
    display_info()

    if time.time() - start_time >= game_duration:
      save_score()
      show_main_menu = True

  pygame.display.flip()
  clock.tick(60)

pygame.quit()
