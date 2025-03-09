import time
from queue import PriorityQueue
from collections import deque
def Heuristic(start, end):
    return abs(end[1] - start[1]) + abs(end[0] - start[0])


def AStar(grid, start, end):
    visited = {(x, y): False for x in range(row) for y in range(col)}
    path = []
    row, col = len(grid), len(grid[0])
    queue = PriorityQueue()
    parent = {}
    cost = {}
    direction = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    
    cost[start] = 0
    queue.put((Heuristic(start, end), start))
    
    while not queue.empty():
        current_weight, current_index = queue.get()
        x, y = current_index
        
        if visited[(x, y)]:
            continue
        visited[(x, y)] = True
        
        if current_index == end:
            path.append((x, y))
            while current_index in parent:
                current_index = parent[current_index]
                path.append(current_index)
            path.reverse()
            return path
        
        for dx, dy in direction:
            new_x, new_y = x + dx, y + dy
            
            if 0 <= new_x < row and 0 <= new_y < col and not visited[(new_x, new_y)] and grid[new_x][new_y] in (0, 1, 9):
                new_cost = cost[current_index] + 1
                if (new_x, new_y) not in cost or new_cost < cost[(new_x, new_y)]:
                    cost[(new_x, new_y)] = new_cost
                    priority = new_cost + Heuristic((new_x, new_y), end)
                    queue.put((priority, (new_x, new_y)))
                    parent[(new_x, new_y)] = current_index
    
    return None
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
        path = AStar(matrix, (ghost_x, ghost_y), (pacman_x, pacman_y), is_valid)
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
