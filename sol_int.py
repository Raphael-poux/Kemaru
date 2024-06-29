import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from copy import deepcopy
import os
import copy

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
                    dico[(i, j)] = [(i + 1, j - 1), (i + 1, j), (i + 1, j + 1), (i, j - 1), (i, j + 1)]
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

def transformation(nom):
    with open(nom,'r') as fichier:
        lignes = fichier.readlines()
        values= lignes[-1].split(sep=" ")
        if len(values)==3:
            L,H,_=values
        else:
            L,H,_,_=values
        K=[[[-1,-1] for _ in range(int(H) + 1)] for _ in range(int(L) + 1)]
        for ligne in lignes :
            ligne = ligne.rstrip("\n")
            contenu_ligne = ligne.split(sep=" ")
            if(contenu_ligne[-1] == ''):
                contenu_ligne = contenu_ligne[0:-1]
                num_ligne, num_col, num_cage = contenu_ligne
                K[int(num_ligne)][int(num_col)] = [-1, int(num_cage) + 1] # On fait commencer les cages à 1 (pas 0)
            else :
                num_ligne, num_col, num_cage, valeur = ligne.split(sep=" ")
                K[int(num_ligne)][int(num_col)] = [int(valeur), int(num_cage) + 1]
    return np.array(K)

def valeure_trouvee(d,coord,grille,dico_est_trouve, cages_valeurs):
    """renvoie True s'il ne reste qu'une valeur possible pour la case de coordonnées coord"""
    table = d[coord]
    (i,j)=coord
    if sum(table) != 1: 
        return False
    dico_est_trouve[coord]=True 
    k=0
    while (not table[k]):
        k+=1
    grille[i][j][0]=k+1
    cages_valeurs[grille[i][j][1]].append(k+1)
    return True

def lancement_interface(grille, return_dico = False):
    grille_copie = deepcopy(grille)
    nb_ligne = len(grille[0])
    nb_colonne = len(grille)
    nb_cages = nb_cage(grille)

    dico_est_trouve={}
    for i in range(nb_ligne):
        for j in range(nb_colonne):
            if grille[i][j][0]!=-1:
                dico_est_trouve[(i,j)] = True 
            else:
                dico_est_trouve[(i,j)] = False

    Taille=[]
    for i in range(1,nb_cages+1):
        Taille.append(taille_cage(grille,i))

    dico_taille = {(i,j) : Taille[grille[i][j][1]-1] for i in range(nb_ligne) for j in range(nb_colonne)}
    
    cages_positions, cages_valeurs = dico_cages(grille, nb_cages)
    dico_voisins = dico_des_voisins(nb_ligne, nb_colonne)
    
    d = { (i, j) : [True]*dico_taille[(i,j)] for i in range(nb_ligne) for j in range(nb_colonne)} 
    for i in range(nb_ligne):
        for j in range(nb_colonne):
            valeur = grille_copie[i][j][0]
            if valeur != -1 :
                d[(i, j)] = [False]*len(d[(i, j)])
                d[(i, j)][valeur - 1] = True
    
    if return_dico:
        return d
                
    return niveau_0_interface(grille_copie, d, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)


