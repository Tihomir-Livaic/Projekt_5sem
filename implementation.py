
import heapq
import string


def find_neighbors(node: tuple, nodes: list, max_row: int, max_col: int) -> list:
    neighbors = []
    row,col = node
    if (row+1 < max_row and nodes[row+1][col]!=0):
        neighbors.append((row+1,col))
    if (row-1 >= 0 and nodes[row-1][col]!=0):
        neighbors.append((row-1,col))
    if (col+1 < max_col and nodes[row][col+1]!=0):
        neighbors.append((row,col+1))
    if (col-1 >= 0 and nodes[row][col-1]!=0):
        neighbors.append((row,col-1))
    return neighbors

def heuristic(current: tuple, end: tuple):

    return 0

def dijkstra(nodes: list, start:tuple, end:tuple, max_row: int, max_col: int , window):
    hq = []
    heapq.heappush(hq, (0, (start, 1)))
    came_from: dict[tuple, tuple] = {}
    cost: dict[tuple, float] = {}
    #came_from[start] = None
    cost[start] = 0
    colors: dict[int, string] = {}
    colors[1]="#FFE5B4"
    colors[2]="#FFD8A8"
    colors[3]="#FFCC99"
    colors[4]="#FFC085"
    colors[5] = "#FFB570"
    colors[6] = "#FFA95A"
    colors[7] = "#FF9E45"
    colors[8] = "#FF922F"
    colors[9] = "#FF871A"
    colors[10] = "#FF7B05"
    colors[11] = "#F36F05"
    colors[12] = "#E76405"
    colors[13] = "#DB5905"
    colors[14] = "#CF4E05"
    colors[15] = "#C34405"
    colors[16] = "#B73905"
    colors[17] = "#AB2F05"
    colors[18] = "#9F2405"
    colors[19] = "#931905"
    colors[20] = "#870F05"





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
        #color+=1
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
