import queue
from collections import deque
import heapq
from queue import PriorityQueue
from ghost_status import ghost_status
def UCS(arr2D, start, end):
    def getCost(before, next):
        if before[0] != next[0] and before[1] != next[1]:
            return 1.5
        else: return 1
    if start == end:
        return None
    if( arr2D[end[0]][end[1]] not in {0, 1, 2, 9} and arr2D[start[0]][start[1]] not in {0, 1, 2, 9} ):
        return 
    rows, cols = len(arr2D), len(arr2D[0])
    queue = []  
    visited = []
    heapq.heappush(queue, (0, start, [tuple(start)], start)) 

    while queue:
        min_cost, now, path, before = heapq.heappop(queue)  # Lấy phần tử có cost nhỏ nhất
        if tuple(now) == tuple(end):
            return path
        visited.append(now)
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in dir:
             node = tuple((now[0] + d[0], now[1] + d[1]))
             if 0 <= node[0] < rows and 0 <= node[1] < cols and node not in visited:
                if arr2D[now[0] + d[0]][now[1] + d[1]] in {0, 1, 2, 9}:
                    heapq.heappush(queue,(getCost(before, node) + min_cost,node, path + [node], now) )

    
    return None

#=====================================================================================================================
queue_max = deque(maxlen = 2)
def IDS(arr2D, start, end):
    def DLS(arr2D, start, end, max_depth):
        stack = [(start, [tuple(start)], 0)]  #[now , path, depth]
        visited = set() 
        visited.add(tuple(start))
        if end in queue_max:
            return None
        while stack:
            now, path, depth = stack.pop()

            if tuple(now) == tuple(end):
                return path
            
            if depth < max_depth:
                
                visited.add(tuple(now))
                dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for d in dir:
                    node = tuple((now[0] + d[0], now[1] + d[1]))
                    if 0 <= node[0] < rows and 0 <= node[1] < cols and node not in visited and node not in queue_max:
                        if arr2D[now[0] + d[0]][now[1] + d[1]] in {0, 1, 2, 9} and ghost_status[now[0] + d[0]][now[1] + d[1]] == 0:
                            stack.append((node, path + [(node)], depth + 1))
        return None


    if start == end:
        return None
    if( arr2D[end[0]][end[1]] not in {0, 1, 2, 9} or arr2D[start[0]][start[1]] not in {0, 1, 2, 9} or ghost_status[end[0]][end[1]] == 1 or ghost_status[start[0]][start[1]] == 1):
        return None
    rows, cols = len(arr2D), len(arr2D[0])
    
     
    depth = 0
    depth_limit = rows*cols
   
    while depth <= depth_limit:
        result = DLS(arr2D, start, end, depth)
        if result != None:
            return result
        depth += 1
    
    
    return None

def bfs(matrix, start, end):
    row_start, col_start = start
    row_end, col_end = end
    rows, cols = len(matrix), len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải
    
    # Kiểm tra nếu điểm bắt đầu hoặc kết thúc không thể đi được
    if matrix[row_start][col_start] in range(2, 9) or matrix[row_end][col_end] in range(2, 9):
        return None
    
    queue = deque([(row_start, col_start, [])])
    visited = set()
    visited.add((row_start, col_start))
    while queue:
        x, y, path = queue.popleft()
        
        # Nếu đến đích, trả về đường đi
        if (x, y) == (row_end, col_end):
            return path + [(x, y)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                if matrix[nx][ny] in (0, 1, 9):  # Chỉ đi được nếu là 0, 1 hoặc 9
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(x, y)]))
    
    return None  # Không tìm thấy đường đi
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
    if grid[start[0]][start[1]] in range(3, 9) or grid[end[0]][end[1]] in range(3, 9) or ghost_status[start[0]][start[1]] == 1 or ghost_status[end[0]][end[1]] == 1:
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
            
            if 0 <= new_x < row and 0 <= new_y < col and not visited[(new_x, new_y)] and grid[new_x][new_y] in (0, 1, 2, 9) and ghost_status[new_x][new_y] == 0:
                new_cost = 0
                if parent and parent[(x, y)][0] != new_x and parent[(x, y)][1] != new_y:
                    new_cost = cost[current_index] + 1.5
                else:
                    new_cost = cost[current_index] + 1
                if (new_x, new_y) not in cost or new_cost < cost[(new_x, new_y)]:
                    cost[(new_x, new_y)] = new_cost
                    priority = new_cost + Heuristic((new_x, new_y), end)
                    queue.put((priority, (new_x, new_y)))
                    parent[(new_x, new_y)] = current_index
    
    return None
board = [
    [0, 0, 3, 0, 0],
    [3, 0, 3, 3, 3],
    [3, 0, 0, 0, 0],
    [0, 0, 3, 3, 0],
    [0, 0, 0, 0, 0]
]
start = (0, 0)
end = (4, 4)
print(AStar2(board, start, end))