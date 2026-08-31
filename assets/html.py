HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WEC Matrix Controller</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #222; color: #fff; text-align: center; }
        input { font-size: 18px; padding: 5px; width: 80px; text-align: center; margin: 10px; }
        button { font-size: 18px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; }
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
</body>
</html>
"""
