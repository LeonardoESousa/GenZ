#!/usr/bin/env python3
import sys
import os
#importing config module
import importlib
wd = os.getcwd()+'/'
config_file = wd+sys.argv[1]
spec  = importlib.util.spec_from_file_location(sys.argv[1].split('.')[0], wd+sys.argv[1])
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

#Program variables
prog      = config.prog
eval      = config.eval
kappa     = config.kappa
maximize  = config.maximize
nproc     = config.nproc
num_gen   = config.num_gen
num_elite = config.num_elite
num_cross = config.num_cross
genes     = config.genes


def main():
    genes.first_gen()
    # Criar o loop sobre o numero de geracoes. Colocar as funcoes na ordem.
    pass

if __name__ == "__main__":
    sys.exit(main())        



