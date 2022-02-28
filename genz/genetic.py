import numpy as np
import os
import random
import sys
import time 

np.set_printoptions(suppress=True)

class Genes():
    def __init__(self,**kwargs):
        self.genes   = []
        self.types   = {}
        self.limits  = {}
        self.formats = {}
        self.fmts    = ['%d']
        self.population  = kwargs['population']

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


## max_id (Pedao)
# args: None
# i) Abre o NextGen.dat com o np.loadtxt e pega o maior numero da primeira coluna.
# ii) Retorna esse numero.
#Funcao provisoria abaixo
def max_id():
    data = np.loadtxt('NextGen.dat')
    num_max = max(data[:,0])
    return num_max


## Orders the Report (Laura)
# args: None
# i)  Try: Incluir elite no report. 
# ii) Pegar os dados do Report. Usar np.loadtxt. Ordenar (maior pro menor se maximize=True, else menor pro maior)
# iii)Retorna matriz ordenada. 
def order(maximize):
    data = np.loadtxt('Report.dat')
    try:
        elite = np.loadtxt('Elite.dat')
        data  = np.vstack((data,elite))
    except:
        pass
    indice = np.argsort(data[:,-1])
    if maximize:
        sorted_arr = data[np.flip(indice),:]
    else:
        sorted_arr = data[indice,:]
    return sorted_arr

## Elite (Laura)
# args: matriz ordenada que sai da funcao order (numpy array), numero de elementos na elite (int)
# i) Pega as primeiras N linhas da matriz ordenada, onde N é o numero de elementos na elite.
# ii) Escreve a matriz no arquivo Elite.dat 
def elite(num_elite,sorted_arr,genes):
    np.savetxt('Elite.dat',sorted_arr[0:num_elite,:], delimiter='\t',fmt=genes.fmts+['%.3f'])

## Best (Pedao)
# args: matriz ordenada que sai da funcao order (numpy array).
# i) Pega a matriz ordenada e retira apenas as linhas e colunas correspondentes ao cara de fitness mais alto. Pode haver mais de um com mesmo fitness!
# ii) Usando um with open('Best.dat', 'w') as file:, escreve os genes e o fitness dos melhores caras até o momento em um arquivo chamado Best.dat. Usar o np.savetxt.
# ii) No mesmo arquivo, escrever a média e o desvio padrão dos genes do melhor cara. Usar o np.mean e np.std que já calcula o de todas as colunas de uma vez.
# Usar o np.savetxt pra escrever no mesmo arquivo.

def Best(matriz_ordenada,genes):
   with open('Best.dat', 'w') as file:
        melhor_indiv=[matriz_ordenada[0,:]]
        best_fitness=matriz_ordenada[0,-1]
        #best_fitness=10  #descomente para debug
        i=1
        while matriz_ordenada[i,-1] == best_fitness:
            melhor_indiv=np.vstack((melhor_indiv,matriz_ordenada[i,:]))
            #best_fitness=9  #descomente para debug
            i += 1
        media=np.mean(melhor_indiv,axis=0)
        media=[media[1:-1]]
        desvi=np.std(melhor_indiv,axis=0)
        desvi=[desvi[1:-1]]
        np.savetxt(file,melhor_indiv,fmt=genes.fmts,delimiter='\t')
        np.savetxt(file,media,fmt=genes.fmts,delimiter='\t')
        np.savetxt(file,desvi,fmt=genes.fmts,delimiter='\t')

