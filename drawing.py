from setup import FONT_COLOR_MAP
from fonts.custom_font import font_4x7, FLAG_DATA, LOGO_DATA, class_vertlines, font_5x9


def horizontal_line(canvas, o_mgr, start_x, start_y, length, color_idx):
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

def small_font_string(canvas, o_mgr, string, x_gaps, x_frame, start_y, colour=None, justify='left'):
    if justify == 'center':
        start_x = sum(x_gaps[:x_frame]) + (x_gaps[x_frame] / 2) - 1
    elif justify == 'right':
        start_x = sum(x_gaps[:x_frame]) + x_gaps[x_frame] - 2
    else:
        start_x = sum(x_gaps[:x_frame])
    font_data = font_4x7
    kerning = 1
    _draw_custom_string(canvas=canvas, o_mgr=o_mgr, text= string, start_x= start_x, start_y = start_y,
                        font_data= font_data, colour= colour, kerning=kerning, justify=justify)

def large_font_string(canvas, o_mgr, string, x_frames, x_frame, start_y, colour=None, justify='left'):
    font_data = font_5x9
    kerning = 1
    if justify == 'center':
        start_x = sum(x_frames[:x_frame]) + (x_frames[x_frame] / 2) - 1
    elif justify == 'right':
        start_x = sum(x_frames[:x_frame]) + x_frames[x_frame] - 2
    else:
        start_x = sum(x_frames[:x_frame])
    _draw_custom_string(canvas=canvas, o_mgr=o_mgr, text= string, start_x= start_x, start_y = start_y,
                        font_data= font_data, colour= colour, kerning=kerning, justify=justify)

def flag(canvas, o_mgr, country, start_x, start_y):
    font_data = FLAG_DATA
    colour=None
    _draw_custom_char(canvas, o_mgr, country, start_x, start_y, font_data, colour)

def draw_logo(canvas, o_mgr, logo, start_x, start_y):
    font_data = LOGO_DATA
    colour=None
    _draw_custom_char(canvas, o_mgr, logo, start_x, start_y, font_data, colour)

def class_line(canvas, o_mgr, class_id, start_x, start_y):
    font_data = class_vertlines
    colour=None
    _draw_custom_char(canvas, o_mgr, class_id, start_x, start_y, font_data, colour)


def _draw_custom_char(canvas, o_mgr, char, start_x, start_y, font_data, colour):
    """Renders a single variable character using virtual layout dimensions."""
    if char not in font_data:
        char = ' '

    if char == ' ':
        return 3, 1

    col_data = font_data[char]
    char_width = len(col_data)

    # Pre-determine override color if a number is passed
    override_rgb = None
    if colour is not None:
        override_rgb = FONT_COLOR_MAP.get(colour, (255, 255, 255))

    for col_idx in range(char_width):
        x = start_x + col_idx
        if not (0 <= x < o_mgr.width):
            continue

        temp_col = col_data[col_idx]
        for row_idx in range(10):
            y = start_y - row_idx
            pixel_4bit = temp_col & 0x0F

            if pixel_4bit > 0 and (0 <= y < o_mgr.height):
                # Use override color if available; otherwise, fall back to pixel's embedded color
                if override_rgb is not None:
                    r, g, b = override_rgb
                else:
                    r, g, b = FONT_COLOR_MAP.get(pixel_4bit, (255, 255, 255))

                o_mgr.set_pixel(canvas, x, y, r, g, b)

            temp_col >>= 4

    # Locked: Height is now directly returned as a static value of 10
    return char_width, 10


def _draw_custom_string(canvas, o_mgr, text, start_x, start_y, font_data, colour, kerning, justify):
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

    # 3. Calculate total width first if center or right justifying
    if justify in ('center', 'right'):
        total_width = 0
        for char in processed_text:
            # Fallback to space if character isn't in font data to get accurate widths
            actual_char = char if char in font_data else ' '
            char_width = len(font_data.get(actual_char, []))
            total_width += char_width + kerning

        if total_width > 0:
            total_width -= kerning  # Remove trailing kerning

        # Shift the starting x position based on the selected justification
        if justify == 'right':
            start_x = start_x - total_width
        elif justify == 'center':
            start_x = start_x - (total_width // 2)

    # 4. Iterate through the processed text and draw
    current_x = start_x
    for char in processed_text:
        char_width, char_height = _draw_custom_char(canvas, o_mgr, char, current_x, start_y, font_data, colour)
        current_x += char_width + kerning

    final_width = current_x - start_x - kerning if current_x != start_x else 0
    return final_width, 10


def _draw_custom_string_gradient(canvas, o_mgr, text, start_x, start_y, font_data, color1, color2, step, kerning=1,
                                 justify='left'):
    """
    Wraps _draw_custom_string to automatically calculate a color transition
    between color1 and color2 at a specific frame step (0 to 49).
    """
    # Force step to wrap around between 0 and 49 to keep it moving continuously
    current_step = step % 50

    # Calculate the interpolation factor (0.0 at step 0, 1.0 at step 49)
    # We use a sine wave calculation for smooth ping-pong cycling,
    # or simple linear step division. Here is smooth ping-pong:
    import math
    # Maps 0->49 step into 0.0->1.0->0.0 smooth wave transition
    factor = (math.sin((current_step / 50.0) * 2 * math.pi) + 1) / 2

    # If you prefer pure straight linear color fading (Color1 -> Color2 -> abrupt jump back to Color1):
    # factor = current_step / 49.0

    # Linearly interpolate between RGB channels
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)

    dynamic_color = (r, g, b)

    # Call your original function with the newly calculated color step
    return _draw_custom_string(canvas, o_mgr, text, start_x, start_y, font_data, dynamic_color, kerning, justify)

def small_font_string_fade(canvas, o_mgr, string, x_gaps, x_frame, start_y, color1, color2 , justify='left'):
    if justify == 'center':
        start_x = sum(x_gaps[:x_frame]) + (x_gaps[x_frame] / 2) - 1
    elif justify == 'right':
        start_x = sum(x_gaps[:x_frame]) + x_gaps[x_frame] - 2
    else:
        start_x = sum(x_gaps[:x_frame])
    font_data = font_4x7
    kerning = 1
    r1, g1, b1 = FONT_COLOR_MAP.get(color1, (255, 255, 255))
    r2, g2, b2 = FONT_COLOR_MAP.get(color2, (255, 255, 255))

    _draw_custom_string_gradient(canvas, o_mgr, string, start_x, start_y, font_data, [r1, g1, b1], [r2, g2, b2], step=1, kerning=1,
                                 justify='left')


