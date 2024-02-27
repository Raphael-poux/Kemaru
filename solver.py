import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from copy import deepcopy


grille = np.array([[[5, 1], [3, 1], [4, 1]], [[-1, 2], [1, 1], [-1, 1]], [[2, 2], [-1, 2], [-1, 2]]])

def affichage(grille):
    for ligne in grille:
        for elem in ligne:
            print(elem[0], end = ' ')
        print()

def nb_cage(grille):
    """""renvoie le nombre de cages"""
    nb_ligne = len(grille)
    nb_colonne = len(grille[0])
    return np.max(grille[:,:,1])
    
def taille_cage(grille, num_cage):
    """donne la taille de la cage"""
    cage = grille[grille[:, :, 1] == num_cage]
    return len(cage)

def dico_des_voisins(nb_ligne, nb_colonne):
    dico = {}
    for i in range(nb_ligne):
        for j in range(nb_colonne):
            if i == 0:
                if j == 0:
                    dico[(i, j)] = [(i + 1, j + 1), (i + 1, j), (i, j + 1)]
    ###d est un dictionnaire avec pour clés les coordonnées des cases et en valeurs une liste L de taille 9
    ### où L[i] vaut True si i+1 est une valeur possible pour la case en question et False si la case ne peut pas avoir la valeur i+1

                elif j == nb_colonne - 1:
                    dico[(i, j)] = [(i + 1, j - 1), (i + 1, j), (i, j - 1)]

                else:
                    dico[(i, j)] = [(i + 1, j - 1), (i + 1, j), (i + 1, j +- 1), (i, j - 1), (i, j + 1)]
                continue

            if i == nb_ligne - 1:
                if j == 0:
                    dico[(i, j)] = [(i - 1, j + 1), (i - 1, j), (i, j + 1)]

                elif j == nb_colonne - 1:
                    dico[(i, j)] = [(i - 1, j - 1), (i - 1, j), (i, j - 1)]

                else :
                    dico[(i, j)] = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1)]
                continue

            if j == nb_colonne - 1:
                dico[(i, j)] = [(i + 1, j), ( i + 1, j- 1), (i, j - 1), (i - 1, j), (i - 1, j - 1)]
                continue

            if j == 0:
                dico[(i, j)] = [(i + 1, j), ( i + 1, j + 1), (i, j + 1), (i - 1, j), (i - 1, j + 1)]
                continue

            dico[(i, j)] = [(i + 1, j + 1), (i + 1, j), ( i + 1, j- 1),
                    (i, j + 1), (i, j - 1),
                    (i - 1, j + 1), (i - 1, j), (i - 1, j - 1)]

    return dico



#def dico_des_voisins2(nb_ligne, nb_colonne):
#    dico = {}
#    for i in range(nb_ligne):
#        for j in range(nb_colonne):
#            #for l in (-1, 0, 1) :
            #    for m in (-1, 0, 1):
            #        vois = (i+l, j+m)
            #        if(vois[0] >= 0 and vois[0] <= nb_ligne and vois[1] >= 0 and vois[1] <= nb_colonne and vois != (i, j)) :
            #            dico[(i, j)].append(vois)
            #if i == 0:
            #    if j == 0:
            #        dico[(i, j)] = [(i + 1, j + 1), (i + 1, j), (i, j + 1)]
    ###d est un dictionnaire avec pour clés les coordonnées des cases et en valeurs une liste L de taille 9
    ### où L[i] vaut True si i+1 est une valeur possible pour la case en question et False si la case ne peut pas avoir la valeur i+1
#
#                elif j == nb_colonne:
#                    dico[(i, j)] = [(i + 1, j - 1), (i + 1, j), (i, j - 1)]
#
#                else:
#                    dico[(i, j)] = [(i + 1, j - 1), (i + 1, j), (i + 1, j +- 1), (i, j - 1), (i, j + 1)]
#                continue
#
#            if i == nb_ligne:
#                if j == 0:
#                    dico[(i, j)] = [(i - 1, j + 1), (i - 1, j), (i, j + 1)]
#
#                elif j == nb_colonne:
#                    dico[(i, j)] = [(i - 1, j - 1), (i - 1, j), (i, j - 1)]
#
#                else :
#                    dico[(i, j)] = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1)]
#                continue
#
#
#            dico[(i, j)] = [(i + 1, j + 1), (i + 1, j), ( i + 1, j- 1),
#                    (i, j + 1), (i, j - 1),
#                    (i - 1, j + 1), (i - 1, j), (i - 1, j - 1)]
#
#    return dico

def dico_cages(grille, nb_cage):
    dico_valeurs = { i : [] for i in range(1,nb_cage+1)}
    dico_positions = { i : [] for i in range(1,nb_cage+1)}
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            value, cage = grille[i][j]
            dico_positions[cage].append((i, j))
            if value != - 1:
                dico_valeurs[cage].append(value)
    return dico_positions, dico_valeurs

