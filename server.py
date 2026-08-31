from flask import Flask, request, render_template_string, redirect

from assets.html import HTML_TEMPLATE
import config
from engine.state import blank_screen, unblank_screen, show_static_image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, max_cars=config.MAX_CARS, display_duration=config.DISPLAY_DURATION)


@app.route("/blank", methods=["POST"])
def blank():
    blank_screen()
    return redirect("/")


@app.route("/unblank", methods=["POST"])
def unblank():
    unblank_screen()
    return redirect("/")


@app.route("/image", methods=["POST"])
@app.route("/static_image", methods=["POST"])
@app.route("/static-image", methods=["POST"])
def image():
    show_static_image()
    return redirect("/")


@app.route('/update', methods=['POST'])
def update_config():
    try:
        config.MAX_CARS = int(request.form.get('max_cars', config.MAX_CARS))
        config.DISPLAY_DURATION = int(request.form.get('display_duration', config.DISPLAY_DURATION))
        print(f"[*] Configuration Updated -> MAX_CARS: {config.MAX_CARS}, DURATION: {config.DISPLAY_DURATION}")
    except ValueError:
        pass
    return render_template_string(HTML_TEMPLATE, max_cars=config.MAX_CARS, display_duration=config.DISPLAY_DURATION)


def run_flask_server(host='0.0.0.0', port=5000):
    """Runs the web server accessible on the local network."""
    app.run(host=host, port=port, debug=False, use_reloader=False)
