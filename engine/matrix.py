# ─── ENVIRONMENT DETECTOR & MOCK INTERFACE ───
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    RUNNING_ON_HARDWARE = True
except ImportError:
    RUNNING_ON_HARDWARE = False

    class RGBMatrixOptions:
        pass

    class DummyCanvas:
        def __init__(self, width: int = 96, height: int = 48):
            """Initializes a persistent interactive window."""
            import matplotlib
            matplotlib.use('TkAgg')  # Forces a single live interactive pop-up window
            from matplotlib import pyplot as plt

            self.plt = plt
            self.width = width
            self.height = height
            self.pixels = {}

            # Setup interactive window mode for PyCharm
            plt.ion()
            self.fig, self.ax = plt.subplots(figsize=(10, 5))
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
            self.ax.set_xlim(-.5, self.width + .5)
            self.ax.set_ylim(-.5, self.height + .5)
            self.ax.invert_yaxis()  # (0,0) Top-Left

            if self.pixels:
                x_coords, y_coords = zip(*self.pixels.keys())
                colors = list(self.pixels.values())

                self.scatter_plot = self.ax.scatter(
                    x_coords, y_coords, color=colors, marker='s', s=10
                )

            self.plt.title(f"LED Matrix Debugger Canvas ({self.width}x{self.height})", color='black')

            # Force draw cycles without freezing execution threads
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            self.plt.pause(0.001)

    class RGBMatrix:
        def __init__(self, options=None):
            pass

        def CreateFrameCanvas(self):
            return DummyCanvas()

        def SwapOnVSync(self, canvas):
            canvas.Show()
            return canvas
