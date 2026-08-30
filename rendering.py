import openwec

from render_row import RenderRow
from render_title import RenderTitle

session = openwec.Session("WEC", 2026, "Le Mans", "Race")
print(session)
openwec.configure(api_key="owec_e8N1kbg-lER2ZccDr6lgX1WmFmN_Gt6y")

rows_data = [
        RenderTitle(flag='ROLEX', session=session),
        RenderRow(num="22", session=session),
        RenderRow(num="7", session=session),
        RenderRow(num="9", session=session),
        RenderRow(num="10", session=session)
    ]