import os
from PIL import Image

from config import FONT_COLOR_MAP, class_colours
from assets.graphics import FLAG_DATA, LOGO_DATA
from assets.fonts import font_4x7, font_5x9, font_3x5

_IMAGE_CACHE = {}


def draw_image(canvas, o_mgr, image_source):
    """Draws a static image onto the canvas using orientation manager coordinates.

    image_source: filepath (str) or PIL.Image.Image instance.
    """
    img = None
    if isinstance(image_source, str):
        if not os.path.exists(image_source):
            return False
        try:
            mtime = os.path.getmtime(image_source)
            cache_key = (image_source, mtime, o_mgr.width, o_mgr.height)
            if cache_key in _IMAGE_CACHE:
                img = _IMAGE_CACHE[cache_key]
            else:
                raw_img = Image.open(image_source).convert('RGB')
                if raw_img.size != (o_mgr.width, o_mgr.height):
                    img = raw_img.resize((o_mgr.width, o_mgr.height), Image.Resampling.LANCZOS)
                else:
                    img = raw_img
                _IMAGE_CACHE.clear()
                _IMAGE_CACHE[cache_key] = img
        except Exception as e:
            print(f"Warning: Failed to load image {image_source}: {e}")
            return False
    elif hasattr(image_source, 'convert'):
        img = image_source.convert('RGB')
        if img.size != (o_mgr.width, o_mgr.height):
            img = img.resize((o_mgr.width, o_mgr.height), Image.Resampling.LANCZOS)
    else:
        return False

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))[:3]
            o_mgr.set_pixel(canvas, x, y, r, g, b)
    return True


def horiz_line(canvas, o_mgr, car_class, start_x, start_y, length):
    """Draws a horizontal line starting at (start_x, start_y) extending right by length.

    color_idx should correspond to the 4-bit key in FONT_COLOR_MAP (e.g., 1-15).
    """
    color_idx = class_colours.get(car_class)
    if color_idx is None:
        return

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

def stint_line(canvas, o_mgr, pixel_pattern, start_x, start_y):
    """Draws a horizontal line based on a pattern of 1s and 0s, replacing the last pixel with a red dot.

    pixel_pattern: A list/sequence of 1s and 0s.
    color_idx: Corresponds to the 4-bit key in FONT_COLOR_MAP.
    """
    # Fetch the standard RGB values from your global map; fallback to white if missing
    normal_lap_rgb = (255, 255, 125)
    fastest_lap_rgb = (148, 0, 255)
    last_pixel_rgb = (255, 0, 0)

    # Early exit if the line is vertically completely out of bounds
    if start_y < 0 or start_y >= o_mgr.height:
        return

    # Cache the total length to easily identify the final index
    total_pixels = len(pixel_pattern)

    # Loop through the pattern indices and values
    for i, val in enumerate(pixel_pattern):
        x = start_x + i

        # Skip drawing entirely if the individual pixel is out of horizontal bounds
        if not (0 <= x < o_mgr.width):
            continue

        # Check if this is the absolute last item in the list
        if i == total_pixels - 1:
            # Force draw a red dot
            o_mgr.set_pixel(canvas, x, start_y, *last_pixel_rgb)

        # Draw fastest lap
        elif val == 2:
            o_mgr.set_pixel(canvas, x, start_y, *fastest_lap_rgb)

        # Otherwise, follow the normal 1/0 plotting logic
        elif val == 1:
            o_mgr.set_pixel(canvas, x, start_y, *normal_lap_rgb)

def _draw_font_string(canvas, o_mgr, string, start_x, x_width, start_y, font_data, colour=None, justify='left'):
    if x_width is not None:
        if justify == 'center':
            draw_x = start_x + (x_width / 2) - 1
        elif justify == 'right':
            draw_x = start_x + x_width - 2
        else:
            draw_x = start_x
        clip_bounds = (start_x, start_x + x_width)
    else:
        draw_x = start_x
        clip_bounds = None

    kerning = 1

    _draw_custom_string(
        canvas=canvas,
        o_mgr=o_mgr,
        text=string,
        start_x=draw_x,
        start_y=start_y,
        font_data=font_data,
        colour=colour,
        kerning=kerning,
        justify=justify,
        clip_bounds=clip_bounds
    )


