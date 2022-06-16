from gameWall import walls
import heapq
import math

VEL = 5
# left, right, up, down, left_up, left_down, right_up, right_down
DIRECTIONS = [[-VEL, 0], [VEL, 0], [-VEL, 0],
              [VEL, 0], [-VEL, -VEL], [-VEL, VEL], [VEL, -VEL], [VEL, VEL]]


FOUND_RADIUS = 10


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
    fire_x = int(fire_x)
    fire_y = int(fire_y)
    heap = [(WEIGHT + distance(enemy.x, enemy.y,
             fire_x, fire_y), WEIGHT, enemy.x, enemy.y)]
    best_parent = {}
    visited = set([(enemy.x, enemy.y)])
    if (fire_x, fire_y) == (enemy.x, enemy.y):
        return []

    last = None
    while heap:
        heuristic, weight, row, column = heapq.heappop(heap)
        # if (row, column) == (fire_x, fire_y):
        #     print("found")
        #     break

        if abs(row - fire_x) <= FOUND_RADIUS and abs(column - fire_y) <= FOUND_RADIUS:
            last = (row, column)
            break

        for row_man, col_man in DIRECTIONS:
            new_row, new_column = row + row_man, column + col_man

            if not valid(new_row, new_column, WIDTH, HEIGHT) or (new_row, new_column) in visited:
                continue

            best_parent[(new_row, new_column)] = (row, column, weight + WEIGHT) if (new_row,
                                                                                    new_column) not in best_parent or weight + WEIGHT < best_parent[(new_row, new_column)][2] else best_parent[(new_row, new_column)]
            visited.add((new_row, new_column))
            heapq.heappush(heap, (weight + distance(new_row, new_column, enemy.x,
                                                    enemy.y), weight + WEIGHT, new_row, new_column))

    path = []
    # curr = (fire_x, fire_y)
    # if (fire_x, fire_y) not in best_parent:
    #     print("not in best paretn")
    #     return []

    curr = last
    if curr not in best_parent:
        return
    while curr != (enemy.x, enemy.y):
        curr_x, curr_y, weight = best_parent[curr]
        curr = (curr_x, curr_y)
        path.append(curr)
    return path
