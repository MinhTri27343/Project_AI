from queue import PriorityQueue
import utils
def Heuristic(start, end):
    return abs(end[1] - start[1]) + abs(end[0] - start[0])


def AStar(grid, start, end):
    row, col = len(grid), len(grid[0])
    visited = {(x, y): False for x in range(row) for y in range(col)}
    path = []
    queue = PriorityQueue()
    parent = {}
    cost = {}
    direction = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    if grid[start[0]][start[1]] not in utils.VALID_VALUES_GHOST or grid[end[0]][end[1]] not in utils.VALID_VALUES_GHOST or utils.ghost_status[start[0]][start[1]] == 1 or utils.ghost_status[end[0]][end[1]] == 1:
        return None
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
            
            if 0 <= new_x < row and 0 <= new_y < col and not visited[(new_x, new_y)] and grid[new_x][new_y] in (0, 1, 2, 9) and utils.ghost_status[new_x][new_y] == 0:
                new_cost = 0
                if parent.get((x, y)) and parent[(x, y)][0] != new_x and parent[(x, y)][1] != new_y:
                    new_cost = cost[current_index] + 1.5
                else:
                    new_cost = cost[current_index] + 1
                if (new_x, new_y) not in cost or new_cost < cost[(new_x, new_y)]:
                    cost[(new_x, new_y)] = new_cost
                    priority = new_cost + Heuristic((new_x, new_y), end)
                    queue.put((priority, (new_x, new_y)))
                    parent[(new_x, new_y)] = current_index
    
    return None