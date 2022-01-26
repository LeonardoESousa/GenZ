#Genetic algorithm

import sys
import numpy as np
import random
import os
import time

#Program
prog = 'predict.py'
#evaluation script
eval = "eval.py"
#coefficient of variation for mutations
cv = 0.3

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

#Establish the genes
genes = []
rounding = []

gene1 = np.round(np.linspace(-1,-1,30),1) #Kct
genes.append(gene1)
rounding.append(3) 
gene2 = np.round(np.linspace(-1,-1,30),1) #t
genes.append(gene2)
rounding.append(3)
gene3 = np.round(np.linspace(-1,1,30),1) #Kx
genes.append(gene3)
rounding.append(3)
gene4 = np.round(np.linspace(-1,1,30),1) #DE
genes.append(gene4)
rounding.append(3)
gene5 = np.round(np.linspace(-1,1,30),1) #Kle
genes.append(gene5)
rounding.append(3)


#Generates the first generation individuals
def initial_gen(n):
    for i in range(0,n):
        ps = []
        for j in range(len(genes)):
            ps.append(random.choice(genes[j]))
            ps = list(map(str,ps))
        #j = i//nproc
        if ps not in configs:
            with open("EX.sh", 'a') as f:
                f.write("ts python3 "+prog+" "+' '.join(ps)+"\n")
            configs.append(ps)  
        

#Orders the results. 
def order(file): #file - results. coluna - collumn with the values of the evaluation function
    with open(file, 'r') as f:
        with open("Order.txt", 'w') as g:
            lines = f.readlines()
            for line in sorted(lines, reverse=maximize, key=lambda line: float(line.split()[len(genes)])):
                g.write(''.join(line))
    
    
#Selects the next generation. 
def tng(number, surv): #number is number of elements in the generation. surv is number or survivors of each iteration
    d = {}
    pesos = []
    for g in range(1,len(genes)+1): #sets a list for each gene
        key = 'gene'+str(g)
        d.setdefault(key, [])
    with open("Order.txt", 'r') as f:
        with open("Survivors.txt", 'w') as g:
            for i, line in enumerate(f):
                line = line.split()
                for l in range(len(genes)):
                    d['gene'+str(l+1)].append(line[l]) 
                pesos.append(line[len(genes)])
                if i < surv:
                    g.write('    '.join(line)+"\n") 
    pesos = list(map(float, pesos))
    if maximize:
        pass
    else:
        pesos = [1/i for i in pesos]
    #probs1 = [max(pesos)/float(x) for x in pesos] #[(max(pesos) - float(x)) for x in pesos]
    #if sum(probs0) < 0.00001:
    #   print "Converged"
    #   sys.exit()
    try:
        probs0 = [(float(x)/sum(pesos)) for x in pesos]
    except:
        probs0 = [1/len(pesos) for x in pesos]
    probs = []
    p = 0
    for j in range(len(probs0)):
        p = p + probs0[j]*100
        probs.append(p)
    pares = []
    while len(pares) < number:
        pais = []
        while len(pais) != 2:
            p = 100*(random.uniform(0,1))
            for x in range(0,len(probs)):
                if p < probs[x]:
                    pais.append(x)
                    break       
        #if (pais[0],pais[1]) not in pares and (pais[1],pais[0]) not in pares:# and pais[1] != pais[0]:
        pares.append((pais[0],pais[1]))         
    with open("NextGen.txt", 'w') as f:
        for k in range(len(pares)):
            newgenes = []
            for g in range(1,len(genes)+1):
                g1 = d['gene'+str(g)][pares[k][0]]
                g2 = d['gene'+str(g)][pares[k][1]]
                ng = mutation(float(g1), float(g2))
                newgenes.append(ng)
            newgenes = list(map(str, newgenes)) 
            f.write('    '.join(newgenes)+'\n')         


def mutation(a, b):
    med = (a+b)/2.0
    sigma = abs(med)*cv
    #ng = +1
    #while ng > 0:
    ng = np.random.normal(med, sigma)
    return ng       
            
