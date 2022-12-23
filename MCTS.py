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
    def __init__(self, othellier, case, n, parent):
        self.othellier = othellier 
        self.n = n 
        self.w = {1 : 0, 2 : 0, 0 : 0 } # 3 clés : 1, 2, ou 0 qui comptabilise ls parties gagnées par le jouer 1, ou 2 ou égalités
        self.parent = parent # un objet appartenant à la classe noeud 
        self.case = case # "case" permet de savoir quelle case jouer pour passer du noeud parent à ce noeud / le chemin à suivre dans l'arbre 
        self.successeurs = [] # la liste des sucesseurs n'est remplie que plus tard. 
                              # Une liste successeurs vide signifie que le noeud est un neoud feuille 
        # N = parent.n 

    def UCB(self, C, joueur): #selection
        try: 
            return self.w[joueur]/self.n + C * sqrt( log(self.parent.n) /self.n )
        except:
            # Si n = 0, UCB vaut + l'infini 
            return + 10000 
    
    def play_out(self):
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


    def genere_successeur(self, case):
        oth_fils = copy.deepcopy(self.othellier)
        oth_fils.mise_a_jour(case, self.othellier.a_des_binomes(case)[2])
        oth_fils.joueur, oth_fils.adversaire = oth_fils.adversaire, oth_fils.joueur
        self.successeurs.append(noeud(oth_fils, case, n=0, parent=self))
        self.case_a_jouer.remove(case)
        self.feuille = False
        

def MCTS(othellier, nb_iter, C, nb_play_out):
    '''
    othellier = l'othellier pour lequel on veut faire l'évaluation
    '''
    # Initialisation de l'arbre  
    oth_racine = copy.deepcopy(othellier)
    noeud_racine = noeud(oth_racine, None, n=0, parent=None)
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
                if s.UCB(C, noeud_racine.othellier.joueur[0]) > best_UCB:
                    best_UCB = s.UCB(C,noeud_racine.othellier.joueur[0])
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
        #print("noeud_elu 1 ", noeud_elu)

        # #print(noeud_elu.othellier.joueur[0])
        for npo in range(nb_play_out):
            gagnant = noeud_elu.play_out()
        #     #print(gagnant)
        #     #print(noeud_racine.othellier.joueur[0])
        #     # gagnant vaut 1, 2 ou 0.
        #     # Or, on souhaite remonter +1 à la racine uniquement si le joueur du noeud racine a gagné. 
        #     # On procède donc ainsi : 
        #     if gagnant == noeud_racine.othellier.joueur[0]:
        #         #print('gagnant == noeud_racine.othellier.joueur[0]')
        #         result = 1
        #     elif gagnant == 0: # cas d'égalité 
        #         result = 0
        #     else : 
        #         #print('gagnant != noeud_racine.othellier.joueur[0]')
        #         result = 1

            
            # III - rétropropagation 
            #print(" w avant backprop ", noeud_racine.w)
            while noeud_courant != None:

                noeud_courant.n += 1 # quel que soit noeud_racine.othellier.joueur[0] on ajoute 1 car le noeud est visité 
                # La  mise à jour de w est un peu plus compliquée : 
                # Si le joueur 1 a gagné, on ajoute +1 dans w[1]. 0 l'inverse, si J2 a gagné, on ajoute +1 à w[2].
                # En cas d'égalité, on ajoute +1 à w[0]
                noeud_courant.w[gagnant] += 1
                #else: # noeud_courant.othellier.joueur[0] != noeud_racine.othellier.joueur[0]: 
                    #noeud_courant.w += result_adversaire
                noeud_courant = noeud_courant.parent 
            #print(" w après backprop ", noeud_racine.w)
            # on replace le noeud courant à celui de départ pour que le play out se fasse sur le meme noeud 
            noeud_courant = noeud_elu  
            #print("noeud_elu 2 ", noeud_courant)
            
    # maintenant que toutes les itérations ont été réalisées, on choisit quelle est la meilleure case à jouer 
    best_s = noeud_racine.successeurs[0] # initialisation 
    # noeud_racine.othellier.joueur[0]  = on se place du point de vue du joeur qui utilise MCTS 
    best_score = best_s.w[noeud_racine.othellier.joueur[0]] / best_s.n # initialisation 
    
    #rd.shuffle(noeud_racine.successeurs)
    best = {}
    for s in noeud_racine.successeurs: # on shuffle (?) --> de telle sorte qu'en cas d'égalité, ce ne soit pas toujours la même case qui soit explorée en premier
        best[s.case] = (s.w[noeud_racine.othellier.joueur[0]],s.n)
        try:
            
            if (s.w[noeud_racine.othellier.joueur[0]]/s.n) > best_score: # !!! si le nombre d'iterations est inferieure au nombre de successeurs, division par zero !!! 
                best_s = s 
                
        except ZeroDivisionError:
            pass # si s.n == 0 --> c'est que le successeur n'a pas été visité --> on ne le considère pas 
    # print('')
    # print("MCTS est utilise par le joueur ", noeud_racine.othellier.joueur[0])
    # print(" w fin iter", noeud_racine.w)
    # print(noeud_racine.othellier.cases)
    # print("successeurs", [s.case for s in noeud_racine.successeurs])
    # print(best)
    # print("MCTS a choisi la case ",best_s.case )

    return best_s

