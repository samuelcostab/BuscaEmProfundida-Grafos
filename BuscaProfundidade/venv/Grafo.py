class Vertice:
    def __init__(self, rotuloVertice):
        self.rotulo = rotuloVertice
        self.qtdLigacoes = 0
        self.tempoEntrada = 0
        self.tempoSaida = 0

    def setTempoEntrada(self, entrada):
        self.tempoEntrada = entrada

    def getTempoEntrada(self):
        return self.tempoEntrada

    def setTempoSaida(self, saida):
        self.tempoSaida = saida

    def getTempoSaida(self):
        return self.tempoSaida

    def getRotulo(self):
        return self.rotulo

    def setCor(self, corV):
        ## B -- Branco C -- Cinza P -- Preto
        self.cor = corV

    def getCor(self):
        return self.cor

    def setQtdLigacoes(self, qtdLigacoes):
        self.qtdLigacoes = qtdLigacoes

    def getQtdLigacoes(self):
        return self.qtdLigacoes


class Grafo:
    def __init__(self, numvertices, qtdArestas):
        self.qntdArestas = qtdArestas
        self.numVertices = numvertices
        self.ordemTopologia = []
        self.classificacaoArestas = []
        self.listaVertices = []
        self.matrizAdjacencia = self.gerarMatriz()
        self.tempo = 1
        self.componentesConexas = []

    def gerarMatriz(self):
        matriz = []
        for j in range(self.numVertices):
            linhaMatriz = []
            for i in range(self.numVertices):
                linhaMatriz.append(0)
            matriz.append(linhaMatriz)

        return matriz

    def addVertice(self, rotulo):
        self.listaVertices.append(Vertice(rotulo))

    def addAdjacente(self, inicio, fim):
        if (self.matrizAdjacencia[inicio][fim] == 0):
            self.matrizAdjacencia[inicio][fim] = 1

    def imprimeMatriz(self):
        for i in range(self.numVertices):
            print('   ' + str(self.listaVertices[i].getRotulo()), end=''),
        print()
        for i in range(self.numVertices):
            print(self.listaVertices[i].getRotulo(), end='')
            for j in range(self.numVertices):
                if (self.matrizAdjacencia[i][j] > 0):
                    print('  ' + str(self.matrizAdjacencia[i][j]), end=' ')
                else:
                    print('  ' + str(self.matrizAdjacencia[i][j]), end=' ')
            print()

    def localizaVertice(self, rotuloPassado):
        for i in range(len(self.listaVertices)):
            if (self.listaVertices[i].getRotulo() == rotuloPassado):
                return i

        return -1

    def contarLigacoes(self):
        for i in range(self.numVertices):
            contadorLigacoesVertice = 0
            for j in range(self.numVertices):
                if (self.matrizAdjacencia[i][j] != 0):  ##Se o Vertice incide em outro
                    contadorLigacoesVertice += 1

                if (self.matrizAdjacencia[j][i] == 1):  ##Se o Vertice é incidido por outro
                    contadorLigacoesVertice += 1

            if (contadorLigacoesVertice > 0):
                self.listaVertices[i].setQtdLigacoes(contadorLigacoesVertice)

    def procurarVerticeInicial(self):
        verticeInicial = self.listaVertices[0]
        qtdLigacoes = 0
        for vertice in self.listaVertices:
            if (vertice.getQtdLigacoes() > 0):
                if (vertice.getQtdLigacoes() > verticeInicial.getQtdLigacoes()) and (vertice.getCor() == "B"):
                    verticeInicial = vertice
            else:
                verticeInicial = vertice

        return verticeInicial

    def obtemAdjacente(self, numV, matriz):
        for i in range(self.numVertices):
            if (matriz[numV][i] == 1) and (self.listaVertices[i].getCor() == "B"):
                return i  ##retorna i se o vertice for NaoVisitado

        for j in range(self.numVertices):
            if (matriz[numV][j] == 1) and (self.listaVertices[j].getCor() == "C"):
                return j  ##retorna j se o vertice for Visitado

        return -1

    ##tem que programar o Metodo de Contar Componentes Conexas

    def contaComponentesConexas(self):
        matrizInversa = self.gerarMatriz()
        for i in range(self.numVertices):
            for j in range(self.numVertices):
                if (self.matrizAdjacencia[i][j] == 1):
                    matrizInversa[i][j] = 0
                    matrizInversa[j][i] = 1


        pilhaVertices = []

        ##ERRO NAS ITERAÇÕES NAO EH PRA USAR A ORDEM DOS VERTICES NORMAL
        for vertice in self.listaVertices:
            ##print("Rotulo vertice {} cor {}".format(vertice.getRotulo(), vertice.getCor()))
            if (vertice.getCor() == "B" or vertice.getCor() == "C"):
                if (pilhaVertices.__contains__(vertice) == False):
                    pilhaVertices.append(vertice)


                vertice.setCor("P")

                indexAdjacente = self.obtemAdjacente(self.localizaVertice(vertice.getRotulo()), matrizInversa)
                if (indexAdjacente == -1):  ##Se nao houver adjacente, o vertice ja é uma componente
                    s = ""
                    print()
                    for comp in pilhaVertices:
                        s += str(comp.getRotulo()) + " "
                    print(s)
                    self.componentesConexas.append(pilhaVertices)
                    pilhaVertices.clear()
                    continue
                else:
                    verticeAdjacente = self.listaVertices[indexAdjacente]
                    verticeAdjacente.setCor("C")
                    pilhaVertices.append(verticeAdjacente)
                    iVraiz = self.localizaVertice(pilhaVertices[0].getRotulo())  ##id vertice raiz
                    iAd = self.obtemAdjacente(self.localizaVertice(verticeAdjacente), matrizInversa)  ##id vertice adjacente

                    if (matrizInversa[iAd][iVraiz] == 1):
                        self.componentesConexas.append(pilhaVertices)
                        pilhaVertices.clear()
                        continue

    def buscarEmProfundidade(self, controle):
        if (controle == 0):
            for vertice in self.listaVertices:
                ##Colorindo todos os vertices para Branco
                vertice.setCor("B")

        verticeInicial = self.procurarVerticeInicial()
        verticeInicial.setCor("C")
        pilha = []
        pilha.append(verticeInicial)  ##adiciona o vertice que inicia a busca na pilha

        while len(pilha) != 0:
            verticeAnalisar = pilha[len(pilha) - 1]  ##Ultimo elemento da Pilha
            verticeAnalisar.setCor("C")
            if (verticeAnalisar.getTempoEntrada() == 0):  ##Seta o valor de entrada no vertice
                verticeAnalisar.setTempoEntrada(self.tempo)

            self.tempo += 1
            indiceVerticeAnalisar = self.localizaVertice(verticeAnalisar.getRotulo())
            indexVAd = self.obtemAdjacente(indiceVerticeAnalisar,
                                           self.matrizAdjacencia)  ##Retorna o Vertice adjacente ao VerticeAnalisar
            verticeAdjacente = self.listaVertices[indexVAd]

            if (verticeAdjacente.getCor() == "B"):
                self.classificacaoArestas.append((verticeAnalisar.getRotulo(), "ARVORE", verticeAdjacente.getRotulo()))
                pilha.append(verticeAdjacente)
            else:
                inicio = self.localizaVertice(verticeAnalisar.getRotulo())
                fim = self.localizaVertice(verticeAdjacente.getRotulo())
                if (self.matrizAdjacencia[inicio][fim] == 1):
                    if (verticeAdjacente.getCor() == "C"):
                        self.classificacaoArestas.append(
                            (verticeAnalisar.getRotulo(), "RETORNO", verticeAdjacente.getRotulo()))

                    elif (verticeAdjacente.getCor() == "P"):
                        self.classificacaoArestas.append(
                            (verticeAnalisar.getRotulo(), "CRUZAMENTO", verticeAdjacente.getRotulo()))

                verticeAnalisar.setCor("P")
                verticeAnalisar.setTempoSaida(self.tempo)
                self.ordemTopologia.append(verticeAnalisar)

                pilha.pop()

        if (self.procurarVerticeInicial().getCor() == "B"):
            return 1

        for vertice in self.listaVertices:
            vertice.setCor("C")

        return -1

    def imprimeTempoDosVertices(self):
        for vertice in self.listaVertices:
            print("VERTICE: {} {} / {}".format(vertice.getRotulo(), vertice.getTempoEntrada(), vertice.getTempoSaida()))

    def imprimeOrdemTopologica(self):
        self.ordemTopologia
        for vertice in self.ordemTopologia:
            print("VERTICE: {} ".format(vertice.getRotulo()))

    def imprimeClassificacaoArestas(self):
        for aresta in self.classificacaoArestas:
            print(aresta)


if __name__ == "__main__":
    with open("teste.txt") as arquivo:
        linhas = arquivo.read().split("\n")

        primeiraLinha = linhas[0].split(" ")  ##Quebra primeira linha do arquivo
        qtdVertices = int(primeiraLinha[0])
        qtdArestas = int(primeiraLinha[1])
        grafo = Grafo(qtdVertices, qtdArestas)

        for i in range(qtdVertices):
            grafo.addVertice(i + 1)

        for linha in linhas:
            if (linha != linhas[0]):
                linhaSeparada = linha.split(" ")
                v1 = int(linhaSeparada[0])
                v2 = int(linhaSeparada[1])
                inicioAresta = grafo.localizaVertice(v1)
                fimAresta = grafo.localizaVertice(v2)

                grafo.addAdjacente(inicioAresta, fimAresta)

    grafo.imprimeMatriz()

    grafo.contarLigacoes()

    n = 0
    while (n != -1):  ##Enquanto houver vertice para visitar
        n = grafo.buscarEmProfundidade(n)

    ##grafo.imprimeTempoDosVertices()

    grafo.contaComponentesConexas()

    ##grafo.imprimeOrdemTopologica()

    ##grafo.imprimeClassificacaoArestas()
