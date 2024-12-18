#import string
import json
import PySimpleGUI as sg

from search_functions import *

def disable_enable(windows, disabled, *args):
    for arg in args:
        windows[arg].update(disabled=disabled)

def create_blue_color_dict():
    colors: dict[int, string] = {1: "#283B5B", 2: "#243655", 3: "#21324F", 4: "#1E2E4A", 5: "#1A2944", 6: "#17253E",
                                 7: "#142139", 8: "#101C33", 9: "#0D182D", 10: "#0A1428"}

    return colors

# inicijalizacija globalnih varijabli
DODAVANJE_ZIDOVA = False
DODAVANJE_ELEVACIJE = False
BIRANJE_POCETKA = False
BIRANJE_KRAJA = False
start = end = (-1, -1)
elevation = 1
color_dict = create_blue_color_dict()
COL_COUNT = 25
ROW_COUNT = 15
nodes = [[1 for _ in range(COL_COUNT)] for _ in range(ROW_COUNT)]
#

menu_def = [['File', ['Load map', 'Save map']], ['Help']]

layout = [[sg.Menu(menu_def, key="-MENU-")]]
layout += [[sg.Text("UREĐIVANJE MAPE: "), sg.Button("Dodavanje zidova", key='-DZ-'),
           sg.VerticalSeparator(),
           sg.Text("ELEVACIJA POLJA: "),
           sg.Slider(range=(1, 10), resolution=1, orientation='h', key='-ES-', enable_events=True),
           sg.Button("Dodaj elevaciju", key='-DE-')]]
column = [[sg.Text("Dijkstra            A*      Greedy BFS")],
          [sg.Slider((-1,1), resolution=0.1, orientation='h', disable_number_display=True, key='-COEFFICIENT-', disabled=True)]]
layout += [[sg.Text("KONFIGURACIJA ALGORITMA: "),
            sg.Checkbox("Sporije izvođenje", key='-CHECK-', enable_events=True),
            sg.Button("Odaberi početak", key='-OP-'),
            sg.Button("Odaberi kraj", key='-OK-'), sg.Button("Gotovo", key='-DONE-', metadata=0, size=(7, None)),
            sg.VerticalSeparator(),
            sg.Column(column, element_justification='center'),
            sg.Button("Start", disabled=True, key='-START-'),
            sg.Button("Reset", disabled=True, key='-RESET-')],
            [[sg.HorizontalSeparator()]],
            [sg.Text("", key='-VRIJEME-', visible=False),
             sg.Text("" ,size=(1,2)),
            sg.Button("Pause", key='-PAUSE-', visible=False),
            sg.Button("Finish", key='-FINISH-', visible=False)]]
layout += [[sg.Button(".", size=(4, 2), pad=(0, 0), border_width=1, metadata=1, key=(row, col))
            for col in range(COL_COUNT)] for row in range(ROW_COUNT)]


window = sg.Window("Početak", layout, finalize=True)

#for row in range(ROW_COUNT):
#    for col in range(COL_COUNT):
#        window[(row, col)].bind("<Enter>", '+')


