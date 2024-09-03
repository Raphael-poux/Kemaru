# Règle du jeu :
Remplir une grille en respectant deux restrictions :
1. Deux chiffres identiques ne peuvent être voisins (même en diagonale)
2. Une cage de taille N doit contenir tous les chiffres de 1 à N

*NB : cf l'exemple donné dans la présentation pour voir à quoi ressemble concrètement une grille*
# Description du projet :
 - Réalisation d'un algorithme de résolution du jeu Kemaru par recherche du plus court chemin de résolution
 - Réalisation d'une interface graphique pour l'utilisateur
 - Utilisation des deux algorithmes pour pouvoir donner des indices pertinents à un joueur bloqué dans la résolution d'une grille

# Répartition du travail
## Membres du groupe
- Raphaël Oculi
- Raphaël Poux
- Gabriel Patry
- Mathis Verdan

## Organisation du travail
 1. Début de la partie algorithmique (niveau 0) avec tout le groupe sur Liveshare
 2. Raphaël P. et Gabriel &rarr; travail sur l'interface graphique / Raphaël O. et Mathis &rarr; travail sur la partie algorithmique
 3. Mise en commun des travaux avec github

# Partie algorithmique 
Ce paragraphe a pour but de détailler l'algorithme de résolution du jeu, notamment en donnant des détails sur le fichier `solver.py`. 

## Différents raisonnements

Pour résoudre une grille de Kemaru de façon algorithmique, on emploie différents raisonnements appelés **niveau 0, 1 et 2**.

### Niveau 0
Ce raisonnement consiste à appliquer simplement les règles du jeu : il faut pour cela **propager les informations** des cases déjà remplies vers les cases vides pour en faire des déductions. 

> *Exemple :* Si dans une cage de taille 3, une case possède un 1 et un 2 comme voisins, on en déduit que la case contient forcément un 3.

### Niveau 1
Il se peut qu'à l'issue du niveau 0 certaines cases de la grille restent vides. Il faut utiliser un raisonnement plus complexe pour trouver leur valeur. Le niveau 1 consiste à **supposer la valeur d'une des cases** parmi les valeurs possibles que celle-ci peut prendre et à en tirer des conclusions en appliquant ensuite un niveau 0. 

Si la case de coordonnées *(i,j)* peut prendre N valeurs différentes, le niveau 1 va tester toutes ces valeurs successivement et voir si cela apporte des nouvelles informations.

> *Exemple 1 :* Si, pour une certaine case notée A, on hésite entre les valeurs 1 et 4, alors le niveau 1 va créer deux *univers parallèles*. L'un dans lequel la case contient un 2, et l'autre dans lequel elle contient un 4. Comme la grille n'a qu'une solution, il y a forcément un des deux *univers* qui est faux (mais on ne le sait pas encore). On propage ensuite les informations "la case est un 2" et "la case est un 4" dans les deux univers. Si l'on s'aperçoit que l'univers "la case est un deux" donne une grille impossible (avec par exemple une case B dans laquelle on ne peut mettre aucune valeur), alors on sait que la case A comporte finalement un 4. 

