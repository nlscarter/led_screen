from setup import FONT_COLOR_MAP
from fonts.custom_font import SMALL_FONT


def draw_custom_char(canvas, o_mgr, char, start_x, start_y, font_data):
    """Renders a single variable character using virtual layout dimensions."""
    if char not in font_data:
        char = ' '

    if char == ' ':
        return 5, 10

    col_data = font_data[char]
    char_width = len(col_data)

    for col_idx in range(char_width):
        packed_col = col_data[col_idx]
        x = start_x + col_idx

        if x < 0 or x >= o_mgr.width:
            continue

        temp_col = packed_col
        for row_idx in range(10):
            # Invert the row rendering order
            y = start_y - row_idx
            pixel_4bit = temp_col & 0x0F

            if pixel_4bit > 0 and 0 <= y < o_mgr.height:
                r, g, b = FONT_COLOR_MAP.get(pixel_4bit, (255, 255, 255))
                o_mgr.set_pixel(canvas, x, y, r, g, b)

            temp_col >>= 4

    # Locked: Height is now directly returned as a static value of 10
    return char_width, 10


def draw_custom_string(canvas, o_mgr, text, start_x, start_y, font_data=SMALL_FONT, kerning=1):
    """Renders an entire string, tracking cumulative widths and maximum element heights."""
    current_x = start_x

    for char in text:
        char_width, char_height = draw_custom_char(canvas, o_mgr, char, current_x, start_y, font_data)
        current_x += char_width + kerning


    total_width = current_x - start_x
    return total_width, 10
