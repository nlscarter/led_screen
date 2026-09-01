HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WEC LED Matrix Controller</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #222; color: #fff; text-align: center; }
        input { font-size: 18px; padding: 5px; width: 80px; text-align: center; margin: 10px; }
        button { font-size: 18px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; margin: 8px; cursor: pointer; }
        .blank-button { background: #343a40; }
        .unblank-button { background: #28a745; }
        .image-button { background: #E4D96F; }
    </style>
</head>
<body>
    <h2>WEC LED Matrix Settings</h2>

    <form action="/update" method="post">
        <label>Max Cars to Display:</label>
        <input type="number" name="max_cars" value="{{ max_cars }}"><br>

        <label>Display Duration (Seconds):</label>
        <input type="number" name="display_duration" value="{{ display_duration }}"><br>

        <button type="submit">Update Matrix</button>
    </form>

    <hr>

    <form action="/pub" method="post">
        <button type="submit" class="image-button">Cock and Pug</button>
    </form>
    
    <form action="/psc" method="post">
        <button type="submit" class="image-button">PSC Racing</button>
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