> *Exemple 2 :* Même situation, on hésite entre mettre un 2 ou un 4 dans une des cases, toujours notée A. Cette fois, la propagation des informations dans les deux *univers parallèles* ne donne pas de contradictions (il reste des cases vides dans les deux univers et on ne sait pas encore lequel est faux, car on n'a pas assez d'informations pour détecter une contradiction). Toutefois, imaginons que dans une autre case de la grille notée B (vide avant l'application du niveau 1, et qui peut prendre les valeurs 1,2, 3 et 4 par exemple) la propagation des informations donne le résultat suivant : 
> - dans l'univers "la case A est un 2", on arrive à remplir la case B par un 1
> - dans l'univers "la case A est un 4", on arrive à remplir la case B par un 3
>
> Alors en regardant les deux univers parallèles, on constate que la case B ne prend jamais les valeurs 2 et 4, ce qui signifie que les valeurs possibles pour cette case passent de 1,2,3,4 à 1,3. 
>
> On a ici réduit les possibilités pour une case en faisant **l'union** des valeurs possibles trouvées dans les univers parallèles. Ce genre de déduction permet potentiellement de tirer de nouvelles conclusions en appliquant un niveau 0 ou un autre niveau 1 après l'union. 

Ces deux exemples simples illustrent la puissance du niveau 1, qui consiste finalement à **faire des suppositions** et à **combiner les informations en faisant l'union des valeurs possibles des "univers parallèles**.

**NB :** Quand on dit que l'on "propage des informations", cela signifie qu'on fait un niveau 0 (on applique les règles du jeu à la grille). Donc en réalité, le niveau 1 inclut automatiquement un niveau 0.

### Niveau 2
Lorsque le niveau 1 ne parvient pas à résoudre la grille, on passe au niveau 2. Ici, au lieu de regarder toutes les possibilités pour une des cases, on regarde toutes les possibilités pour un **couple de cases** (ce qui fait vite beaucoup de possibilités). De la même manière, on propage les informations avec un niveau 0 après chaque hypothèse.

### Niveau 3, 4, ..., N ? 
On pourrait continuer ainsi en supposant 3, 4 ... N cases si le niveau 2 ne suffit pas. En réalité, en testant de nombreuses grilles (un échantillon de 23 580 grilles de différents niveaux), on s'est aperçu que le niveau 2 permettait de toutes les résoudre (cf le tableau de la diapo 18 de la soutenance). Il n'est donc pas nécessaire d'aller au-delà du niveau 2 qui est déjà assez lourd à calculer. 

*NB : certaines des grilles testées étaient loin d'être faciles (elles étaient même très difficiles), ce qui nous permet de penser que le niveau 2 suffit pour toutes les grilles qui existent*

## Plus court chemin 
La recherche du plus court chemin de résolution est utile pour donner des indices pertinents à l'utilisateur. On peut en effet se dire qu'au lieu de dévoiler une case au hasard en guise d'indice, il est plus efficace de diriger l'utilisateur vers une étape de raisonnement clef (par exemple en montrant sur quelle case réfléchir). On peut obtenir cela en partant du principe que les étapes du plus court chemin de résolution sont aussi les plus faciles à faire pour un humain. 

### Dijkstra, ou presque ...
Pour trouver le plus court chemin, on calcule le "coût" (détails ci-dessous) de chaque étape (niveau 0, niveau 1 sur telle case ...) pour construire le graphe du jeu. Pour la première étape, l'algorithme prend la grille initiale et essaie tous les coups possibles (niveau 0, niveau 1 sur la case (0,0), niveau 1 sur la case (1,0) ... ), en gardant en mémoire le résulat de chaque coup. Une fois tous les coups possibles appliquées, l'algorithme sélectionne le coup dont le coût est le plus faible, puis il refait pareil à partir de la grille initiale à laquelle on a appliqué le coup. 

> *Exemple :* Supposons que le coup de plus faible coût soit un niveau 1 sur la case (1,1), que ce coup coûte 100, et que la grille résultant de ce coup s'appelle A. Alors le programme applique ensuite à A tous les coups possibles, en gardant en mémoire les résultats de ces coups ainsi que le coût résultant. Dans ce cas, si on applique à A un niveau 1 de coût 50, le coût résultant sera 100+50 (supposons aussi que ce soit le coup  de plus faible coût). 
>
> A la prochaine itération, si la grille n'est pas résolue, il faudra repartir de la grille dont le coup est le plus faible. Peut-être que celle-ci sera A + le niveau 1 de coût 50, mais peut-être que cette grille sera celle résultant d'un autre coup que A (disons un coup B de coût 120). 

Cet algorithme nous assure de trouver le chemin de résolution minimisant le coût.

### Le coût
Dans notre algorithme, le coût est défini assez simplement : dès que l'on se sert d'une case pour éliminer une valeur possible dans les cases voisines, on augmente le coût de 1 (cela revient à compter les comparaisons que l'on fait). 

Pour le niveau 1, on choisit de rajouter un coût supplémentaire (car un niveau 1 est plus difficile à faire de tête) pénalisant les cases où il y a beaucoup de valeurs possibles. Il est en effet plus logique pour un humain de regarder une case où il hésite entre deux valeurs plutôt qu'une case où il hésite entre 5 valeurs. 

De même, pour des raisons de rapidité, nous avons choisi de faire un niveau 2 seulement si les niveaux 0 et 1 ne sont pas suffisants. Il est en effet très long de calculer tous les niveaux 2 possibles, et il est très difficile pour un humain de réfléchir à un niveau 2. Donc autant rediriger les joueurs vers les niveaux 2 le moins souvent possible.

## Implémentation
### Encodage d'une grille dans un fichier .txt
Les grilles du jeu sont stockées dans des fichiers au format `.txt`. Ces grilles, données par l'encadrant, sont disponibles dans le fichier `instances.zip`. Il y en a 23 580 (de quoi s'amuser longtemps) et les difficultés sont très variables. 

Les fichiers sont construits de la façon suivante : 
- Il y a autant de lignes que de cases dans la grille 
- Chaque ligne contient 3 ou 4 chiffres
- Les deux premiers sont les coordonnées de la case
- Le troisième désigne le numéro de la cage à laquelle appartient la case 
- Et l'éventuel dernier désigne la valeur de la case si celle-ci est non vide
### Les dictionnaires/array utiles
Pour repésenter le jeu, nous utilisons plusieurs dictionnaires et array numpy car certaines représentations sont plus utiles que d'autres selon les situations.

**La grille** : c'est un array tel que `grille[i][j] = [valeur, n° de la cage]`, et où i, j sont les coordonnées spatiales de la case.

**Le dictionnaire d/dico** : dans le solveur, tous les dictionnaires qui s'appellent d ou dico <small>(il faut reconnaître que le nom n'est pas terrible)</small> désignent un objet d'une forme bien particulière : 
```python
d[i][j] = [True, True, False, False, True] #exemple 1 
d[i][j] = [True, False, False] #exemple 2
```
Dans l'exemple 1, la case (i,j) est dans une cage de taille 5 et il est possible de mettre un 1, un 2 ou un 5. 

