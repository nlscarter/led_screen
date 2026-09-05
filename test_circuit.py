import unittest
from assets.graphics import CIRCUIT, SECTORS
from engine.drawing import OrientationManager, plot_circuit, draw_circuit, plot_sector, draw_sector
from engine.matrix import RGBMatrix
from renders.render_circuit import RenderCircuit


class MockCanvas:
    def __init__(self, width=96, height=48):
        self.width = width
        self.height = height
        self.pixels = {}

    def Clear(self):
        self.pixels.clear()

    def SetPixel(self, x, y, r, g, b):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[(x, y)] = (r, g, b)


class TestCircuitPlotting(unittest.TestCase):
    def test_circuit_and_sectors_types(self):
        self.assertIsInstance(CIRCUIT, list)
        self.assertIsInstance(SECTORS, list)
        self.assertGreater(len(CIRCUIT), 0)
        self.assertGreater(len(SECTORS), 1)

    def test_plot_circuit_default_color(self):
        canvas = MockCanvas()
        plot_circuit(canvas)
        self.assertGreater(len(canvas.pixels), 0)
        for coord in CIRCUIT:
            x, y = coord
            self.assertEqual(canvas.pixels.get((x, y)), (200, 200, 200))

    def test_plot_circuit_with_orientation_mgr(self):
        canvas = MockCanvas()
        matrix = RGBMatrix()
        o_mgr = OrientationManager(matrix, portrait_mode=False)
        draw_circuit(canvas, o_mgr)
        for coord in CIRCUIT:
            x, y = coord
            self.assertEqual(canvas.pixels.get((x, y)), (200, 200, 200))

    def test_plot_sector_yellow(self):
        canvas = MockCanvas()
        plot_circuit(canvas)
        # Plot sector 0 (between SECTORS[0] and SECTORS[1])
        plot_sector(canvas, n=0)
        start_idx = SECTORS[0]
        end_idx = SECTORS[1]
        for coord in CIRCUIT[start_idx:end_idx + 1]:
            x, y = coord
            self.assertEqual(canvas.pixels.get((x, y)), (255, 255, 0))

        # Check an unselected coordinate remains grey (200, 200, 200)
        if len(CIRCUIT) > SECTORS[2]:
            unselected_coord = CIRCUIT[SECTORS[2]]
            self.assertEqual(canvas.pixels.get(unselected_coord), (200, 200, 200))

    def test_plot_sector_all_sectors(self):
        for n in range(len(SECTORS) - 1):
            canvas = MockCanvas()
            plot_circuit(canvas)
            plot_sector(canvas, n=n)
            start_idx = SECTORS[n]
            end_idx = SECTORS[n + 1]
            for coord in CIRCUIT[start_idx:end_idx + 1]:
                x, y = coord
                self.assertEqual(canvas.pixels.get((x, y)), (255, 255, 0))

    def test_render_circuit_class(self):
        canvas = MockCanvas()
        matrix = RGBMatrix()
        o_mgr = OrientationManager(matrix, portrait_mode=False)
        renderer = RenderCircuit(sector=1)
        used_height = renderer.render(canvas, o_mgr)
        self.assertEqual(used_height, 48)
        start_idx = SECTORS[1]
        end_idx = SECTORS[2]
        for coord in CIRCUIT[start_idx:end_idx + 1]:
            x, y = coord
            self.assertEqual(canvas.pixels.get((x, y)), (255, 255, 0))


if __name__ == "__main__":
    unittest.main()
