#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil
import time
#importing config module
import importlib
import genz.genetic as gen
import numpy as np
import shutil

def reset():
    try:
        shutil.rmtree('Logs')
        files = [i for i in os.listdir('.') if '.dat' in i]
        for file in files:
            os.remove(file)
    except:
        print('Could not find files to delete!') 


def main():
    if sys.argv[1] == 'reset':
        sys.exit(reset())    
    wd = os.getcwd()+'/'
    spec   = importlib.util.spec_from_file_location(sys.argv[1].split('.')[0], wd+sys.argv[1])
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
    
    deltat = 30
    try:
        initial = int(max(np.loadtxt('Progress.dat')[:,0])) + 1
    except:
        genes.first_gen()
        initial = 1
    gen.killswitch(wd)
    # Criar o loop sobre o numero de geracoes. Colocar as funcoes na ordem.    
    for num in range(initial,num_gen+1):
        gen.script_batch(nproc,prog)
        scripts = [i for i in os.listdir(wd) if 'genbatch' in i and '.sh' in i]
        for script in scripts:
            subprocess.Popen(['bash', batch, script])
        start_time = time.time()
        gen.hold_watch(wd,deltat/4,num_cross)
        deltat = min(time.time() - start_time,120)
        for script in scripts:
            os.remove(wd + script)
        gen.evaluate(eval,genes)
        individual = [i for i in os.listdir(wd) if 'Individual_' in i]
        for i in individual:
            shutil.move(wd + i, wd + 'Logs/'+ i)
        sorted_arr = gen.order(maximize, genes)
        gen.elite(num_elite, sorted_arr, genes)
        best_ind = gen.best(sorted_arr, genes, maximize)
        gen.progress(num, best_ind, genes)
        gen.tng(sorted_arr, num_cross, num_parents, kappa, genes, maximize)
               

if __name__ == "__main__":   
    sys.exit(main())        