def individuals():
    c = 0
    with open("NextGen.txt", 'r') as f:
        for n, line in enumerate(f):
            line = line.split()
            ps = [] 
            for i in range(0,len(line)):
                ps.append(round(float(line[i]),rounding[i]))
            ps = list(map(str,ps))
            #j = 10 + n//nproc
            if ps not in configs:
                c = c+1
                with open("EX.sh", 'a') as h:
                    h.write("ts python3 "+prog+" "+'     '.join(ps)+"\n")
                configs.append(ps)
            else:
                pass
    if c == 0:
        print("No new configurations")
        sys.exit()

def include_survivors():
    with open("Survivors.txt", 'r') as h:
        for line in h:
            line = line.split()
            with open("Report.txt", 'a') as g:
                g.write('     '.join(line)+'\n')            
                
                
def pick_best(file):
    with open(file, 'r') as f:
        for line in f:
            return line, line.split()[len(genes)]
            break
                
def check_best(file, best):
    with open(file, 'r') as f:
        for line in f:
            line1 = line.split()
            if float(line1[len(genes)]) == float(best):     
                with open("Best.txt", 'a') as g:
                    g.write(line)
            elif maximize and float(line1[len(genes)]) > float(best):
                with open("Best.txt", 'w') as g:
                    g.write(line)
                    best = float(line1[len(genes)])
            elif not maximize and float(line1[len(genes)]) < float(best):
                with open("Best.txt", 'w') as g:
                    g.write(line)
                    best = float(line1[len(genes)])        
        param = []
        for i in range(0,len(genes)):
            ls = []
            j = 0
            with open("Best.txt", 'r') as f:
                for line in f:
                    line = line.split()
                    ls.append(float(line[i]))
                    j = j+1
            m = np.mean(ls)
            s = np.nanstd(ls)
            param.append([m,s,j])
    with open("2Best.txt", 'w') as f:
        f.write("----------------------------------\n")
        f.write("\nMean    StD    Degeneracy\n")
        for elem in param:
            f.write(str(elem[0])+"    "+str(elem[1])+"    "+str(elem[2])+"\n")  
        f.write("----------------------------------\n")
        

def watcher(counter):
    sims = [i for i in os.listdir('.') if 'Simulation' in i]
    oks = []
    for sim in sims:
        passar = False
        with open(sim,'r') as f:
            for line in f:
                if 'termination' in line:
                    passar = True
                    oks.append(1)
        if not passar:
            break 
    if len(oks) == counter:
        return True
    else:
        return False
 
def conta(file):
    counter = 0
    with open(file,'r') as f:
        for line in f:
            if 'python' in line:
                counter += 1
    return counter     

    

configs = []    
#If results are available before the start of the genetic process
rounds = []
try:
    with open("Progress.txt", 'r') as f:
        for line in f:
            rounds.append([line.split()[0],line.split()[-1]])
    ultimo = int(float(rounds[-1][0])) +1           
    best = float(rounds[-1][1])
    os.chdir("Logs")
    params = []
    for file in os.listdir('.'):
        if 'Simulation_' in file:
            file = file.split('_')
            for i in range(2,len(file),2):
                params.append(file[i])
        configs.append(params)
    os.chdir("..")
    individuals()
except:
    ultimo = 0
    #Generates initial population
    initial_gen(num_cross)
    best = 0

           
                

#Initiate loop for generations
for a in range(ultimo,num_gen):
    #Runs exciton simulations
    os.system("chmod +x EX.sh")
    counter = conta('EX.sh')
    os.system("./EX.sh")
    seguir = False
    while seguir == False:
        seguir = watcher(counter)
        time.sleep(20)
    os.system("rm EX.sh")
    #Evaluates the results
    os.system("python3 "+eval)
    #Check the best
    if a > 0:
        line, best = pick_best("Order.txt")
        check_best("Report.txt", best)
    #Add survivors to the results
    try:
        include_survivors()
    except:
        pass
    #Orders the results
    order("Report.txt") 
    #Creates next generation
    tng(num_cross,num_elite)
    #Generates new individuals
    individuals()
    line, best = pick_best("Order.txt")
    if a == 0:
        check_best("Order.txt", best)
    with open("Progress.txt", 'a') as f:
        f.write(str(a)+"    "+line)

    
            