Dans l'exemple 2, la case (i,j) est dans une cage de taille 3 et il est possible d'y mettre un 1 uniquement (donc la case contient un 1).

**TODO : la suite !!**

**Dico_est_trouve**

**Dico_taille**

**Taille**

**Dico_voisins**

### Niveau 0
C'est le niveau le plus imortant puisque celui-ci va être utilisé très souvent. Dans l'implémentation, on utilise un `set`nommé `To_treat` qui fait office de pile contenant l'ensemble des cases à analyser. On l'initialise en mettant toutes les cases de la grille :
```python
To_treat = set([(i, j) for i in range(nb_ligne) for j in range(nb_colonne)]) 
```
On va ensuite dépiler `To_treat`pour mettre à jour le dictionnaire `d`. Pour cela, on propage la valeur de la case aux voisins (si la case est non vide) : 
```python
value, cage = grille_copie[i][j]
for v in dico_voisins[(i, j)] :
    if value <= dico_taille[v] :
        # augmentation du coût en cas de modification de d
        if d[v][value-1]:
            cout+=1
        # mise à jour de d : il ne peut pas y avoir deux chiffres identiques à côté ! Le "-1" vient juste d'un décalage des indices.
        d[v][value - 1] = False
        # on ajoute les voisins et les cages dans la pile
        if grille_copie[v[0]][v[1]][0] == -1:
            To_treat.add(v)
            To_treat.add((grille_copie[v[0]][v[1]][1],))
```
Il faut aussi mettre à jour les cases dans la même cage que la case dépilée :
```python
# Il ne peut pas y avoir deux fois la même valeur dans une même cage (cage_positions contient les coordonnées des cases d'une même cage)
for v in cages_positions[grille_copie[i][j][1]]:
    if v != element :
        if d[v][value-1]:
            cout+=1
        d[v][value - 1] = False
        if grille_copie[v[0]][v[1]][0] == -1:
            To_treat.add(v)
```
On constate que la pile contient deux types d'éléments : des couples (i,j) pour désigner les cases et des tuples à un élément (n° de cage) pour désigner des cages. Mettre des cages dans la pile sert à raisonner sur l'ensemble des cages, car il peut arriver qu'on devine où se trouve une valeur si jamais on ne peut la mettre qu'à un seul endroit dans la cage :
```python
# une des valeurs ne peut aller qu'à un endroit de la cage, donc elle y va forcément !
if len(cases_possibles) == 1 :
    seule_case_possible = cases_possibles[0]
    d[seule_case_possible ] = [False]*len(d[seule_case_possible])
    d[seule_case_possible ][i - 1] = True
    if grille_copie[seule_case_possible[0]][seule_case_possible[1]][0] == -1:
        dico_est_trouve[seule_case_possible] = True
        To_treat.add(seule_case_possible)
``` 
### Niveaux 1 et 2
Les niveaux 1 et 2 ne sont en fait pas bien compliqués : on applique simplement un niveau 0 à une copie de la grille, à laquelle on remplit une des cases par une valeur possible. 
```python
# on suppose que la grille contient la valeur e à la coordonnée (i, j). Il y a encore un +1 pour des raisons d'indiçage.
grille_copie[i][j][0]=e+1
```
### Le plus court chemin
Les étapes clefs de la recherche du plus court chemin sont : l'essai de tous les niveaux 1 possibles (on parlera des niveaux 2 par la suite) sur la grille, et la mise à jour de l'arbre des possibilités après chaque essai. On fait cela dans les lignes suivantes (le code est volontairement simplifié par rapport au code du solveur par soucis de clarté) :
```python 
for case in liste_cases_vides :
    i,j=case
    # niveau 1 sur une case vide
    d_niveau_1, cout_n1 = niveau_1(case, current_grille, d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
    # on fait automatiquement un niveau 0 pour propager les informations du niveau 1
    new_grille, new_dico, new_dico_est_trouve, new_grille_valide, new_cout = niveau_0(current_grille, d_niveau_1, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions, nb_ligne, nb_colonne)
    # mise à jour de l'arbre des possibilités
    arbre[historique +"1-"+str(i)+"-"+str(j)+"_"]=(new_grille,current_cout+new_cout+cout_n1, (new_dico, new_dico_est_trouve, dico_taille, Taille, dico_voisins, cages_positions))
```
En ce qui concerne l'arbre des possibilités, il s'agit d'un dictionnaire dont les clefs sont de la forme suivante : 
`0_1-5-2_2-2-3-1-4` si l'on a appliqué un niveau 0, puis un niveau 1 sur la case (5,2), puis un niveau 2 sur les cases (2,3) et (1,4) par exemple. 

