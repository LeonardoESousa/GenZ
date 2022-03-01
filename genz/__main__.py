#!/usr/bin/env python3
import subprocess
import sys
import os
#importing config module
import importlib
from genz.genetic import *
wd = os.getcwd()+'/'
config_file = wd+sys.argv[1]
spec  = importlib.util.spec_from_file_location(sys.argv[1].split('.')[0], wd+sys.argv[1])
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

#Program variables
prog        = config.prog
eval        = config.eval
kappa       = config.kappa
maximize    = config.maximize
nproc       = config.nproc
num_gen     = config.num_gen
num_elite   = config.num_elite
num_cross   = config.num_cross
genes       = config.genes
num_parents = config.num_parents
batch       = config.batch

def main():
    killswitch()
    genes.first_gen()
    # Criar o loop sobre o numero de geracoes. Colocar as funcoes na ordem.    
    for num in range(1,num_gen+1):
        script_batch(nproc,prog)
        scripts = [i for i in os.listdir(wd) if 'genbatch' in i and '.sh' in i]
        for script in scripts:
            subprocess.call(['bash',script])
        hold_watch(wd)
        subprocess.call(eval)
        sorted_arr = order(maximize)
        elite(num_elite, sorted_arr, genes)
        best(sorted_arr, genes)
        progress(num, sorted_arr, genes)
        tng(sorted_arr, num_cross, num_parents, kappa, genes, maximize)
        script_batch(nproc,prog)
        
        

if __name__ == "__main__":
    sys.exit(main())        
