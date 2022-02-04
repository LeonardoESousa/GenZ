import numpy as np
import os
import random

np.set_printoptions(suppress=True)

class Genes():
    def __init__(self,**kwargs):
        self.genes   = []
        self.types   = {}
        self.limits  = {}
        self.formats = {}
        self.fmts    = ['%d']
        self.population  = kwargs['population']
        self.generations = kwargs['generations']
        self.maximize    = kwargs['maximize']


    def add_gene(self,**kwargs):
        num = len(self.genes)
        self.genes.append(num)
        self.types[num]  = kwargs['type']
        self.limits[num] = kwargs['space']
        if kwargs['type'] == float:
            self.formats[num] = kwargs['format']
            self.fmts.append('%+.{}f'.format(kwargs['format']))
        else:
            self.fmts.append('%d')    

    def mutation(self,num,gene):
        if self.types[num] !=  float:
            lista = self.limits[num]
            del lista[lista.index(gene)]
            new_gene = random.choice(lista)
        else:
            new_gene = np.random.uniform(self.limits[num][0],self.limits[num][-1])
            new_gene = np.round(new_gene,self.formats[num])
        return new_gene 

    def first_gen(self):
        first = np.zeros((1,len(self.genes)+1))
        for i in range(self.population):
            linha = np.zeros((1,len(self.genes)+1))
            linha[0,0] = i
            for g in self.genes:
                if self.types[g] != float:
                    linha[0,g+1] = random.choice(self.limits[g])
                else:
                    linha[0,g+1] = np.round(np.random.uniform(self.limits[g][0],self.limits[g][-1]),self.formats[g])
            first = np.vstack((first,linha))
        first = first[1:,:]
        np.savetxt('NextGen.dat', first, fmt=self.fmts, delimiter='\t')


## Cria instancia da classe Genes com populacao de 10 individuos e 10 geracoes
genes = Genes(population=10,generations=10, maximize=True)
## Adiciona um gene de tipo float, com valores de 0 a 100 e duas casas decimais
genes.add_gene(type=float, space=[-5,5], format=3)
genes.add_gene(type=float, space=[-5,5], format=3)
genes.add_gene(type=float, space=[-5,5], format=3)
# Printa lista que identifica cada gene
print(genes.genes)
# Realiza a mutacao no gene 0 que tem valor 1 agora e retorna o novo valor
print(genes.mutation(0,1))
# Realiza a mutacao no gene 1 que tem valor 0 agora e retorna o novo valor
print(genes.mutation(1,0))
# Cria a primeira geracao de individuos 
genes.first_gen()

## max_id (Pedao)
# args: None
# i) Abre o NextGen.dat com o np.loadtxt e pega o maior numero da primeira coluna.
# ii) Retorna esse numero.
#Funcao provisoria abaixo
def max_id():
    return 4


## Orders the Report (Laura)
# args: None
# i)  Try: Incluir elite no report. 
# ii) Pegar os dados do Report. Usar np.loadtxt. Ordenar (maior pro menor se maximize=True, else menor pro maior)
# iii)Retorna matriz ordenada. 
def order():
    data = np.loadtxt('Report.dat')
    try:
        elite = np.loadtxt('Elite.dat')
        data  = np.vstack((data,elite))
    except:
        pass
    indice = np.argsort(data[:,-1])
    if genes.maximize:
        sorted_arr = data[np.flip(indice),:]
    else:
        sorted_arr = data[indice,:]
    return sorted_arr

## Elite (Laura)
# args: matriz ordenada que sai da funcao order (numpy array), numero de elementos na elite (int)
# i) Pega as primeiras N linhas da matriz ordenada, onde N é o numero de elementos na elite.
# ii) Escreve a matriz no arquivo Elite.dat 
def elite(num_elite,sorted_arr):
    np.savetxt('Elite.dat',sorted_arr[0:num_elite,:], delimiter='\t',fmt=genes.fmts+['%.3f'])

## Best (Pedao)
# args: matriz ordenada que sai da funcao order (numpy array).
# i) Pega a matriz ordenada e retira apenas as linhas e colunas correspondentes ao cara de fitness mais alto. Pode haver mais de um com mesmo fitness!
# ii) Usando um with open('Best.dat', 'w') as file:, escreve os genes e o fitness dos melhores caras até o momento em um arquivo chamado Best.dat. Usar o np.savetxt.
# ii) No mesmo arquivo, escrever a média e o desvio padrão dos genes do melhor cara. Usar o np.mean e np.std que já calcula o de todas as colunas de uma vez.
# Usar o np.savetxt pra escrever no mesmo arquivo.

## Crossover (Laura)
# args: array com genes de todos os pais
# i)  Sortear qual pai vai passar seu gene.
# ii) Funcao retorna um array com os genes do filho. 
def crossover(parents,id_new_gen):
    individual = np.zeros((1,np.shape(parents)[1]-1))
    individual[0,0] = id_new_gen
    for i in range(1,np.shape(parents)[1]-1):
        gene = random.choice(parents[:,i])
        individual[0,i] = gene
    return individual

## Mutacao (Pedao)
# args: array com os genes de um individuo, parametro que controla a chance de mutacao. 
# i) Faz um loop sobre todos os genes. Decide aleatoriamente se o gene vai sofrer mutacao. Chama a funcao mutation e altera o valor do gene.
# ii) Funcao retorna um array com os genes do filho. 

## TNG (Laura)
# args: matriz ordenada (numpy array), numero de filhos (int), numero de pais (int) (pode ser 2 ou mais), maximize (Boolean)
# i)   Chamar a funcao max_id, guardar o que ela retorna e somar um. Esse vai ser o id do primeiro filho a ser gerado, 
# ii)  Criar um loop for para realizar o procedimento para cada filho que precisa ser gerado.
#   iii)  Selecionar conjuntos de pais. Chance de ser escolhido é proporcional ao fitness se maximize=True, caso contrário deve ser proporcional ao inverso do fitness.
#   iv)   Escrever um array (numero de pais x numero de genes) com os genes dos pais. Vai servir de input para a funcao de crossover.
#   v)    Chamar a funcao de crossover e pegar o que ela retorna
#   vi)   Chamar a funcao de mutacao e pegar o que ela retorna
#   vii)  Usar o np.vstack para criar um array em que cada linha corresponde a um filho e cada coluna os seus genes. A primeira coluna tem de ser o numero identificador do individuo.
#   viii) Somar um ao identficador.
#ix)  Escrever filhos em um novo arquivo  (id, genes)
def tng(sorted_arr, num_new_gen, num_parents):
    fitness = sorted_arr[:,-1]
    id_new_gen = max_id() + 1
    next_gen = np.zeros((1,np.shape(sorted_arr)[1]-1))
    for i in range(0,num_new_gen):
        if genes.maximize:
            indices = random.choices(np.arange(len(fitness)), weights=fitness, k=num_parents)
        else:
            indices = random.choices(np.arange(len(fitness)), weights=np.nan_to_num(1/fitness), k=num_parents)
        parents = sorted_arr[indices,:] 
        new_individual = crossover(parents,id_new_gen)
        #          = mutation()
        next_gen = np.vstack((next_gen,new_individual))
        id_new_gen += 1
    next_gen = next_gen[1:,:]
    np.savetxt('NextGen.dat',next_gen,fmt=genes.fmts, delimiter='\t')








