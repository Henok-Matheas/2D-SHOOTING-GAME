import pygame
from gameWall import walls
import heapq
import math
from M import VEL, WIDTH, HEIGHT
from collections import defaultdict

# left, right, up, down, left_up, left_down, right_up, right_down
dirc = [[0, VEL], [VEL, 0], [VEL,VEL], [-VEL, -VEL], [0,-VEL],[-VEL,0],[-VEL, VEL], [VEL, -VEL]]

def heuristic(cur, tar):
    return abs(math.sqrt((cur[0]-tar[0])**2+(cur[1]-tar[1])**2))
def retrace(start, paths):

        cur = start
        path = []

        while cur != None:
            path.append(cur) 
            cur = paths[cur][0]
             
        return path
        
def findPath( start, end, width, height):
    #radius in miles

    if start.x < 0:
        start.x = 0
    if start.y < 0:
        start.y = 0
    collide = False
    for i in walls:
       
        if i.rect.colliderect(start):
            collide = True
            break
    if collide:
        start.x += 20
        start.y += 20

    paths = defaultdict(list)

    heap = [[0,0, (start.x, start.y), None]]
    
    visited = set()
    while heap:
        
        current = heapq.heappop(heap)
        if current[2] not in paths or paths[current[2]][1] > current[1]:
            paths[current[2]] = [current[3], current[1]]
        visited.add(current[2])

        if abs(end.x -current[2][0]) < 20 and abs(end.y -current[2][1]) < 20:
            return retrace(current[2], paths)

        for d in dirc:
            new = (current[2][0]+d[0] , current[2][1]+d[1])
            if new not in visited and new[0] >= 0 and new[0] <= WIDTH and new[1] >= 0 and new[1] <= HEIGHT:
                iscollide = False
                visited.add(new)
                for i in walls:
                    pos = pygame.Rect(new[0], new[1], 20,20)
                    if i.rect.colliderect(pos):
                        iscollide = True
                        break
                if not iscollide:
                    heapq.heappush(heap, [current[1] + VEL + 
                    heuristic(new, end.topleft), current[1] + VEL , 
                    new, current[2]])
            

    return []

# def valid(x, y, WIDTH, HEIGHT):
#     if not (0 < x < WIDTH and 0 < y < HEIGHT):
#         return False
#     for wall in walls:
#         if wall.x <= x <= wall.x + wall.width and wall.y <= y <= wall.y + wall.height:
#             return False
#     return True


# def distance(x1, y1, x2, y2):
#     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# def path_find(enemy, fire_x, fire_y, WIDTH, HEIGHT):
#     WEIGHT = 1
#     heap = [(WEIGHT + distance(enemy.x, enemy.y,
#              fire_x, fire_y), WEIGHT, fire_x, fire_y)]
#     best_parent = {}
#     visited = set([(fire_x, fire_y)])
#     if (enemy.x, enemy.y) == (fire_x, fire_y):
#         return []

#     # best_parent[(row, column)] = (
#     #     parent_row, parent_column) if (row, column) not in best_parent or weight <= best_weight[edge.right.name] else best_parent[edge.right.name]

#     while heap:
#         heuristic, weight, row, column = heapq.heappop(heap)
#         if (row, column) == (enemy.x, enemy.y):
#             break

#         for row_man, col_man in DIRECTIONS:
#             new_row, new_column = row + row_man, column + col_man

#             if not valid(new_row, new_column, WIDTH, HEIGHT) or (new_row, new_column) in visited:
#                 continue

#             best_parent[(new_row, new_column)] = (row, column, weight + WEIGHT) if (new_row,
#                                                                                     new_column) not in best_parent or weight + WEIGHT < best_parent[(new_row, new_column)][2] else best_parent[(new_row, new_column)]
#             visited.add((new_row, new_column))
#             heap.add((weight + distance(new_row, new_column, enemy.x,
#                      enemy.y), weight + WEIGHT, new_row, new_column))

#     path = []
#     curr = (enemy.x, enemy.y)
#     path.append(curr)
#     if (enemy.x, enemy.y) not in best_parent:
#         return []
#     while curr != (fire_x, fire_y):
#         curr_x, curr_y, weight = best_parent[curr]
#         curr = (curr_x, curr_y)
#         path.append(curr)
#     return path
