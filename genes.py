from genz.genetic import *

#Program
prog = 'predict.py'
#evaluation script
eval = "eval.py"
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


## Cria instancia da classe Genes
genes = Genes(population=num_cross)
## Adiciona um gene de tipo float, com valores de 0 a 100 e duas casas decimais
genes.add_gene(type=float, space=[-5,5], format=3)
genes.add_gene(type=float, space=[-5,5], format=3)
genes.add_gene(type=float, space=[-5,5], format=3)