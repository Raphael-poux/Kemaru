
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from copy import deepcopy
import os
import copy
import time 

temps_des_dicos = {"grille_n0" : 0, 
                   "d_n0" : 0, 
                   "dico_trouve_n0" : 0, 
                   "cage_valeur_n0" : 0,
                   "grille_n1" : 0, 
                   "d_n1" : 0, 
                   "dico_trouve_n1" : 0, 
                   "cage_valeur_n1" : 0}

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
            
        
# print(transformation("exemples_grilles/instances/v10_b1_3.txt"))

#grille = np.array([[[-1, 1], [3, 1], [4, 1]], [[-1, 2], [1, 1], [-1, 1]], [[2, 2], [-1, 2], [-1, 2]]])
#grille = np.array(transformation("exemples_grilles/instances/v10_b1_9.txt"))
def affichage(grille):
    for ligne in grille:
        for elem in ligne:
            print(elem[0], end = ' ')
        print()

def affichage2(grille):
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if (i, j) == (2, 1) :
                print('A', end = ' ')
            else :
                print(grille[i][j][0], end = ' ')
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

def get_missing_values(grille, dico_taille ):
    """return the coordinates of cases with no value"""
    nb_ligne = len(grille)
    nb_colonne = len(grille[0])
    List_coords = []
    cages_valeurs = {}
    for i in range(nb_ligne):
        for j in range(nb_colonne):
            if grille[i][j][0]<0:
                List_coords.append((i,j))
                cage_number = grille[i][j][1]
                if cage_number not in cages_valeurs:
                    cages_valeurs[cage_number] = []
                cages_valeurs[cage_number].append(grille[i][j][0])

    liste_a_trier = [dico_taille[coord] - len(cages_valeurs[grille[coord[0]][coord[1]][1]]) for coord in List_coords]
    indices_tries = sorted(range(len(liste_a_trier)), key=lambda i: liste_a_trier[i])

    return [List_coords[i] for i in indices_tries]

def valeure_trouvee(d,coord,grille,dico_est_trouve):
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
    return True

