class Vertice:
    def __init__(self, rotuloVertice):
        self.rotulo = rotuloVertice
        self.qtdLigacoes = 0
        self.tempoEntrada = 0
        self.tempoSaida = 0

class Grafo:
    def __init__(self, numvertices, qtdArestas):
        self.qntdArestas = qtdArestas
        self.numVertices = numvertices
        self.ordemTopologica = []
        self.classificacaoArestas = []
        self.listaVertices = []
        self.matrizAdjacencia = self.gerarMatriz()
        self.tempo = 1
        self.componentesConexas = []
        self.arquivo = []

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
            print('   ' + str(self.listaVertices[i].rotulo), end=''),
        print()
        for i in range(self.numVertices):
            print(self.listaVertices[i].rotulo, end='')
            for j in range(self.numVertices):
                if (self.matrizAdjacencia[i][j] > 0):
                    print('  ' + str(self.matrizAdjacencia[i][j]), end=' ')
                else:
                    print('  ' + str(self.matrizAdjacencia[i][j]), end=' ')
            print()

    def localizaVertice(self, rotuloPassado, listaVertice):
        for i in range(len(listaVertice)):
            if (self.listaVertices[i].rotulo == rotuloPassado):
                return i

        return -1

    def contaLigacoes(self):
        for i in range(self.numVertices):
            contadorLigacoesVertice = 0
            for j in range(self.numVertices):
                if (self.matrizAdjacencia[i][j] != 0):  ##Se o Vertice incide em outro
                    contadorLigacoesVertice += 1

                if (self.matrizAdjacencia[j][i] == 1):  ##Se o Vertice é incidido por outro
                    contadorLigacoesVertice += 1

            if (contadorLigacoesVertice >= 0):
                self.listaVertices[i].qtdLigacoes = contadorLigacoesVertice

    def procurarVerticeInicial(self):
        verticeInicial = self.listaVertices[0]
        for vertice in self.listaVertices:
            if(vertice.cor == "B"):
                if (verticeInicial.cor == "B"):
                    if(vertice.qtdLigacoes > verticeInicial.qtdLigacoes):
                        verticeInicial = vertice
                else:
                    verticeInicial = vertice


        return verticeInicial

    def obtemAdjacente(self,vertice, listaVertice):
        numV = self.localizaVertice(vertice.rotulo, listaVertice)##indece do Vertice passado
        for i in range(self.numVertices):
            if (self.matrizAdjacencia[numV][i] == 1) and (self.listaVertices[i].cor == "B"):
                return i  ##retorna i se o vertice for NaoVisitado

        for j in range(self.numVertices):
            if (self.matrizAdjacencia[numV][j] == 1) and (self.listaVertices[j].cor == "C"):
                return j  ##retorna j se o vertice for Visitado

        for k in range(self.numVertices):
            if (self.matrizAdjacencia[numV][k] == 1) and (self.listaVertices[j].cor == "P"):
                return k

        return None

    def criaGrafoTransposto(self):
        matrizInversa = self.gerarMatriz()
        for i in range(self.numVertices):
            for j in range(self.numVertices):
                if (self.matrizAdjacencia[i][j] == 1):
                    if(self.matrizAdjacencia[j][i] == 1):
                        matrizInversa[i][j] = 1
                        matrizInversa[j][i] = 1
                    else:
                        matrizInversa[i][j] = 0
                        matrizInversa[j][i] = 1


        grafoT = Grafo(self.numVertices, self.qntdArestas)
        grafoT.matrizAdjacencia = matrizInversa
        grafoT.listaVertices = self.listaVertices
        grafoT.ordemTopologica = self.ordemTopologica

        return grafoT

    def contaComponentes(self):
        for vertice in self.ordemTopologica:
            vertice.cor = "B"
            vertice.tempoEntrada = 0
            vertice.tempoSaida = 0


        for v in self.ordemTopologica:
            if(v.cor == "B" and v.tempoEntrada == 0):
                self.dfsT(v)

    def dfsT(self, verticeInicial):
        verticeInicial.cor = "C"
        pilha = []
        pilha.append(verticeInicial)##adiciona o vertice que inicia a busca na pilha
        compontenteFechou = False

        while len(pilha) > 0:
            verticeAnalisar = pilha[len(pilha) - 1]##Ultimo elemento da Pilha
            verticeAnalisar.cor = "C"

            indexVAd = self.obtemAdjacente(verticeAnalisar, self.listaVertices) ##Retorna o Vertice adjacente ao VerticeAnalisar
            if(indexVAd != None):
                verticeAdjacente = self.listaVertices[indexVAd]

                if (verticeAdjacente.cor == "B"):
                    pilha.append(verticeAdjacente)
                else:
                    verticeAnalisar.cor = "P"

                    s = ""
                    for i in pilha:
                        s += " " + str(i.rotulo)
                    self.componentesConexas.append(s)

                    pilha.clear()


            else:
                if(compontenteFechou == False):
                    pilhaComponente = pilha
                    s = ""
                    for i in pilhaComponente:
                        s += " " + str(i.rotulo)
                    self.componentesConexas.append(s)
                    compontenteFechou = True

                verticeAnalisar.cor = "P"
                pilha.pop()

    def dfs(self, verticeInicial):
        verticeInicial.cor = "C"
        pilha = []
        pilha.append(verticeInicial)##adiciona o vertice que inicia a busca na pilha

        while len(pilha) > 0:
            verticeAnalisar = pilha[len(pilha) - 1]##Ultimo elemento da Pilha
            verticeAnalisar.cor = "C"

            if (verticeAnalisar.tempoEntrada == 0):  ##Seta o valor de entrada no vertice
                verticeAnalisar.tempoEntrada = self.tempo

            self.tempo += 1

            indexVAd = self.obtemAdjacente(verticeAnalisar, self.listaVertices) ##Retorna o Vertice adjacente ao VerticeAnalisar

            if(indexVAd != None):
                verticeAdjacente = self.listaVertices[indexVAd]

                if (verticeAdjacente.cor == "B"):
                    self.classificacaoArestas.append((verticeAnalisar.rotulo, "ARVORE", verticeAdjacente.rotulo))
                    pilha.append(verticeAdjacente)
                else:
                    verticeAnalisar.cor = "P"
                    verticeAnalisar.tempoSaida = self.tempo

                    self.ordemTopologica.append(verticeAnalisar)

                    s = ""
                    for i in pilha:
                        s += " " + str(i.rotulo)
                    self.componentesConexas.append(s)
                    pilha.pop()


                    inicio = self.localizaVertice(verticeAnalisar.rotulo, self.listaVertices)
                    fim = self.localizaVertice(verticeAdjacente.rotulo, self.listaVertices)
                    if (self.matrizAdjacencia[inicio][fim] == 1):
                        if (verticeAdjacente.cor == "C"):
                            self.classificacaoArestas.append(
                                (verticeAnalisar.rotulo, "RETORNO", verticeAdjacente.rotulo))

                        elif (verticeAdjacente.cor == "P"):
                            if(verticeAdjacente.rotulo == verticeAnalisar.rotulo):
                                self.classificacaoArestas.append((verticeAnalisar.rotulo, "RETORNO", verticeAdjacente.rotulo))
                            elif(verticeAdjacente.cor == "P" ):
                                self.classificacaoArestas.append((verticeAnalisar.rotulo, "CRUZAMENTO", verticeAdjacente.rotulo))
            else:
                verticeAnalisar.cor = "P"
                verticeAnalisar.tempoSaida = self.tempo
                self.tempo += 1
                self.ordemTopologica.append(verticeAnalisar)
                pilha.pop()


        if (self.procurarVerticeInicial().cor == "B"):##Se existe vertice NãoVisitado
            return 1
        else:
            for vertice in self.listaVertices:
                vertice.cor = "B"

        return -1

    def buscaEmProfundidade(self, controle):
        if (controle == 0):##Se for a primeira iteração
            for vertice in self.listaVertices:
                ##Colorindo todos os vertices para Branco
                vertice.cor = "B"

        verticeInicial = self.procurarVerticeInicial()


        return self.dfs(verticeInicial)

    def imprimeTempoDosVertices(self):
        for vertice in self.listaVertices:
            print("VERTICE: {} {} / {}".format(vertice.rotulo, vertice.tempoEntrada, vertice.tempoSaida))

    def imprimeOrdemTopologica(self):
        self.ordemTopologica.reverse()
        print()
        s = ""
        for vertice in self.ordemTopologica:
            s += str(vertice.rotulo) + " "

        print(s)
        self.arquivo.append("ORDEM TOPOLOGICA\n")
        self.arquivo.append(s)

    def imprimeClassificacaoArestas(self):
        s = ""
        for aresta in self.classificacaoArestas:
            s += str(aresta) + '\n'
            print(aresta)
        self.arquivo.append("\nCLASSIFICAO ARESTAS\n")
        self.arquivo.append(s)

    def imprimeComponentes(self):
        s = "\nCOMPONENTES CONEXAS:\n"
        count = 0
        for i in self.componentesConexas:
            count += 1
            s += i + '\n'
            print(i)


        s += "qtd:" + str(count)

        return s


if __name__ == "__main__":
    with open("GPABLO.txt") as arquivo:
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
                inicioAresta = grafo.localizaVertice(v1, grafo.listaVertices)
                fimAresta = grafo.localizaVertice(v2, grafo.listaVertices)

                grafo.addAdjacente(inicioAresta, fimAresta)

    ##grafo.imprimeMatriz()

    grafo.contaLigacoes()

    n = 0
    while (n != -1):  ##Enquanto houver vertice para visitar
        n = grafo.buscaEmProfundidade(n)

    ##grafo.imprimeTempoDosVertices()
    grafo.imprimeOrdemTopologica()
    grafo.imprimeClassificacaoArestas()

    grafoT = grafo.criaGrafoTransposto()

    grafoT.contaComponentes()

    s = grafoT.imprimeComponentes()

    grafo.arquivo.append(s)

    arquivo = open("saida.txt", "w")
    arquivo.writelines(grafo.arquivo)
    for i in grafo.arquivo:
      print(i)
