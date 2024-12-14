import string

import PySimpleGUI as sg

from implementation import dijkstra

COL_COUNT = 25
ROW_COUNT = 15

def disable_enable(windows, disabled, *args):
    for arg in args:
        windows[arg].update(disabled=disabled)

def create_blue_color_dict():
    colors: dict[int, string] = {}
    colors[1] = "#283B5B"
    colors[2] = "#243655"
    colors[3] = "#21324F"
    colors[4] = "#1E2E4A"
    colors[5] = "#1A2944"
    colors[6] = "#17253E"
    colors[7] = "#142139"
    colors[8] = "#101C33"
    colors[9] = "#0D182D"
    colors[10] = "#0A1428"

    return colors

nodes = [[1 for _ in range(COL_COUNT)] for _ in range(ROW_COUNT)]

layout = [[sg.Text("UREĐIVANJE MAPE: "), sg.Button("Dodavanje zidova", key='-DZ-'),
           sg.VerticalSeparator(),
           sg.Text("ELEVACIJA POLJA: "),
           sg.Slider(range=(1, 10), resolution=1, orientation='h', key='-ES-', enable_events=True),
           sg.Button("Dodaj elevaciju", key='-DE-')]]
layout += [[sg.Text("KONFIGURACIJA ALGORITMA: "),
            sg.Checkbox("Sporije izvođenje", key='-CHECK-', enable_events=True),
            sg.Button("Odaberi početak", key='-OP-'),
            sg.Button("Odaberi kraj", key='-OK-'), sg.Button("Gotovo", key='-DONE-', metadata=0),
            sg.VerticalSeparator(),
            sg.Button("A*", disabled=True, key='-A*-'), sg.Button("Dijkstra", disabled=True, key='-DIJKSTRA-'),
            sg.Button("Reset", disabled=True, key='-RESET-')]]
layout += [[sg.Button(".", size=(4, 2), pad=(0, 0), border_width=1, metadata=1, key=(row, col))
            for col in range(COL_COUNT)] for row in range(ROW_COUNT)]

# inicijalizacija nekih varijabli
DODAVANJE_ZIDOVA = False
DODAVANJE_ELEVACIJE = False
BIRANJE_POCETKA = False
BIRANJE_KRAJA = False
start = end = (-1, -1)
elevation = 1
color_dict = create_blue_color_dict()

window = sg.Window("Početak", layout, finalize=True)

# for col in range(20):
#    for row in range(10):
#        window[(row+1, col+1)].bind("<B1-Motion>", '')


while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-DZ-':
        if DODAVANJE_ZIDOVA == False:
            DODAVANJE_ZIDOVA = True
            disable_enable(window, True, '-DE-', '-ES-', '-CHECK-', '-OP-', '-OK-', '-DONE-')
            window['-DZ-'].update("Dodavanje gotovo")
        elif DODAVANJE_ZIDOVA == True:
            DODAVANJE_ZIDOVA = False
            disable_enable(window, False, '-DE-', '-ES-', '-CHECK-', '-OP-', '-OK-', '-DONE-')
            window['-DZ-'].update("Dodavanje zidova")

    elif event == '-ES-':
        elevation = values['-ES-']
        print(elevation)

    elif event == '-DE-':
        if DODAVANJE_ELEVACIJE == False:
            DODAVANJE_ELEVACIJE = True
            disable_enable(window, True, '-DZ-', '-CHECK-', '-OP-', '-OK-', '-DONE-')
            window['-DE-'].update("Dodavanje gotovo")
        elif DODAVANJE_ELEVACIJE == True:
            DODAVANJE_ELEVACIJE = False
            disable_enable(window, False, '-DZ-', '-CHECK-', '-OP-', '-OK-', '-DONE-')
            window['-DE-'].update("Dodavanje elevacije")

    elif isinstance(event, tuple):
        if DODAVANJE_ZIDOVA == True and event != start and event != end:
            if window[event].ButtonColor == ('#FFFFFF', '#283b5b'):
                window[event].update(button_color=("black", "black"))
                #window[event].metadata = 0
                nodes[event[0]][event[1]] = 0
            else:
                window[event].update(button_color=sg.DEFAULT_BUTTON_COLOR)
                #window[event].metadata = 1 if window[event].ButtonText=="." else int(window[event].ButtonText)
                nodes[event[0]][event[1]] = 1 if window[event].ButtonText=="." else int(window[event].ButtonText)

        if nodes[event[0]][event[1]] != 0:
            if DODAVANJE_ELEVACIJE == True:
                window[event].update(button_color=("white", color_dict[elevation]))
                nodes[event[0]][event[1]] = round(elevation)
                window[event].update(round(elevation) if elevation > 1 else ".")
                window[event].metadata = round(elevation)

            elif BIRANJE_POCETKA:
                window[event].update(button_color=("black", "yellow"))
                event: tuple
                if start != (-1, -1):
                    window[start].update(button_color=sg.DEFAULT_BUTTON_COLOR)
                start = event

            elif BIRANJE_KRAJA:
                window[event].update(button_color=("black", "red"))
                event: tuple
                if end != (-1, -1):
                    window[end].update(button_color=sg.DEFAULT_BUTTON_COLOR)
                end = event

    elif event == '-DONE-':
        if window[event].metadata == 0 and start != (-1, -1) and end != (-1, -1):
            disable_enable(window, False, '-A*-', '-DIJKSTRA-')
            disable_enable(window, True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-')
            window[event].metadata = 1
            window[event].update("Povratak")
        else:
            disable_enable(window, True, '-A*-', '-DIJKSTRA-')
            disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-')
            window[event].metadata = 0
            window[event].update("Gotovo")

    elif event == '-OP-':
        if BIRANJE_POCETKA == False:
            disable_enable(window, True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-DONE-')
            BIRANJE_POCETKA = True
            window[event].update("Potvrdi početak")
        else:
            disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-DONE-')
            BIRANJE_POCETKA = False
            window[event].update("Odaberi početak")

    elif event == '-OK-':
        if BIRANJE_KRAJA == False:
            disable_enable(window, True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OP-', '-DONE-')
            BIRANJE_KRAJA = True
            window[event].update("Potvrdi kraj")
        else:
            disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OP-', '-DONE-')
            BIRANJE_KRAJA = False
            window[event].update("Odaberi kraj")

    elif event == '-DIJKSTRA-':
        dijkstra(nodes, start, end, ROW_COUNT, COL_COUNT, window)
        disable_enable(window, False, '-RESET-')
        disable_enable(window, True, '-DONE-')

    elif event == '-RESET-':
        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                if nodes[row][col] != 0:
                    print(color_dict[window[(row,col)].metadata])
                    window[(row, col)].update(button_color=("white", color_dict[window[(row,col)].metadata]))
        window[start].update(button_color=("black", "yellow"))
        window[end].update(button_color=("black", "orange"))
        window['-DONE-'].update("Gotovo")
        window['-DONE-'].metadata = 0
        disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-OK-', '-OP-', '-DONE-')
        disable_enable(window, True, '-DIJKSTRA-', '-A*-')

window.close()