On récupère ensuite le chemin le moins cher dans l'arbre et on actualise la grille avant de recommencer (on continue le programme tant qu'on n'a pas résolu la grille) :
```python
# on prend les infos du chemin le moins cher
min_grille, min_cout, min_cle = min(arbre) 
d, dico_est_trouve_0, dico_taille, Taille, dico_voisins, cages_positions = arbre[min_cle][2]
# on met à jour le coût et la grille
current_cout = min_cout
current_grille = min_grille
historique = min_cle
# on supprime enfin la branche de coût minimal pour ne pas tomber dans une boucle infinie
del arbre[min_cle]
```
## Quelques difficultés
Au départ, notre algorithme de plus court chemin était légèrement différent de celui dans le solveur, et il présentait un inconvénient majeur : le temps d'exécution. En effet, pour les grilles les plus compliquées, même après plusieurs heures, le plus court chemin n'était toujours pas trouvé. Cela s'explique notamment par le fait que minimiser le coût va à l'encontre de progresser rapidement dans la grille. En effet, les coups de plus faible coût sont ceux qui font peu de comparaison et donc peu de déductions.
>*Exemple :* si on applique un niveau 1 sur une case perdue au milieu de cases vides, on n'apprendra probablement pas grand chose, voire rien (on ne va pas éliminer beaucoup de valeurs) ... donc le coût sera proche de 0. Or, l'algorithme favorise ce genre de coups.

