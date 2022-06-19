
import PySimpleGUI as sg
import sys
from pathlib import Path
from modules.ChimeBroadcaster import ChimeBroadcaster
from modules.CSVreader import CSVreader


class SimpleChimeBroadcaster:
    def __init__(self):
        self.__main_window = None
        self.__version = None
        self.__broadcaster = ChimeBroadcaster()
        self.__csv_reader = CSVreader()
        self.__targets = self.__csv_reader.read_csv(''.join((str(Path(__file__).parent), '\\webhooks.csv')))
        self.__launch()

    def __launch(self):
        layout = [[sg.Menu([['File', ['Refresh', 'Exit']],
                            ['About', ['Wiki', 'Webhooks API', 'Source']]])],
                  [sg.Text('Message:')],
                  [sg.Multiline(size=(75, 15), key='-input_box-')],
                  [sg.Column([[sg.Text('Pick the targets:', size=(13, 1), pad=(1, 2))],
                              [sg.Combo(list(self.__targets.keys()), size=(13, 1), pad=(1, 2),
                                        expand_x=True, key='-target_list-')],
                              [sg.Button('Send Message', size=(13, 1), pad=(1, 2), key='-submit_button-')]])]]
        self.__main_window = sg.Window(title='SimpleChimeBroadcaster', layout=layout)
        while True:
            event, values = self.__main_window(timeout=2500)
            if event == '-submit_button-':
                pass
                message = values['-input_box-']
                if len(message) > 0:
                    targets = values['-target_list-']
                    self.__broadcaster.run_broadcaster(message=message, targets=targets, number_of_threads=20)
                print(values)

            elif event == 'Restart':
                self.__main_window.close()
                SimpleChimeBroadcaster()
            elif event == 'Exit':
                sys.exit()
            elif event in ['Wiki', 'Webhooks API', 'Source']:
                pass
            elif event is None:
               break


if __name__ == '__main__':
    SimpleChimeBroadcaster()

