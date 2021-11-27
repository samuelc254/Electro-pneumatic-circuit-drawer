import svgwrite

dwg = svgwrite.Drawing('circuit.svg', profile='tiny') 

cor = "black"
nome = "k1"

x_global = 30
y_global = 100
x_passo = x_global
y_passo = y_global

def Na(x,y,name): # Desenho de contato normalmente aberto
    dwg.add(dwg.line((x, y), (x, y+25), stroke=cor))
    dwg.add(dwg.line((x-10, y+25), (x, y+50), stroke=cor))
    dwg.add(dwg.line((x, y+50), (x, y+75), stroke=cor))
    dwg.add(dwg.text(name, insert=(x+6, y+36), fill=cor))
    global y_passo 
    y_passo += 75

def Nf(x,y,name): # Desenho de contato normalmente fechado
    dwg.add(dwg.line((x, y), (x, y+25), stroke=cor))
    dwg.add(dwg.line((x+10, y+25), (x, y+25), stroke=cor))
    dwg.add(dwg.line((x+10, y+25), (x, y+50), stroke=cor))
    dwg.add(dwg.line((x, y+50), (x, y+75), stroke=cor))
    dwg.add(dwg.text(name, insert=(x+16, y+36), fill=cor))
    global y_passo 
    y_passo += 75

def contator(x,y,name): # Desenho do contator 
    dwg.add(dwg.line((x, y), (x, y+20), stroke=cor))
    dwg.add(dwg.line((x-20, y+20), (x+20, y+20), stroke=cor))
    dwg.add(dwg.line((x-20, y+20), (x-20, y+40), stroke=cor))
    dwg.add(dwg.line((x+20, y+20), (x+20, y+40), stroke=cor))
    dwg.add(dwg.line((x-20, y+40), (x+20, y+40), stroke=cor))
    dwg.add(dwg.line((x, y+40), (x, y+60), stroke=cor))
    dwg.add(dwg.text(name, insert=(x+26, y+36), fill=cor))
    global y_passo 
    y_passo += 60


#diagrama = input("Insira o diagrama: ")

Na(x_global, y_passo, nome)
Nf(x_global, y_passo, "k2")
contator(x_global, y_passo, nome)
dwg.save()
