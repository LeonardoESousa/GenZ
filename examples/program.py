import sys
from genz.genetic import get_genes

id = sys.argv[1]
genes = get_genes(id)

resultado = abs(genes[0]**2 - genes[1]**3 + genes[2]**2)

with open('Individual_'+id+'_.log', 'w') as f:
    f.write(str(resultado))