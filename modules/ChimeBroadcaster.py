"""
File name: ChimeBroadcaster.py
Author: Martin Hein (@heimarti)
Date created: 14/03/2022
Date last modified: 14/03/2022
Version: 1.02
Python Version: 3.9
"""

import threading
import time
from modules.WebhookSender import WebhookSender


class ChimeBroadcaster(object):
    def __init__(self):
        self.__failed_to_send_messages = []
        self.__webhook_messenger = WebhookSender()

    def run_broadcaster(self, message: str, targets: list[str], number_of_threads: int = 5):
        if len(targets) < number_of_threads:
            number_of_threads = len(targets)

        # Set a maximum of 20 threads
        if number_of_threads > 20:
            number_of_threads = 20

        equal_split = len(targets) // number_of_threads
        splits_list = []

        if equal_split == 0:
            number_of_threads = len(targets)
            equal_split = 1
            reminder = 0
        else:
            reminder = len(targets) % number_of_threads

        start_bookmark = 0
        end_bookmark = start_bookmark + equal_split

        for i in range(0, number_of_threads):
            if reminder != 0:
                end_bookmark += 1
                reminder -= 1
            splits_list.append(targets[start_bookmark:end_bookmark])
            start_bookmark = end_bookmark
            end_bookmark = start_bookmark + equal_split

        # Set up messenger threads
        thread = None
        for entry in splits_list:
            thread = threading.Thread(target=self._messenger_thread, args=([entry, message]))
            thread.start()
        thread.join()
        result = {'successful': True,
                  'failed_to_send': self.__failed_to_send_messages}
        if len(self.__failed_to_send_messages) > 0:
            result['successful'] = False
        self.__failed_to_send_messages = []
        return result

    def _messenger_thread(self, urls, message):
        try:
            for entry in urls:
                if not self.__webhook_messenger.send_webhook(entry, message, 1):
                    fail_message = entry
                    self.__failed_to_send_messages.append(fail_message)
                time.sleep(0.8)
        except Exception as e:
            print(e)
