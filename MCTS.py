from othellier import othello
import numpy as np 
import copy
from math import ln , sqrt
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
    def __init__(self, othellier, n, w, parent):
        self.othellier = othellier 
        self.n = n 
        self.w = w 
        self.parent = parent # un objet appartenant à la classe noeud 
        self.successeurs = self.genere_successeurs()
        # N = pere.n 
    
    def is_terminal(self):
        pass

    def UCB(self, C):
        return self.w/self.n + C * sqrt( ln(self.pere.n) /self.n )
    
    def play_out(self):
        while (self.othellier.case == 0).any() == 0 : # on va jusque finir la partie 
            choix = rd.choice(self.othellier.promesses_de_gain().keys())
            self.othellier.tour(choix)
            self.othellier.joueur, self.othellier.adversaire = self.othellier.adversaire, self.othellier.joueur
        return self.othellier.qui_gagne()
    
    def genere_successeurs(self): # on fournit en input un objet de classe noeud
        cases_possibles = self.othellier.promesses_de_gain().keys() 
        for case in cases_possibles:
            oth_fils = copy.deepcopy(self.othellier)
            oth_fils.mise_a_jour(case, self.othellier.a_des_binomes(case)[2])
            oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur
            #noeuds.append(noeud(oth_fils, n=0, w=0))


def MCTS(othellier, nb_iter, noeuds, C):
    '''
    othellier = l'othellier pour lequel on veut faire l'évaluation
    nb_iter = le nombre d'iterations que l'on veut réaliser avec MCTS

    "noeuds" est une liste vide au début de l'algorithme. 
    '''
    
    # Initialisation de l'arbre  
    oth_racine = copy.deepcopy(othellier)
    noeud_racine = noeud(oth_racine, n=0, w=0, parent=None)
    # l'arbre est initialisé :) 

    # On commence les iterations 
    for i in range(nb_iter):
        noeud_courant = noeud_racine
        # Si le noeud a déjà été visité  (noeud_courant.n > 0) ET qu'il n'est pas associé à un othellier terminal, ie (noeud_courant.othellier.cases == 0).any(), 
        # alors on continue de descendre dans l'arbre en choisissant le successeur avec le meilleur UCB  
        # if noeud_courant != feuille : 
        
        while (noeud_courant.n > 0) and (noeud_courant.othellier.cases == 0).any(): 
            print("on avance dans l'arbre")
            print("je choisi le successeur qui a le meilleur UCB")
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
                return 1
            else:
                return 0
        
        if not (noeud_courant.othellier.cases == 0).any(): # le noeud est associé à un othellier dont la partie est finie 
            gagnant = noeud_courant.othellier.qui_gagne()
            if gagnant == noeud_racine.othellier.joueur[0]:
                return 1
            else:
                return 0

        
  