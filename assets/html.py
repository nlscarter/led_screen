HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WEC Matrix Controller</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #222; color: #fff; text-align: center; }
        input { font-size: 18px; padding: 5px; width: 80px; text-align: center; margin: 10px; }
        button { font-size: 18px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; margin: 8px; cursor: pointer; }
        .blank-button { background: #dc3545; }
        .unblank-button { background: #28a745; }
        .image-button { background: #6f42c1; }
    </style>
</head>
<body>
    <h2>WEC Matrix Settings</h2>

    <form action="/update" method="post">
        <label>Max Cars to Display:</label><br>
        <input type="number" name="max_cars" value="{{ max_cars }}"><br>

        <label>Display Duration (Seconds):</label><br>
        <input type="number" name="display_duration" value="{{ display_duration }}"><br>

        <button type="submit">Update Matrix</button>
    </form>

    <hr>

    <form action="/image" method="post">
        <button type="submit" class="image-button">Swap to Static Image</button>
    </form>

    <form action="/blank" method="post">
        <button type="submit" class="blank-button">Blank Screen</button>
    </form>

    <form action="/unblank" method="post">
        <button type="submit" class="unblank-button">Unblank Screen</button>
    </form>
</body>
</html>
"""

if __name__ == "__main__":
    rendered_html = (
        HTML_TEMPLATE
        .replace("{{ max_cars }}", "4")
        .replace("{{ display_duration }}", "20")
    )

    with open("debug_controller.html", "w", encoding="utf-8") as file:
        file.write(rendered_html)

    print("Rendered debug_controller.html")