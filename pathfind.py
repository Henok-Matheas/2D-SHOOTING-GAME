from gameWall import walls
import heapq
import math

# left, right, up, down, left_up, left_down, right_up, right_down
DIRECTIONS = [[-1, 0], [1, 0], [-1, 0],
              [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]


def valid(x, y, WIDTH, HEIGHT):
    if not (0 < x < WIDTH and 0 < y < HEIGHT):
        return False
    for wall in walls:
        if wall.x <= x <= wall.x + wall.width and wall.y <= y <= wall.y + wall.height:
            return False
    return True


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def path_find(enemy, fire_x, fire_y, WIDTH, HEIGHT):
    WEIGHT = 1
    heap = [(WEIGHT + distance(enemy.x, enemy.y,
             fire_x, fire_y), WEIGHT, fire_x, fire_y)]
    best_parent = {}
    visited = set([(fire_x, fire_y)])
    if (enemy.x, enemy.y) == (fire_x, fire_y):
        return []

    # best_parent[(row, column)] = (
    #     parent_row, parent_column) if (row, column) not in best_parent or weight <= best_weight[edge.right.name] else best_parent[edge.right.name]

    while heap:
        heuristic, weight, row, column = heapq.heappop(heap)
        if (row, column) == (enemy.x, enemy.y):
            break

        for row_man, col_man in DIRECTIONS:
            new_row, new_column = row + row_man, column + col_man

            if not valid(new_row, new_column, WIDTH, HEIGHT) or (new_row, new_column) in visited:
                continue

            best_parent[(new_row, new_column)] = (row, column, weight + WEIGHT) if (new_row,
                                                                                    new_column) not in best_parent or weight + WEIGHT < best_parent[(new_row, new_column)][2] else best_parent[(new_row, new_column)]
            visited.add((new_row, new_column))
            heap.add((weight + distance(new_row, new_column, enemy.x,
                     enemy.y), weight + WEIGHT, new_row, new_column))

    path = []
    curr = (enemy.x, enemy.y)
    path.append(curr)
    if (enemy.x, enemy.y) not in best_parent:
        return []
    while curr != (fire_x, fire_y):
        curr_x, curr_y, weight = best_parent[curr]
        curr = (curr_x, curr_y)
        path.append(curr)
    return path
