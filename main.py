import os
from flask import Flask, render_template

app = Flask('Eletropnumatic circuit drawer')


def main():
    port = int(os.environ.get('PORT', 5000))
    app.run(
        debug=True,
        host='0.0.0.0',
        port=port,
        )


@app.route('/')
def gerador():
    return render_template('homepage.html')


if __name__ == "__main__":
    main()
