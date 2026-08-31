from assets.html import HTML_TEMPLATE

if __name__ == "__main__":
    rendered_html = (
        HTML_TEMPLATE
        .replace("{{ max_cars }}", "4")
        .replace("{{ display_duration }}", "20")
    )

    with open("debug_controller.html", "w", encoding="utf-8") as file:
        file.write(rendered_html)

    print("Rendered debug_controller.html")