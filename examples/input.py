from genz.genetic import *
import numpy as np

def evaluate(log):
    res = np.loadtxt(log)
    return res



#Program
prog = 'python3 program.py'
#evaluation script
eval = evaluate
#coefficient for mutations
kappa = 0.3
#Maximize?
maximize = True
#Number of processes per script
nproc=1
#Number of generations
num_gen = 100
#Number of survivors
num_elite = 5
#Number of crossings
num_cross = 20
#Number of parents
num_parents = 3
#Batch script
batch = 'batch.sh'
#Decimal places in fitness function
prec  = 3


## Cria instancia da classe Genes
genes = Genes(population=num_cross, precision=prec)
## Adiciona um gene de tipo float, com valores de 0 a 100 e duas casas decimais
genes.add_gene(type=float, space=[-5,5], format=3)
genes.add_gene(type=float, space=[-5,5], format=3)
genes.add_gene(type=float, space=[-5,5], format=3)