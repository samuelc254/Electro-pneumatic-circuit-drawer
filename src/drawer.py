import svgwrite

dwg = svgwrite.Drawing('circuit.svg', size=("500%", "500%"))

cor = "black"
tamanho = 10
espaçamento = tamanho * 5

vezes = 0

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
        dwg.add(dwg.line((x_passo, y_passo), (x_passo - espaçamento, y_passo), stroke=cor))
    else:
        dwg.add(dwg.line((espaçamento, y_global), (x_passo, y_global), stroke=cor))
        dwg.add(dwg.line((x_passo, y_passo), (espaçamento, y_passo), stroke=cor))
    
    x_global += espaçamento*2
    x_passo = x_global
    y_passo = y_global


def espacar():

  global x_passo
  global y_passo
  global N_etapas_p
  global N_etapas_p2

  if N_etapas_p > N_etapas_p2:
    espacos = N_etapas_p 
  else:
    espacos = N_etapas_p2

  for x in range(int(espacos)-1):
        dwg.add(dwg.line((x_passo, y_passo), (x_passo , y_passo+(tamanho * 7.5)), stroke=cor))
        y_passo += (tamanho * 7.5)


def etapa_p(item):

  global x_global
  global y_global
  global x_passo
  global y_passo

  global diagrama
  global N_etapas
  global N_etapas_p
  global vezes

  if vezes == 0:
    if item != "(":  
      vezes += 1

      # Ativa
      Na(x_passo, y_passo, "S1") 
      espacar()

      # Habilita
      Nf(x_passo, y_passo, "K"+str(N_etapas)) 
      contator(x_passo, y_passo, "K"+str(vezes))

      # selo
      x_passo += espaçamento
      y_passo = y_global
      Na(x_passo, y_passo, "K"+str(vezes))
      espacar()
      dwg.add(dwg.line((x_passo, y_passo), (x_passo - espaçamento, y_passo), stroke=cor))


# ----------------------------Inicio----------------------------
print("Electro-pneumatic circuit drawer v0.1.2")
print("Programa feito para desenhar circuitos eletropneumáticos de cadeia estacionaria")
print("para desenhar insira um diagramas como: a+b-a-b+")
print("Criado por: Samuel Oliveira Costa")
print("Repositório do projeto: https://github.com/samuelc254/Electro-pneumatic-circuit-drawer")
print("")

diagrama = input("Insira o diagrama: ")
diagrama = list(str.lower(diagrama))

check_p = 0
for caracteres in diagrama:
  if caracteres == "(" or caracteres == ")":
    check_p = 1

if check_p == 0:
  N_etapas = int(len(diagrama)/2) + 1

  i = 1
  j = 0
  while i <= N_etapas:
      etapa(i,j)
      i += 1
      j += 2
else:
  check_p = 0
  N_etapas_p = 0
  N_etapas_p2 = 0
  for caracteres in diagrama:
    if caracteres == "(" and check_p == 0:
      check_p = 1
    elif caracteres == ")" and check_p == 1:
      check_p = 2
    elif check_p == 1 :
      N_etapas_p += 1
    elif caracteres == "(" and check_p == 2:
      check_p = 3
    elif caracteres == ")" and check_p == 3:
      check_p = 4
    elif check_p == 3:
      N_etapas_p2 += 1
    
  N_etapas = int(((int(len(diagrama))-(N_etapas_p + N_etapas_p2))/2)+1)
  N_etapas_p = (N_etapas_p/2)
  N_etapas_p2 = (N_etapas_p2/2)
  for caracteres in diagrama:
    etapa_p(caracteres)


#print("O desenho terá: ", N_etapas_p, " etapas dentro do ()")
print("O desenho terá: ", N_etapas, " etapas")

#dwg.add(dwg.text("https://github.com/samuelc254/Electro-pneumatic-circuit-drawer", insert=(espaçamento, espaçamento * 6), fill=cor))
dwg.save()
input("Circuito desenhado com sucesso!")