def nb_h(dico):
    h = 0
    for k,v in dico.items():
        a = 887*k[0] + 991 * k[1] + 643*sum(v[i] * (1 << i) for i in range(len(v)))
        h += a
    return h
    exit()

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
    
    cages_positions, _ = dico_cages(grille, nb_cages)
    dico_voisins = dico_des_voisins(nb_ligne, nb_colonne)
    
    d = { (i, j) : [True]*dico_taille[(i,j)] for i in range(nb_ligne) for j in range(nb_colonne)} 
    for i in range(nb_ligne):
        for j in range(nb_colonne):
            valeur = grille_copie[i][j][0]
            if valeur != -1 :
                d[(i, j)] = [False]*len(d[(i, j)])
                d[(i, j)][valeur - 1] = True
                
    niv0 = niveau_0(grille_copie, d, dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
    variables = dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne

    return niv0 + variables
    
def niveau_0(grille, dico, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne):
    """"return peu être quelquechose, ce quelquechose c'est la grille remplie au mieux"""
    cout = 0
    t = time.time()
    grille_copie = deepcopy(grille)
    temps_des_dicos["grille_n0"] += time.time() - t

    t = time.time()
    d = deepcopy(dico)
    temps_des_dicos["d_n0"] += time.time()- t

    #t = time.time()
    #dico_est_trouve=copy.deepcopy(dico_est_trouve_0)
    #temps_des_dicos["dico_trouve_n0"] += time.time() - t
    dico_est_trouve = {}

    t = time.time()    
    temps_des_dicos["cage_valeur_n0"] += time.time() - t

    #To_treat = [(i, j) for i in range(nb_ligne) for j in range(nb_colonne)] 
    To_treat = set([(i, j) for i in range(nb_ligne) for j in range(nb_colonne)]) 
   
    while len(To_treat):
        
        #print("la grille")
        #affichage(grille_copie)
        #input()
        # cas 1 : on traite une case
        element = To_treat.pop()
        if len(element) == 2:
            i, j = element
            # contact avec les voisins
            if valeure_trouvee(d,(i,j),grille_copie,dico_est_trouve): 
                value, cage = grille_copie[i][j]
                for v in dico_voisins[(i, j)] :
                    if value <= dico_taille[v] :
                        if d[v][value-1]:
                            cout+=1
                        d[v][value - 1] = False
                        #pour le test :
                        if grille_copie[v[0]][v[1]][0] == -1:
                            To_treat.add(v)
                            To_treat.add((grille_copie[v[0]][v[1]][1],))
                for v in cages_positions[grille_copie[i][j][1]]:
                    if v != element :
                        if d[v][value-1]:
                            cout+=1
                        d[v][value - 1] = False
                        if grille_copie[v[0]][v[1]][0] == -1:
                            To_treat.add(v)
                To_treat.add((cage,))
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
                        print("debug niveau 0" + str(i-1))
                        print(len(d[case]))
                    if (d[case][i - 1] == True) :
                        cases_possibles.append(case)
                cout+=len(cases_dans_la_cage) # ici ?
                if len(cases_possibles) == 1 :
                    # cout+=len(cases_dans_la_cage) # ou là ?
                    seule_case_possible = cases_possibles[0]
                    d[seule_case_possible ] = [False]*len(d[seule_case_possible])
                    d[seule_case_possible ][i - 1] = True
                    if grille_copie[seule_case_possible[0]][seule_case_possible[1]][0] == -1:
                        dico_est_trouve[seule_case_possible] = True
                        To_treat.add(seule_case_possible)


    if any(sum(v) == 0 for _,v in d.items()):
        return grille_copie, d, dico_est_trouve, False # à changer ?
                
    return grille_copie, d, dico_est_trouve, True, cout #rajouter d pour plus tard

#def niveau_n(n,grille:list,d:dict):
#    """level n processing including deep research black box PST research and Von Marken  stochastic process"""                             
#    grille_copie = deepcopy(grille)
#    if n == 0:return niveau_0
#    niveau_n(n-1,grille,d)


def cases_restantes(dico_est_trouve):
   return sum(list(dico_est_trouve.values()))




# v10_b1_15.txt : non résolue avec le niveau 0



def niveau_1(coord, grille, d, dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne):
    i,j=coord
    L=d[coord]
    possible=[]
    cout=sum(L)**5
    for e in range(len(L)):
        if L[e]:

            t = time.time()
            d_copie=copy.copy(d)
            temps_des_dicos["dico_trouve_n1"] += time.time() - t

            d_copie[(i,j)]=[False]*e + [True]+[False]*(len(L)-1-e)

            t = time.time()
            grille_copie= copy.deepcopy(grille)
            temps_des_dicos["grille_n1"] += time.time() - t

            grille_copie[i][j][0]=e+1

            t = time.time()
            dico_est_trouve_copie=copy.deepcopy(dico_est_trouve)    #Complexité linéaire en n^2
            temps_des_dicos["dico_trouve_n1"] += time.time() - t

            dico_est_trouve_copie[(i,j)]=True

            t = time.time()
            temps_des_dicos["cage_valeur_n1"] += time.time() - t

            retours=niveau_0(grille_copie, d_copie, dico_est_trouve_copie, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            if retours[3]:
                cout += retours[-1]
                possible.append(retours[1])

    return concurrent_de_union_de_dicos_(possible, nb_ligne, nb_colonne), cout

def niveau_2(coord1,coord2, grille, d, dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne) :
    (i,j),(k,l)=coord1,coord2
    L1=d[coord1]
    L2 = d[coord2]
    cout = (sum(L1) + sum(L2))**2
    possible=[]
    for e1 in range(len(L1)):
        for e2 in range(len(L2)):
            if L1[e1] and L2[e2]:
                d_copie=copy.deepcopy(d)
                d_copie[(i,j)]=[False]*e1 + [True]+[False]*(len(L1)-1-e1)
                d_copie[(k,l)] = [False]*e2 + [True] + [False]*(len(L2)-1-e2)
                grille_copie= copy.deepcopy(grille)
                grille_copie[i][j][0]=e1+1
                grille_copie[k][l][0]=e2+1
                dico_est_trouve_copie=copy.deepcopy(dico_est_trouve)    #Complexité linéaire en n^2
                dico_est_trouve_copie[(i,j)]=True
                dico_est_trouve_copie[(k,l)]=True
                retours=niveau_0(grille_copie, d_copie, dico_est_trouve_copie, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
                if retours[3]:
                    cout += retours[-1]
                    possible.append(retours[1])
    return concurrent_de_union_de_dicos_(possible, nb_ligne, nb_colonne), cout

def get_pairs(ens:list)->list:
    """copyright  @GabrielPatry"""
    n = len(ens)
    list_pairs = []
    for i in range(n-1):
        for j in range(i+1,n):
            list_pairs.append((ens[i],ens[j]))
    #maintenant on trie
    for i in range(len(list_pairs)):
        for j in range(len(list_pairs)):
            (i1,j1),(k,l) = list_pairs[i]
            (m,n),(o,p)  =list_pairs[j]
            if (k-i1)**2+(l-j1)**2 < (m-o)**2+(p-n)**2 and j<i :
                list_pairs[i],list_pairs[j] = list_pairs[j],list_pairs[i]
    return list_pairs

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
    dico2 = {0:1}
    niveau_max_utilise = 0
    #grille_niveau_0, dico,dico_est_trouve = niveau_0(grille)
    grille, dico, dico_est_trouve, grille_valide, cout, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne = premier_niveau_0
    if not grille_valide :
        print("grille non valide")
        return 1
    liste_cases_vides = get_missing_values(grille, dico_taille)
    if len(liste_cases_vides) == 0 :
        return grille, niveau_max_utilise
    else:
        k2 = 0
        list_pairs = get_pairs(liste_cases_vides)
        while k2 < len(list_pairs) :
            k1 = 0
            while k1 < len(liste_cases_vides):
                i,j = liste_cases_vides[k1]
                niveau_max_utilise = max((niveau_max_utilise, 1))
                d_niveau_1, _ = niveau_1((i,j), grille, dico, dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
                new_grille, new_dico, new_dico_est_trouve, new_grille_valide, new_cout = niveau_0(grille, d_niveau_1, dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
                #si on n'apprend pas des nouvelles choses
                if dico == new_dico :
                    k1 += 1
                else:
                    grille, dico, dico_est_trouve = new_grille, new_dico, new_dico_est_trouve
                    liste_cases_vides = get_missing_values(grille, dico_taille)
                    k1 = 0
            if (grille == -1).any() :
                if dico2 != dico:
                    dico2 = dico
                    liste_cases_vides = get_missing_values(grille, dico_taille)
                    list_pairs = get_pairs(liste_cases_vides)
                    k2 = 0
                else:
                    k2 = k2+1
                (i,j), (k,l) = list_pairs[k2] 
                niveau_max_utilise = 2
                d_niveau_2, _ = niveau_2((i,j), (k,l), grille, dico, dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
                new_grille, new_dico, new_dico_est_trouve, new_grille_valide, _ = niveau_0(grille, d_niveau_2, dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
                #si on n'apprend pas des nouvelles choses
                grille, dico, dico_est_trouve = new_grille, new_dico, new_dico_est_trouve
                liste_cases_vides = get_missing_values(grille, dico_taille)
            else : 
                return grille, niveau_max_utilise
    return grille
    
#def niveau_0(grille_copie, d, dico_taille, Taille, dico_voisins, cages_positions, dico_est_trouve, nb_ligne, nb_colonne):

#print(lancement(grille))
#affichage(lancement(grille))
#print(os.listdir("instances"))
nb_false = 0
nb_true = 0
cpt = 0
file = "exemples_grilles/instances/v10_b100_11.txt" 
#grille = main(file)
#print("--------------niveau 1 sur la grille------------")
#affichage(grille)
#input()

#for file in os.listdir("exemples_grilles/instances") : # "exemples_grilles/instances"
#    
#    grille = transformation("exemples_grilles/instances/" + file)
#    grille, niveau_max = main("exemples_grilles/instances/" + file)
#    
#    if (grille == -1).any() :
#        nb_false += 1
#        print(file)
#        affichage(grille)
#        input()
#    else :
#        nb_true += 1
#        print(file, niveau_max)
#    cpt += 1
#    if cpt % 10 == 0 :
#        print("nombre de grilles testees" + str(cpt))
#        print("nombre de grilles non résolues :" + str(nb_false))
#        print("nombre de grilles résolues :" + str(nb_true))
#        print()

print("nombre de grilles testees" + str(cpt))
print("nombre de grilles non résolues :" + str(nb_false))
print("nombre de grilles résolues :" + str(nb_true))
print()
    
#v10_b33_11.txt non résolue avec le niveau 1

def test_niveaux_et_couts(path):
    grille = np.array(transformation(path))
    premier_niveau_0 = lancement(grille)
    grille, dico, dico_est_trouve, grille_valide, cout, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne = premier_niveau_0
    affichage(grille)
    print(cout)
    d_niveau_1, cout_niv1 = niveau_1((0,0), grille, dico, dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
    affichage(grille)
    print(cout_niv1)
    

def plus_court_chemin(grille,arbre,cout,cle_actuelle):
    """ prend une grille en entrée et calcule le plus court chemin de résolution
    grille : la configuration initiale
    arbre : dico qui contient l'abre du jeu. Les clefs sont de la forme 
    0_1-5-3_1-6-4 si le chemin est un niveau 0 puis un niveau 1 sur la case (5,3)...
    les élements sont des tuples qui contiennent la grille et le cout correspondant
    cout : le cout qui nous a permi d'obtenir la conf initiale
    liste_etapes : liste des étapes faites pour arriver à cette configuration """
    nb_cases_vides = sum(sum(grille[:,:,0] == -1))
    print(cle_actuelle, nb_cases_vides)
    if nb_cases_vides == 0 :
        return grille, arbre, cout, cle_actuelle
    else : 

        
        d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne=données_grille(grille)
        
        #on traite le cas où deux chemins différents donnent le même résultat
        #liste_etapes.append((grille_n0,[0]))
        
        if not ((len(cle_actuelle)>=3 and cle_actuelle[-3 : ]=="_0_") or cle_actuelle == "0_") :
            grille_n0, _, _, _, _, cout_n0 =niveau_0(grille,d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            arbre[cle_actuelle+"0_"] = (grille_n0,cout+cout_n0)

    liste_cases_vides = get_missing_values(grille, dico_taille)
    for case in liste_cases_vides :
        i,j=case
        d_niveau_1, cout_n1 = niveau_1(case, grille, d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
        new_grille, new_dico, new_dico_est_trouve, new_grille_valide, new_cout = niveau_0(grille, d_niveau_1, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
        #liste_etapes.append((new_grille,[1,case]))
        arbre[cle_actuelle+"1-"+str(i)+"-"+str(j)+"_"]=(new_grille,cout+new_cout+cout_n1)

   # list_pairs = get_pairs(liste_cases_vides)
   # for i in range(len(list_pairs)):
    #    (x,y), (z,t) = list_pairs[i] 
     #   d_niveau_2, cout_n2 = niveau_2((x,y), (z,t), grille, d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
      #  new_grille, new_dico, new_dico_est_trouve, new_grille_valide, new_cout = niveau_0(grille, d_niveau_2, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
       # arbre[cle_actuelle+"2-"+str(x)+"-"+str(y)+"-"+str(z)+"-"+str(t)+"_"]=(new_grille,cout+new_cout+cout_n2)

    min_grille, min_cout, min_cle=min(arbre)
    del arbre[min_cle]
    return plus_court_chemin(min_grille,arbre,min_cout,min_cle)
    
        
        
#test_niveaux_et_couts("exemples_grilles/instances/v10_b100_11.txt")

def données_grille(grille):
    grille_copie = deepcopy(grille)
    nb_colonne = len(grille[0])
    nb_ligne = len(grille)
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
    return d, dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne

def min(d):
    i=None
    j=None
    cle=None
    for e in d:
        if i==None or d[e][1]<i:
            i=d[e][1]
            j=d[e][0]
            cle=e
    return j,i,cle
            
def max_info(d):
    i=None
    j=None
    cle=None
    for e in d:
        if i==None or d[e][1]>i:
            i=d[e][1]
            j=d[e][0]
            cle=e
    return j,i,cle,d[cle][-1]



#v10_b100_1.txt 1
#v10_b100_10.txt 2
#v10_b100_11.txt 2
#v10_b100_12.txt 1
#v10_b100_13.txt 1
#v10_b100_14.txt 1


#v10_b11_9.txt 1
#v10_b12_1.txt 1
#v10_b12_10.txt 1
#v10_b12_11.txt 1
#v10_b12_12.txt 1
#v10_b12_13.txt 1
#v10_b12_14.txt 1

def plus_court_chemin_non_récursif(grille):
    cout=0
    historique=""
    current_grille=grille
    current_cout = 0
    arbre = {}
    nb_cases_vides = sum(sum(grille[:,:,0] == -1))
    d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne=données_grille(current_grille)

    current_grille, d, dico_est_trouve_0, _, current_cout =niveau_0(current_grille,d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
    
    hashes = {nb_h(d) : d}

    while nb_cases_vides != 0 :
        
        #on traite le cas où deux chemins différents donnent le même résultat
        #liste_etapes.append((grille_n0,[0]))
        # if not ((len(historique)>=3 and historique[-3 : ]=="_0_") or historique == "0_") :
        #     grille_n0, d_n0, dico_est_trouve_n0, _, cout_n0 =niveau_0(current_grille,d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
        #     arbre[historique+"0_"] = (grille_n0, current_cout + cout_n0, (d_n0, dico_est_trouve_n0, dico_taille, Taille, dico_voisins, cages_positions))

        liste_cases_vides = get_missing_values(current_grille, dico_taille)
        did_niveau_1 = False
        for case in liste_cases_vides :
            i,j=case
            information_avant = (~np.array(sum(d.values(), []))).sum()

            d_niveau_1, cout_n1 = niveau_1(case, current_grille, d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            new_grille, new_dico, new_dico_est_trouve, new_grille_valide, new_cout = niveau_0(current_grille, d_niveau_1, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            #liste_etapes.append((new_grille,[1,case]))
            information_apres = (~np.array(sum(new_dico.values(), []))).sum()

            hash = nb_h(new_dico)

            if information_apres > information_avant and hash not in hashes.keys():
                did_niveau_1 = True
                hashes[hash] = new_dico
                arbre[historique +"1-"+str(i)+"-"+str(j)+"_"]=(new_grille,current_cout+new_cout+cout_n1, (new_dico, new_dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions))

        if not did_niveau_1:
            pairs = get_pairs(liste_cases_vides)
            pairs.sort(key=lambda p: dico_taille[p[0]] + dico_taille[p[1]] )
            for case1, case2 in pairs:
                information_avant = (~np.array(sum(d.values(), []))).sum()

                d_niveau_2, cout_n2 = niveau_2(case1, case2, current_grille, d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
                new_grille, new_dico, new_dico_est_trouve, new_grille_valide, new_cout = niveau_0(current_grille, d_niveau_2, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
                #liste_etapes.append((new_grille,[1,case]))
                information_apres = (~np.array(sum(new_dico.values(), []))).sum()

                # print(case1, case2, information_avant, information_apres)

                hash = nb_h(new_dico)

                if information_apres > information_avant and hash not in hashes.keys():
                    hashes[hash] = new_dico
                    i1,j1=case1
                    i2,j2=case2
                    new_cout = current_cout+new_cout+cout_n2 + (10000 if information_apres - information_avant <= 5 else 0)
                    arbre = {}
                    hashes = {}
                    arbre[historique +"2-"+str(i1)+"-"+str(j1)+"-"+str(i2)+"-"+str(j2)+"_"]=(new_grille,new_cout, (new_dico, new_dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions))
        
        min_grille, min_cout, min_cle=min(arbre)
        d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions = arbre[min_cle][2]
        current_cout = min_cout
        current_grille = min_grille
        historique = min_cle
        del arbre[min_cle]
        nb_cases_vides = sum(sum(min_grille[:,:,0] == -1))
        print(min_cle, nb_cases_vides, min_cout, len(arbre), (~np.array(sum(d.values(), []))).sum())
    affichage(min_grille)
    return arbre

   # list_pairs = get_pairs(liste_cases_vides)
   # for i in range(len(list_pairs)):
    #    (x,y), (z,t) = list_pairs[i] 
     #   d_niveau_2, cout_n2 = niveau_2((x,y), (z,t), grille, d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
      #  new_grille, new_dico, new_dico_est_trouve, new_grille_valide, new_cout = niveau_0(grille, d_niveau_2, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
       # arbre[cle_actuelle+"2-"+str(x)+"-"+str(y)+"-"+str(z)+"-"+str(t)+"_"]=(new_grille,cout+new_cout+cout_n2)


def plus_court_chemin_non_récursif_maximisation_informations(grille):
    """reprend le même algo que dessus mais cette fois, on veut maximiser la quantité d'informations"""
    cout=0
    historique=""
    current_grille=grille
    current_cout = 0
    arbre = {}
    nb_cases_vides = sum(sum(grille[:,:,0] == -1))
    d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne=données_grille(current_grille)
    information = (~np.array(sum(d.values(), []))).sum() #faut pas poser trop de questions mais ça marche : 
                                                         #ça permet de compter le nombre total de False dans d (ie le nombre d'info qu'on a sur la grille)
    while nb_cases_vides != 0 :
        
        #on traite le cas où deux chemins différents donnent le même résultat
        #liste_etapes.append((grille_n0,[0]))
        if not ((len(historique)>=3 and historique[-3 : ]=="_0_") or historique == "0_") :
            grille_n0, d_n0, dico_est_trouve_n0, _, cout_n0 =niveau_0(current_grille,d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            new_information = (~np.array(sum(d_n0.values(), []))).sum()
            arbre[historique+"0_"] = (grille_n0, new_information - information, (d_n0, dico_est_trouve_n0, dico_taille, Taille, dico_voisins, cages_positions), current_cout + cout_n0)

        liste_cases_vides = get_missing_values(current_grille, dico_taille)
        for case in liste_cases_vides :
            i,j=case
            d_niveau_1, cout_n1 = niveau_1(case, current_grille, d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            new_grille, new_dico, new_dico_est_trouve, new_grille_valide, new_cout = niveau_0(current_grille, d_niveau_1, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            #liste_etapes.append((new_grille,[1,case]))
            new_information = (~np.array(sum(new_dico.values(), []))).sum()
            arbre[historique +"1-"+str(i)+"-"+str(j)+"_"]=(new_grille,new_information - information, (new_dico, new_dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions), current_cout+new_cout+cout_n1)
        min_grille, max_information, min_cle, gros_cout =max_info(arbre)
        d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions = arbre[min_cle][2]
        information = (~np.array(sum(d.values(), []))).sum()
        current_grille = min_grille
        historique = min_cle
        current_cout = gros_cout
        del arbre[min_cle]
        affichage(min_grille)
        nb_cases_vides = sum(sum(min_grille[:,:,0] == -1))
        print(min_cle, nb_cases_vides)
        print(information,gros_cout)
        print(len(arbre))
    return arbre


def affichage_etapes(liste_etape_str, grille):
    liste_etape = liste_etape_str.split("_")
    dico, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne=données_grille(grille)

    liste_cases_vides = get_missing_values(grille, cages_valeurs, dico_taille)
    nb_cases_vides = sum(sum(grille[:,:,0] == -1))
    affichage(grille)
    print(nb_cases_vides)
    input()
    for etape in liste_etape:
        if etape[0] == "0":
            new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs, new_grille_valide, new_cout = niveau_0(grille, dico, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            grille, dico, dico_est_trouve, cages_valeurs = new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs
            nb_cases_vides = sum(sum(grille[:,:,0] == -1))
            affichage(grille)
            print(nb_cases_vides)
            input()
        else:
            i, j = int(etape[2]), int(etape[4])
            d_niveau_1, _ = niveau_1((i,j), grille, dico, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs, new_grille_valide, new_cout = niveau_0(grille, d_niveau_1, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
            grille, dico, dico_est_trouve, cages_valeurs = new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs
            nb_cases_vides = sum(sum(grille[:,:,0] == -1))
            affichage(grille)
            print(nb_cases_vides)
            input()
    print("toutes les étapes sont faites")
    input()

    
# --------------------------------------------------------------------------------------
# Démonstration du solveur de grilles  


# d'abord, on choisit l'emplacemet de la grille
path = "exemples_grilles/instances/v10_b100_14.txt"
path = "instances/v10_b100_14.txt"
# path = "test.txt"

# ensuite on transforme le fichier txt en une grille sympa
grille = np.array(transformation(path))
#print("la grille en question")
#affichage(grille)

#affichage_etapes("0", grille)
# ensuite on a le choix entre deux algo : la minimisation du cout ou la maximisation de la quantité 
# d'informations (le deuxième est souvent bien plus rapide) 

# mettre une des deux lignes en commentaire

#plus_court_chemin_non_récursif(grille)
t = time.time()
plus_court_chemin_non_récursif(grille)
# plus_court_chemin_non_récursif_maximisation_informations(grille)
print(time.time() - t)

print(temps_des_dicos)
a = 0
for d in temps_des_dicos :
    a += temps_des_dicos[d]

print(a)
print("finito")
input()

# ------------------------------------------------------------------------------------------


# niveau 0 amélioré
# faut vraiment faire un truc pour la génération d'indices
# pouvoir "faire" des niveaux 2

#  -4-5_1-1-1_0_1-0-5_ 30 /// 1-0-3_1-3-2_ 0 132 12883
#565
#  9181
#  1-4-5_1-0-5_1-1-1_0_ 30
#  9181
#  1-4-5_1-1-1_1-0-5_0_ 30
#  9181
#  1-4-5_0_1-1-4_0_1-0-5_ 28
#  9182
#  0_1-1-5_0_1-0-3_0_ 30
#  9182
#  0_1-0-3_0_1-1-5_0_ 30
#  9182
#  0_1-4-4_1-4-4_1-0-3_ 30
#  9183
#  1-4-5_0_1-1-5_1-2-0_ 30
#  9183
#  1-4-5_1-1-5_0_1-2-0_ 30
#  9183
#  1-4-5_0_1-2-0_1-1-5


#grille = np.array(transformation(path))
#premier_niveau_0 = données_grille(grille)
#
#dico, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne=données_grille(grille)
#
#liste_cases_vides = get_missing_values(grille, dico_taille)
#nb_cases_vides = sum(sum(grille[:,:,0] == -1))
#affichage(grille)
#print(nb_cases_vides)
#
#d_niveau_1, _ = niveau_1((4,5), grille, dico, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
#new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs, new_grille_valide, new_cout = niveau_0(grille, d_niveau_1, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
#grille, dico, dico_est_trouve, cages_valeurs = new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs
#nb_cases_vides = sum(sum(grille[:,:,0] == -1))
#affichage(grille)
#print(nb_cases_vides)
##  1-4-5_0_1-1-4_0_1-0-5_ 28
#
#new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs, new_grille_valide, new_cout = niveau_0(grille, dico, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
#grille, dico, dico_est_trouve, cages_valeurs = new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs
#nb_cases_vides = sum(sum(grille[:,:,0] == -1))
#affichage(grille)
#print(nb_cases_vides)
#
#
#d_niveau_1, _ = niveau_1((1,4), grille, dico, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
#new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs, new_grille_valide, new_cout = niveau_0(grille, d_niveau_1, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
#grille, dico, dico_est_trouve, cages_valeurs = new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs
#nb_cases_vides = sum(sum(grille[:,:,0] == -1))
#affichage(grille)
#print(nb_cases_vides)
#
#new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs, new_grille_valide, new_cout = niveau_0(grille, dico, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
#grille, dico, dico_est_trouve, cages_valeurs = new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs
#nb_cases_vides = sum(sum(grille[:,:,0] == -1))
#affichage(grille)
#print(nb_cases_vides)
#
#d_niveau_1, _ = niveau_1((0,5), grille, dico, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
#new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs, new_grille_valide, new_cout = niveau_0(grille, d_niveau_1, dico_est_trouve, cages_valeurs, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
#grille, dico, dico_est_trouve, cages_valeurs = new_grille, new_dico, new_dico_est_trouve, new_cages_valeurs
#nb_cases_vides = sum(sum(grille[:,:,0] == -1))
#affichage(grille)
#print(nb_cases_vides)



#idée d'amélioration : 
# optimiser les niveaux 0 et 1
# on peut s'interesser à la "quantité d'information" dans une grille :
# ce serait le nombre de "false" dans le dictionnaire d

#autre idée, si on trouve un chemin qui élimine une case en n niveaux 1, on ne regarde pas 
#les chemins qui font plus de n niveaux 1 et qui ne donnent pas plus d'info 

#nouvelle autre idée : on maximise la quantité d'info supplémentaire à chaque étape

#nouvelle nouvelle autre idée : on dégage les chmins qui conduisent à des grilles et des d identiques en ne gardant que le moins cher

#avec le premier algo, au bout de plus ou moins 2h
#l'arbre a 450 000 branches et on n'a pas appris grand chose mdr