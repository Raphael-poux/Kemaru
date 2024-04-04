
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from copy import deepcopy
import os
import copy

def si_jamais(fichier):
    grid = {}
    number_of_groups = 0

    with open(fichier, 'r', encoding='utf-8') as file:
        for line in file:
            numbers = line.split()
            row = int(numbers[0])
            col = int(numbers[1])
            group = int(numbers[2])
            number_of_groups = max(group, number_of_groups)
            if len(numbers) == 4:
                value = int(numbers[3])
            else:
                value = -1
            
            grid[(row, col)] = (value, group)
    h, w = (max(grid))
    grid = [[grid[(i, j)] for j in range(w + 1)] for i in range(h + 1)]
    
    return grid, number_of_groups + 1

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
            
        
print(transformation("exemples_grilles/instances/v10_b1_3.txt"))

#grille = np.array([[[-1, 1], [3, 1], [4, 1]], [[-1, 2], [1, 1], [-1, 1]], [[2, 2], [-1, 2], [-1, 2]]])
#grille = np.array(transformation("exemples_grilles/instances/v10_b1_9.txt"))
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
    if sum(table) != 1: 
        return False
    dico_est_trouve[coord]=True 
    k=0
    while (not table[k]):
        k+=1
    grille[i][j][0]=k+1
    cages_valeurs[grille[i][j][1]].append(k+1)
    return True


