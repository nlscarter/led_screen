from drawing import _draw_custom_string, _draw_custom_char
from fonts.custom_font import BIG_FONT, LOGO_DATA


class Stint:
    def __init__(self, tyre, laps, length=12):
        self.tyre = tyre
        self.laps = laps
        self.complete = laps / length if (laps and length) else 0.0


class Driver:
    def __init__(self, initial, surname, country, stint1: Stint, stint2: Stint, stint3: Stint):
        self.name = f'{initial}.{surname}'
        self.country = country
        self.stint1 = stint1
        self.stint2 = stint2
        self.stint3 = stint3


class Car:
    def __init__(self, number, team, driver: Driver, category, laps, time_delta):
        self.category = category
        self.driver = driver
        self.team = team
        self.laps = laps
        self.time_delta = time_delta
        self.number = number


class Race:
    def __init__(self, status):
        self.time_left = '12:15:36'  # change to time object


class Position:
    def __init__(self, num, car: Car):
        self.num = num
        self.car = car


soft = "S"
hard = "H"
medium = "M"
position1 = Position(1,
                     Car(34,
                         "BMW",
                         Driver("S",
                                "Panish",
                                "ESP",
                                Stint(soft, 12),
                                Stint(medium, 8),
                                Stint(None, None)
                                ),
                         category='LMP2',
                         laps=12,
                         time_delta=None
                         )
                     )
positions = [position1]


class TelemetryRow:
    """Represents a static row of racing data aligned into columns."""

    def __init__(self, position: Position):
        # Store the Position object directly
        self.position = position

    def render(self, canvas, o_mgr, y_pos):
        """Draws data fields sequentially across the X axis, tracking both layout dimensions."""
        current_x = 0
        max_h = 0

        # Column 1: Position
        w1, h1 = _draw_custom_string(canvas, o_mgr, str(self.position.num), start_x=current_x, start_y=y_pos,
                                     font_data=BIG_FONT)
        current_x += w1
        max_h = max(max_h, h1)

        # Column 2: Team Logo
        w2, h2 = _draw_custom_char(canvas, o_mgr, self.position.car.team, start_x=current_x, start_y=y_pos, font_data=LOGO_DATA)
        current_x += w2
        max_h = max(max_h, h2)

        # Column 3: Driver Name (using the combined initialized string string)
        # w3, h3 = draw_custom_string(canvas, o_mgr, self.position.car.driver.name, start_x=current_x, start_y=y_pos, font_data=BIG_FONT)
        # current_x += w3
        # max_h = max(max_h, h3)

        # Column 4: Laps
        # w4, h4 = draw_custom_string(canvas, o_mgr, str(self.position.car.laps), start_x=current_x, start_y=y_pos, font_data=BIG_FONT)
        # max_h = max(max_h, h4)

        return max_h
