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

def main():
    pass

if __name__ == "__main__":
    sys.exit(main())        

