
# ------------------------------------ IMPORTATIONS ----------------------------------------------------
from othellier import Othellier
import numpy as np 
import copy

# -------------------------------------- MIN MAX ------------------------------------------------

'''
Pour implémenter l'algorithme minMax, nous avons procédé de la manière suivante : 

'''
def genere_successeurs(echiquier): # on fournit en input un objet de classe Othellier
    '''
    Cette fonction génère pour un othellier donné, tous ses successeurs possibles 
    '''
    successeurs = {} # les successeurs de l'objet donné en input seront sonsignés dans cette liste. 
    pdg = echiquier.fonction_evaluation() # on crée le dictionnaire "promesses de gain" pour l'othellier d'interet 
    for i, case_possible in enumerate(pdg.keys()): 
        # pour chacune des cases possibles, on simule un tour
        cases = copy.deepcopy(echiquier.cases)
        if len(pdg[case_possible]) != 0: 
            # on crée un othellier à partir de celui d'interet 
            i = Othellier(cases, echiquier.joueur, echiquier.adversaire)
            # on le met a jour comme si on avait joué case_possible
            i.mise_a_jour(case_possible, echiquier.a_des_binomes(case_possible)[2])
            i.joueur[0], i.adversaire[0] = i.adversaire[0], i.joueur[0]
            # on l'ajoute à "successeurs" avec sa promesse de gain associée 
            successeurs[i] = i.fonction_evaluation() # NB : il y a alors un dictionnaire dans un dictionnaire 
            
    print(successeurs)
    '''
    print(successeurs[0].cases)
    print()
    print(successeurs[1].cases)
    print()
    print(successeurs[2].cases)
    print()
    print(successeurs[3].cases)
    print(successeurs)
    print(len(successeurs)) 
    '''
    return successeurs


# il faut déjà se poser la question : 
# qu'est ce qu'on veut remonter : un plateau ? un nombre de jetons gagnants ? une case ? 
# une combinaison de ces trois possibilité ? 
# --> juste un nombre 
# En revanche, pour avoir ce nombre, on doit évaluer des plateaux dans tous les cas ... 

def MinMax(othellier, prof, min_ou_max):
    '''
    othellier = l'othellier pour lequel  on veut faire l'évaluation
    prof = la profondeur jusqu'à laquelle on veut réaliser l'algo
    min_ou_max = 1 ou 2, pour savoir si le noeud est un noeud min ou un noeud max 
    '''

    # pour l'instant, ce MinMax ne fonctionne que si l'othellier de départ est un othellier 
    # où c'est au joueur 1 (= pion noirs) de jouer 
    
    pdg = copy.deepcopy(othellier.fonction_evaluation())
    cases_possibles = othellier.fonction_evaluation().keys() # on va envisager toutes les possibilités de jeu (= facteur de branchement)
    cases = copy.deepcopy(othellier.cases) 
    # on "recopie" le plateau de l'othellier de départ, sinon les modifications se font sur cet othellier de départ ! 

    max_score = -1000 # initialisation --> le max score sera forcément meilleur que ça 
    min_score = 1000 # initialisation 

    # si on est au niveau d'une feuille, on return la valeur de la fonction d'évaluation
    # NB : (np.where(othellier.cases == 0, 10, 0).sum() == 0) signifie qu'il n'y a a plus de cases libres 
    if prof == 0 or np.where(othellier.cases == 0, 10, 0).sum() == 0: 
        return np.where(othellier.cases == 1, True, False).sum() - np.where(othellier.cases == 2, True, False).sum()
        '''
        pdg = othellier.fonction_evaluation()
        v1 = []
        v2 = []
        for item in pdg.items():
            # "si je joue telle case, mon plateau aura tant de pion de telle couleur" 
            # --> notre fonction d'évaluation"
            v1.append(item[0])
            v2.append(np.where(othellier.cases == 1, True, False).sum() - np.where(othellier.cases == 2, True, False).sum())
        print("v1", v1)
        print("v2", v2)

        if min_ou_max == 1:
            max_score = max(v2)
            case_choisie = v1[np.argmax(v2)]
            #print('la case choisie est ', case_choisie , ' car elle me permet d avoir ', max_score)
            #print(' pion noirs sur mon plateau à la profondeur', prof)
            print("case_choisie = " , case_choisie,  "max_score = ", max_score)
            #print(case_choisie, max_score)
            return max_score

        else:
            min_score = min(v2)
            case_choisie = v1[np.argmin(v2)]
            print("case_choisie = " ,case_choisie, " min_score = ", min_score)
            return min_score
       
        '''

    # Dans le cas où le noeud n'est pas terminal, on réapplique la fonction MinMax sur ses successeurs possibles 
    if othellier.joueur[0] == 1:
        for case in cases_possibles:
            # on crée le nouvel othellier qui découlerait de ce choix de case 
            #oth_fils = Othellier(cases, othellier.joueur[1], othellier.adversaire[1])
            oth_fils = copy.deepcopy(othellier)
            oth_fils.mise_a_jour(case, othellier.a_des_binomes(case)[2])
            oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur
            # on enregistre la valeur que cet othellier nous rapporterait 
            score = MinMax(oth_fils, prof - 1, min_ou_max)
            #max_case = pass # la case associée au score max 
            
            max_score = max(max_score, int(score))
 
        return max_score 
    
    else:

        for case in cases_possibles:
            # on crée le nouvel othellier qui découlerait de ce choix de case 
            #oth_fils = Othellier(cases, othellier.joueur[1], othellier.adversaire[1])
            oth_fils = copy.deepcopy(othellier) 
            # Quand on crée un othellier, le joueur[0] vaut toujours, 1, or nous, ici, joueur[0] doit valoir 2
            # --> on écrit donc la ligne suivante : 
            #oth_fils.joueur[0], oth_fils.adversaire[0] = oth_fils.adversaire[0], oth_fils.joueur[0]
            oth_fils.mise_a_jour(case, othellier.a_des_binomes(case)[2])
            # Une fois la mise à jour faite, il faut de nouveau changer à qui est le tour 
            # --> on réecrit la ligne suivante :) 
            oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur         
            # on enregistre la valeur que cet othellier nous rapporterait si la case était jouée  
            score = MinMax(oth_fils, prof - 1, min_ou_max)
            min_score = min(min_score, int(score))

        return min_score 

