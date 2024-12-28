import heapq
import itertools
import math
import string
import time
import random
import PySimpleGUI as sg



def create_orange_color_dict(no_of_colors: int) -> dict[int, string]:
    colors: dict[int, string] = {}
    no_of_loops = math.ceil(no_of_colors/36)
    index = 1
    for loops in range(no_of_loops):
        g = 30
        colors[index] = "#ff0000"
        index += 1
        for i in range(8):
            colors[index] = "#ff" + str(hex(g)[2:]) + "00"
            index += 1
            g += 30
        colors[index] = "#ffff00"
        index += 1
        r = 240
        for i in range(8):
            colors[index] = "#" + str(hex(r)[2:]) + "ff00"
            index += 1
            r -= 30
        colors[index] = "#00ff00"
        index += 1
        r += 30
        for i in range(8):
            colors[index] = "#" + str(hex(r)[2:]) + "ff00"
            index += 1
            r += 30
        g = 240
        colors[index] = "#ffff00"
        index += 1
        for i in range(8):
            colors[index] = "#ff" + str(hex(g)[2:]) + "00"
            index += 1
            g -= 30

    return colors

def find_neighbors(node: tuple, nodes: list, max_row: int, max_col: int) -> list:
    neighbors = []
    row,col = node
    if row+1 < max_row and nodes[row + 1][col]!=0:
        neighbors.append((row+1,col))
    if row-1 >= 0 and nodes[row - 1][col]!=0:
        neighbors.append((row-1,col))
    if col+1 < max_col and nodes[row][col + 1]!=0:
        neighbors.append((row,col+1))
    if col-1 >= 0 and nodes[row][col - 1]!=0:
        neighbors.append((row,col-1))
    random.shuffle(neighbors)
    return neighbors

def heuristic(current: tuple, end: tuple, min_distance: int) -> float:       #početna jednostavna heuristika
    dx = abs(current[0] - end[0])
    dy = abs(current[1] - end[1])
    return min_distance * (dx + dy)


def find_min_distance(nodes: list, rows: int, columns: int) -> int:
    d = 10
    for row in range(rows):
        for col in range(columns):
            if nodes[row][col] < d and nodes[row][col] != 0:
                d = nodes[row][col]
    return d

def graph_search(nodes: list, start:tuple, end:tuple, max_row: int, max_col: int, coefficient, window) -> tuple:
    #print(coefficient)
    min_distance = find_min_distance(nodes, max_row, max_col)
    h: int
    g: int
    if coefficient < 0:
        g = 1
        h = round(1 + coefficient, 1)
    elif coefficient > 0:
        h = 1
        g = round(1 - coefficient, 1)
    else:
        g = h = 1
    #print(g, " ", h)

    hq = []
    counter = itertools.count()
    count = next(counter)
    heapq.heappush(hq, [0, count, (start, 1)])
    came_from: dict[tuple, tuple] = {}
    cost: dict[tuple, float] = {start: 0}
    window[start].update("START")
    window[end].update("STOP")
    window.refresh()
    nodes_colors: list[tuple] = []
    found_path = False
    start_time = time.perf_counter()

    while len(hq)>0:
        elem = heapq.heappop(hq)[2]
        current, color = elem

        if current == end:
            found_path = True
            break

        neighbors: list = find_neighbors(current, nodes, max_row, max_col)
        neighbors_to_color = []
        #nodes_colors.append((current, neighbors, color))
        for neighbor in neighbors:
            new_cost = cost[current] + nodes[neighbor[0]][neighbor[1]]      #moze se dogoditi da se doda vec postojeci node
            if neighbor not in cost or new_cost < cost[neighbor]:
                neighbors_to_color.append(neighbor)
                cost[neighbor] = new_cost
                priority = g * new_cost + h * heuristic(neighbor, end, min_distance)
                count = next(counter)
                heapq.heappush(hq, [priority, count, (neighbor,color+1)])
                came_from[neighbor] = current
        nodes_colors.append((current, neighbors_to_color, color))

    stop_time = time.perf_counter()
    path = None
    if found_path:
        window['-VRIJEME-'].update("Vrijeme izvođenja: " + str((stop_time - start_time) * 1000) + "ms")
        window['-VRIJEME-'].update(visible = True)
        path = reconstruct_path(came_from, start, end)
    return nodes_colors, color, found_path, path

def color_graph(nodes_colors: list, no_of_colors: int, path: list, window):
    colors = create_orange_color_dict(no_of_colors)
    for elem in nodes_colors:
        neighbors = elem[1]
        color = elem[2]
        for neighbor in neighbors:
            window[neighbor].update(button_color=("black", colors[color]))
    for node in path:
        window[node].update(button_color=("black", "green"))

def color_graph_pausable(nodes_colors: list, no_of_colors: int, path: list, window) -> bool:
    window['-PAUSE-'].update(visible=True)
    window['-FINISH-'].update(visible=True)
    is_paused = False
    finish = False
    should_exit = False
    colors = create_orange_color_dict(no_of_colors)
    for elem in nodes_colors:
        while is_paused:
            event, values = window.read(timeout=10)
            if event == sg.WIN_CLOSED:
                should_exit = True
                return should_exit
            if event == '-PAUSE-':
                is_paused = False
                window['-PAUSE-'].update("Pause")
                window[node].update(button_color=("black", node_color))
            if event == '-FINISH-':
                window['-PAUSE-'].update(visible=False)
                window['-FINISH-'].update(visible=False)
                is_paused = False
                finish = True

        node, neighbors, color = elem
        node_color = window[node].ButtonColor[1]
        window[node].update(button_color=("black", "blue"))
        window.refresh()
        time.sleep(1 if not finish else 0)
        for neighbor in neighbors:
            window[neighbor].update(button_color=("black", colors[color]))
        window.refresh()
        time.sleep(1 if not finish else 0)

        if not finish:
            event, values = window.read(timeout=10)
            if event == sg.WIN_CLOSED:
                should_exit = True
                return should_exit
            if event == '-FINISH-':
                window['-PAUSE-'].update(visible=False)
                window['-FINISH-'].update(visible=False)
                finish = True
            elif event == '-PAUSE-':
                is_paused = True
                window['-PAUSE-'].update("Resume")

        window[node].update(button_color=("black", node_color))
        window.refresh()
        time.sleep(1 if not finish else 0)
    for node in path:
        window[node].update(button_color=("black", "green"))
    return should_exit

def reconstruct_path(came_from: dict[tuple, tuple], start: tuple, end: tuple) -> list:
    path = []
    node = end
    path.append(node)
    while node != start:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path
