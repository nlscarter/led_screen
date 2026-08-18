from setup import FONT_COLOR_MAP
from fonts.custom_font import SMALL_FONT


def draw_horizontal_line(canvas, o_mgr, start_x, start_y, length, color_idx):
    """Draws a horizontal line starting at (start_x, start_y) extending right by length.

    color_idx should correspond to the 4-bit key in FONT_COLOR_MAP (e.g., 1-15).
    """
    # Fetch the RGB values from your global map; fallback to white if missing
    r, g, b = FONT_COLOR_MAP.get(color_idx, (255, 255, 255))

    # Early exit if the line is vertically completely out of bounds
    if start_y < 0 or start_y >= o_mgr.height:
        return

    # Draw pixel by pixel horizontally
    for i in range(length):
        x = start_x + i

        # Check horizontal bounds for every pixel
        if 0 <= x < o_mgr.width:
            o_mgr.set_pixel(canvas, x, start_y, r, g, b)

def draw_custom_char(canvas, o_mgr, char, start_x, start_y, font_data):
    """Renders a single variable character using virtual layout dimensions."""
    if char not in font_data:
        char = ' '

    #if char == ' ':
    #    return 3, 1

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


def draw_custom_string(canvas, o_mgr, text, start_x, start_y, font_data=SMALL_FONT, kerning=1, right_justify=False):
    """Renders an entire string, tracking cumulative widths and mapping special multi-char tokens.

    If right_justify is True, start_x acts as the right alignment margin.
    """
    # 1. Define the mapping from 3-character codes to unique 1-character placeholders
    token_map = {
        "007": "\uE007",
        "008": "\uE008",
        "009": "\uE009"
    }

    # 2. Replace the 3-character substrings with their 1-character equivalents
    processed_text = text
    for token, single_char in token_map.items():
        processed_text = processed_text.replace(token, single_char)

    # 3. Calculate total width first if right justifying
    if right_justify:
        total_width = 0
        for char in processed_text:
            # Fallback to space if character isn't in font data to get accurate widths
            actual_char = char if char in font_data else ' '
            char_width = len(font_data.get(actual_char, []))
            total_width += char_width + kerning

        if total_width > 0:
            total_width -= kerning  # Remove trailing kerning

        # Shift the starting x position left by the total calculated width
        start_x = start_x - total_width

    # 4. Iterate through the processed text and draw
    current_x = start_x
    for char in processed_text:
        char_width, char_height = draw_custom_char(canvas, o_mgr, char, current_x, start_y, font_data)
        current_x += char_width + kerning

    final_width = current_x - start_x - kerning if current_x != start_x else 0
    return final_width, 10

