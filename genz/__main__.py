#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil
import time
import importlib.util
import numpy as np
import genz.genetic as gen


def reset():
    if os.path.isdir('Logs'):
        shutil.rmtree('Logs')
    files = [i for i in os.listdir('.') if '.dat' in i or 'genbatch' in i]
    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            continue


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
    except FileNotFoundError:
        genes.first_gen()
        initial = 1
    gen.killswitch(wd)

    # Criar o loop sobre o numero de geracoes. Colocar as funcoes na ordem.
    for num in range(initial,num_gen+1):
        data = np.loadtxt('NextGen.dat')
        if data.ndim == 1:
            data = data.reshape(1, -1)
        all_ids = [int(i) for i in data[:,0]]
        pending = gen.pending_ids(all_ids)
        pop  = len(pending)
        if pop > 0:
            gen.script_batch(nproc,prog,pending)
            scripts = [i for i in os.listdir(wd) if 'genbatch' in i and '.sh' in i]
            for script in scripts:
                subprocess.Popen(['bash', batch, script])
            start_time = time.time()
            gen.hold_watch(wd,deltat/4,pop)
            deltat = min(time.time() - start_time,120)
            for script in scripts:
                os.remove(wd + script)
        else:
            # Restart path: all current individuals already finished.
            # If their logs are present, continue with evaluation/tng.
            current_logs = [
                i for i in os.listdir(wd)
                if 'Individual_' in i and i.endswith('_.log')
            ]
            if len(current_logs) == 0:
                print('No pending jobs and no Individual_*.log files in the working directory. Skipping generation.')
                continue
            print('No pending jobs. Resuming from existing completed Individual_*.log files.')

        gen.evaluate(eval,genes)
        individual = [i for i in os.listdir(wd) if 'Individual_' in i]
        for i in individual:
            shutil.move(wd + i, wd + 'Logs/'+ i)
        sorted_arr = gen.order(maximize, genes)
        gen.elite(num_elite, sorted_arr, genes)
        best_ind = gen.best(sorted_arr, genes, maximize)
        gen.progress(num, best_ind, genes)
        pop = gen.tng(sorted_arr, num_cross, num_parents, kappa, genes)


if __name__ == "__main__":
    sys.exit(main())
