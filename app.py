from flask import Flask, render_template,request
from mod_prepare_meditation import prepare_meditation
from mod_feedback import feedback
from mod_register import register
from mod_login_logout import login

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')

app.add_url_rule('/prepare_meditation', 'prepare_meditation', prepare_meditation, methods=['GET', 'POST'])

@app.route('/start_meditation')
def start_meditation():
    audio_file = request.args.get('audio_file')
    return render_template('start_meditation.html', audio_file=audio_file)

@app.route('/meditation_end')
def meditation_end():
    return render_template('meditation_end.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
      return render_template('register.html' )

if __name__ == '__main__':
    app.run(debug=True)
