import sys
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

sys.path.append('./src')
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
    uvicorn.run(app)


@app.get('/')
async def homepage():
    return HTMLResponse('<p>operando!</p><p>exemplo de uso https://circuit-drawer.herokuapp.com/a+b-a-b+</p>')


@app.get('/favicon.ico')
async def favicon():
    return FileResponse('images/ico.ico')


@app.get('/{sequencia}')
async def gerador(sequencia: str):
    utils.apagar_antigos()
    try:
        draw = Drawer(sequencia=sequencia, debug=False)
        draw.cadeia_simples()
        file = open(f'images/{sequencia}.svg', 'rb')
        a = StreamingResponse(file)
        return a
    except Exception as error:
        print(str(error))
        return HTMLResponse('<p>ih meu parseiro deu merda</p>')

if __name__ == "__main__":
    main()
