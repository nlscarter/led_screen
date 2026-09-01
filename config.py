import os
from engine.matrix import RGBMatrixOptions, RUNNING_ON_HARDWARE

FONT_COLOR_MAP = {
    0: (0, 0, 0),  # Black (Unused/Empty space background
    1: (255, 0, 0),  # Red good
    2: (0, 128, 0),  # Green good
    3: (123, 61, 0),  # Brown ok
    4: (0, 0, 255),  # Dark Blue / Navy
    5: (128, 0, 0),  # Dark Red / Maroon
    6: (116, 250, 82),  # Lime
    7: (50, 50, 50),  # Dark Charcoal / Off-Black
    8: (150, 150, 150),  # Gray
    9: (224, 29, 111),  # Coral / Pinkish Red
    10: (0, 255, 128),  # Light Mint Green
    11: (255, 255, 0),  # Pale Yellow
    12: (100, 100, 255),  # Light Blue / Lavender
    13: (128, 255, 255),  # Baby Blue
    14: (255, 146, 40),  # Orange
    15: (255, 255, 255),  # White
}

class_colours = {
    'HYPERCAR': 0x1,
    'LMP2': 0x4,
    'LMGT3': 0x2
}

api_key = "owec_e8N1kbg-lER2ZccDr6lgX1WmFmN_Gt6y"
led_rows = 48
led_cols = 96
IS_PORTRAIT = False  # Set to True for Portrait (48x96), False for Landscape (96x48)
DATA_FETCH_INTERVAL = 180  # Fetch fresh data every 3 minutes (180s)
DISPLAY_DURATION = 20
MAX_CARS = 4

PUB_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "assets", "pub.png")
PSC_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "assets", "psc.png")

_HAS_HARDWARE = RUNNING_ON_HARDWARE
if _HAS_HARDWARE:
    print('running on RPi4')
else:
    print('running on LAPTOP')


def get_matrix_options():
    options = RGBMatrixOptions()
    if _HAS_HARDWARE:
        options.rows = led_rows
        options.cols = led_cols
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "regular"
        options.gpio_slowdown = 4
        options.drop_privileges = False
        options.pwm_bits = 8
        options.brightness = 100
        options.scan_mode = 0
    return options