while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-DZ-':
        if not DODAVANJE_ZIDOVA:
            DODAVANJE_ZIDOVA = True
            disable_enable(window, True, '-DE-', '-ES-', '-CHECK-', '-OP-', '-OK-', '-DONE-')
            window['-DZ-'].update("Dodavanje gotovo")
        elif DODAVANJE_ZIDOVA:
            DODAVANJE_ZIDOVA = False
            disable_enable(window, False, '-DE-', '-ES-', '-CHECK-', '-OP-', '-OK-', '-DONE-')
            window['-DZ-'].update("Dodavanje zidova")

    elif event == '-ES-':
        elevation = values['-ES-']

    elif event == '-DE-':
        if not DODAVANJE_ELEVACIJE:
            DODAVANJE_ELEVACIJE = True
            disable_enable(window, True, '-DZ-', '-CHECK-', '-OP-', '-OK-', '-DONE-')
            window['-DE-'].update("Dodavanje gotovo")
        elif DODAVANJE_ELEVACIJE:
            DODAVANJE_ELEVACIJE = False
            disable_enable(window, False, '-DZ-', '-CHECK-', '-OP-', '-OK-', '-DONE-')
            window['-DE-'].update("Dodavanje elevacije")

    elif isinstance(event, tuple):
        if DODAVANJE_ZIDOVA == True and event != start and event != end:
            if nodes[event[0]][event[1]] != 0:
                window[event].update(button_color=("black", "black"))
                nodes[event[0]][event[1]] = 0
            else:
                window[event].update(button_color=("white", color_dict[window[event].metadata]))
                nodes[event[0]][event[1]] = 1 if window[event].ButtonText=="." else int(window[event].ButtonText)

        if nodes[event[0]][event[1]] != 0:
            if DODAVANJE_ELEVACIJE:
                window[event].update(button_color=("white", color_dict[elevation]))
                nodes[event[0]][event[1]] = round(elevation)
                window[event].update(round(elevation) if elevation > 1 else ".")
                window[event].metadata = round(elevation)

            elif BIRANJE_POCETKA:
                if event == start:
                    if window[event].ButtonColor == ("black", "yellow"):
                        window[event].update(button_color=("white", color_dict[window[event].metadata]))
                        start = (-1, -1)
                    else:
                        window[event].update(button_color=("black", "yellow"))
                        start = event
                else:
                    window[event].update(button_color=("black", "yellow"))
                    event: tuple
                    if start != (-1, -1):
                        window[start].update(button_color=("white", color_dict[window[start].metadata]))
                    start = event

            elif BIRANJE_KRAJA:
                if event == end:
                    if window[event].ButtonColor == ("black", "green"):
                        window[event].update(button_color=("white", color_dict[window[event].metadata]))
                        end = (-1, -1)
                    else:
                        window[event].update(button_color=("black", "green"))
                        end = event
                else:
                    window[event].update(button_color=("black", "green"))
                    event: tuple
                    if end != (-1, -1):
                        window[end].update(button_color=("white", color_dict[window[end].metadata]))
                    end = event

    elif event == '-DONE-':
        if start != (-1, -1) and end != (-1, -1):
            if window[event].metadata == 0:
                disable_enable(window, False, '-START-', '-COEFFICIENT-')
                disable_enable(window, True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-')
                window[event].metadata = 1
                window[event].update("Povratak")
            else:
                disable_enable(window, True, '-START-', '-COEFFICIENT-')
                disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-')
                window[event].metadata = 0
                window[event].update("Gotovo")
        else:
            sg.popup("Odaberite početak i kraj")

    elif event == '-OP-':
        if not BIRANJE_POCETKA:
            disable_enable(window, True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-DONE-')
            BIRANJE_POCETKA = True
            window[event].update("Potvrdi početak")
        else:
            disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-DONE-')
            BIRANJE_POCETKA = False
            window[event].update("Odaberi početak")

    elif event == '-OK-':
        if not BIRANJE_KRAJA:
            disable_enable(window, True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OP-', '-DONE-')
            BIRANJE_KRAJA = True
            window[event].update("Potvrdi kraj")
        else:
            disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OP-', '-DONE-')
            BIRANJE_KRAJA = False
            window[event].update("Odaberi kraj")

    elif event == '-START-':
        nodes_colors, no_of_colors, found_path, path = graph_search(nodes, start, end, ROW_COUNT, COL_COUNT, values['-COEFFICIENT-'], window)
        print("Number of colors: ", no_of_colors)
        if not found_path:
            sg.popup("There is no path between the start and end nodes :(", title="No path found")
        else:
            if not values['-CHECK-']:
                color_graph(nodes_colors, no_of_colors, path, window)
            else:
                color_graph_pausable(nodes_colors, no_of_colors, path, window)
            disable_enable(window, False, '-RESET-')
            disable_enable(window, True, '-DONE-', '-COEFFICIENT-', '-START-')

    elif event == '-RESET-':
        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                if nodes[row][col] != 0:
                    #print(color_dict[window[(row,col)].metadata])
                    window[(row, col)].update(button_color=("white", color_dict[window[(row,col)].metadata]))
        window[start].update(button_color=("black", "yellow"))
        window[start].update("." if window[start].metadata == 1 else window[start].metadata)
        window[end].update(button_color=("black", "green"))
        window[end].update("." if window[end].metadata == 1 else window[end].metadata)
        window['-DONE-'].update("Gotovo")
        window['-DONE-'].metadata = 0
        window['-VRIJEME-'].update(visible=False)
        disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-', '-DONE-')
        disable_enable(window, True, '-START-', '-RESET-', '-COEFFICIENT-')

    elif event == 'Save map':
        if start == (-1, -1) or end == (-1 ,-1):
            sg.popup("Definicija mape nije gotova, dodajte početak i kraj prije spremanja.", title="Pogreška pri spremanju")
        else:
            file_path = sg.popup_get_file("Save As", save_as=True, file_types=(("JSON Files", "*.json"),))
            if file_path:
                # Ensure the file ends with .json
                if not file_path.endswith(".json"):
                    file_path += ".json"
                # Save the list to the JSON file
                json_file = {
                    "nodes": nodes,
                    "start": start,
                    "end": end
                }
                with open(file_path, "w") as f:
                    json.dump(json_file, f) #type: ignore
                sg.popup("Map saved successfully!")

    elif event == 'Load map':
        file_path = sg.popup_get_file("Open File", file_types=(("JSON Files", "*.json"),))
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)  # Load the list from the JSON file
                json_nodes: list = data.get("nodes", [])
                if len(json_nodes) == ROW_COUNT and len(json_nodes[1]) == COL_COUNT:
                    nodes = json_nodes
                    start_list = data.get("start", (-1, -1))
                    start = (start_list[0], start_list[1])
                    end_list = data.get("end", (-1, -1))
                    end = (end_list[0], end_list[1])
                    for row in range(ROW_COUNT):
                        for col in range(COL_COUNT):
                            if nodes[row][col] == 0:
                                window[(row, col)].metadata = 1
                                window[(row, col)].update(".")
                                window[(row, col)].update(button_color=("black", "black"))

                            elif nodes[row][col] == 1:
                                window[(row, col)].metadata = 1
                                window[(row, col)].update(".")
                                window[(row, col)].update(button_color=("white", color_dict[window[(row, col)].metadata]))

                            else:
                                window[(row, col)].metadata = nodes[row][col]
                                window[(row, col)].update(nodes[row][col])
                                window[(row, col)].update(button_color=("white", color_dict[window[(row, col)].metadata]))

                    window[start].update(button_color=("black", "yellow"))
                    window[end].update(button_color=("black", "green"))
                    window['-DONE-'].update("Gotovo")
                    window['-DONE-'].metadata = 0
                    disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-', '-DONE-')
                    disable_enable(window, True, '-START-')
                    sg.popup("Map loaded successfully!")

                else:
                    sg.popup("Broj redaka i stupaca ne poklapa se")
            except Exception as e:
                sg.popup_error(f"Failed to load file: {e}")

window.close()
