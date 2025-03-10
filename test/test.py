import pygame
import time
import tracemalloc

# Khởi tạo pygame
pygame.init()
WIDTH, HEIGHT = 800, 600  # Có thể thay đổi kích thước tùy ý
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Search Algorithm Statistics")
pygame.font.init()

# Font chữ
font = pygame.font.Font(None, 40)
font_bold = pygame.font.Font(None, 50)

# Đo thời gian & bộ nhớ
tracemalloc.start()
start_time = time.time()
time.sleep(0.002)  # Giả lập thuật toán tìm kiếm
search_time = time.time() - start_time
current_memory, peak_memory = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (128, 0, 128)  # Màu tím (Purple)

def draw_text(screen, text, center_x, y, font, color=BLACK):
    """Vẽ text căn giữa theo trục X."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, y))
    screen.blit(text_surface, text_rect)

def draw_statistics(screen, search_time, memory_usage, expanded_nodes):
    """Vẽ các thông số thuật toán lên screen (căn giữa tự động)."""
    screen.fill(BACKGROUND_COLOR)  # Xóa màn hình trước khi vẽ lại

    # Lấy kích thước màn hình
    WIDTH, HEIGHT = screen.get_size()
    
    # Vị trí của tiêu đề
    title = "Search Algorithm Statistics"
    draw_text(screen, title, WIDTH // 2, HEIGHT * 0.2, font_bold)

    # Danh sách thông tin
    labels = ["Search Time:", "Memory Usage:", "Expanded Nodes:"]
    values = [
        f"{search_time:.6f} seconds",
        f"{memory_usage / 1024:.2f} KB",
        f"{expanded_nodes}"
    ]
    
    # Vị trí bắt đầu hiển thị nội dung, căn giữa
    start_y = HEIGHT * 0.4  # Bắt đầu từ 40% chiều cao màn hình
    y_offset = HEIGHT * 0.1  # Khoảng cách giữa các dòng (10% chiều cao)

    # for i in range(len(labels)):
    #     draw_text(screen, labels[i], WIDTH * 0.4, start_y + i * y_offset, font)
    #     draw_text(screen, values[i], WIDTH * 0.6, start_y + i * y_offset, font)

    pygame.display.flip()  # Cập nhật màn hình

# Hiển thị kết quả
draw_statistics(screen, search_time, peak_memory, 45)

# Vòng lặp sự kiện
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.time.delay(10)

pygame.quit()
