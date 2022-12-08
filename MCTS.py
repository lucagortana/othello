from othellier import Othellier
import numpy as np 
import copy
from math import log , sqrt
import random as rd 


'''
I - Selection : 
Choisir un neoud successeur tout en respectant un équilibre exploration/exploitation 
Le successeur i choisi est le successeur dont la valeur suivante est maximale :
 
(w/n) + c * sqrt( ln(N) /n )
Avec : 
    w = nombre de win 
    n = nombre de fois où i a été visité 
    N = nombre de fois où le noeud pere de i a été visité 
    C = le paramètre d'exploration ( souvent égal à sqrt(2) )

Le terme w/n représente l'exploitation 
Le terme c * sqrt( ln(N) /n ) représente l'exploration 

II - Expansion

III - Simulation

IV - Backpropagation 

V - Fin des itérations 

MCTS retournera son successeur qui présente le meilleur w/n 

'''
# programmation objet des noeuds 

class noeud:
    def __init__(self, othellier, case, n, w, parent):
        self.othellier = othellier 
        self.n = n 
        self.w = w 
        self.parent = parent # un objet appartenant à la classe noeud 
        self.case = case # "case" permet de savoir quelle case jouer pour passer du noeud parent à ce noeud / le chemin à suivre dans l'arbre 
        self.successeurs = [] # la liste des sucesseurs n'est remplie que plus tard. 
                              # Une liste successeurs vide signifie que le noeud est un neoud feuille 
        # N = parent.n 

    def UCB(self, C): #selection
        try: 
            return self.w/self.n + C * sqrt( log(self.parent.n) /self.n )
        except:
            # Si n = 0, UCB vaut + l'infini 
            return + 10000 
    
    def play_out(self):
        peut_pas_jouer = 0
        while (self.othellier.cases == 0).any(): # on itère jusqu'à finir la partie 
            if self.othellier.peut_jouer():
                peut_pas_jouer = 0
                choix = rd.choice(list(self.othellier.promesses_de_gain().keys()))
                self.othellier.tour(choix)
                self.othellier.joueur, self.othellier.adversaire = self.othellier.adversaire, self.othellier.joueur
            else :
                self.othellier.joueur, self.othellier.adversaire = self.othellier.adversaire, self.othellier.joueur
                # Si adversaire ne peut pas jouer non plus, alors personne ne peut jouer et la partie se finit. 
                peut_pas_jouer +=1 
                if peut_pas_jouer == 2:
                    return self.othellier.qui_gagne()
        
        return self.othellier.qui_gagne()
    
    def genere_successeurs(self):
        cases_possibles = self.othellier.promesses_de_gain().keys() 
        # une case possible = un successeur possible 
        for case in cases_possibles:
            oth_fils = copy.deepcopy(self.othellier)
            oth_fils.mise_a_jour(case, self.othellier.a_des_binomes(case)[2])
            oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur
            # on ajoute au noeud parent le successeur que l'on vient de créer 
            self.successeurs.append(noeud(oth_fils, case, n=0, w=0, parent=self)) 


    def genere_successeur(self, case):
        oth_fils = copy.deepcopy(self.othellier)
        oth_fils.mise_a_jour(case, self.othellier.a_des_binomes(case)[2])
        oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur
        self.successeurs.append(noeud(oth_fils, case, n=0, w=0, parent=self))
        self.case_a_jouer.remove(case)
        self.feuille = False
        


def MCTS(othellier, nb_iter, C, nb_play_out = 3 ):
    '''
    othellier = l'othellier pour lequel on veut faire l'évaluation
    '''
    boucle = 0 
    # Initialisation de l'arbre  
    oth_racine = copy.deepcopy(othellier)
    noeud_racine = noeud(oth_racine, None, n=0, w=0, parent=None)
    noeud_racine.genere_successeurs()
    


    # On commence les iterations 
    for i in range(nb_iter):
        noeud_courant = noeud_racine # on part de la racine de l'arbre 

        # On explore l'arbre jusqu'à trouver des feuilles.
        # J'avance dans l'arbre en choisissant le noeud avec le meilleur UCB 

        # I - Selection 
        while len(noeud_courant.successeurs) > 0 :
            best_UCB = -100  # initialisation 
            for s in noeud_courant.successeurs:
                if s.UCB(C) > best_UCB:
                    best_UCB = s.UCB(C)
                    noeud_courant = s 

        # len(noeud_courant.successeurs) == 0 --> Le noeud est une feuille. 
        # 2 possibilités : 
        # a - Il a été exploré une fois mais pas développé (noeud_courant.n == 1) 
        #     --> on le developpe et on réalisera un play_out sur un de ces successeurs 
        # b - il n'a jamais été exploré du tout (ie noeud_courant.n == 0) Dans ce cas on va réaliser un play out 
        
    
        if noeud_courant.n != 0:
            noeud_courant.genere_successeurs() # on developpe le noeud = II - EXPANSION
            # et on fait un play out sur le successeur avec le plus haut UCB
            best_UCB = -100  # initialisation 
            for s in noeud_courant.successeurs:
                if s.UCB(C) > best_UCB:
                    best_UCB = s.UCB(C)
                    noeud_courant = s 

        # Etant donné que les étapes de propagation vont modifier le noeud courant, on le garde en mémoire grâce à noeud_elu 
        noeud_elu = noeud_courant
        for npo in range(nb_play_out):
            #print("play out")
            boucle += 1 
            gagnant = noeud_elu.play_out()
            # gagnant vaut 1, 2 ou 0.
            # Or, on souhaite remonter 1 uniquement si le joueur du noeud racine a gagné. 
            # On procède donc ainsi : 
            if gagnant == noeud_racine.othellier.joueur[0]:
                result =  1
                result_adversaire = 0
            elif gagnant == 0: # cas d'égalité 
                result = 0
                result_adversaire = 0
            else : 
                result = 0
                result_adversaire = 1
            
            
            # III - rétropropagation 
            # maintenant on retropropage le resultat 
            noeud_courant = noeud_elu 
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
    best_s = noeud_racine.successeurs[0] # initialisation 
    best_score = best_s.w / best_s.n # initialisation 
    
    #successeurs = list(rd.shuffle(noeud_racine.successeurs))
    #print(type(successeurs))
    #rd.shuffle(noeud_racine.successeurs)
    for s in noeud_racine.successeurs: # on shuffle (?) --> de telle sorte qu'en cas d'égalité, ce ne soit pas toujours la même case qui soit explorée en premier
        try:
            if (s.w/s.n) > best_score: # !!! si le nombre d'iterations est inferieure au nombre de successeurs, division par zero !!! 
                best_s = s 
        except ZeroDivisionError:
            pass # si s.n == 0 --> c'est que le successeur n'a pas été visité --> on ne le considère pas 
        
    if i == 1:
        print(len(noeud_racine.successeurs))
        print(noeud_racine.successeurs.index(s))
    #print('MCTS a choisi la case', s.case)
    #print(boucle)
    return s.case

