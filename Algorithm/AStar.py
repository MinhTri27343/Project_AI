import heapq
import utils
from const import *
def Heuristic(start, end):
    return abs(end[1] - start[1]) + abs(end[0] - start[0])

def AStar(grid, start, end):
    def getCost(before, next):
        if before[0] != next[0] and before[1] != next[1]:
            return 1.5
        return 1
    row, col = len(grid), len(grid[0])
    visited = set()
    queue = []
    expand_nodes = 0  # Biến đếm số lượng node mở rộng
    
    if grid[start[0]][start[1]] not in utils.VALID_VALUES_GHOST or grid[end[0]][end[1]] not in utils.VALID_VALUES_GHOST or utils.ghost_status[start[0]][start[1]] == 1 or utils.ghost_status[end[0]][end[1]] == 1:
        return None, expand_nodes, "AStar"
    
    heapq.heappush(queue, (Heuristic(start, end), 0, start, [start], start))  # (priority, g_cost, node, path, node_before)
    while queue:
        _, current_cost, current_index, path, parent = heapq.heappop(queue)
        x, y = current_index
        
        if current_index in visited:
            continue
        visited.add(current_index)
        expand_nodes += 1
        if current_index == end:
            return path, expand_nodes, "AStar"
        
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            
            if 0 <= new_x < row and 0 <= new_y < col and (new_x, new_y) not in visited and grid[new_x][new_y] in utils.VALID_VALUES_GHOST and utils.ghost_status[new_x][new_y] == 0:
                new_cost = current_cost + getCost(parent, (new_x, new_y))
                priority = new_cost + Heuristic((new_x, new_y), end)
                heapq.heappush(queue, (priority, new_cost, (new_x, new_y), path + [(new_x, new_y)], (x, y)))
    
    return None, expand_nodes, "AStar"