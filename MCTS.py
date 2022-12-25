from othellier import Othellier
import numpy as np 
import copy
from math import log , sqrt
import random as rd 


''' RAPPELS 
I - Selection : 
Choisir un noeud successeur tout en respectant un équilibre exploration/exploitation 
Le successeur i choisi est le successeur dont la valeur suivante est maximale : (w/n) + c * sqrt( ln(N) /n )
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

# MCTS et représenté sous forme d'arbre. 
# Nous avons choisi une programmation objet pour les noeuds constitutifs de l'arbre

class noeud:
    def __init__(self, othellier, case, n, parent):
        self.othellier = othellier 
        self.n = n 
        self.w = {1 : 0, 2 : 0, 0 : 0 } # un dictionnaire avec 3 clés : 1, 2, ou 0 qui comptabilise les parties gagnées par le joueur 1, par le joueur 2 et les égalités
        self.parent = parent # un objet appartenant à la classe noeud. Nécéssaire pour la rétro-propagation
        self.case = case # "case" permet de savoir quelle case jouer pour passer du noeud parent à ce noeud / le chemin à suivre dans l'arbre 
        self.successeurs = [] # la liste des sucesseurs n'est remplie que plus tard. 
                              # Une liste successeurs vide signifie que le noeud est un noeud feuille 

    def UCB(self, C, joueur): # Upper Confidence Bound : pour la selection des noeuds 
        try: 
            return self.w[joueur]/self.n + C * sqrt( log(self.parent.n) /self.n )
        except:
            # Si n = 0, UCB vaut en théorie + l'infini
            return + 10000 
    
    def play_out(self): # Réaliser les parties aléatoires pour les "roll out".  
        peut_pas_jouer = 0
        while (self.othellier.cases == 0).any(): # tant qu'il y a une case de libre, on itère 
            if self.othellier.peut_jouer():
                peut_pas_jouer = 0
                choix = rd.choice(list(self.othellier.promesses_de_gain().keys())) # choix au hasard de la case à jouer 
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
            self.successeurs.append(noeud(oth_fils, case, n=0, parent=self)) 
        

def MCTS(othellier, nb_iter, C, nb_play_out):
    '''
    othellier = l'othellier pour lequel on veut faire l'évaluation (= othellier racine)
    nb_iter = le nombre d'itérations qui vont être réalisées
    nb_play_out = le nombre de parties jouées lors de la phase 'Simulations'
    '''
    # Initialisation de l'arbre  
    oth_racine = copy.deepcopy(othellier) # deepcopy pour ne pas altérer l'objet en lui même 
    noeud_racine = noeud(oth_racine, None, n=0, parent=None)
    noeud_racine.genere_successeurs()

    # On commence les iterations 
    for i in range(nb_iter):
        
        noeud_courant = noeud_racine # On part de la racine de l'arbre 
        # On explore l'arbre jusqu'à trouver des feuilles.
        # On avance dans l'arbre en choisissant le noeud avec le meilleur UCB.

        # I - Selection 
        while len(noeud_courant.successeurs) > 0 :
            best_UCB = -100  # initialisation 
            for s in noeud_courant.successeurs:
                if s.UCB(C, noeud_racine.othellier.joueur[0]) > best_UCB:
                    best_UCB = s.UCB(C,noeud_racine.othellier.joueur[0])
                    noeud_courant = s 

        # len(noeud_courant.successeurs) == 0 --> Le noeud est une feuille. 
        # 2 possibilités : 
        # a - Il a été exploré une fois mais pas développé (noeud_courant.n == 1) 
        #     --> on le developpe et on réalisera un play_out sur un de ces successeurs 
        # b - il n'a jamais été exploré du tout (ie noeud_courant.n == 0). Dans ce cas on va réaliser un play out. 
    
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
            gagnant = noeud_elu.play_out() # III - Simulations 

            # IV - rétropropagation 
            while noeud_courant != None:

                noeud_courant.n += 1 # quel que soit noeud_racine.othellier.joueur[0] on ajoute 1 car le noeud est visité 
                # La  mise à jour de w est un peu plus compliquée : # Si le joueur 1 a gagné, on ajoute +1 dans w[1]. 
                # À l'inverse, si J2 a gagné, on ajoute +1 à w[2]. En cas d'égalité, on ajoute +1 à w[0]
                noeud_courant.w[gagnant] += 1
                noeud_courant = noeud_courant.parent 

            # on replace le noeud courant à celui de départ pour que le play out se fasse sur le meme noeud 
            noeud_courant = noeud_elu  

    # maintenant que toutes les itérations ont été réalisées, on choisit quelle est la meilleure case à jouer.
    # En utilisant noeud_racine.othellier.joueur[0], on se place du point de vue du joeur qui utilise MCTS 
    best_s = noeud_racine.successeurs[0] # initialisation 
    best_score = best_s.w[noeud_racine.othellier.joueur[0]] / best_s.n # initialisation 
    
    #rd.shuffle(noeud_racine.successeurs) # on shuffle (?) --> de telle sorte qu'en cas d'égalité, ce ne soit pas toujours la même case qui soit explorée en premier
    best = {}
    for s in noeud_racine.successeurs: 
        best[s.case] = (s.w[noeud_racine.othellier.joueur[0]] , s.n)
        try:
            if (s.w[noeud_racine.othellier.joueur[0]]/s.n) > best_score: 
                best_s = s 
        except ZeroDivisionError:
            pass # si s.n == 0 --> c'est que le successeur n'a pas été visité --> on ne le considère pas 

    return best_s

