import utils
from collections import deque
from const import *

queue_max = deque(maxlen=5)

def IDS(arr2D, start, end):
    def DLS(arr2D, start, end, max_depth):
        stack = [(start, [tuple(start)], 0)]  # [current position, path, depth]
        visited = set()
        visited.add(tuple(start))
        expanded_nodes = 0  # Biến đếm số node mở rộng
        
        if end in queue_max:
            return None, 0
        
        while stack:
            now, path, depth = stack.pop()
            expanded_nodes += 1  # Đếm số node đã duyệt
            
            if tuple(now) == tuple(end):
                return path, expanded_nodes
            
            if depth < max_depth:
                visited.add(tuple(now))
                for d in DIRECTIONS:
                    node = (now[0] + d[0], now[1] + d[1])
                    if 0 <= node[0] < rows and 0 <= node[1] < cols and node not in visited and node not in queue_max:
                        if arr2D[node[0]][node[1]] in utils.VALID_VALUES_GHOST and utils.ghost_status[node[0]][node[1]] == 0:
                            stack.append((node, path + [node], depth + 1))
        
        return None, expanded_nodes  # Không tìm thấy đường đi

    if start == end:
        return None, 0
    
    if arr2D[start[0]][start[1]] not in utils.VALID_VALUES_GHOST or \
       arr2D[end[0]][end[1]] not in utils.VALID_VALUES_GHOST or \
       utils.ghost_status[start[0]][start[1]] == 1 or \
       utils.ghost_status[start[1]][end[1]] == 1:
        return None, 0
    
    rows, cols = len(arr2D), len(arr2D[0])
    depth = 0
    depth_limit = rows * cols
    total_expanded_nodes = 0  # Biến tổng số node đã mở rộng
    
    while depth <= depth_limit:
        result, expanded_nodes = DLS(arr2D, start, end, depth)
        total_expanded_nodes += expanded_nodes  # Cộng dồn số node mở rộng
        if result is not None:
            return result, total_expanded_nodes
        depth += 1
    
    return None, total_expanded_nodes  # Không tìm thấy đường đi
