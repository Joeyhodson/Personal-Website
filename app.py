from flask import Flask, render_template, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/JosephHodsonResume.pdf')
def path():
    try:
        return send_file('./JosephHodsonResume.pdf', attachment_filename='JosephHodsonResume.pdf')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')