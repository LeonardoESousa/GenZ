import numpy as np
import os
import random
import sys
import time 

random.seed(1)
np.random.seed(1)
np.set_printoptions(suppress=True)

class Genes():
    def __init__(self,**kwargs):
        self.genes   = []
        self.types   = {}
        self.limits  = {}
        self.formats = {}
        self.probs   = {}
        self.fmts    = ['%.0f']
        self.precision   = ['%.{}f'.format(kwargs['precision'])]
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
            self.fmts.append('%.0f')    
        try:
            self.probs[num] = kwargs['probs']
        except:    
            self.probs[num] = np.ones(len(self.limits[num]))     

    def mutation(self,num,gene):
        if self.types[num] !=  float:
            lista = self.limits[num].copy()
            del lista[lista.index(gene)]
            new_gene = random.choice(lista)
        else:
            interval = abs(self.limits[num][1]-self.limits[num][0])/2
            interval = min(interval, 3*(10**(-1*self.formats[num]))) 
            new_gene = np.random.normal(gene, interval)
            new_gene = min(new_gene,self.limits[num][1])
            new_gene = max(new_gene,self.limits[num][0])
            new_gene = np.round(new_gene,self.formats[num])
        return new_gene 

    def first_gen(self):
        first = np.zeros((1,len(self.genes)+1))
        for i in range(self.population):
            linha = np.zeros((1,len(self.genes)+1))
            linha[0,0] = i
            for g in self.genes:
                if self.types[g] != float:
                    linha[0,g+1] = random.choices(self.limits[g], weights=self.probs[g])[0]
                else:
                    linha[0,g+1] = np.round(np.random.uniform(self.limits[g][0],self.limits[g][-1]),self.formats[g])
            first = np.vstack((first,linha))
        first = first[1:,:]
        np.savetxt('NextGen.dat', first, fmt=self.fmts, delimiter='\t')

## Pega genes (Laura)
# args: id do individuo (int)
# i) Abre o NextGen.dat, encontra a linha que corresponde ao id.
# ii) Retorna um array com os genes correspondentes a esse id. O array deve conter apenas os genes.
def get_genes(id_ind):
    id_ind = float(id_ind)
    data = np.loadtxt('NextGen.dat')
    id = np.where(data[:,0] == id_ind)[0][0]
    ind_genes = data[id,1:]
    return ind_genes

#def get_best_genes(folder='.'):
#    data = np.loadtxt(folder+'/Best.dat')
#    data = data[0,1:-1]
#    return data

def get_by_id(id_ind,file):
    id_ind = float(id_ind)
    data = np.loadtxt(file)
    id = np.where(data[:,0] == id_ind)[0][0]
    ind_genes = data[id,1:]
    return ind_genes

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
def order(maximize, genes, inc_elite):
    data = np.loadtxt('Report.dat')
    if inc_elite:
        try:
            elite = np.loadtxt('Elite.dat')
            data  = np.vstack((data,elite))
        except:
            pass
    with open('Avg_Population.dat', 'a') as f, open('Std_Population.dat', 'a') as g: 
        average = np.average(data[:,1:],axis=0)
        np.savetxt(f,[average], delimiter='\t',fmt=genes.fmts[1:]+genes.precision)
        std = np.std(data[:,1:], axis=0)
        np.savetxt(g,[std], delimiter='\t',fmt=genes.fmts[1:]+genes.precision)
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
def elite(num_elite, sorted_arr, genes):
    if num_elite > 0:
        top = sorted_arr[0:num_elite,:]
        np.savetxt('Elite.dat',top, delimiter='\t',fmt=genes.fmts+genes.precision)


## Best (Pedao)
# args: matriz ordenada que sai da funcao order (numpy array).
# i) Pega a matriz ordenada e retira apenas as linhas e colunas correspondentes ao cara de fitness mais alto. Pode haver mais de um com mesmo fitness!
# ii) Usando um with open('Best.dat', 'w') as file:, escreve os genes e o fitness dos melhores caras até o momento em um arquivo chamado Best.dat. Usar o np.savetxt.
# ii) No mesmo arquivo, escrever a média e o desvio padrão dos genes do melhor cara. Usar o np.mean e np.std que já calcula o de todas as colunas de uma vez.
# Usar o np.savetxt pra escrever no mesmo arquivo.

def best(matriz_ordenada,genes,maximize):
    try:
        matriz_ordenada = np.vstack((matriz_ordenada,np.genfromtxt('Best.dat',skip_footer=2)))
        matriz_ordenada = np.unique(matriz_ordenada,axis=0,return_index=False)
    except:
        pass
    if maximize:
        best_fitness = max(matriz_ordenada[:,-1])
    else:        
        best_fitness = min(matriz_ordenada[:,-1])

    inds = np.where(matriz_ordenada[:,-1] == best_fitness)[0]
    melhor_indiv = matriz_ordenada[inds,:]
    media=np.mean(melhor_indiv,axis=0)
    media=[media[1:-1]]
    desvi=np.std(melhor_indiv,axis=0)
    desvi=[desvi[1:-1]]
    with open('Best.dat', 'w') as file:
        file.write('#Best individual:\n')
        np.savetxt(file,melhor_indiv,fmt=genes.fmts + genes.precision,delimiter='\t')
        file.write('\n\n')
        file.write('#Average Gene Values:\n')
        np.savetxt(file,media,fmt=genes.fmts[1:],delimiter='\t')
        file.write('\n')
        file.write('#Standard Deviation:\n')
        np.savetxt(file,desvi,fmt=genes.fmts[1:],delimiter='\t')
    return melhor_indiv

