import numpy as np
import os



## Orders the Report
# args: None
# i)  Try: Incluir elite no report. 
# ii) Pegar os dados do Report. Usar np.loadtxt. Ordenar (maior pro menor se maximize=True, else menor pro maior)
# iii)Retorna matriz ordenada. 
maximize=True
def order():
    r=np.loadtxt('Report.txt')
   
    try:
        e=np.loadtxt('Elite.txt')
        f=np.vstack((r,e))
    except:
        f=r

    arr=np.array(f)

    if maximize==True:
        sorted_arr=sorted(arr,reverse=True,key=lambda x:x[-1])
        #sorted_arr=np.sort(arr,axis=-1)
    else:
        sorted_arr=sorted(arr,reverse=False,key=lambda x:x[-1])
    return(sorted_arr)

## TNG
# args: matriz ordenada
# i)   Selecionar conjuntos de pais (numero de pais variavel)
# ii)  Fazer crossover e mutacao (mutacao variavel)
# iii) Escrever filhos em um novo arquivo  (id, genes)