## Gera arquivo Progress.dat
# Esse arquivo registra o melhor individuo de cada round do genetico.
# args: numero da geracao (N).


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
# args: array com os genes de um individuo, parametro (k) que controla a chance de mutacao (float), objeto genes. 
# i) Faz um loop sobre todos os genes. Decide aleatoriamente se o gene vai sofrer mutacao. Chama a funcao mutation. Isso e feito fazendo genes.mutation(a,b) em que a e o numero do gene e b o valor desse gene. Ex:
# new_gene = genes.mutation(0,1) - Realiza a mutacao no gene 0 que tem valor 1 agora e retorna o novo valor
# new_gene = genes.mutation(1,0) - Realiza a mutacao no gene 1 que tem valor 0 agora e retorna o novo valor
# ii) Troca o gene velho pelo novo. Repete para todos os genes.
# iii) Funcao retorna um array com os genes do filho. 
def mutation(individual):
    return individual


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
def tng(sorted_arr, num_new_gen, num_parents,k,genes, maximize):
    fitness = sorted_arr[:,-1]
    id_new_gen = max_id() + 1
    next_gen = np.zeros((1,np.shape(sorted_arr)[1]-1))
    for i in range(0,num_new_gen):
        if maximize:
            indices = random.choices(np.arange(len(fitness)), weights=fitness, k=num_parents)
        else:
            indices = random.choices(np.arange(len(fitness)), weights=np.nan_to_num(1/fitness), k=num_parents)
        parents = sorted_arr[indices,:] 
        new_individual = crossover(parents,id_new_gen)
        new_individual = mutation(new_individual,k)
        next_gen = np.vstack((next_gen,new_individual))
        id_new_gen += 1
    next_gen = next_gen[1:,:]
    np.savetxt('NextGen.dat',next_gen,fmt=genes.fmts, delimiter='\t')


## Pega genes
# args: id do individuo (int)
# i) Abre o NextGen.dat, encontra a linha que corresponde ao id.
# ii) Retorna um array com os genes correspondentes a esse id. O array deve conter apenas os genes.
def get_genes(id_ind):
    data = np.loadtxt('NextGen.dat')
    id = np.where(data[:,0] == id_ind)[0][0]
    ind_genes = data[id,1:]
    return ind_genes


## Gera batch script
# args: numero N de jobs por script (int), nome do arquivo (file) .py que vai rodar os calculos de cada indivíduo (str).
# i) Abre o NextGen.dat e pega a primeira coluna. Esses sao os ids dos calculos que vao rodar.
# ii) Calcular quantos scripts são necessários. Se vc tem 10 individuos no NextGen e N = 2, são 5 scripts.
# iii) Usar um loop pra criar cada script. Esse é um arquivo com nome 'batch_i.sh' onde i é o numero do batch.
#Cada linha desse arquivo deve conter 'python3 file id\n'
# iv) Feitos os arquivos batch, criar um arquivo master.sh com uma linha pra cada arquivo batch gerado. Cada linha
# deve ter './batch_i.sh &\n' 

def script_batch(N,prog):
    data = np.loadtxt('NextGen.dat')
    num_script = len(data[:,0])/N
    modulo = len(data[:,0])%N
    
    m = 0
    for j in range(int(num_script)):
        with open('batch_'+str(j+1)+'.sh','w') as script:
            l = 0
            while l < N:
                script.write('python3 {} {:.0f}\n'.format(prog,data[m,0]))
                script.write('echo #Genetic Job Done! >> Individual_{:.0f}_*\n'.format(data[m,0]))
                l += 1
                m += 1

    if (modulo != 0):
        with open('batch_'+str(int(num_script)+1)+'.sh','w') as script:
            for i in range(modulo):
                script.write('python3 {} {:.0f}\n'.format(prog,data[m,0]))
                script.write('echo #Genetic Job Done! >> Individual_{:.0f}_*\n'.format(data[m,0]))
                m += 1

    with open ('master.sh', 'w') as master: 
        for i in range(int(num_script)):
            master.write('./batch_' + str(i+1) + '.sh \n')
        if (modulo != 0): 
            master.write('./batch_' + str(int(num_script)+1) + '.sh \n')


##CHECKS WHETHER JOBS ARE DONE#################################
def watcher(files):
    rodando = files.copy()
    done = []
    for input in rodando: 
        try:
            with open(input[:-3]+'log', 'r') as f:
                for line in f:
                    if '#Genetic Job Done!' in line:
                        done.append(input)
        except:
            pass 
    for elem in done:
        del rodando[rodando.index(elem)]                                
    return rodando
###############################################################

##CHECKS WHETHER JOBS ARE DONE#################################
def hold_watch(files):
    rodando = files.copy()
    while len(rodando) > 0:
        rodando = watcher(rodando)
        if 'limit.lx' not in os.listdir('.'):
            with open('omega.lx','a') as f:
                f.write('#Aborted!')
            sys.exit()
        time.sleep(60)    
###############################################################