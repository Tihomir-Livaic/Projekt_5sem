import heapq
import string
import time
from PySimpleGUI import timer_start, timer_stop_usec


def create_orange_color_dict(no_of_colors: int) -> dict[int, string]:
    colors: dict[int, string] = {}
    no_of_loops = round(no_of_colors/33)
    index = 1
    for loops in range(no_of_loops):
        G = 30
        colors[index] = "#ff0000"
        index += 1
        colors[index] = "#ff0f00"
        index += 1
        for i in range(1, 17):
            colors[index] = "#ff" + str(hex(G)[2:]) + "00"
            index += 1
            G += 15

        R = 240
        for i in range(1, 16):
            colors[index] = "#" + str(hex(R)[2:]) + "ff00"
            index += 1
            R -= 15
        colors[index] = "#0fff00"
        index += 1
        colors[index] = "#00ff00"
        index += 1
        colors[index] = "#0fff00"
        index += 1
        R += 15
        for i in range(1,17):
            colors[index] = "#" + str(hex(R)[2:]) + "ff00"
            index += 1
            R += 15
        G = 240
        for i in range(1, 16):
            colors[index] = "#ff" + str(hex(G)[2:]) + "00"
            index += 1
            G -= 15
        colors[index] = "#ff0f00"

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
    return neighbors

#def heuristic(current: tuple, end: tuple):
#
#    return 0

def graph_search(nodes: list, start:tuple, end:tuple, max_row: int, max_col: int, window):
    hq = []
    heapq.heappush(hq, (0, (start, 1)))
    came_from: dict[tuple, tuple] = {}
    cost: dict[tuple, float] = {start: 0}
    window[start].update("START")
    window[end].update("STOP")
    window.refresh()
    nodes_colors: list[tuple] = []
    timer_start()

    while len(hq)>0:
        elem = heapq.heappop(hq)[1]
        current, color = elem

        if current == end:
            break

        neighbors: list = find_neighbors(current, nodes, max_row, max_col)
        nodes_colors.append((current, neighbors, color))
        for neighbor in neighbors:
            new_cost = cost[current] + nodes[neighbor[0]][neighbor[1]]      #moze se dogoditi da se doda vec postojeci node
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(hq, (priority, (neighbor,color+1)))
                came_from[neighbor] = current

    vrijeme_izvodenja = timer_stop_usec()
    window['-VRIJEME-'].update("Vrijeme izvođenja: " + str(vrijeme_izvodenja) + "ms")
    window['-VRIJEME-'].update(visible = True)
    path = reconstruct_path(came_from, start, end)
    return nodes_colors, color, path

def color_graph(nodes_colors: list, no_of_colors: int, path: list, window):
    colors = create_orange_color_dict(no_of_colors)
    for elem in nodes_colors:
        neighbors = elem[1]
        color = elem[2]
        for neighbor in neighbors:
            window[neighbor].update(button_color=("black", colors[color]))
    for node in path:
        window[node].update(button_color=("black", "green"))

def color_graph_pausable(nodes_colors: list, no_of_colors: int, path: list, window):
    window['-PAUSE-'].update(visible=True)
    window['-FINISH-'].update(visible=True)
    is_paused = False
    finish = False
    colors = create_orange_color_dict(no_of_colors)
    for elem in nodes_colors:
        while is_paused:
            event, values = window.read(timeout=10)
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
        time.sleep(0.25 if not finish else 0)
        for neighbor in neighbors:
            window[neighbor].update(button_color=("black", colors[color]))
        window.refresh()
        time.sleep(0.25 if not finish else 0)

        if not finish:
            event, values = window.read(timeout=10)
            if event == '-FINISH-':
                window['-PAUSE-'].update(visible=False)
                window['-FINISH-'].update(visible=False)
                finish = True
            elif event == '-PAUSE-':
                is_paused = True
                window['-PAUSE-'].update("Resume")
            else:
                window[node].update(button_color=("black", node_color))
        else:
            window[node].update(button_color=("black", node_color))
    for node in path:
        window[node].update(button_color=("black", "green"))

def reconstruct_path(came_from: dict[tuple, tuple], start: tuple, end: tuple) -> list:
    path = []
    node = end
    path.append(node)
    while node != start:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path
