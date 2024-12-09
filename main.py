import PySimpleGUI as sg

COL_COUNT = 25
ROW_COUNT = 15

def disable_enable(windows, disabled, *args):
    for arg in args:
        windows[arg].update(disabled=disabled)


layout = [[sg.Text("UREĐIVANJE MAPE: "), sg.Button("Dodavanje zidova", key='-DZ-'),
           sg.VerticalSeparator(),
           sg.Text("ELEVACIJA POLJA: "),
           sg.Slider(range=(1, 10), resolution=1, orientation='h', key='-ES-', enable_events=True),
           sg.Button("Dodaj elevaciju", key='-DE-'), sg.Button("Gotovo", key='-DONE-')]]
layout += [[sg.Text("KONFIGURACIJA ALGORITMA: "),
            sg.Checkbox("Sporije izvođenje", key='-CHECK-', enable_events=True, disabled=True),
            sg.Button("Odaberi početak", key='-OP-', disabled=True),
            sg.Button("Odaberi kraj", key='-OK-', disabled=True),
            sg.VerticalSeparator(),
            sg.Button("A*", disabled=True, key='-A*-'), sg.Button("Dijkstra", disabled=True, key='-DIJKSTRA-')]]
layout += [
    [sg.Button("1", size=(4, 2), pad=(0, 0), border_width=1, metadata=1, key=(row + 1, col + 1))
     for col in range(COL_COUNT)] for row in range(ROW_COUNT)]

# inicijalizacija nekih varijabli
DODAVANJE_ZIDOVA = False
DODAVANJE_ELEVACIJE = False
BIRANJE_POCETKA = False
BIRANJE_KRAJA = False
start = end = (0, 0)
elevation = 1

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
            disable_enable(window, True, '-DE-', '-ES-')
            window['-DZ-'].update("Dodavanje gotovo")
        elif DODAVANJE_ZIDOVA == True:
            DODAVANJE_ZIDOVA = False
            disable_enable(window, False, '-DE-', '-ES-')
            window['-DZ-'].update("Dodavanje zidova")

    elif event == '-ES-':
        elevation = values['-ES-']
        print(elevation)

    elif event == '-DE-':
        if DODAVANJE_ELEVACIJE == False:
            DODAVANJE_ELEVACIJE = True
            disable_enable(window, True, '-DZ-')
            window['-DE-'].update("Dodavanje gotovo")
        elif DODAVANJE_ELEVACIJE == True:
            DODAVANJE_ELEVACIJE = False
            disable_enable(window, False, '-DZ-')
            window['-DE-'].update("Dodavanje elevacije")

    elif isinstance(event, tuple):
        if DODAVANJE_ZIDOVA == True:
            if window[event].ButtonColor == ('#FFFFFF', '#283b5b'):
                window[event].update(button_color=("black", "black"))
                window[event].metadata = 0
            else:
                window[event].update(button_color=sg.DEFAULT_BUTTON_COLOR)
                window[event].metadata = int(window[event].ButtonText)

        if window[event].metadata != 0:
            if DODAVANJE_ELEVACIJE == True:
                window[event].update(round(elevation))

            elif BIRANJE_POCETKA:
                window[event].update(button_color=("black", "yellow"))
                event: tuple
                if start != (0, 0):
                    window[start].update(button_color=sg.DEFAULT_BUTTON_COLOR)
                start = event

            elif BIRANJE_KRAJA:
                window[event].update(button_color=("black", "red"))
                event: tuple
                if end != (0, 0):
                    window[end].update(button_color=sg.DEFAULT_BUTTON_COLOR)
                end = event

    elif event == '-DONE-':
        disable_enable(window, False, '-CHECK-', '-A*-', '-DIJKSTRA-', '-OP-', '-OK-')

    elif event == '-OP-':
        if BIRANJE_POCETKA == False:
            disable_enable(window, True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-A*-', '-DIJKSTRA-', '-OK-', '-DONE-')
            BIRANJE_POCETKA = True
            window[event].update("Potvrdi početak")
        else:
            disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-A*-', '-DIJKSTRA-', '-OK-', '-DONE-')
            BIRANJE_POCETKA = False
            window[event].update("Odaberi početak")

    elif event == '-OK-':
        if BIRANJE_KRAJA == False:
            disable_enable(window, True, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-A*-', '-DIJKSTRA-', '-OP-', '-DONE-')
            BIRANJE_KRAJA = True
            window[event].update("Potvrdi kraj")
        else:
            disable_enable(window, False, '-DE-', '-ES-', '-DZ-', '-CHECK-', '-A*-', '-DIJKSTRA-', '-OP-', '-DONE-')
            BIRANJE_KRAJA = False
            window[event].update("Odaberi kraj")

window.close()
