import os
from flask import Flask, render_template
from drawer import drawer

app = Flask('Eletropnumatic circuit drawer')


def main():
    port = int(os.environ.get('PORT', 5000))
    app.run(
        debug=True,
        host='0.0.0.0',
        port=port,
        )


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/<sequencia>')
def gerador(sequencia):
    draw = drawer(sequencia)
    draw.cadeia_simples()
    svg = open('circuit')
    return str(svg.read())


if __name__ == "__main__":
    main()
