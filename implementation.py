
import heapq


def find_neighbors(node: tuple, nodes: list, max_row: int, max_col: int) -> list:
    neighbors = []
    row = node[0]
    col = node[1]
    if (row+1 < max_row and nodes[row+1][col]!=0):
        neighbors.append((row+1,col))
    if (row-1 >= 0 and nodes[row-1][col]!=0):
        neighbors.append((row,col+1))
    if (col+1 < max_col and nodes[row][col+1]!=0):
        neighbors.append((row,col+1))
    if (col-1 >= 0 and nodes[row][col-1]!=0):
        neighbors.append((row,col-1))
    return neighbors

def heuristic(current: tuple, end: tuple):

    return 0

def dijkstra(nodes: list, start:tuple, end:tuple, max_row: int, max_col: int , window):
    hq = []
    heapq.heappush(hq, (0, start))
    came_from: dict[tuple, tuple] = {}
    cost: dict[tuple, float] = {}
    #came_from[start] = None
    cost[start] = 0

    while len(hq)>0:
        current: tuple = heapq.heappop(hq)

        if current == end:
            break

        neighbors: list = find_neighbors(current, nodes, max_row, max_col)
        for neighbor in neighbors:
            new_cost = cost[current] + nodes[neighbor[0]][neighbor[1]]      #moze se dogoditi da se doda vec postojeci node
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(hq, (priority, neighbor))
                came_from[neighbor] = current
                window[neighbor].update(button_color=("black", "orange"))
                print("OVDJE")
    print("KRAJ DIJKSTRE")
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
