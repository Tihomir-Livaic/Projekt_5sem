import json
from search_functions import *

class GUI:
    def __init__(self, num_of_rows_int: int):
        self.DODAVANJE_ZIDOVA: bool = False
        self.DODAVANJE_ELEVACIJE: bool = False
        self.BIRANJE_POCETKA: bool = False
        self.BIRANJE_KRAJA: bool = False
        self.start: tuple = (-1, -1)
        self.end: tuple = (-1, -1)
        self.elevation: int = 1
        self.color_dict: dict[int, string] = {1: "#283B5B", 2: "#243655", 3: "#21324F", 4: "#1E2E4A", 5: "#1A2944", 6: "#17253E",
                           7: "#142139", 8: "#101C33", 9: "#0D182D", 10: "#0A1428"}
        self.COL_COUNT: int = 30
        self.ROW_COUNT: int = num_of_rows_int
        self.nodes: list = [[1 for _ in range(self.COL_COUNT)] for _ in range(self.ROW_COUNT)]
        self.window = sg.Window("A* and other graph search algorithms", self.create_layout(), finalize=True)

    def render(self):
        while True:
            event, values = self.window.read()
            print(event, values)
            if event == sg.WIN_CLOSED:
                break
            elif event == '-DZ-':
                self.dz_handler()
            elif event == '-ES-':
                self.es_handler(values['-ES-'])
            elif event == '-DE-':
                self.de_handler()
            elif isinstance(event, tuple):
                self.node_button_press_handler(event)
            elif event == '-DONE-':
                self.done_handler()
            elif event == '-MAP_RESET-':
                self.map_reset_handler()
            elif event == '-OP-':
                self.op_handler()
            elif event == '-OK-':
                self.ok_handler()
            elif event == '-START-':
                if self.start_handler(values):
                    break
            elif event == '-RESET-':
                self.reset_handler()
            elif event == 'Save map':
                self.save_handler()
            elif event == 'Load map':
                self.load_handler()
        self.window.close()

    def create_layout(self) -> list:
        menu_def = [['File', ['Load map', 'Save map']], ['Help']]

        layout = [[sg.Menu(menu_def, key="-MENU-")]]
        layout += [[sg.Text("UREĐIVANJE MAPE: "), sg.Button("Dodavanje zidova", key='-DZ-', size=(13, None)),
                    sg.VerticalSeparator(),
                    sg.Text("ELEVACIJA POLJA: "),
                    sg.Slider(range=(1, 10), resolution=1, orientation='h', key='-ES-', enable_events=True),
                    sg.Button("Dodavanje elevacije", key='-DE-', size=(15, None)),
                    sg.Button("Resetiraj mapu", key='-MAP_RESET-', size=(12, None))]]
        column = [[sg.Text("Dijkstra             A*       Greedy BFS")],
                  [sg.Text("|                      |                      |", auto_size_text=True)],
                  [sg.Slider((-1, 1), resolution=0.1, orientation='h', disable_number_display=True, default_value=0,
                             key='-COEFFICIENT-', disabled=True)]]
        layout += [[sg.Text("KONFIGURACIJA ALGORITMA: "),
                    sg.Checkbox("Sporije izvođenje", key='-CHECK-', enable_events=True),
                    sg.Button("Odaberi početak", key='-OP-', size=(12, None)),
                    sg.Button("Odaberi kraj", key='-OK-', size=(10, None)),
                    sg.Button("Gotovo", key='-DONE-', metadata=0, size=(7, None)),
                    sg.VerticalSeparator(),
                    sg.Column(column, element_justification='center'),
                    sg.Button("Start", disabled=True, key='-START-'),
                    sg.Button("Reset", disabled=True, key='-RESET-')],
                   [[sg.HorizontalSeparator()]],
                   [sg.Text("", key='-VRIJEME-', visible=False),
                    sg.Text("", size=(1, 2)),
                    sg.Button("Pause", key='-PAUSE-', visible=False),
                    sg.Button("Finish", key='-FINISH-', visible=False)]]
        layout += [[sg.Button(".", size=(4, 2), pad=(0, 0), border_width=1, metadata=1, key=(row, col))
                    for col in range(self.COL_COUNT)] for row in range(self.ROW_COUNT)]

        return layout

    def dz_handler(self):
        if not self.DODAVANJE_ZIDOVA:
            self.DODAVANJE_ZIDOVA = True
            self.disable_enable(True, '-DE-', '-ES-', '-CHECK-', '-OP-', '-OK-', '-DONE-' , '-MAP_RESET-')
            self.window['-DZ-'].update("Dodavanje gotovo")
        elif self.DODAVANJE_ZIDOVA:
            self.DODAVANJE_ZIDOVA = False
            self.disable_enable(False, '-DE-', '-ES-', '-CHECK-', '-OP-', '-OK-', '-DONE-' , '-MAP_RESET-')
            self.window['-DZ-'].update("Dodavanje zidova")

    def es_handler(self, elevation: int):
        self.elevation = elevation

    def de_handler(self):
        if not self.DODAVANJE_ELEVACIJE:
            self.DODAVANJE_ELEVACIJE = True
            self.disable_enable(True, '-DZ-', '-CHECK-', '-OP-', '-OK-', '-DONE-' , '-MAP_RESET-')
            self.window['-DE-'].update("Dodavanje gotovo")
        elif self.DODAVANJE_ELEVACIJE:
            self.DODAVANJE_ELEVACIJE = False
            self.disable_enable(False, '-DZ-', '-CHECK-', '-OP-', '-OK-', '-DONE-' , '-MAP_RESET-')
            self.window['-DE-'].update("Dodavanje elevacije")

    def node_button_press_handler(self, event):
        if self.DODAVANJE_ZIDOVA == True and event != self.start and event != self.end:
            if self.nodes[event[0]][event[1]] != 0:
                self.window[event].update(button_color=("black", "black"))
                self.nodes[event[0]][event[1]] = 0
            else:
                self.window[event].update(button_color=("white", self.color_dict[self.window[event].metadata]))
                self.nodes[event[0]][event[1]] = 1 if self.window[event].ButtonText=="." else int(self.window[event].ButtonText)

        if self.nodes[event[0]][event[1]] != 0:
            if self.DODAVANJE_ELEVACIJE:
                if event != self.start and event != self.end:
                    self.window[event].update(button_color=("white", self.color_dict[self.elevation]))
                self.nodes[event[0]][event[1]] = round(self.elevation)
                self.window[event].update(round(self.elevation) if self.elevation > 1 else ".")
                self.window[event].metadata = round(self.elevation)

            elif self.BIRANJE_POCETKA:
                if event != self.end:
                    if event == self.start:
                        if self.window[event].ButtonColor == ("black", "yellow"):
                            self.window[event].update(button_color=("white", self.color_dict[self.window[event].metadata]))
                            self.start = (-1, -1)
                        else:
                            self.window[event].update(button_color=("black", "yellow"))
                            self.start = event
                    else:
                        self.window[event].update(button_color=("black", "yellow"))
                        event: tuple
                        if self.start != (-1, -1):
                            self.window[self.start].update(button_color=("white", self.color_dict[self.window[self.start].metadata]))
                        self.start = event

            elif self.BIRANJE_KRAJA:
                if event != self.start:
                    if event == self.end:
                        if self.window[event].ButtonColor == ("black", "green"):
                            self.window[event].update(button_color=("white", self.color_dict[self.window[event].metadata]))
                            self.end = (-1, -1)
                        else:
                            self.window[event].update(button_color=("black", "green"))
                            self.end = event
                    else:
                        self.window[event].update(button_color=("black", "green"))
                        event: tuple
                        if self.end != (-1, -1):
                            self.window[self.end].update(button_color=("white", self.color_dict[self.window[self.end].metadata]))
                        self.end = event

    def map_reset_handler(self):
        for row in range(self.ROW_COUNT):
            for col in range(self.COL_COUNT):
                self.nodes[row][col] = 1
                self.window[(row,col)].metadata = 1
                self.window[(row,col)].update(".")
                self.window[(row,col)].update(button_color=("white", self.color_dict[self.window[(row,col)].metadata]))
                self.start = (-1, -1)
                self.end = (-1, -1)

    def done_handler(self):
        if self.start != (-1, -1) and self.end != (-1, -1):
            if self.window['-DONE-'].metadata == 0:
                self.disable_enable(False, '-START-', '-COEFFICIENT-')
                self.disable_enable(True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-', '-MAP_RESET-')
                self.window['-DONE-'].metadata = 1
                self.window['-DONE-'].update("Povratak")
            else:
                self.disable_enable(True, '-START-', '-COEFFICIENT-')
                self.disable_enable(False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-', '-MAP_RESET-')
                self.window['-DONE-'].metadata = 0
                self.window['-DONE-'].update("Gotovo")
        else:
            sg.popup("Odaberite početak i kraj")

    def op_handler(self):
        if not self.BIRANJE_POCETKA:
            self.disable_enable(True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-DONE-' , '-MAP_RESET-')
            self.BIRANJE_POCETKA = True
            self.window['-OP-'].update("Potvrdi početak")
        else:
            self.disable_enable(False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-DONE-' , '-MAP_RESET-')
            self.BIRANJE_POCETKA = False
            self.window['-OP-'].update("Odaberi početak")

    def ok_handler(self):
        if not self.BIRANJE_KRAJA:
            self.disable_enable(True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OP-', '-DONE-' , '-MAP_RESET-')
            self.BIRANJE_KRAJA = True
            self.window['-OK-'].update("Potvrdi kraj")
        else:
            self.disable_enable(False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OP-', '-DONE-' , '-MAP_RESET-')
            self.BIRANJE_KRAJA = False
            self.window['-OK-'].update("Odaberi kraj")

    def start_handler(self, values) -> bool:
        self.disable_enable(True, '-START-', '-DONE-')
        nodes_colors, no_of_colors, found_path, path = graph_search(self.nodes, self.start, self.end, self.ROW_COUNT, self.COL_COUNT, values['-COEFFICIENT-'], self.window)
        if not found_path:
            sg.popup("There is no path between the start and end nodes :(", title="No path found")
        else:
            if not values['-CHECK-']:
                color_graph(nodes_colors, no_of_colors, path, self.window)
            else:
                should_exit = color_graph_pausable(nodes_colors, no_of_colors, path, self.window)
                if should_exit:
                    return True
            self.disable_enable(False, '-RESET-')
            self.disable_enable(True, '-DONE-', '-COEFFICIENT-', '-START-')
        return False

    def reset_handler(self):
        for row in range(self.ROW_COUNT):
            for col in range(self.COL_COUNT):
                if self.nodes[row][col] != 0:
                    #print(color_dict[window[(row,col)].metadata])
                    self.window[(row, col)].update(button_color=("white", self.color_dict[self.window[(row,col)].metadata]))
        self.window[self.start].update(button_color=("black", "yellow"))
        self.window[self.start].update("." if self.window[self.start].metadata == 1 else self.window[self.start].metadata)
        self.window[self.end].update(button_color=("black", "green"))
        self.window[self.end].update("." if self.window[self.end].metadata == 1 else self.window[self.end].metadata)
        self.window['-DONE-'].update("Gotovo")
        self.window['-DONE-'].metadata = 0
        self.window['-VRIJEME-'].update(visible=False)
        self.disable_enable(False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-', '-DONE-' , '-MAP_RESET-')
        self.disable_enable(True, '-START-', '-RESET-', '-COEFFICIENT-')

    def save_handler(self):
        if self.start == (-1, -1) or self.end == (-1 ,-1):
            sg.popup("Definicija mape nije gotova, dodajte početak i kraj prije spremanja.", title="Pogreška pri spremanju")
        else:
            file_path = sg.popup_get_file("Save As", save_as=True, file_types=(("JSON Files", "*.json"),))
            if file_path:
                # Ensure the file ends with .json
                if not file_path.endswith(".json"):
                    file_path += ".json"
                # Save the list to the JSON file
                json_file = {
                    "nodes": self.nodes,
                    "start": self.start,
                    "end": self.end
                }
                with open(file_path, "w") as f:
                    json.dump(json_file, f) #type: ignore
                sg.popup("Map saved successfully!")

    def load_handler(self):
        file_path = sg.popup_get_file("Open File", file_types=(("JSON Files", "*.json"),))
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)  # Load the list from the JSON file
                json_nodes: list = data.get("nodes", [])
                if len(json_nodes) == self.ROW_COUNT and len(json_nodes[1]) == self.COL_COUNT:
                    self.nodes = json_nodes
                    start_list = data.get("start", (-1, -1))
                    self.start = (start_list[0], start_list[1])
                    end_list = data.get("end", (-1, -1))
                    self.end = (end_list[0], end_list[1])
                    for row in range(self.ROW_COUNT):
                        for col in range(self.COL_COUNT):
                            if self.nodes[row][col] == 0:
                                self.window[(row, col)].metadata = 1
                                self.window[(row, col)].update(".")
                                self.window[(row, col)].update(button_color=("black", "black"))

                            elif self.nodes[row][col] == 1:
                                self.window[(row, col)].metadata = 1
                                self.window[(row, col)].update(".")
                                self.window[(row, col)].update(button_color=("white", self.color_dict[self.window[(row, col)].metadata]))

                            else:
                                self.window[(row, col)].metadata = self.nodes[row][col]
                                self.window[(row, col)].update(self.nodes[row][col])
                                self.window[(row, col)].update(button_color=("white", self.color_dict[self.window[(row, col)].metadata]))

                    self.window[self.start].update(button_color=("black", "yellow"))
                    self.window[self.end].update(button_color=("black", "green"))
                    self.window['-DONE-'].update("Gotovo")
                    self.window['-DONE-'].metadata = 0
                    self.disable_enable(False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-', '-DONE-')
                    self.disable_enable(True, '-START-')
                    sg.popup("Map loaded successfully!")

                else:
                    sg.popup(f"Broj redaka i stupaca ne poklapa se,\ntrenutni su {self.ROW_COUNT} {self.COL_COUNT}, iz datoteke su {len(json_nodes)} {len(json_nodes[1])}")
            except Exception as e:
                sg.popup_error(f"Failed to load file: {e}")

    def disable_enable(self, disabled: bool, *args: string):
        for arg in args:
            self.window[arg].update(disabled=disabled)

def main():
    num_of_rows = sg.popup_get_text(
        message="Upišite broj redova\n(preporuka je između 10 i 15, ovisi o veličini ekrana):", default_text="15")
    if num_of_rows is None:
        return

    while True:
        try:
            num_of_rows_int = int(num_of_rows)
            if num_of_rows_int <= 0 or num_of_rows_int > 20:
                num_of_rows = sg.popup_get_text(message="Upišite broj veći od nule i manji od 20:",
                                                default_text="15")
                if num_of_rows is None:
                    return
                continue
            break
        except:
            num_of_rows = sg.popup_get_text(message="Upišite cijeli broj:",
                                            default_text="15")
            if num_of_rows is None:
                return

    gui = GUI(num_of_rows_int)
    gui.render()

    exit()

main()