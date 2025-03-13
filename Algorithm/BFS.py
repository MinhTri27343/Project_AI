from collections import deque 
import utils 
from const import * 

def BFS(matrix, start, end):
    row_start, col_start = start
    row_end, col_end = end
    rows, cols = len(matrix), len(matrix[0])
    directions = DIRECTIONS  # Lên, xuống, trái, phải
    expanded_nodes = 0  # Biến đếm số node mở rộng
    
    if matrix[row_start][col_start] not in utils.VALID_VALUES_GHOST or matrix[row_end][col_end] not in utils.VALID_VALUES_GHOST or utils.ghost_status[row_start][col_start] == 1 or utils.ghost_status[row_end][col_end] == 1:
        return None, expanded_nodes, "BFS"
    queue = deque([(row_start, col_start, [])])
    visited = set()
    visited.add((row_start, col_start))
    while queue:
        x, y, path = queue.popleft()
        expanded_nodes += 1
        # Nếu đến đích, trả về đường đi
        if (x, y) == (row_end, col_end):
            return path + [(x, y)], expanded_nodes, "BFS"
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                if matrix[nx][ny] in utils.VALID_VALUES_GHOST and utils.ghost_status[nx][ny] == 0:  # Sửa điều kiện này
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(x, y)]))
    return None, expanded_nodes, "BFS"  # Không tìm thấy đường đi