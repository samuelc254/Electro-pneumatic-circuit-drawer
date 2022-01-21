from flask import Flask, render_template

app = Flask('Eletropnumatic circuit drawer')


@app.route('/')
def homepage():
    return render_template("homepage.html")


@app.route('/gerar/<sequencia>')
def gerador(sequencia):
    return 'arroz com ' + sequencia


app.run(debug=True)