def niveau_0_interface(grille, dico, dico_est_trouve_0, cages_valeurs_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne):
    """"return peu être quelquechose, ce quelquechose c'est la grille remplie au mieux"""
    cout = 0
    steps = []
    grille_copie = deepcopy(grille)
    d = deepcopy(dico)

    dico_est_trouve=copy.deepcopy(dico_est_trouve_0)    
    cages_valeurs=copy.deepcopy(cages_valeurs_0)
    To_treat = [(i, j) for i in range(nb_ligne) for j in range(nb_colonne)] 
   
    while len(To_treat):
        
        # cas 1 : on traite une case
        element = To_treat.pop()
        if len(element) == 2:
            i, j = element
            # contact avec les voisins
            if valeure_trouvee(d,(i,j),grille_copie,dico_est_trouve, cages_valeurs): 
                value, cage = grille_copie[i][j]
                for v in dico_voisins[(i, j)] :
                    if value <= dico_taille[v] :
                        if d[v][value-1]:
                            d[v][value - 1] = False
                            cout+=1
                            steps.append(([(i,j)], deepcopy(d), v))
                        d[v][value - 1] = False
                        
                        #pour le test :
                        if not dico_est_trouve[v]:
                            To_treat.append(v)
                            To_treat.append((grille_copie[v[0]][v[1]][1],))
                for v in cages_positions[grille_copie[i][j][1]]:
                    if v != element :
                        if d[v][value-1]:
                            cout+=1
                            d[v][value - 1] = False
                            steps.append(([(i,j)],deepcopy(d), v))
                        d[v][value - 1] = False
                        if not dico_est_trouve[v]:
                            To_treat.append(v)
                To_treat.append((cage,))
        # Cas 2 : on traite une cage
        else :
            # vérifier si une valeur n'est possible que dans une seule case de la cage
            # cage = tuple de la forme (numéro de cage)
            num_cage = element[0]
            nb_elements_cage = Taille[num_cage-1]
            cases_dans_la_cage = cages_positions[num_cage]
            for i in range(1, nb_elements_cage + 1) :
                cases_possibles = []
                for case in cases_dans_la_cage :
                    if i - 1 >= len(d[case]):
                        pass
                    if (d[case][i - 1] == True) :
                        cases_possibles.append(case)
                cout+=len(cases_dans_la_cage) # ici ?
                if len(cases_possibles) == 1 :
                    # cout+=len(cases_dans_la_cage) # ou là ?
                    seule_case_possible = cases_possibles[0]
                    d[seule_case_possible ] = [False]*len(d[seule_case_possible])
                    d[seule_case_possible ][i - 1] = True
                    if not dico_est_trouve[seule_case_possible]:
                        dico_est_trouve[seule_case_possible] = True
                        steps.append(((cases_dans_la_cage),deepcopy(d), seule_case_possible))
                        To_treat.append(seule_case_possible)


    if any(sum(v) == 0 for _,v in d.items()):
        return grille_copie, steps, d, dico_est_trouve, cages_valeurs, False # à changer ?
                
    return grille_copie, steps, d, dico_est_trouve, cages_valeurs, True, cout #rajouter d pour plus tard

def niveau_1_interface(coord, grille, d, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne):
    i,j=coord
    L=d[coord]
    possible=[]
    steps_1 = {} #dico qui contient en clef les valeurs testées dans la case et en items les étapes 
    cout=sum(L)**5
    for e in range(len(L)):
        if L[e]:
            d_copie=copy.copy(d)
            d_copie[(i,j)]=[False]*e + [True]+[False]*(len(L)-1-e)
            grille_copie= copy.deepcopy(grille)
            grille_copie[i][j][0]=e+1
            dico_est_trouve_copie=copy.deepcopy(dico_est_trouve)    
            dico_est_trouve_copie[(i,j)]=True
            cages_valeurs_copie=copy.deepcopy(cages_valeurs)
            cages_valeurs_copie[grille_copie[i][j][1]].append(e+1)
            retours = niveau_0_interface(grille_copie, d_copie, dico_est_trouve_copie, cages_valeurs_copie, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            if retours[5]:
                cout += retours[-1]
                possible.append(retours[2])
                steps_1[e] = retours[1]
    steps_1[0] = concurrent_de_union_de_dicos_(possible, nb_ligne, nb_colonne)
    return steps_1


def concurrent_de_union_de_dicos_(possible:list, nb_ligne:int, nb_colonne:int) :
    n = len(possible)
    dico = {}
    for i in range(nb_ligne):
        for j in range(nb_colonne):
            dico[(i, j)] = union([possible[k][(i, j)] for k in range(n)])
    return dico

def union(liste) :
    n = len(liste[0])
    liste_union = [False]*n
    for i in range(n):
        for j in range(len(liste)):
            if liste[j][i]:
                liste_union[i] = True
                break
    return liste_union