from genz.genetic import *


## Cria instancia da classe Genes com populacao de 10 individuos e 10 geracoes
genes = Genes(population=10,generations=10, maximize=True)
## Adiciona um gene de tipo float, com valores de 0 a 100 e duas casas decimais
genes.add_gene(type=float, space=[-5,5], format=3)
genes.add_gene(type=float, space=[-5,5], format=3)
genes.add_gene(type=float, space=[-5,5], format=3)