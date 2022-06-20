import time

import PySimpleGUI as sg
import sys
import webbrowser
import threading
from pathlib import Path
from modules.ChimeBroadcaster import ChimeBroadcaster
from modules.CSVreader import CSVreader
from modules.ConfigParser import ConfigParser


class SimpleChimeBroadcaster:
    def __init__(self):
        self.__main_window = None
        self.__version = None
        self.__broadcast_results = None
        self.__broadcaster = ChimeBroadcaster()
        self.__csv_reader = CSVreader()
        self.__config_file = ConfigParser().get_config_as_dictionary('simple_broadcaster_configuration.ini')
        self.__targets = self.__csv_reader.read_csv('webhooks.csv')
        self.__launch()

    def __launch(self):
        layout = [[sg.Menu([['File', ['Refresh', 'Exit']],
                            ['About', ['How to use', 'Webhooks API', 'Source']]])],
                  [sg.Text('Message:')],
                  [sg.Multiline(size=(75, 15), key='-input_box-')],
                  [sg.Column([[sg.Text('Pick the targets:', size=(13, 1), pad=(1, 2))],
                              [sg.Combo(list(self.__targets.keys()), size=(13, 1), pad=(1, 2),
                                        expand_x=True, key='-target_list-')],
                              [sg.Button('Send Message', size=(13, 1), pad=(1, 2), key='-submit_button-')]])]]
        self.__main_window = sg.Window(title='SimpleChimeBroadcaster', layout=layout)
        while True:
            event, values = self.__main_window(timeout=2500)
            # Handle broadcast request
            if event == '-submit_button-':
                message = values['-input_box-']
                if len(message) > 0:
                    targets = values['-target_list-']
                    if len(targets) > 0:
                        targets = self.__targets[targets]
                        temp_targets = []
                        for target in targets:
                            if len(target) > 0:
                                temp_targets.append(target)
                        targets = temp_targets
                        if len(targets) > 0:
                            self.__disable_send_button(True)
                            threading.Thread(target=self.__broadcast, args=([message, targets])).start()
                        else:
                            sg.popup_ok('Target column is empty.\nPlease fill the column in webhooks.csv file.')
                    else:
                        sg.popup_ok('Please select a target column from the drop-down menu.')
                else:
                    sg.popup_ok('Message is blank.')
            # Handle Restart
            elif event == 'Refresh':
                self.__main_window.close()
                SimpleChimeBroadcaster()
            # Handle Exit
            elif event == 'Exit':
                sys.exit()
            # Handle information queries
            elif event in ['How to use', 'Webhooks API', 'Source']:
                resources = self.__config_file['Resources']
                if not resources[event.lower()].lower() == 'none':
                    webbrowser.open(url=resources[event.lower()], new=0, autoraise=True)
            # Handle broadcasting results
            elif self.__broadcast_results:
                results = self.__broadcast_results
                if results['status'] == 'success':
                    sg.popup_ok('Broadcast completed without errors.')
                    self.__disable_send_button(False)
                else:
                    retry = sg.popup_yes_no(''.join(['Failed to broadcast to:\n\n',
                                                     '\n\n'.join(results['errors']), '\n\nWould you like to re-try?']))
                    if retry == 'Yes':
                        threading.Thread(target=self.__broadcast, args=([results['message'], results['errors']]))\
                            .start()
                    else:
                        sg.popup_ok('Broadcast completed.')
                        self.__disable_send_button(False)
                self.__broadcast_results = None
            # Handle loop break
            elif event is None:
               break

    def __broadcast(self, message, targets):
        results = self.__broadcaster.run_broadcaster(message=message, targets=targets, number_of_threads=20)
        if len(results['failed_to_send']) <= 0:
            status = 'success'
        else:
            status = 'failure'
        self.__broadcast_results = {'status': status, 'message': message, 'errors': results['failed_to_send']}

    def __disable_send_button(self, disable: bool):
        self.__main_window['-submit_button-'].update(disabled=disable)


if __name__ == '__main__':
    try:
        SimpleChimeBroadcaster()
    except FileNotFoundError as e:
        print(e)
        time.sleep(5)
        sys.exit()
