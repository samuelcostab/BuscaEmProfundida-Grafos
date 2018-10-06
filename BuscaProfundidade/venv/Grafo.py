class Vertice:
    def __init__(self, rotuloVertice):
        self.rotulo = rotuloVertice
        self.qtdLigacoes = 0
        self.visitado = False

    def visitado(self):
        self.visitado = True

class Grafo:
    def __init__(self, numvertices,  qtdArestas):
        self.qntdArestas = qtdArestas
        self.numVertices = numvertices
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
            print('   ' + str(self.listaVertices[i].rotulo), end=''),
        print()
        for i in range(self.numVertices):
            print(self.listaVertices[i].rotulo, end='')
            for j in range(self.numVertices):
                if(self.matrizAdjacencia[i][j] > 0):
                    print('   ' + str(self.matrizAdjacencia[i][j]), end='')
                else:
                    print('  ' + str(self.matrizAdjacencia[i][j]), end=' ')
            print()

    def localizaVertice (self, vertice):
        for i in range (len(self.listaVertices)):
            if self.listaVertices[i].rotulo == vertice:
                return i

        return -1

    def contarLigacoes(self):
        contadorLigacoes = 0
        for i in range(self.numVertices):
            contadorLigacoesVertice = 0
            for j in range(self.numVertices):
                if (self.matrizAdjacencia[i][j] != 0):
                    contadorLigacoesVertice += 1

                if(self.matrizAdjacencia[i][j] == 2):
                    contadorLigacoesVertice += 1

            if(contadorLigacoesVertice > 0):
                self.listaVertices[i].qtdLigacoes = contadorLigacoesVertice

    def procurarVerticeInicial(self):
        verticeInicial = self.listaVertices[0]
        for vertice in self.listaVertices:
            if (vertice.qtdLigacoes > verticeInicial.qtdLigacoes):
                verticeInicial = vertice

        self.listaVertices.remove(verticeInicial)

        return verticeInicial


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

    verticeInicial = grafo.procurarVerticeInicial()