Cela fait que l'algorithme va essayer tous les coups que l'on pourrait qualifier de "pas chers mais inutiles", en faisant augmenter la taille de l'arbre des possibilités sans progresser dans la résolution. 

Une des premières solutions que nous avons mise en place est la modification de la variable optimisée par l'algorithme, en ne choisissant pas le chemin le moins coûteux, mais celui qui **maximise la quantité d'informations apprises**. On obtient la **quantité d'informations** que l'on a sur une grille en comptant le nombre de `False` dans le dictionnaire d (ie : on compte le nombre de possibilités éliminées). Cela se fait avec la syntaxe suivante (pas hyper claire mais a le mérite de faire ça en une ligne) : 
```python
information = (~np.array(sum(d.values(), []))).sum()
```
En employant un algorithme très similaire à Dijkstra, mais qui maximise la quantité de nouvelles informations à chaque étape, on arrive à trouver un chemin de résolution efficace pour n'importe quelle grille (en un temps raisonnable).

Nous verrons dans la prochaine partie que nous avons finalement réussi à améliorer le premier algorithme pour le rendre bien plus rapide. Cela nous permet de trouver le plus court chemin (au sens du coût) en un temps raisonnable, ce qui est l'un des objectifs du projet.
## Améliorations du plus court chemin
### TODO : parler du hash et des autres améliorations faites avec N. Stott

# Partie interface
Ce paragraphe a pour but de détailler la façon dont la grille et les différentes profondeurs de résolution seront représentés, sans considérations sur l'implémentation de cette interface, qui a été codé avec pygame. Nous avons choisi pygame essentiellement car au début du projet nous n'avions pas encore commencé les cours de HTML/Css/javascript.

## Interface joueur
Deux modes de jeu distincts ont étés implémentés. Le premier permet a joueur de résoudre la grille par lui-même. Il peut pour s'aider afficher les possibilités dans chaque case et les éliminer manuellement.

## Représentation des différents niveaux
Le second mode de jeu permet de voir le chemin de résolution d'une grille par l'algorithme précedemment décrit. Seuls des représentations pour les niveaux 0 et 1 ont étés implémentés, par soucis de lisibilité. Cela suffit pour résoudre la plupart des grilles de Kemaru disponibles. 

### Représentation du niveau 0
Pour représenter le niveau 0, la case qui gagne de l'information en perdant une possibililité est affichée en bleu tandis que la ou les cases utilisés pour déterminer cette information sont affichées en rouge. Le joueur fait avancer la résolution en presssant la touche S.

### Représentation du niveau 1
Pour représenter le niveau 1, on scinde la grille en autant de possibilités que comporte la case de laquelle part la résolution ( celle sur laquelle différentes hypothèses sont faites ). Une résolution de niveau 0 s'engage alors sur chaqu'une de ces grilles. Pour faciliter l'affichage de plusieurs grilles, toutes celles-ci sont déformés pour être carrés.

### (non implémenté) Représentation des niveau supérieurs
Pour n'importe quel autre niveau, le seul paramètre qui change par rapport au niveau 1 est le nombre potentiel de possibilités. On pourrait alors représenter n'importe quel niveau de résolution en scindant la grille en autant de possibilité que d'hypothèse que l'algorithme de résolution fait sur une (on a alors une résolution de niveau 1) ou plusieurs cases.