def small_font(canvas, o_mgr, string, start_x, x_width, start_y, colour=None, justify='left'):
    _draw_font_string(
        canvas=canvas,
        o_mgr=o_mgr,
        string=string,
        start_x=start_x,
        x_width=x_width,
        start_y=start_y,
        font_data=font_4x7,
        colour=colour,
        justify=justify
    )


def tiny_font(canvas, o_mgr, string, start_x, x_width, start_y, colour=None, justify='left'):
    _draw_font_string(
        canvas=canvas,
        o_mgr=o_mgr,
        string=string,
        start_x=start_x,
        x_width=x_width,
        start_y=start_y,
        font_data=font_3x5,
        colour=colour,
        justify=justify
    )

def flag(canvas, o_mgr, country, start_x, start_y):
    font_data = FLAG_DATA
    colour=None
    _draw_custom_char(canvas, o_mgr, country, start_x, start_y, font_data, colour)

def draw_logo_(canvas, o_mgr, logo, start_x, start_y):
    font_data = LOGO_DATA
    colour=None
    _draw_custom_char(canvas, o_mgr, logo, start_x, start_y, font_data, colour)

def class_line(canvas, o_mgr, class_id, start_x, start_y, height=9):
    """Draws a vertical 1-pixel line upwards from start_y using the class color."""
    color_idx = class_colours.get(class_id)
    if color_idx is None:
        return

    r, g, b = FONT_COLOR_MAP.get(color_idx, (255, 255, 255))

    for i in range(height):
        y = start_y - i
        if (0 <= y < o_mgr.height) and (0 <= start_x < o_mgr.width):
            o_mgr.set_pixel(canvas, start_x, y, r, g, b)


def _draw_custom_char(canvas, o_mgr, char, start_x, start_y, font_data, colour, clip_bounds=None):
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
        if clip_bounds and not (clip_bounds[0] <= x < clip_bounds[1]):
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


def _draw_custom_string(canvas, o_mgr, text, start_x, start_y, font_data, colour, kerning, justify, clip_bounds=None):
    """Renders an entire string, tracking cumulative widths and mapping special multi-char tokens.

    If right_justify is True, start_x acts as the right alignment margin.
    """
    text=str(text)

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
        # Skip characters that start after the right clip boundary
        if clip_bounds and current_x >= clip_bounds[1]:
            break

        char_width, char_height = _draw_custom_char(
            canvas, o_mgr, char, current_x, start_y, font_data, colour, clip_bounds=clip_bounds
        )
        current_x += char_width + kerning

    final_width = current_x - start_x - kerning if current_x != start_x else 0
    return final_width, 10


class OrientationManager:
    """Handles layout dimensions and pixel transformations based on rotation state."""

    def __init__(self, matrix, portrait_mode):
        self.matrix = matrix
        self.portrait_mode = portrait_mode

        # Base hardware configurations (assuming a physical 96x48 canvas)
        self.hw_width = 96
        self.hw_height = 48

        # Virtual layout dimensions exposed to drawing functions
        if self.portrait_mode:
            self.width = self.hw_height  # 48
            self.height = self.hw_width  # 96
        else:
            self.width = self.hw_width  # 96
            self.height = self.hw_height  # 48

    def set_pixel(self, canvas, x, y, r, g, b):
        """Maps virtual layout coordinates to physical matrix hardware pixels."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        if self.portrait_mode:
            canvas.SetPixel(y, x, r, g, b)
        else:
            canvas.SetPixel(x, y, r, g, b)


