import svgwrite

dwg = svgwrite.Drawing('circuit.svg', size=("500%","500%")) 

cor = "black"
nome = "k1"
tamanho = 10
espaçamento = tamanho * 5

y_global = espaçamento
x_global = espaçamento
x_passo = x_global
y_passo = y_global

def Na(x,y,name): # Desenho de contato normalmente aberto
    global y_passo 
    dwg.add(dwg.line((x, y), (x, y + tamanho * 2.5), stroke=cor))
    dwg.add(dwg.line((x - tamanho, y + tamanho * 2.5), (x, y + tamanho * 5), stroke=cor))
    dwg.add(dwg.line((x, y + tamanho * 5), (x, y + tamanho * 7.5), stroke=cor))
    dwg.add(dwg.text(name, insert=(x + tamanho * 0.6, y + tamanho * 3.6), fill=cor))
    y_passo += tamanho * 7.5

def Nf(x,y,name): # Desenho de contato normalmente fechado
    global y_passo 
    dwg.add(dwg.line((x, y), (x, y + tamanho * 2.5), stroke=cor))
    dwg.add(dwg.line((x + tamanho, y + tamanho * 2.5), (x, y + tamanho * 2.5), stroke=cor))
    dwg.add(dwg.line((x + tamanho, y + tamanho * 2.5), (x, y + tamanho * 5), stroke=cor))
    dwg.add(dwg.line((x, y + tamanho * 5), (x, y + tamanho * 7.5), stroke=cor))
    dwg.add(dwg.text(name, insert=(x + tamanho * 1.6, y + tamanho * 3.6), fill=cor))
    y_passo += tamanho * 7.5

def contator(x,y,name): # Desenho do contator 
    global y_passo 
    dwg.add(dwg.line((x, y), (x, y + tamanho * 2), stroke=cor))
    dwg.add(dwg.line((x - tamanho * 2, y + tamanho * 2), (x + tamanho * 2, y + tamanho * 2), stroke=cor))
    dwg.add(dwg.line((x - tamanho * 2, y + tamanho * 2), (x - tamanho * 2, y + tamanho * 4), stroke=cor))
    dwg.add(dwg.line((x + tamanho * 2, y + tamanho * 2), (x + tamanho * 2, y + tamanho * 4), stroke=cor))
    dwg.add(dwg.line((x - tamanho * 2, y + tamanho * 4), (x + tamanho * 2, y + tamanho * 4), stroke=cor))
    dwg.add(dwg.line((x, y + tamanho * 4), (x, y + tamanho * 6), stroke=cor))
    dwg.add(dwg.text(name, insert=(x + tamanho * 2.6, y + tamanho * 3), fill=cor))
    y_passo += tamanho * 6

def etapa(n1): # Função para desenhar cada etapa 

    global x_global 
    global y_global
    global x_passo
    global y_passo

    if n1 == 1: # Ativa
        Na(x_passo,y_passo,"S1")
    else:
        Na(x_passo,y_passo,"K"+str(n1))

    if n1 == 1: # Habilita
        Nf(x_passo,y_passo,"K"+str(N_etapas))
    else:
        Na(x_passo,y_passo,"K"+str(n1-1))

    contator(x_passo,y_passo,"K"+str(n1))

    x_global += espaçamento*2
    x_passo += espaçamento
    y_passo = y_global

    if n1 != N_etapas:
        dwg.add(dwg.line((x_passo, y_passo), (x_passo - espaçamento, y_passo), stroke=cor))
        Na(x_passo,y_passo,"K"+str(n1))
        dwg.add(dwg.line((x_passo, y_passo), (x_passo - espaçamento, y_passo), stroke=cor))



diagrama = input("Insira o diagrama: ")
diagrama = list(diagrama)
N_etapas = int(len(diagrama)/2) + 1

print("O desenho terá: ", N_etapas ," etapas")
print(diagrama)

etapa(4)
dwg.save()
