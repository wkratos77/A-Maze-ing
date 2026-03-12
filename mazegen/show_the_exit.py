from collections import deque


def find_the_way(mg):
    start = mg.entry
    goal = mg.exit

    queue = deque([start])
    visited = {start}
    parent = {start: None}

    # North=1, East=2, South=4, West=8
    directions = [
        (0, -1, 1),
        (1, 0, 2),
        (0, 1, 4),
        (-1, 0, 8)
    ]

    while queue:
        curr_x, curr_y = queue.popleft()

        if (curr_x, curr_y) == goal:
            path = []
            temp = goal
            while temp is not None:
                path.append(temp)
                temp = parent[temp]  # move to the parent
            return path[::-1]  # reverse the path start to exit
        # the path was reversed from the deque so we reversed back
        for dx, dy, mask in directions:
            nx, ny = curr_x + dx, curr_y + dy

            if 0 <= nx < mg.width and 0 <= ny < mg.height:
                # in the current coord if there is no wall we pass
                if not (mg.grid[curr_y][curr_x] & mask):
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (curr_x, curr_y)
                        queue.append((nx, ny))
    return None


# def print_maze_with_path(mg, path):
#     path_set = set(path) if path else set()

#     for y in range(mg.height):
#         # 1. Print North walls
#         line_n = ""
#         for x in range(mg.width):
#             line_n += "+---" if (mg.grid[y][x] & 1) else "+   "
#         print(line_n + "+")

#         # 2. Print Side walls and the Path
#         line_c = ""
#         for x in range(mg.width):
#             # Check if this cell is part of the path
#             if (x, y) in path_set:
#                 mark = "."  # This is a step on the path
#             elif (x, y) == mg.entry or (x, y) == mg.exit:
#                 mark = "*"
#             else:
#                 mark = " "

#             if (mg.grid[y][x] & 8):  # West wall
#                 line_c += f"| {mark} "
#             else:
#                 line_c += f"  {mark} "
#         print(line_c + "|")

#     print("+---" * mg.width + "+")