def lancement(grille):
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
                
    niv0 = niveau_0(grille_copie, d, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
    variables = dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne

    return niv0 + variables
    
def niveau_0(grille, dico, dico_est_trouve_0, cages_valeurs_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne):
    """"return peu être quelquechose, ce quelquechose c'est la grille remplie au mieux"""
    grille_copie = deepcopy(grille)
    d= deepcopy(dico)
    dico_est_trouve=copy.deepcopy(dico_est_trouve_0)    
    cages_valeurs=copy.deepcopy(cages_valeurs_0)
    To_treat = [(i, j) for i in range(nb_ligne) for j in range(nb_colonne)] 
   
    while len(To_treat):
        
        #print("la grille")
        #affichage(grille_copie)
        #input()
        # cas 1 : on traite une case
        element = To_treat.pop()
        if len(element) == 2:
            i, j = element
            # contact avec les voisins
            if valeure_trouvee(d,(i,j),grille_copie,dico_est_trouve, cages_valeurs): 
                value, cage = grille_copie[i][j]
                for v in dico_voisins[(i, j)] :
                    if value <= dico_taille[v] :
                        d[v][value - 1] = False
                        #pour le test :
                        if not dico_est_trouve[v]:
                            To_treat.append(v)
                            To_treat.append((grille_copie[v[0]][v[1]][1],))
                for v in cages_positions[grille_copie[i][j][1]]:
                    if v != element :
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
                    if (d[case][i - 1] == True) :
                        cases_possibles.append(case)
                if len(cases_possibles) == 1 :
                    seule_case_possible = cases_possibles[0]
                    d[seule_case_possible ] = [False]*len(d[seule_case_possible])
                    d[seule_case_possible ][i - 1] = True
                    if not dico_est_trouve[seule_case_possible]:
                        dico_est_trouve[seule_case_possible] = True
                        To_treat.append(seule_case_possible)


    if any(sum(v) == 0 for _,v in d.items()):
        return grille_copie, d, dico_est_trouve, cages_valeurs, False # à changer ?
                
    return grille_copie, d, dico_est_trouve, cages_valeurs, True #rajouter d pour plus tard

#def niveau_n(n,grille:list,d:dict):
#    """level n processing including deep research black box PST research and Von Marken  stochastic process"""                             
#    grille_copie = deepcopy(grille)
#    if n == 0:return niveau_0
#    niveau_n(n-1,grille,d)


def cases_restantes(dico_est_trouve):
   return sum(list(dico_est_trouve.values()))




# v10_b1_15.txt : non résolue avec le niveau 0



def niveau_1(coord, grille, d, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne):
    i,j=coord
    L=d[coord]
    possible=[]
    for e in range(len(L)):
        if L[e]:
            d_copie=copy.copy(d)
            d_copie[(i,j)]=[False]*e + [True]+[False]*(len(L)-1-e)
            grille_copie= copy.deepcopy(grille)
            grille_copie[i][j][0]=e+1
            dico_est_trouve_copie=copy.deepcopy(dico_est_trouve)    #Complexité linéaire en n^2
            dico_est_trouve_copie[(i,j)]=True
            cages_valeurs_copie=copy.deepcopy(cages_valeurs)
            cages_valeurs_copie[grille_copie[i][j][1]].append(e+1)
            if valeure_trouvee(d_copie,coord,grille_copie,dico_est_trouve_copie, cages_valeurs_copie):
                dico=niveau_0(grille_copie, d_copie, dico_est_trouve_copie, cages_valeurs_copie, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
                if dico[4]:
                    possible.append(dico[1])
    return concurrent_de_union_de_dicos_(possible, nb_ligne, nb_colonne)

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
    
    
            
def union_de_dicos(possible:list, nb_ligne:int, nb_colonnes:int)->dict:
    if len(possible):
        A_union = [[[possible[0][(i,j)][k] for k in range(len(possible[0][(i,j)]))]for j in range(nb_colonnes) ]for i in range(nb_ligne) ]
        for dico in possible:
            A_union = [[list(np.logical_or(np.array(dico[(i,j)]),np.array(A_union[i][j]))) for j in range(nb_colonnes) ]for i in range(nb_ligne) ]
        return dict(zip([(i,j) for i in range(nb_ligne) for j in range(nb_colonnes)],[A_union[i][j] for i in range(nb_ligne) for j in range(nb_colonnes)]))    
    return 'rutabaga'
    
    
            
def main(path) :
    #path = "exemples_grilles/instances/v10_b100_1.txt"
    grille = np.array(transformation(path))
    premier_niveau_0 = lancement(grille)
    #grille_niveau_0, dico,dico_est_trouve,cages_valeurs = niveau_0(grille)
    grille, dico, dico_est_trouve, cages_valeurs, grille_valide, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne = premier_niveau_0
    if not grille_valide :
        print("grille non valide")
        return 1
    liste_cases_vides = get_missing_values(grille)
    if len(liste_cases_vides) == 0 :
        return grille
    else:
        k = 0
        while k < len(liste_cases_vides):
            i,j = liste_cases_vides[k]#liste_cases_vides = [[i1, i2 ...], [j1, j2, ...]]
            d_niveau_1 = niveau_1((i,j), grille, dico, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs, new_grille_valide = niveau_0(grille, d_niveau_1, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            #si on n'apprend pas des nouvelles choses
            if dico == new_dico :
                k += 1
            else:
                grille, dico, dico_est_trouve, cages_valeurs = new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs
                liste_cases_vides = get_missing_values(grille)
                k = 0
    return grille
    
#def niveau_0(grille_copie, d, dico_taille, Taille, dico_voisins, cages_positions, cages_valeurs, dico_est_trouve, nb_ligne, nb_colonne):

#print(lancement(grille))
#affichage(lancement(grille))
#print(os.listdir("instances"))
nb_false = 0
nb_true = 0
cpt = 0
for file in os.listdir("exemples_grilles/instances") : # "exemples_grilles/instances"
    
    grille = transformation("exemples_grilles/instances/" + file)
    grille = main("exemples_grilles/instances/" + file)
    if (grille == -1).any() :
        nb_false += 1
    else :
        nb_true += 1
    cpt += 1
    if cpt % 50 == 0 :
        print("nombre de grilles testees" + str(cpt))
        print("nombre de grilles non résolues :" + str(nb_false))
        print("nombre de grilles résolues :" + str(nb_true))
        print()

print("nombre de grilles testees" + str(cpt))
print("nombre de grilles non résolues :" + str(nb_false))
print("nombre de grilles résolues :" + str(nb_true))
print()
    
    