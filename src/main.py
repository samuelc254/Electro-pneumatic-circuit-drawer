import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from drawer import Drawer
import utils

tags_metadata = [
    {
        'name': 'sequencia',
        'description': 'Retorna imagem do circuito com a sequência escolhida.'
    }
]

app = FastAPI()


def main():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host='localhost', port=port, debug=True)


@app.get('/')
async def homepage():
    return HTMLResponse('<p>a</p>')


@app.get('/favicon.ico')
async def favicon():
    return FileResponse('images/ico.ico')


@app.get('/{sequencia}')
async def gerador(sequencia: str):
    utils.apagar_antigos()

    draw = Drawer(sequencia=sequencia, debug=False)
    draw.cadeia_simples()
    try:
        file = open(f'images/{sequencia}.svg', 'rb')
        a = StreamingResponse(file)
        return a
    except Exception as error:
        print(str(error))
        pass

if __name__ == "__main__":
    main()
