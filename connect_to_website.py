from pynput.keyboard import Key, Controller
import time
import os

keyboard = Controller()
EMAIL = os.environ['FIGURE_ACCOUNT_EMAIL']
PASSWORD = os.environ['FIGURE_ACCOUNT_PASSWORD']

time.sleep(5)

keyboard.type(EMAIL)
keyboard.press(Key.tab)
keyboard.release(Key.tab)
keyboard.type(PASSWORD)
keyboard.press(Key.enter)
keyboard.release(Key.enter)