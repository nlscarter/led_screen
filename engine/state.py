DISPLAY_MODE = "LIVE"  # Options: "LIVE", "BLANK", "IMAGE"
SCREEN_BLANKED = False


def blank_screen():
    global DISPLAY_MODE, SCREEN_BLANKED
    DISPLAY_MODE = "BLANK"
    SCREEN_BLANKED = True


def unblank_screen():
    global DISPLAY_MODE, SCREEN_BLANKED
    DISPLAY_MODE = "LIVE"
    SCREEN_BLANKED = False


def show_static_image():
    global DISPLAY_MODE, SCREEN_BLANKED
    DISPLAY_MODE = "IMAGE"
    SCREEN_BLANKED = False