def solved(grille)->bool:  
    """return True if grille is full, else return False"""    
    nb_ligne = len(grille)
    nb_colonne = len(grille[0])
    for i in range(nb_ligne):
        for j in range(nb_colonne):
            if grille[i][j][0]<0:return False
    return True

def get_missing_values(grille):
    """return the coordinates of cases with no value"""
    nb_ligne = len(grille)
    nb_colonne = len(grille[0])
    List_coords = []
    for i in range(nb_ligne):
        for j in range(nb_colonne):
            if grille[i][j][0]<0:List_coords.append((i,j))
    return List_coords

def valeure_trouvee(d,coord,grille,dico_est_trouve, cages_valeurs):
    """renvoie True s'il ne reste qu'une valeur possible pour la case de coordonnées coord"""
    table = d[coord]
    (i,j)=coord
    if grille[i][j][0] != - 1:
        return True
    if sum(table) > 1:
        return False
    dico_est_trouve[coord]=True 
    k=0
    while not table[k]:
        k+=1
    grille[i][j][0]=k+1
    cages_valeurs[grille[i][j][1]].append(k+1)
    return True

    
def niveau_0(grille,**kwds):
    """"return peu être quelquechose, ce quelquechose c'est la grille remplie au mieux"""
    # On ne touche pas à la grille, on ne modifie que la copie
    grille_copie = deepcopy(grille)
    nb_ligne = len(grille[0])
    nb_colonne = len(grille)
    nb_cages = nb_cage(grille)
    # Liste des tailles de chaque cage, ie Taille[i] donne la taille de la cage i
    Taille=[]
    for i in range(1,nb_cages+1):
        Taille.append(taille_cage(grille,i))
    # dico_est_trouve[(i, j)] faut True si la case (i, j) a été trouvée et false sinon
    dico_est_trouve={}
    for i in range(nb_ligne):
        for j in range(nb_colonne):
            if grille[i][j][0]!=-1:
                dico_est_trouve[(i,j)] = True 
            else:
                dico_est_trouve[(i,j)] = False 
    dico_taille = {(i,j) : Taille[grille[i][j][1]-1] for i in range(nb_ligne) for j in range(nb_colonne)}
    if 'd' in dict(**kwds).keys(): d = d
    else : d = { (i, j) : [True]*dico_taille[(i,j)] for i in range(nb_ligne) for j in range(nb_colonne)}  
    dico_voisins = dico_des_voisins(nb_ligne, nb_colonne) 
    cages_positions, cages_valeurs = dico_cages(grille, nb_cages)
    
                
    To_treat = [(i, j) for i in range(nb_ligne) for j in range(nb_colonne)] 
   
    while len(To_treat):
        print("la grille")
        affichage(grille_copie)
        input()
        # cas 1 : on traite une case
        element = To_treat.pop()
        print("element retiré de la pile")
        print(element)
        if len(element) == 2:
            i, j = element
            # contact avec les voisins
            print(valeure_trouvee(d,(i,j),grille_copie,dico_est_trouve, cages_valeurs))
            if valeure_trouvee(d,(i,j),grille_copie,dico_est_trouve, cages_valeurs): 
                value, cage = grille_copie[i][j]
                for v in dico_voisins[(i, j)] :
                    if value <= dico_taille[v] :
                        d[v][value - 1] = False
                        if not dico_est_trouve[v]:
                            To_treat.append(v)
                for v in cages_positions[grille_copie[i][j][1]]:
                    d[v][value - 1] = False
                    if not dico_est_trouve[v]:
                        To_treat.append(v)
                To_treat.append((cage,))
        # Case 2 : on traite une case
        else :
            # vérifier si une valeur n'est possible que dans une seule case de la cage
            # cage = tuple de la forme (numéro de cage)
            num_cage = element[0]
            nb_elements_cage = Taille[num_cage]
            cases_dans_la_cage = cages_positions[num_cage]
            for i in range(1, nb_elements_cage + 1) :
                cases_possibles = []
                for case in cases_dans_la_cage :
                    if (d[case][i - 1] == True) :
                        cases_possibles.append[case]
                if len(cases_possibles) == 1 :
                    seule_case_possible = cases_possibles[0]
                    grille_copie[seule_case_possible[0]][seule_case_possible[1]] = i
                    dico_est_trouve[seule_case_possible] = True
                    To_treat.append(seule_case_possible)
                
                
    return grille_copie #rajouter d pour plus tard

#def niveau_n(n,grille:list,d:dict):
#    """niveau n processing including deep research black box ppt research and Von Marken  stochastic process"""                             
#    grille_copie = deepcopy(grille)
#    if n == 0:return niveau_0
#    niveau_n(n-1,grille,d)


def cases_restantes(dico_est_trouve):
   return sum(list(dico_est_trouve.values()))


print(niveau_0(grille))


affichage(niveau_0(grille))
   