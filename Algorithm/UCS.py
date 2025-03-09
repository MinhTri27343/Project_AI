import heapq
import utils
from const import *
def UCS(arr2D, start, end):
    def getCost(before, next):
        if before[0] != next[0] and before[1] != next[1]:
            return 1.5
        else: return 1
    if start == end:
        return None
    if arr2D[start[0]][start[1]] not in utils.VALID_VALUES_GHOST  or arr2D[end[0]][end[1]] not in  utils.VALID_VALUES_GHOST  or utils.ghost_status[start[0]][start[1]] == 1 or utils.ghost_status[start[1]][end[1]] == 1:
        return None
    
    rows, cols = len(arr2D), len(arr2D[0])
    queue = []  
    visited = []
    heapq.heappush(queue, (0, start, [tuple(start)], start)) 

    while queue:
        min_cost, now, path, before = heapq.heappop(queue)  # Lấy phần tử có cost nhỏ nhất
        if tuple(now) == tuple(end):
            return path
        visited.append(now)
        dir = DIRECTIONS
        for d in dir:
             node = tuple((now[0] + d[0], now[1] + d[1]))
             if 0 <= node[0] < rows and 0 <= node[1] < cols and node not in visited:
                if arr2D[node[0]][node[1]] in utils.VALID_VALUES_GHOST  and utils.ghost_status[node[0]][node[1]] == 0:
                    heapq.heappush(queue,(getCost(before, node) + min_cost,node, path + [node], now) )

    return None