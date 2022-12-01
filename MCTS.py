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
        self.feuille = True # True si le noeud est une feuille (ie plus de place sur l'othellier, ou bien pas de successeurs générés)
        self.n = n 
        self.w = w 
        self.parent = parent # un objet appartenant à la classe noeud 
        self.case = case
        #self.case_a_jouer = list(othellier.promesses_de_gain().keys()) # tous les moves qui menent à un succeseur 
        self.successeurs = []
        # N = pere.n 

    def UCB(self, C): #selection
        try: 
            return self.w/self.n + C * sqrt( log(self.parent.n) /self.n )
        except:
            # Si n = 0, UCB vaut + l'infini 
            return + 10000 
    
    def play_out(self):
        #print('coucou')
        while (self.othellier.cases == 0).any(): # on va jusqu'à finir la partie 
            #print("je rentre dans le while")
            if len(self.othellier.promesses_de_gain().keys()) == 0:
                return self.othellier.qui_gagne()
            choix = rd.choice(list(self.othellier.promesses_de_gain().keys()))
            self.othellier.tour(choix)
            self.othellier.joueur, self.othellier.adversaire = self.othellier.adversaire, self.othellier.joueur

        return self.othellier.qui_gagne()
    
    def genere_successeurs(self):
        cases_possibles = self.othellier.promesses_de_gain().keys() 
        for case in cases_possibles:
            oth_fils = copy.deepcopy(self.othellier)
            oth_fils.mise_a_jour(case, self.othellier.a_des_binomes(case)[2])
            oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur
            self.successeurs.append(noeud(oth_fils, case, n=0, w=0, parent=self))
            self.feuille = False # En generant des successeurs, on perd le statut de feuille 


    def genere_successeur(self, case):
        oth_fils = copy.deepcopy(self.othellier)
        oth_fils.mise_a_jour(case, self.othellier.a_des_binomes(case)[2])
        oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur
        self.successeurs.append(noeud(oth_fils, case, n=0, w=0, parent=self))
        self.case_a_jouer.remove(case)
        self.feuille = False
        
    

def MCTS(othellier, nb_iter, C):
    '''
    othellier = l'othellier pour lequel on veut faire l'évaluation
    '''
    
    # Initialisation de l'arbre  
    oth_racine = copy.deepcopy(othellier)
    noeud_racine = noeud(oth_racine, None, n=0, w=0, parent=None)
    noeud_racine.genere_successeurs()
    noeud_racine.feuille = False
    #print([s.case for s in noeud_racine.successeurs])
    # l'arbre est initialisé :) 
    #show_tree(noeud_racine)
    #print(noeud_racine)

    # On commence les iterations 
    for i in range(nb_iter):
        noeud_courant = noeud_racine # on part de la racine de l'arbre 

        # On explore l'arbre jusqu'à trouver des feuilles.
        # J'avance dans l'arbre en choisissant le noeud avec le meilleur UCB 

        # I - Selection 
        #while noeud_courant.feuille == False :  # and (noeud_courant.othellier.cases == 0).any(): 
        while len(noeud_courant.successeurs) > 0 :
            best_UCB = -100  # initialisation 
            for s in noeud_courant.successeurs:
                if s.UCB(C) > best_UCB:
                    best_UCB = s.UCB(C)
                    noeud_courant = s 

        # len(noeud_courant.successeurs) --> Le noeud est une feuille. 
        # 2 possibilités : 
        # a - Il a été exploré une fois mais pas développé (noeud_courant.n == 1) 
        #     --> on le developpe et on réalisera un play_out sur un de ces successeurs 
        # b - il n'a jamais été exploré du tout (ie noeud_courant.n == 0) Dans ce cas on va réaliser un play out 
        
    
        if noeud_courant.n != 0:
            noeud_courant.genere_successeurs() # on developpe le noeud = II - EXPANSION
            # et on fait un play out surs le successeur avec le plus haut UCB
            best_UCB = -100  # initialisation 
            for s in noeud_courant.successeurs:
                if s.UCB(C) > best_UCB:
                    best_UCB = s.UCB(C)
                    noeud_courant = s 


        #else: # noeud_courant.n == 0:
        #print("play out")
        gagnant = noeud_courant.play_out()
        # gagnant vaut 1, 2 ou 0.
        # Or, on ne souhaite remonter 1 si le joueur du noeud évalué a gagné : 
        if gagnant == noeud_racine.othellier.joueur[0]:
            result =  1
            result_adversaire = 0
        elif gagnant == 0: # cas d'égalité 
            result = 0
            result_adversaire = 0
        else : 
            result = 0
            result_adversaire = 1


        '''
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
        '''
        
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
    

    # maintenant que toutes les itérations ont été réalisées, on choisit quelle est la meilleure case à jouer 
    best_s = noeud_racine.successeurs[0]
    best_score = best_s.w / best_s.n

    for s in noeud_racine.successeurs: # on shuffle (?) --> de telle sorte qu'en cas d'égalité, ce ne soit pas toujours la même case qui soit explorée en premier
        try:
            if (s.w/s.n) > best_score: # !!! si le nombre d'iterations est inferieure au nombre de successeurs, division par zero !!! 
                best_s = s 
        except ZeroDivisionError:
            pass # si s.n == 0 --> c'est que le successeur n'a pas été visité --> on ne le considère pas 
    print('MCTS a choisi la case', s.case)
    #print(' parmi les cases : ',[ s.case for s in  noeud_racine.successeurs])
    return s.case

