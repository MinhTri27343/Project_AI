import utils
from collections import deque
queue_max = deque(maxlen= 5)
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
                        if arr2D[node[0]][node[1]] in {0, 1, 2, 9}  and utils.ghost_status[node[0]][node[1]] == 0:
                            stack.append((node, path + [(node)], depth + 1))
        return None


    if start == end:
        return None
    if arr2D[start[0]][start[1]] not in utils.VALID_VALUES_GHOST  or arr2D[end[0]][end[1]] not in    utils.VALID_VALUES_GHOST  or utils.ghost_status[start[0]][start[1]] == 1 or utils.ghost_status[start[1]][end[1]] == 1:
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
   