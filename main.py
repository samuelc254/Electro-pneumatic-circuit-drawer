from flask import Flask

app = Flask('Eletropnumatic circuit drawer')

@app.route('/')
def homepage():
    return 'Hello World'

app.run(debug=True)