## Gera arquivo Progress.dat (Laura)
# Esse arquivo registra o melhor individuo de cada round do genetico.
# args: numero da geracao (N).

def progress(num_gen, best_ind, genes):
    try:
        best_ind = best_ind[0,:]
    except:
        pass
    with open('Progress.dat', 'a') as file:
        best_ind = np.insert(best_ind,0,num_gen)
        np.savetxt(file, [best_ind], fmt=['%.0f'] + genes.fmts + genes.precision, delimiter='\t')

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
def mutation(individual,genes,kappa,sigma):
    #prob     = np.exp(-sigma[1:]/kappa)
    prob     = sigma[1:]
    prob     = np.cumsum(prob/np.sum(prob))
    mut      = np.argmax(random.uniform(0,1) <= prob)
    new_gene = genes.mutation(mut,individual[0,mut+1])
    individual[0,mut+1] = new_gene
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
def tng(sorted_arr, num_new_gen, num_parents, k, genes, maximize):
    fitness = sorted_arr[:,-1]
    id_new_gen = max_id() + 1
    next_gen = np.zeros((1,np.shape(sorted_arr)[1]-1))
    mean  =  np.mean(sorted_arr[:,1:],axis=0)
    try:
        sigma =  np.nan_to_num(np.abs(np.std(sorted_arr[:,1:],axis=0)/mean))   #np.nan_to_num(np.std(fitness)/abs(np.mean(fitness)))
    except:
        sigma = k*np.ones(sorted_arr[:,1:].shape())    
    for _ in range(0,num_new_gen):
        if maximize:
            indices = random.choices(np.arange(len(fitness)), weights=fitness, k=num_parents)
        else:
            indices = random.choices(np.arange(len(fitness)), weights=np.nan_to_num(1/(fitness+1e-12)), k=num_parents)
        parents = sorted_arr[indices,:] 
        new_individual = crossover(parents,id_new_gen)
        new_individual = mutation(new_individual,genes,k,sigma)
        next_gen = np.vstack((next_gen,new_individual))
        id_new_gen += 1
    next_gen = next_gen[1:,:]
    ind = np.unique(next_gen[:,1:],axis=0,return_index=True)[1]
    next_gen = next_gen[ind,:]
    np.savetxt('ModelGen.dat',next_gen,fmt=genes.fmts, delimiter='\t')
    return next_gen.shape[0]


## Gera batch script (Laura)
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
        with open('genbatch_'+str(j+1)+'.sh','w') as script:
            l = 0
            while l < N:
                script.write('{} {:.0f}\n'.format(prog,data[m,0]))
                script.write('echo "\n#Genetic Job Done!" >> Individual_{:.0f}_.log\n'.format(data[m,0]))
                l += 1
                m += 1

    if modulo != 0:
        with open('genbatch_'+str(int(num_script)+1)+'.sh','w') as script:
            for i in range(modulo):
                script.write('{} {:.0f}\n'.format(prog,data[m,0]))
                script.write('echo "\n#Genetic Job Done!" >> Individual_{:.0f}_.log\n'.format(data[m,0]))
                m += 1


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
def hold_watch(wd,deltat,num_cross):
    rodando = [1,1,1]
    while len(rodando) > 0:
        logs = [i for i in os.listdir(wd) if 'Individual_' in i and '_.log' in i]
        if len(logs) == num_cross:
            rodando = watcher(logs)
        if 'limit.lx' not in os.listdir('.'):
            with open('Progress.dat','a') as f:
                f.write('#Aborted!')
            sys.exit()
        time.sleep(deltat)    
###############################################################

def killswitch(wd):
    try:
        os.mkdir(wd + 'Logs')
    except:
        pass
    with open(wd + 'limit.lx', 'w') as f:
        f.write('Running')


def evaluate(func,genes):
    individuals = sorted([i for i in os.listdir('.') if 'Individual_' in i and '.log' in i])
    with open('Report.dat', 'w') as f, open('Space.dat', 'a') as g:
        for ind in individuals:
            id = ind.split('_')[1]
            params = get_genes(id)
            try:
                fitness = max(0,func(ind))
            except:
                fitness = 0
            params = np.append(params,fitness)
            params = np.insert(params,0,float(id))
            np.savetxt(f,[params],fmt=genes.fmts + genes.precision,delimiter='\t')
            np.savetxt(g,[params],fmt=genes.fmts + genes.precision,delimiter='\t')  
            
def remake_nextgen(func, genes,maximize):
    data = np.loadtxt('Space.dat')
    grid = func(data)
    model5 = grid.best_estimator_
    newgen = np.loadtxt('ModelGen.dat')
    ids = np.sort(newgen[:genes.population,0])
    X_test = newgen[:, 1:]
    y_5 = model5.predict(X_test)
    argsort = np.argsort(y_5)
    if maximize:
        argsort = argsort[::-1]
    ind = np.unique(newgen[:,1:],axis=0,return_index=True)[1]
    newgen = newgen[ind,:]    
    newgen = np.hstack((ids[:,np.newaxis],newgen[argsort[:genes.population],1:]))
    np.savetxt('NextGen.dat', newgen, fmt=genes.fmts,delimiter='\t')

    with open('Model.dat','a') as f:
        f.write(f'{grid.best_params_}\t{grid.best_score_}\n')