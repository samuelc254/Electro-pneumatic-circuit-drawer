import os

def apagar_antigos():
    diretorio = os.listdir('./images/')
    for arquivo in diretorio:
        if arquivo.endswith('.svg'):
            try:
                os.remove(f'./images/{arquivo}')
            except Exception as error:
                a = False
                if a:
                    print(error)
