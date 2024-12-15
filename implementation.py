import heapq
import string
#import time
from PySimpleGUI import timer_start, timer_stop_usec


def create_orange_color_dict() -> dict[int, string]:
    colors: dict[int, string] = {}
    hex_code = "0xFFF000"
    print(int(hex_code, 16))
    for i in range (1, 41):
        colors[i] = "#" + hex_code[2:]
        hex_code = hex(int(hex_code, 16) - 1024)

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

def heuristic(current: tuple, end: tuple):

    return 0

def dijkstra(nodes: list, start:tuple, end:tuple, max_row: int, max_col: int, window):
    hq = []
    heapq.heappush(hq, (0, (start, 1)))
    came_from: dict[tuple, tuple] = {}
    cost: dict[tuple, float] = {}
    #came_from[start] = None
    cost[start] = 0
    colors = create_orange_color_dict()

    timer_start()

    while len(hq)>0:
        #current: tuple = heapq.heappop(hq)[1]
        elem = heapq.heappop(hq)[1]
        current, color = elem

        if current == end:
            break

        neighbors: list = find_neighbors(current, nodes, max_row, max_col)
        for neighbor in neighbors:
            new_cost = cost[current] + nodes[neighbor[0]][neighbor[1]]      #moze se dogoditi da se doda vec postojeci node
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(hq, (priority, (neighbor,color+1)))
                came_from[neighbor] = current
                #print(colors[color], " ", type(colors[color]))
                window[neighbor].update(button_color=("black", colors[color]))

    window['-VRIJEME-'].update("Vrijeme izvođenja: " + str(timer_stop_usec()/1000000) + "s")
    window['-VRIJEME-'].update(visible = True)
    reconstruct_path(came_from, start, end, window)

def reconstruct_path(came_from: dict[tuple, tuple], start: tuple, end: tuple, window):
    path = []
    node = end
    path.append(node)
    while node != start:
        node = came_from[node]
        path.append(node)
    path.reverse()
    for node in path:
        window[node].update(button_color=("black", "green"))
