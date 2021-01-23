
from flask import Flask, render_template, send_file, redirect, request
from gevent.pywsgi import WSGIServer
import logging
import logging.handlers as handlers



app = Flask(__name__)


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

@app.route('/Website')
def website():
    return render_template('website.html')

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

    # Development Server
    #app.run(host = '0.0.0.0', port=443, threaded=True, ssl_context=('/etc/letsencrypt/live/joeyhodson.com/fullchain.pem', '/etc/letsencrypt/live/joeyhodson.com/privkey.pem'))
    #app.run(host = '0.0.0.0', port=80, threaded=True)

    #Localhost
    #app.run(host='0.0.0.0', debug=True, port=80, threaded=True)

    # Production Server
    logger = logging.getLogger('MainProgram')
    logger.setLevel(10)
    logHandler = handlers.RotatingFileHandler('/personalserver/logs.txt', maxBytes = 1000000, backupCount = 1) #sets log to cap off at 1MB, logs.txt.1 will be created after.
    logger.addHandler(logHandler)
    logger.info("Logging configuration done")

    http_server = WSGIServer(('', 80), app, log = logger)
    http_server.serve_forever()