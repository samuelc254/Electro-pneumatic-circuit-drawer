import os
from flask import Flask, render_template, send_file
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


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_file('images/ico.ico')


@app.route('/circuit.svg', methods=['GET'])
def circuitsvg():
    return send_file('images/circuit.svg')


@app.route('/debug/circuit.svg', methods=['GET'])
def dbgcircuitsvg():
    return send_file('images/circuit.svg')


@app.route('/<sequencia>', methods=['GET'])
def gerador(sequencia):
    draw = drawer(sequencia=sequencia, debug=False)
    draw.cadeia_simples()
    return render_template('circuit_page.html')


@app.route('/debug/<sequencia>', methods=['GET'])
def debug(sequencia):
    draw = drawer(sequencia=sequencia, debug=True)
    draw.cadeia_simples()
    return render_template('circuit_page.html')
    '''
    try:
        return send_file(
            'images/circuit.svg',
            as_attachment=True)
    except Exception as error:
        return(str(error))
    '''


if __name__ == "__main__":
    main()
