from othellier import Othellier
import numpy as np 
import copy
from math import log , sqrt
import random as rd 


'''
I - Selection : 
Choisir un enfant tout en respectant un équilibre exploration/exploitation 
Le successeur i choisi est le successeur dont la valeur suivante est maximale :
 
(w/n) + c * sqrt( ln(N) /n )

w = nombre de win 
n = nombre de fois où i a été visité 
N = nombre de fois où le noeud pere de i a été visité 
C = le paramètre d'exploration ( souvent égal à sqrt(2) )

w/n représente l'exploitation 
 c * sqrt( ln(N) /n ) représente l'exploration 

II - Expansion

III - Simulation

IV - Backpropagation 

V - Fin des itérations 
MCTS indiquera son successeur qui présente le meilleur w/n 

'''
# programmation objet des noeuds ? --> peut etre pas mal hein ... 

class noeud:
    def __init__(self, othellier, case, n, w, parent):
        self.othellier = othellier 
        self.n = n 
        self.w = w 
        self.parent = parent # un objet appartenant à la classe noeud 
        self.case = case
        self.successeurs = []
        # N = pere.n 
    
    def is_terminal(self):
        pass

    def UCB(self, C):
        try: 
            return self.w/self.n + C * sqrt( log(self.parent.n) /self.n )
        except:
            # Si n = 0, UCB vaut + l'infini 
            return + 10000 
    
    def play_out(self):
        while (self.othellier.cases == 0).any() == 0 : # on va jusque finir la partie 
            choix = rd.choice(self.othellier.promesses_de_gain().keys())
            self.othellier.tour(choix)
            self.othellier.joueur, self.othellier.adversaire = self.othellier.adversaire, self.othellier.joueur
        return self.othellier.qui_gagne()
    
    def genere_successeurs(self): # on fournit en input un objet de classe noeud
        #successeurs = []
        cases_possibles = self.othellier.promesses_de_gain().keys() 
        for case in cases_possibles:
            oth_fils = copy.deepcopy(self.othellier)
            oth_fils.mise_a_jour(case, self.othellier.a_des_binomes(case)[2])
            oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur
            #successeurs.append(noeud(oth_fils, case, n=0, w=0)))
            self.successeurs.append(noeud(oth_fils, case, n=0, w=0, parent=self))
        #return successeurs


def MCTS(othellier, nb_iter, C):
    '''
    othellier = l'othellier pour lequel on veut faire l'évaluation
    '''
    
    # Initialisation de l'arbre  
    oth_racine = copy.deepcopy(othellier)
    noeud_racine = noeud(oth_racine, None, n=0, w=0, parent=None)
    noeud_racine.genere_successeurs()
    # l'arbre est initialisé :) 

    # On commence les iterations 
    for i in range(nb_iter):
        noeud_courant = noeud_racine # on part de la racine de l'arbre 

        # Si le noeud a déjà été visité  (noeud_courant.n > 0) ET qu'il n'est pas associé à un othellier terminal, ie (noeud_courant.othellier.cases == 0).any(), 
        # alors on continue de descendre dans l'arbre en choisissant le successeur avec le meilleur UCB  
        # if noeud_courant != feuille : 
        while (noeud_courant.n > 0) and (noeud_courant.othellier.cases == 0).any(): 
            print("on avance dans l'arbre")
            print("je choisi le successeur qui a le meilleur UCB")
            noeud_courant.genere_successeurs()
            best_UCB = noeud_courant.successeurs[0].UCB(C) # on initialise le score UCB avec celui du premier successeur
            for s in noeud_courant.successeurs:
                if s.UCB(C) > best_UCB:
                    best_UCB = s.UCB(C)
                    noeud_courant = s 

        if noeud_courant.n == 0:
            print('roll out')
            gagnant = noeud_courant.play_out()
            # gagnant vaut 1, 2 ou 0.
            # Or, on ne souhaite remonter 1 si le joueur du noeud évalué a gagné : 
            if gagnant == noeud_racine.othellier.joueur[0]:
                result =  1
                result_adversaire = 0
            else:
                result = 0
                result_adversaire = 1
        
        if not (noeud_courant.othellier.cases == 0).any(): # le noeud est associé à un othellier dont la partie est finie 
            gagnant = noeud_courant.othellier.qui_gagne()
            if gagnant == noeud_racine.othellier.joueur[0]:
                result =  1
                result_adversaire = 0
            elif gagnant == 0: # cas d'égalité 
                result = 0
                result_adversaire = 0
            else:
                result = 0
                result_adversaire = 1
        
        # maintenant on retropropage le resultat 
        while noeud_courant != None:

            noeud_courant.n += 1 # quel que soit noeud_racine.othellier.joueur[0] on ajoute 1 car le noeud est visité 
            # La  mise à jour de w est un peu plus compliquée : 
            # "Si J1 n'a pas gagné son w n'augmente pas, mais J2 a gagné et son w augmente, et inversement + cas particulier des égalités  "
            if noeud_courant.othellier.joueur[0] == noeud_racine.othellier.joueur[0]:
                noeud_courant.w += result
            else: # noeud_courant.othellier.joueur[0] != noeud_racine.othellier.joueur[0]: 
                noeud_courant.w += result_adversaire

            noeud_courant = noeud_courant.parent 

    # maintenant que toutes les itérations ont été réalis&ees, on choisit quel est la meilleure case à jouer 
    
    best_s = noeud_racine.successeurs[0]
    best_score = best_s.w / best_s.n
    for s in noeud_racine.successeurs:
        if (s.w/s.n) > best_score:
            best_s = s 
    
    return s.case


# ------------------------------- fonctions copiées collées depuis git hub --------------------------

        
def show_tree(noeud, indent='', max_depth=3):
    if max_depth < 0:
        return
    if noeud is None:
        return
    if noeud.parent is None:
        print('%sroot' % indent)
    else:
        player = noeud.parent.othellier.joueur[0]
        case = noeud.case
        print('%s%s %s %d %.3f' % (
            indent,
            noeud.n,
            noeud.w,
        ))
    for child in sorted(noeud.successeurs, key=lambda i: i.n, reverse=True):
        show_tree(child, indent + '  ', max_depth - 1)