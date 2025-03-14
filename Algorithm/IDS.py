import utils
from collections import deque
from const import *
queue_max = deque(maxlen= 10)
def IDS(arr2D, start, end):
    def DLS(arr2D, start, end, max_depth):
        stack = [(start, [tuple(start)], 0)]  #[now , path, depth]
        visited = set() 
        depth = {start : 0}
        # visited.add(tuple(start))
        expand_nodes = 0
        if end in queue_max:
             return None, expand_nodes
        while stack:
            now, path, dep = stack.pop()
            expand_nodes += 1
            if tuple(now) == tuple(end):
                return path, expand_nodes
            # print(queue_max)
            if dep < max_depth:
                visited.add(tuple(now))
                dir = DIRECTIONS
                for d in dir:
                    node = tuple((now[0] + d[0], now[1] + d[1]))
                    if 0 <= node[0] < rows and 0 <= node[1] < cols and (node not in visited or dep + 1 < depth.get(node, float('inf'))) and node not in queue_max:
                    # if 0 <= node[0] < rows and 0 <= node[1] < cols and (node not in visited or dep + 1 < depth.get(node, float('inf'))):
                        if arr2D[node[0]][node[1]] in utils.VALID_VALUES_GHOST  and utils.ghost_status[node[0]][node[1]] == 0:
                            stack.append((node, path + [(node)], dep + 1))
                            depth[node] = dep + 1
        return None, expand_nodes

    if start == end:
        return None, 0, "IDS"
    if arr2D[start[0]][start[1]] not in utils.VALID_VALUES_GHOST  or arr2D[end[0]][end[1]] not in utils.VALID_VALUES_GHOST or utils.ghost_status[start[0]][start[1]] == 1 or utils.ghost_status[end[0]][end[1]] == 1:
        return None, 0, "IDS"
    rows, cols = len(arr2D), len(arr2D[0]) 
    depth = 0
    depth_limit = rows * cols
    if utils.isUseLargeDepth == True:
        depth_limit = LARGE_DEPTH_IDS
    total_expanded_nodes = 0
   
    while depth <= depth_limit:
        result, expand_nodes = DLS(arr2D, start, end, depth)
        total_expanded_nodes += expand_nodes
        if result != None:
            # print(result)
            return result, total_expanded_nodes, "IDS"
        depth += SMALL_DEPTH_IDS if utils.isUseLargeDepth == False else LARGE_DEPTH_IDS  
    return None,total_expanded_nodes, "IDS"