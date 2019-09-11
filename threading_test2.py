#!/usr/bin/env python

import threading
import keyboard
import logging
import time

class LightshowThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(LightshowThread, self).__init__()
        self._stop_event = threading.Event()
        self._bounce_event = threading.Event()

    def run(self):
        n = 0
        while not self._stop_event.isSet():
            time.sleep(0.2)
            n += 1
            logging.debug(n)
            if(self._bounce_event.isSet()):
                self._bounce_event.clear()
                logging.debug('BOUNCE!')
                n = 0
        logging.debug('i could do cleanup here instead of in stop')

    def bounce(self):
        self._bounce_event.set()

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



lightshow_thread = LightshowThread()

def go():
    global lightshow_thread
    lightshow_thread.start()
    while True:
        # wait for the space key
        keyboard.wait(' ')
        logging.debug('space!')
        lightshow_thread.bounce()
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