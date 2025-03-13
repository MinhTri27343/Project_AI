import heapq
import utils
from const import *

def UCS(arr2D, start, end):
    def getCost(before, next):
        if before[0] != next[0] and before[1] != next[1]:
            return 1.5
        return 1

    if start == end:
        return None, 0, "UCS"

    if arr2D[start[0]][start[1]] not in utils.VALID_VALUES_GHOST or \
       arr2D[end[0]][end[1]] not in utils.VALID_VALUES_GHOST or \
       utils.ghost_status[start[0]][start[1]] == 1 or \
       utils.ghost_status[end[0]][end[1]] == 1:
        return None, 0, "UCS"

    rows, cols = len(arr2D), len(arr2D[0])
    queue = []  
    visited = set()
    heapq.heappush(queue, (0, start, [tuple(start)], start))  
    expanded_nodes = 0  # Biến đếm số node đã mở rộng

    while queue:
        min_cost, now, path, before = heapq.heappop(queue)  # Lấy phần tử có cost nhỏ nhất

        if tuple(now) == tuple(end):
            return path, expanded_nodes, "UCS"

        if tuple(now) in visited:
            continue

        visited.add(tuple(now))
        expanded_nodes += 1  # Đếm số node mở rộng

        for d in DIRECTIONS:
            node = (now[0] + d[0], now[1] + d[1])
            if 0 <= node[0] < rows and 0 <= node[1] < cols and tuple(node) not in visited:
                if arr2D[node[0]][node[1]] in utils.VALID_VALUES_GHOST and utils.ghost_status[node[0]][node[1]] == 0:
                    heapq.heappush(queue, (getCost(before, node) + min_cost, node, path + [node], now))

    return None, expanded_nodes, "UCS"  # Trả về None nếu không tìm thấy đường đi