import matplotlib
matplotlib.use('TkAgg')  # Forces a single live interactive pop-up window
from matplotlib import pyplot as plt

from config import FONT_COLOR_MAP, class_colours
from assets.graphics import FLAG_DATA, LOGO_DATA
from assets.fonts import font_4x7, font_5x9


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

def stint_line(canvas, o_mgr, pixel_pattern, start_x, start_y, colour):
    """Draws a horizontal line based on a pattern of 1s and 0s, replacing the last pixel with a red dot.

    pixel_pattern: A list/sequence of 1s and 0s.
    color_idx: Corresponds to the 4-bit key in FONT_COLOR_MAP.
    """
    # Fetch the standard RGB values from your global map; fallback to white if missing
    r, g, b = FONT_COLOR_MAP.get(colour, (255, 255, 255))

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
            o_mgr.set_pixel(canvas, x, start_y, 255, 0, 0)

        # Otherwise, follow the normal 1/0 plotting logic
        elif val == 1:
            o_mgr.set_pixel(canvas, x, start_y, r, g, b)

def small_font(canvas, o_mgr, string, start_x, x_width, start_y, colour=None, justify='left'):
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

    font_data = font_4x7
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

def large_font_string(canvas, o_mgr, string, start_x, x_width, start_y, colour=None, justify='left'):
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

    font_data = font_5x9
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


def _scroll_custom_string(canvas, o_mgr, text, start_x, start_y, font_data, colour, kerning, justify, frame_width=50,
                        scroll_speed=50):
    """Renders an entire string, tracking cumulative widths and mapping special multi-char tokens.

    Supports dynamic persistent scrolling inside an active UI loop framework.

    :param frame_width: Maximum horizontal pixel width available for the text.
    :param scroll_speed: Number of pixels to shift the text per render frame.
    """
    text = str(text)

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

    # 3. Calculate full total width of the processed text
    total_width = 0
    for char in processed_text:
        actual_char = char if char in font_data else ' '
        char_width = len(font_data.get(actual_char, []))
        total_width += char_width + kerning

    if total_width > 0:
        total_width -= kerning  # Remove trailing kerning

    # 4. Handle state-based persistent text scrolling
    current_offset = 0
    is_scrolling = False

    if frame_width is not None and total_width > frame_width:
        is_scrolling = True

        # Determine the loop resetting threshold (Text width + padding gap)
        loop_reset_point = total_width + 40

        # Retrieve or initialize the scroll offset tracker from your manager or active row state
        # We try to bind it to 'o_mgr' so it survives across individual render cycles
        if not hasattr(o_mgr, '_scroll_tracker'):
            o_mgr._scroll_tracker = 0

        # Increment the persistent offset position frame-by-frame
        o_mgr._scroll_tracker = (o_mgr._scroll_tracker + scroll_speed) % loop_reset_point
        current_offset = int(o_mgr._scroll_tracker)

    # 5. Shift the starting x position based on justification (Only if NOT scrolling)
    if not is_scrolling and justify in ('center', 'right'):
        if justify == 'right':
            start_x = start_x - total_width
        elif justify == 'center':
            start_x = start_x - (total_width // 2)

    # 6. Iterate through the processed text and draw with layout boundary clipping
    current_x = start_x - current_offset

    for char in processed_text:
        actual_char = char if char in font_data else ' '
        char_width = len(font_data.get(actual_char, []))

        if frame_width is not None:
            # Performance optimization: Skip rendering characters completely out of the viewport
            if current_x + char_width < start_x or current_x > start_x + frame_width:
                current_x += char_width + kerning
                continue

        # Draw the valid visible character chunk
        _draw_custom_char(canvas, o_mgr, char, current_x, start_y, font_data, colour)
        current_x += char_width + kerning

    # Return total bounds width
    if is_scrolling:
        final_width = frame_width
    else:
        final_width = current_x - start_x - kerning if current_x != start_x else 0

    return final_width, 10


class DummyCanvas:
    def __init__(self, width: int = 96, height: int = 48):
        """Initializes a persistent interactive window."""
        self.width = width
        self.height = height
        self.pixels = {}

        # Setup interactive window mode for PyCharm
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 5))

        # Scatter plot placeholder so we only update data, not recreate the grid
        self.scatter_plot = None
        self.Clear()

    def Clear(self):
        """Resets the internal pixel storage buffer."""
        self.pixels = {}

    def SetPixel(self, x, y, r, g, b):
        """Stores the pixel color internally."""
        if 0 <= x < self.width and 0 <= y < self.height:
            # Normalize RGB from 0-255 to 0.0-1.0 for Matplotlib
            self.pixels[(x, y)] = (r / 255.0, g / 255.0, b / 255.0)

    def Show(self):
        """Flushes the buffer and updates the live canvas frame instantly."""
        self.ax.clear()
        self.ax.set_facecolor('black')

        # Lock the grid dimensions to match the matrix properties
        self.ax.set_xlim(-.5, self.width+.5)
        self.ax.set_ylim(-.5, self.height+.5)

        # Turn off ticks/labels to speed up execution, but keep the core grid boundaries
        #self.ax.set_xticks(range(0, self.width, 4))
        #self.ax.set_yticks(range(0, self.height, 4))
        #self.ax.grid(False, color='#151515', linestyle='-', linewidth=0.5)
        self.ax.invert_yaxis()  # (0,0) Top-Left

        if self.pixels:
            x_coords, y_coords = zip(*self.pixels.keys())
            colors = list(self.pixels.values())

            self.scatter_plot = self.ax.scatter(
                x_coords, y_coords, color=colors, marker='s', s=10
            )

        plt.title(f"LED Matrix Debugger Canvas ({self.width}x{self.height})", color='black')

        # Force draw cycles without freezing execution threads
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.001)


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


