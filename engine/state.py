DISPLAY_MODE = "LIVE"  # Options: "LIVE", "BLANK", "PUB", "PSC"
SCREEN_BLANKED = False


def blank_screen():
    global DISPLAY_MODE, SCREEN_BLANKED
    DISPLAY_MODE = "BLANK"
    SCREEN_BLANKED = True


def unblank_screen():
    global DISPLAY_MODE, SCREEN_BLANKED
    DISPLAY_MODE = "LIVE"
    SCREEN_BLANKED = False


def show_pub_image():
    global DISPLAY_MODE, SCREEN_BLANKED
    DISPLAY_MODE = "PUB"
    SCREEN_BLANKED = False


def show_psc_image():
    global DISPLAY_MODE, SCREEN_BLANKED
    DISPLAY_MODE = "PSC"
    SCREEN_BLANKED = False

