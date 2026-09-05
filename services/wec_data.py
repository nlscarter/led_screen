from view.render_row import RenderRow
from view.render_title import RenderTitle


def build_rows_for_category(session, car_rows, current_lap):
    """Pulls laps data for top cars from openwec and builds render objects."""
    rows = [RenderTitle(flag='ROLEX', lap=current_lap)]
    for index, car_row in car_rows.iterrows():
        car_num = str(car_row['car_number'])
        try:
            car_laps = session.laps(car_num)
        except Exception as e:
            print(f"Warning: Failed to fetch laps for car {car_num}: {e}")
            car_laps = None
        rows.append(RenderRow(car_data=car_row, car_laps=car_laps, current_lap=current_lap))
    return rows
