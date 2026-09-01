import os
import webbrowser
from assets.html import HTML_TEMPLATE

if __name__ == "__main__":
    filename = "debug_controller.html"

    rendered_html = (
        HTML_TEMPLATE
        .replace("{{ max_cars }}", "4")
        .replace("{{ display_duration }}", "20")
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write(rendered_html)

    print(f"Rendered {filename}")

    # Open the file in the default browser
    file_path = os.path.abspath(filename)
    webbrowser.open(f"file://{file_path}")
