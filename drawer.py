import svgwrite


class Drawer:
    def __init__(self, sequencia: str, debug: bool):

        self.nome = sequencia
        self.sequencia = list(str.lower(sequencia))
        self.N_etapas = int((len(self.sequencia))/2) + 1

        self.scale = str((self.N_etapas * 100) + 300)
        self.dwg = svgwrite.Drawing('circuit.svg',
                                    size=(self.scale, '350'))

        self.cor = 'black'
        self.tamanho = 10
        self.espacamento = self.tamanho * 5

        self.y_global = self.espacamento
        self.x_global = self.espacamento * 1.5
        self.x_passo = self.x_global
        self.y_passo = self.y_global

        self.debug = debug

    def N_atuador(self, letra: str) -> str:
        """
        Numera o sensor de cada atuador conforme sua letra

        Parametros
        ----------
        letra: str
          Letra do atuador

        Retorno
        -------
        str
          Numero do sensor
        """

        letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                  'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                  'y', 'z']

        return str(letras.index(letra) + 1)

    def A_atuador(self, sinal: str) -> str:
        """
        Numera o sensor de cada atuador conforme seu sinal

        Parametros
        ----------
        sinal: str
            Sinal do movimento

        Retorno
        -------
        str
            Numero do sensor
        """

        if sinal == '-':
            return '1'
        elif sinal == '+':
            return '2'

    def plug(self, text: str, y: int):
        self.dwg.add(
            self.dwg.circle(
                    (self.espacamento / 3.7, y),
                    self.tamanho / 2.5,
                    stroke=self.cor,
                    fill='none'
                )
            )
        self.dwg.add(
            self.dwg.line(
                (self.espacamento / 3, y),
                (self.espacamento, y),
                stroke=self.cor
                )
            )
        self.dwg.add(
            self.dwg.text(
                text,
                insert=(self.espacamento / 2.5, y - self.espacamento / 16),
                fill=self.cor
            )
        )

    def Na(self, x: int, y: int, name: str) -> None:
        """
        Desenha o contato normalmente aberto
                Parametros
        ----------
        x: int
            Posição x do contato
        y: int
            Posição y do contato
        name: str
            Nome do contato
                Retorno
        -------
        None
        """
        # Linha superior
        self.dwg.add(
            self.dwg.line(
                (x, y),
                (x, y + self.tamanho * 2.5),
                stroke=self.cor
            )
        )
        # Linha do contato
        self.dwg.add(
            self.dwg.line(
                (x - self.tamanho, y + self.tamanho * 2.5),
                (x, y + self.tamanho * 5),
                stroke=self.cor
            )
        )
        # Linha inferior
        self.dwg.add(
            self.dwg.line(
                (x, y + self.tamanho * 5),
                (x, y + self.tamanho * 7.5),
                stroke=self.cor
            )
        )
        # Nome do contato
        self.dwg.add(
            self.dwg.text(
                name,
                insert=(x + self.tamanho * 0.6, y + self.tamanho * 3.6),
                fill=self.cor
            )
        )
        self.y_passo += self.tamanho * 7.5

    def Nf(self, x: int, y: int, name: str) -> None:
        """
        Desenha o contato normalmente fechado

        Parametros
        ----------
        x: int
            Posição x do contato
        y: int
            Posição y do contato
        name: str
            Nome do contato

        Retorno
        -------
        None
        """
        # Linha superior
        self.dwg.add(
            self.dwg.line(
                (x, y),
                (x, y + self.tamanho * 2.5),
                stroke=self.cor
            )
        )

        # Linha do contato fechado
        self.dwg.add(
            self.dwg.line(
                (x + self.tamanho, y + self.tamanho * 2.5),
                (x, y + self.tamanho * 2.5),
                stroke=self.cor
            )
        )

        # Linha do contato
        self.dwg.add(
            self.dwg.line(
                (x + self.tamanho, y + self.tamanho * 2.5),
                (x, y + self.tamanho * 5),
                stroke=self.cor
            )
        )

        # Linha inferior
        self.dwg.add(
            self.dwg.line(
                (x, y + self.tamanho * 5),
                (x, y + self.tamanho * 7.5),
                stroke=self.cor
            )
        )

        # Nome do contato
        self.dwg.add(
            self.dwg.text(
                name,
                insert=(x + self.tamanho * 1.6, y + self.tamanho * 3.6),
                fill=self.cor
            )
        )
        self.y_passo += self.tamanho * 7.5

    def contator(self, x: int, y: int, name: str) -> None:
        """
        Desenha a bobina do contator

        Parametros
        ----------
        x: int
            Posição x do contator
        y: int
            Posição y do contator
        name: str
            Nome do contator

        Retorno
        -------
        None
        """
        # Linha superior
        self.dwg.add(self.dwg.line(
            (x, y),
            (x, y + self.tamanho * 2),
            stroke=self.cor))

        # Contator
        self.dwg.add(
            self.dwg.rect(
                insert=(x - self.tamanho * 2, y + self.tamanho * 2),
                size=(self.tamanho * 4, self.tamanho * 2),
                stroke=self.cor,
                fill='none'
            )
        )

        # Linha inferior
        self.dwg.add(
            self.dwg.line(
                (x, y + self.tamanho * 4),
                (x, y + self.tamanho * 6),
                stroke=self.cor
            )
        )

        # Nome do contator
        self.dwg.add(
            self.dwg.text(
                name,
                insert=(x + self.tamanho * 2.6, y + self.tamanho * 3),
                fill=self.cor
            )
        )
        self.y_passo += self.tamanho * 6

    def cadeia_simples(self):  # Função para desenhar a cadeia simples

        self.plug('24V', self.espacamento)
        self.plug('0V', self.espacamento * 5.2)

        for i in range(self.N_etapas):

            if i != self.N_etapas - 1:
                self.dwg.add(self.dwg.circle((self.x_passo, self.y_passo),
                                             self.tamanho/4))

            if i == 0:
                self.Na(self.x_passo, self.y_passo, 'S1')  # Ativa
                if i != self.N_etapas - 1:
                    self.dwg.add(self.dwg.circle((self.x_passo, self.y_passo),
                                 self.tamanho/4))
                # Habilita
                self.Nf(self.x_passo, self.y_passo, 'K'+str(self.N_etapas))
            else:
                self.Na(
                    self.x_passo,
                    self.y_passo,
                    str(self.N_atuador((self.sequencia[(i*2)-2]))) + 'S' +
                    str(self.A_atuador((self.sequencia[(i*2)-1])))
                )  # Ativa

                if i != self.N_etapas - 1:
                    self.dwg.add(self.dwg.circle((self.x_passo, self.y_passo),
                                 self.tamanho/4))
                self.Na(self.x_passo, self.y_passo, 'K'+str(i))  # Habilita

            self.contator(self.x_passo, self.y_passo, 'K'+str(i + 1))

            if i != self.N_etapas - 1:  # Sela
                self.dwg.add(self.dwg.circle((self.x_passo, self.y_passo),
                                             self.tamanho/4))

                self.x_passo += self.espacamento
                self.y_passo = self.y_global

                self.dwg.add(self.dwg.circle((self.x_passo, self.y_passo),
                                             self.tamanho/4))
                self.Na(self.x_passo, self.y_passo, 'K'+str(i + 1))
                self.dwg.add(
                    self.dwg.line(
                        (self.x_passo, self.y_passo),
                        (self.x_passo - self.espacamento, self.y_passo),
                        stroke=self.cor
                    )
                )

            else:  # Desenha a linha superior e a inferior
                self.dwg.add(
                    self.dwg.line(
                        (self.espacamento, self.y_global),
                        (self.x_passo, self.y_global),
                        stroke=self.cor
                    )
                )
                self.dwg.add(
                    self.dwg.line(
                        (self.x_passo, self.y_passo),
                        (self.espacamento, self.y_passo),
                        stroke=self.cor
                    )
                )

            self.x_global += self.espacamento*2
            self.x_passo = self.x_global
            self.y_passo = self.y_global

        if self.debug:
            self.dwg.add(
                self.dwg.text(
                    self.sequencia,
                    insert=(self.espacamento * 7, self.espacamento / 1.8),
                    fill=self.cor
                )
            )

        self.dwg.add(
            self.dwg.text(
                'https://github.com/' +
                'samuelc254/Electro-pneumatic-circuit-drawer',
                insert=(self.espacamento, self.espacamento * 6),
                fill=self.cor
            )
        )

        self.dwg.add(
            self.dwg.text(
                'Electro-pneumatic circuit drawer v0.1.3',
                insert=(self.espacamento, self.espacamento / 2.2),
                fill=self.cor
            )
        )

        self.dwg.saveas(
            f'./images/{"".join(self.sequencia)}.svg',
            pretty=True
        )
