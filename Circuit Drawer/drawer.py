import svgwrite

dwg = svgwrite.Drawing('circuit.svg', size=("500%", "500%"))

cor = "black"
tamanho = 10
espaçamento = tamanho * 5

y_global = espaçamento
x_global = espaçamento
x_passo = x_global
y_passo = y_global


def N_atuador(letra):  # Numera o sensor de cada atuador conforme sua letra (Numero do atuador)
    if letra == "a":
        return "1"
    elif letra == "b":
        return "2"
    elif letra == "c":
        return "3"
    elif letra == "d":
        return "4"
    elif letra == "e":
        return "5"
    elif letra == "f":
        return "6"


def A_atuador(sinal):  # Numera o sensor de cada atuador conforme seu sinal (Avanço do atuador)
    if sinal == "-":
        return "1"
    elif sinal == "+":
        return "2"


def Na(x, y, name):  # Desenho de contato normalmente aberto
    global y_passo
    dwg.add(dwg.line((x, y), (x, y + tamanho * 2.5), stroke=cor))
    dwg.add(dwg.line((x - tamanho, y + tamanho * 2.5),
            (x, y + tamanho * 5), stroke=cor))
    dwg.add(dwg.line((x, y + tamanho * 5), (x, y + tamanho * 7.5), stroke=cor))
    dwg.add(dwg.text(name, insert=(x + tamanho * 0.6, y + tamanho * 3.6), fill=cor))
    y_passo += tamanho * 7.5


def Nf(x, y, name):  # Desenho de contato normalmente fechado
    global y_passo
    dwg.add(dwg.line((x, y), (x, y + tamanho * 2.5), stroke=cor))
    dwg.add(dwg.line((x + tamanho, y + tamanho * 2.5),
            (x, y + tamanho * 2.5), stroke=cor))
    dwg.add(dwg.line((x + tamanho, y + tamanho * 2.5),
            (x, y + tamanho * 5), stroke=cor))
    dwg.add(dwg.line((x, y + tamanho * 5), (x, y + tamanho * 7.5), stroke=cor))
    dwg.add(dwg.text(name, insert=(x + tamanho * 1.6, y + tamanho * 3.6), fill=cor))
    y_passo += tamanho * 7.5


def contator(x, y, name):  # Desenho do contator
    global y_passo
    dwg.add(dwg.line((x, y), (x, y + tamanho * 2), stroke=cor))
    dwg.add(dwg.line((x - tamanho * 2, y + tamanho * 2),
            (x + tamanho * 2, y + tamanho * 2), stroke=cor))
    dwg.add(dwg.line((x - tamanho * 2, y + tamanho * 2),
            (x - tamanho * 2, y + tamanho * 4), stroke=cor))
    dwg.add(dwg.line((x + tamanho * 2, y + tamanho * 2),
            (x + tamanho * 2, y + tamanho * 4), stroke=cor))
    dwg.add(dwg.line((x - tamanho * 2, y + tamanho * 4),
            (x + tamanho * 2, y + tamanho * 4), stroke=cor))
    dwg.add(dwg.line((x, y + tamanho * 4), (x, y + tamanho * 6), stroke=cor))
    dwg.add(dwg.text(name, insert=(x + tamanho * 2.6, y + tamanho * 3), fill=cor))
    y_passo += tamanho * 6


def etapa(n1,n2):  # Função para desenhar cada etapa

    global x_global
    global y_global
    global x_passo
    global y_passo

    global diagrama
    global N_etapas

    if n1 != N_etapas:
        dwg.add(dwg.circle((x_passo, y_passo), tamanho/4 ))

    if n1 == 1:  
        Na(x_passo, y_passo, "S1") # Ativa
        if n1 != N_etapas: dwg.add(dwg.circle((x_passo, y_passo), tamanho/4 ))
        Nf(x_passo, y_passo, "K"+str(N_etapas)) # Habilita
    else:
        Na(x_passo, y_passo, (str(N_atuador(
            diagrama[n2-2]))) + "S" + str(A_atuador(diagrama[n2-1]))) # Ativa
        if n1 != N_etapas: dwg.add(dwg.circle((x_passo, y_passo), tamanho/4 ))
        Na(x_passo, y_passo, "K"+str(n1-1)) # Habilita


    contator(x_passo, y_passo, "K"+str(n1))

    if n1 != N_etapas:  # Sela
        dwg.add(dwg.circle((x_passo, y_passo), tamanho/4 ))

        x_passo += espaçamento
        y_passo = y_global

        dwg.add(dwg.circle((x_passo, y_passo), tamanho/4 ))
        Na(x_passo, y_passo, "K"+str(n1))
        dwg.add(dwg.line((x_passo, y_passo),
                (x_passo - espaçamento, y_passo), stroke=cor))
    else:
        dwg.add(dwg.line((espaçamento, y_global), (x_passo, y_global), stroke=cor))
        dwg.add(dwg.line((x_passo, y_passo), (espaçamento, y_passo), stroke=cor))
    
    x_global += espaçamento*2
    x_passo = x_global
    y_passo = y_global


# ----------------------------Inicio----------------------------
print("Electro-pneumatic circuit drawer v0.1.2")
print("Programa feito para desenhar circuitos eletropneumáticos de cadeia estacionaria")
print("para desenhar insira um diagramas como: a+b-a-b+")
print("Criado por: Samuel Oliveira")
print("Repositório do projeto: https://github.com/samuelc254/Electro-pneumatic-circuit-drawer")
print("")
print("nota: o programa ainda está no inicio de seu desinvolvimento")
print("ainda não é possivel desenhar circuitos muito complexos")
print("qualquer um interessado em ajudar o projeto é mais que bem vindo!")
print("")

diagrama = input("Insira o diagrama: ")
diagrama = list(str.lower(diagrama))
N_etapas = int(len(diagrama)/2) + 1

print("O desenho terá: ", N_etapas, " etapas")

i = 1
j = 0
while i <= N_etapas:
    etapa(i,j)
    i += 1
    j += 2

dwg.add(dwg.text("https://github.com/samuelc254/Electro-pneumatic-circuit-drawer", insert=(espaçamento, espaçamento * 6), fill=cor))
dwg.save()
input("Circuito desenhado com sucesso!")


