import time
from collections import deque

def bfs(matrix, x_start, y_start, x_end, y_end, can_move):
    rows, cols = len(matrix), len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
    queue = deque([(x_start, y_start, [])])
    visited = set()
    visited.add((x_start, y_start))

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == (x_end, y_end):
            return path + [(x, y)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                if can_move(matrix[nx][ny]):
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(x, y)]))

    return None

# Hàm kiểm tra có thể di chuyển qua ô không
def is_valid(value):
    return value in (0, 1, 9)

# Giả lập quá trình di chuyển của con ma
def move_ghost(matrix, ghost_x, ghost_y, pacman_x, pacman_y, speed=2, delay=1):
    while (ghost_x, ghost_y) != (pacman_x, pacman_y):
        path = bfs(matrix, ghost_x, ghost_y, pacman_x, pacman_y, is_valid)
        print("Path: ", path)
        if not path or len(path) == 1:
            print("Con ma không thể đến Pacman!")
            break
        
        # Chọn bước tiếp theo theo tốc độ speed
        steps = min(speed, len(path) - 1)  # Không vượt quá đường đi có sẵn
        ghost_x, ghost_y = path[steps]

        # In vị trí con ma
        print(f"Con ma di chuyển đến: ({ghost_x}, {ghost_y})")
        
        time.sleep(delay)  # Tạo hiệu ứng di chuyển

    print("Con ma đã đến Pacman!")

# Ví dụ ma trận
maze = [
    [0, 1, 2, 0],
    [0, 2, 0, 9],
    [1, 0, 0, 0],
    [2, 9, 2, 0]
]

# Vị trí ban đầu
ghost_x, ghost_y = 0, 0
pacman_x, pacman_y = 3, 3

move_ghost(maze, ghost_x, ghost_y, pacman_x, pacman_y, speed=2, delay=0.5)
