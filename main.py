from flask import Flask

app = Flask(__name__)

@app.route('/debug')
def debug():
    return 'Server is Up!'

@app.route('/')
def root():
    return debug()

if __name__ == '__main__':
    app.run(debug=True,port=2357)