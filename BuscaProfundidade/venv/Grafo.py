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

    def setCor (self, corV):
        ## B -- Branco C -- Cinza P -- Preto
        self.cor = corV

    def getCor(self):
        return self.cor

    def setQtdLigacoes(self, qtdLigacoes):
        self.qtdLigacoes = qtdLigacoes

    def getQtdLigacoes(self):
        return self.qtdLigacoes

class Grafo:
    def __init__(self, numvertices,  qtdArestas):
        self.qntdArestas = qtdArestas
        self.numVertices = numvertices
        self.ordemTopologia = []
        self.classificacaoArestas = []
        self.listaVertices = []
        self.matrizAdjacencia = []

        for j in range(self.numVertices):
            linhaMatriz = []
            for i in range(self.numVertices):
                linhaMatriz.append(0)
            self.matrizAdjacencia.append(linhaMatriz)

    def addVertice(self, rotulo):
        self.listaVertices.append(Vertice(rotulo))

    def addAdjacente(self, inicio, fim):
        if (inicio == fim):
            self.matrizAdjacencia[inicio][fim] = -2

        elif(self.matrizAdjacencia[inicio][fim] == 0) and (self.matrizAdjacencia[fim][inicio] == 0):
            self.matrizAdjacencia[inicio][fim] = -1
            self.matrizAdjacencia[fim][inicio] = 1

        else:
            self.matrizAdjacencia[inicio][fim] = 2
            self.matrizAdjacencia[fim][inicio] = 2

    def imprimeMatriz(self):
        for i in range(self.numVertices):
            print('   ' + str(self.listaVertices[i].getRotulo()), end=''),
        print()
        for i in range(self.numVertices):
            print(self.listaVertices[i].getRotulo(), end='')
            for j in range(self.numVertices):
                if(self.matrizAdjacencia[i][j] > 0):
                    print('   ' + str(self.matrizAdjacencia[i][j]), end='')
                else:
                    print('  ' + str(self.matrizAdjacencia[i][j]), end=' ')
            print()

    def localizaVertice (self, rotuloPassado):
        for i in range (len(self.listaVertices)):
            if self.listaVertices[i].getRotulo() == rotuloPassado:
                return i

        return -1

    def contarLigacoes(self):
        for i in range(self.numVertices):
            contadorLigacoesVertice = 0
            for j in range(self.numVertices):
                if (self.matrizAdjacencia[i][j] != 0):
                    contadorLigacoesVertice += 1

                if(self.matrizAdjacencia[i][j] == 2):
                    contadorLigacoesVertice += 1

            if(contadorLigacoesVertice > 0):
                self.listaVertices[i].setQtdLigacoes(contadorLigacoesVertice)

    def procurarVerticeInicial(self):
        verticeInicial = self.listaVertices[0]
        for vertice in self.listaVertices:
            if (vertice.getQtdLigacoes() > verticeInicial.getQtdLigacoes()) and (vertice.getCor() == "B"):
                verticeInicial = vertice

        return verticeInicial

    def obtemAdjacenteNaoVisitado(self, numV):
        ##Método para buscar o primeiro adjacente ainda não visitado
        ##Retorna o INDICE do vertice
        for i in range(self.numVertices):
            if (self.matrizAdjacencia[numV][i] == -1 or self.matrizAdjacencia[numV][i] == 2) and (self.listaVertices[i].getCor() == "B"):
                return i

        return -1

    def obtemAdjacenteVisitado(self,numV):
        for i in range(self.numVertices):
            if (self.matrizAdjacencia[numV][i] == -1 or self.matrizAdjacencia[numV][i] == 2) and (self.listaVertices[i].getCor() == "C"):
                return i

        return -1

    def buscarEmProfundidade (self):
        for vertice in self.listaVertices:
            ##Colorindo todos os vertices para Branco
            vertice.setCor("B")

        verticeInicial = self.procurarVerticeInicial()
        verticeInicial.setCor("C")
        pilha = []
        pilha.append(verticeInicial) ##adiciona o vertice que inicia a busca na pilha
        tempo = 1
        while len(pilha) != 0:
            verticeAnalisar = pilha[len(pilha) - 1] ##Ultimo elemento da Pilha
            print("verticeAnalisar {}".format(verticeAnalisar.getRotulo()))
            if(verticeAnalisar.getTempoEntrada() == 0):##Seta o valor de entrada no vertice
                verticeAnalisar.setTempoEntrada(tempo)

            tempo += 1

            indexVAd = self.obtemAdjacenteNaoVisitado(self.localizaVertice(verticeAnalisar.getRotulo()))##Retorna o Vertice adjacente ao VerticeAnalisar
            if(indexVAd != -1):
                verticeAdjacente = self.listaVertices[indexVAd]

            else:
                indexVAd = self.obtemAdjacenteVisitado(self.localizaVertice(verticeAnalisar.getRotulo()))  ##Retorna o Vertice adjacente ao VerticeAnalisar

                verticeAdjacente = self.listaVertices[indexVAd]
                print("indice do vertice adjacente vistado:{} rotulo {}".format(indexVAd, verticeAdjacente.getRotulo()))

            if (verticeAdjacente.getCor() == "B"):
                self.classificacaoArestas.append((verticeAnalisar.getRotulo(), "ARVORE", verticeAdjacente.getRotulo()))
                verticeAdjacente.setCor("C")
                pilha.append(verticeAdjacente)
            else:
                inicio = self.localizaVertice(verticeAnalisar.getRotulo())
                fim = self.localizaVertice(verticeAdjacente.getRotulo())
                if (self.matrizAdjacencia[inicio][fim] == -1 or self.matrizAdjacencia[inicio][fim] == 2):
                    if(verticeAdjacente.getCor() == "C"):
                        self.classificacaoArestas.append((verticeAnalisar.getRotulo(), "RETORNO", verticeAdjacente.getRotulo()))

                    elif(verticeAdjacente.getCor() == "P"):
                        self.classificacaoArestas.append((verticeAnalisar.getRotulo(), "CRUZAMENTO", verticeAdjacente.getRotulo()))

                verticeAnalisar.setCor("P")
                verticeAnalisar.setTempoSaida(tempo)
                self.ordemTopologia.append(verticeAnalisar)

                pilha.pop()

        for vertice in self.listaVertices:
            vertice.setCor("B")

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

        primeiraLinha = linhas[0].split(" ")##Quebra primeira linha do arquivo
        qtdVertices = int(primeiraLinha[0])
        qtdArestas = int(primeiraLinha[1])
        grafo = Grafo(qtdVertices, qtdArestas)

        for i in range(qtdVertices):
                grafo.addVertice(i+1)

        for linha in linhas:
            if(linha != linhas[0]):
                linhaSeparada = linha.split(" ")
                v1 = int(linhaSeparada[0])
                v2 = int(linhaSeparada[1])
                inicioAresta = grafo.localizaVertice(v1)
                fimAresta = grafo.localizaVertice(v2)

                grafo.addAdjacente(inicioAresta, fimAresta)



    grafo.imprimeMatriz()

    grafo.contarLigacoes()

    grafo.buscarEmProfundidade()

    grafo.imprimeTempoDosVertices()

    grafo.imprimeOrdemTopologica()

    grafo.imprimeClassificacaoArestas()

