MODULE_PATH = "/home/pi/.local/lib/python3.7/site-packages/flask_talisman/__init__.py"
MODULE_NAME = "flask_talisman"
import importlib
import sys
spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

from flask import Flask, render_template, send_file, redirect, request
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/3DPrinting')
def threedprinting():
    return render_template('3DPrinting.html')

@app.route('/ElectricSkateboard')
def electricskateboard():
    return render_template('ElecSkate.html')

@app.route('/Fishing')
def fishing():
    return render_template('Fishing.html')

@app.route('/FishTank')
def fishtank():
    return render_template('fishTank.html')

@app.route('/LEDCube')
def ledcube():
    return render_template('LEDCube.html')

@app.route('/LEDFootwells')
def ledfootwells():
    return render_template('LEDFootwells.html')

@app.route('/Photography')
def photography():
    return render_template('Photography.html')

@app.route('/RoboticQuadruped')
def robot():
    return render_template('robotQuad.html')

@app.route('/JosephHodsonResume.pdf')
def pathToResume():
    try:
        return send_file('./JosephHodsonResume.pdf', attachment_filename='JosephHodsonResume.pdf')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=443, threaded=True, ssl_context=('/etc/letsencrypt/live/joeyhodson.com/fullchain.pem', '/etc/letsencrypt/live/joeyhodson.com/privkey.pem'))
    #app.run(host = '0.0.0.0', port=80, threaded=True) http requests