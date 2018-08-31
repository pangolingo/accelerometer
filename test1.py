#!/usr/bin/env python

import threading
import keyboard
import logging
import time

# prove that I can spin off a async thing when I press the space bar
# and then interrupt/kill it later

# this will be used to kick off a lightshow when we detect a bounce
# and then halt it/start a new one when we detect a new bounce

# this subclasses Thread
# we add the ability to send a stop event, which the run method can check
class LightshowThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(LightshowThread, self).__init__()
        self._stop_event = threading.Event()

    def run(self):
        logging.debug('Starting lights')
        n = 0
        while not self._stop_event.isSet( ):
            n += 1
            logging.debug('W: {}'.format(n))
            time.sleep(0.4)
            if n >= 20:
                logging.debug('got to 20')
                break
        logging.debug('thread has stopped')

    def stop(self):
        logging.debug('trying to stop thread')
        self._stop_event.set()
        n = 0
        while n < 5:
            n += 1
            logging.debug('killing: {}'.format(n))
            time.sleep(0.2)

    def stopped(self):
        return self._stop_event.isSet()

# set up logger to show the thread name, use debug mode
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)


lightshow_thread = None


def go():
    while True:
        global lightshow_thread
        # wait for the space key
        keyboard.wait(' ')
        logging.debug('space!')
        # stop and reset the existing thread
        stop_lightshow(lightshow_thread)
        lightshow_thread = LightshowThread()
        # start the new thread
        lightshow_thread.start()
    logging.debug('exiting')

def stop_lightshow(thread):
    if thread is not None and thread.is_alive():
        logging.debug('thread is alive - stopping it')
        # send the stop event
        thread.stop()
        # join it to the main context so it can finish
        # this blocks the main thread until that thread terminates
        thread.join()

try:
    go()
except(KeyboardInterrupt):
    logging.debug('closing')
    stop_lightshow(lightshow_thread)