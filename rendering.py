import datetime
from zoneinfo import ZoneInfo

import openwec

from drawing import horizontal_line, class_line, small_font_string, flag, draw_logo, large_font_string, \
    small_font_string_fade, stint_line

class RenderRow:
    """Heading of page"""

    def __init__(self, status, country, category, num, pos, name, session):
        self.status = status
        self.country = country
        self.category = category
        self.num = num
        self.pos = pos
        self.name = name
        self.session = session

        # 1. Fetch backend data
        self.team = self.get_team()
        self.car_laps = session.laps(self.num)

        # 2. Extract the last driver's group of laps safely
        self.stint = self.get_stint()

        # 3. Generate the pixel layout using the fresh stint data
        self.stint_list = self.stint_pixels()

    def driver(self):
        df = self.car_laps
        return df['driver_name'].iloc[-1]

    def name(self):
        return self.driver().split()[0]

    def surname(self):
        return self.driver().split()[1]

    def get_stint(self):
        # Handle edge case where a car has run 0 laps to prevent code from crashing
        if self.car_laps.empty:
            return self.car_laps.copy()

        df = self.car_laps.copy()
        name_changes = df['driver_name'] != df['driver_name'].shift()

        # Extract indices where changes occur
        change_indices = name_changes.to_numpy().nonzero()[0]

        # Use the last change index, or fallback to 0 if there are no changes
        last_group_start = change_indices[-1] if change_indices.size > 0 else 0

        return df.iloc[last_group_start:]

    def stint_pixels(self):
        df = self.stint.copy()
        return (~df['crossing_finish_in_pit']).astype(int).tolist()

    def get_team(self):
        df = self.session.results().copy()
        row = df[df['car_number'] == self.num]
        return row['team'].values[0]


    def render(self, canvas, o_mgr, y_pos):
        x_frames = [13,1,10,11,46]
        large_font_string(canvas, o_mgr, self.pos, x_frames=x_frames, x_frame=0, start_y=y_pos - 1, justify='center')
        class_line(canvas, o_mgr, self.category, start_x=sum(x_frames[:1]) - 1, start_y=y_pos)
        horizontal_line(canvas, o_mgr, start_x=sum(x_frames[:1]), start_y=y_pos, length=x_frames[2], color_idx=self.category)
        small_font_string(canvas, o_mgr, self.num, x_gaps=x_frames, x_frame=2, start_y=y_pos - 2, colour=8)
        draw_logo(canvas, o_mgr, self.status, start_x=sum(x_frames[:3]), start_y=y_pos)
        small_font_string(canvas, o_mgr, self.surname(), x_gaps=x_frames, x_frame=4, start_y=y_pos - 2)
        flag(canvas, o_mgr, self.country, start_x=sum(x_frames[:5]), start_y=y_pos)

        #horizontal_line(canvas, o_mgr, start_x=sum(x_frames[:4]), start_y=y_pos, length=x_frames[-1] - 1, color_idx=11)
        stint_line(canvas, o_mgr, start_x=sum(x_frames[:4]), start_y=y_pos, pixel_pattern=self.stint_list, color_idx=11)
        return 10

class RenderTitle:
    """Heading of page"""
    def __init__(self, flag, lap, session):
        self.session = session
        self.flag = flag
        tz = ZoneInfo("UTC")
        ft = "%H:%M:%S"
        time_now = datetime.datetime.now(tz=tz).strftime(ft)
        self.time_now = time_now
        self.lap = lap
        self.lap_string = f'Lap:{lap}'

    def render(self, canvas, o_mgr, y_pos):
        x_lengths = [22, 43, 33]
        draw_logo(canvas, o_mgr, self.flag, start_x=0, start_y=y_pos)
        small_font_string(canvas, o_mgr, self.time_now, x_gaps=x_lengths, x_frame=1, start_y=y_pos - 1, colour=0xB, justify='center')
        small_font_string_fade(canvas, o_mgr, self.lap_string, x_gaps=x_lengths, x_frame=2, start_y=y_pos - 1, color1=0xD, color2=1, justify='right')

        return 9

session = openwec.Session("WEC", 2026, "Le Mans", "Race")
print(session)
openwec.configure(api_key="owec_e8N1kbg-lER2ZccDr6lgX1WmFmN_Gt6y")

rows_data = [
        RenderTitle(flag='ROLEX', lap=358, session=session),
        RenderRow(status="FERRARI", country="GBR", category=1, num="12", pos="1", name="abcdefghi", session=session),
        RenderRow(status="PORSCHE", country="JAP", category=4, num="7", pos="8", name="jklmnopqr", session=session),
        RenderRow(status="BMW", country="ITY", category=2, num="007", pos="14",   name="stuvwxyz!", session=session),
        RenderRow(status="COLOUR1", country="JAP", category=1, num="20", pos="23", name="  ;+=;", session=session)
    ]