from flask import Flask, render_template

app = Flask(__name__)

@app.route('/debug')
def debug():
    return render_template('server_up.html',title='Debug', content='Server is Up!', paragraph='The Server is Up and running, if you expected someting diferent than this erase cache in your web browser')

@app.route('/')
def root():
    return debug()

if __name__ == '__main__':
    app.run(debug=True,port=2357)