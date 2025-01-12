import numpy as np


INFINI = np.iinfo(int).max


#############################################
#
#     Arbre couvrant de cout minimal 
#  D'après Cormen p 572 (algorithme de Prim)
#  Le graphe de départ est un graphe complet 
#  dont les sommets ont pour coordonnées x et y
#  et les distances par la matrice des distances.
#
#    L'algorithme de Prim évolue de sommets en sommets
#  et est similaire à l'algo de Dijkstra pour les plus courts chemins.
#
#  Le calcul des distances est très long. 
#  Cet algo général pourrait etre amélioré 
#  pour ce cas particulier : regarder simplement les voisins
#  au lieu de considérer tous les sommets de la file dans la boucle
#  for dans le while.
#  
#    L'avantage de cet algo est de pouvoir choisir la racine
#  d'où une meilleure esthétique car l'arbre se développe
#  à partir de la racine.
#
#############################################


def compute(x, y, vs, graph) :

    n = len(x)
    
    racine = plusPresDuCentre(x,y)
    print('racine=', racine)
    
    # initialisations
    
    cout = [INFINI] * n
    prec = [-1] * n
    distances = computeDist(vs,graph) 
   
    # file de priorité des sommets
    # triée en permanence en ordre non décroissant des couts

    file = [v for v in range(n)]

    # on place la racine en tete de la file, avec un cout 0

    file[0] = racine
    file[racine] = 0  # echange
    cout[racine] = 0

    # c'est parti
    
    while file != [] :
        v = file.pop(0)  # (deletemin)
        for i, z in enumerate(file) :   # i est l'index de z dans file
            d = distances[v][z]
            if  d < cout[z] :
                cout[z] = d
                prec[z] = v
                # on reordonne la file (decreasekey)
                while i > 0 and d < cout[file[i-1]] :
                    file[i] = file[i-1]
                    i -= 1
                file[i] = z
                
    # on recupere le cout de l'arbre
    #c = 0
    #for i, v in enumerate(prec) :
    #    if v != -1 :
    #        c += distances[i][v]

    return prec


def plusPresDuCentre(x,y) :
    n = len(x)
    d2min = INFINI
    ic = -1
    for i in range(n) :
        d2 = x[i]*x[i] + y[i]*y[i]
        if d2 < d2min :
            d2min = d2
            ic = i
    return ic
        

def computeDist(vs,graph) :
    n = len(vs)
    d = np.full((n,n), 2, dtype = int)
    for i,v  in enumerate(vs) :
        for j,w in enumerate(vs) :
            if i == j :
                d[i][j] = 0
            elif graph.exist_edge(v,w) :
                d[i][j] = 1
    return d