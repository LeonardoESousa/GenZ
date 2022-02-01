import numpy as np
import os


np.set_printoptions(suppress=True)
## Orders the Report
# args: None
# i)  Try: Incluir elite no report. 
# ii) Pegar os dados do Report. Usar np.loadtxt. Ordenar (maior pro menor se maximize=True, else menor pro maior)
# iii)Retorna matriz ordenada. 

def order(maximize=True):
    data = np.loadtxt('Report.dat')
    try:
        elite = np.loadtxt('Elite.dat')
        data  = np.vstack((data,elite))
    except:
        pass
    indice = np.argsort(data[:,-1])
    if maximize == True:
        sorted_arr = data[np.flip(indice),:]
    else:
        sorted_arr = data[np.flip(indice),:]
    return sorted_arr

print(order())

## TNG
# args: matriz ordenada
# i)   Selecionar conjuntos de pais (numero de pais variavel)
# ii)  Fazer crossover e mutacao (mutacao variavel)
# iii) Escrever filhos em um novo arquivo  (id, genes)




