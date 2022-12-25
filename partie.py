import numpy as np
from othellier import Othellier
from MinMax import MinMax
from alphaBeta import alphaBeta
from MCTS import MCTS
import random as rd 
from random import randint 


def partie(joueur1 = True , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = 'minmax', prof_algo_j2 = 2, valeur_c = 1.414, nb_play_out = 1 ):
    # paramètres par défaut : une vraie personne face à un ordinateur qui joue aléatoirement selon minmax en profondeur 2
    # les paramètres par défaut dans le cas où MCTS est utilisé : 1.414 et 1. 

    # On crée un othellier :
    # en début de partie, l'othellier est tel que : 
    debut_partie = np.zeros([8,8]) 
    debut_partie[4,3] = 1   # pion noir 
    debut_partie[3,4] = 1   # pion noir 
    debut_partie[3,3] = 2   # pion blanc 
    debut_partie[4,4] = 2   # pion blanc 

    # On initialise l'othellier 
    othellier = Othellier(debut_partie, joueur1, algo_j1, prof_algo_j1, joueur2, algo_j2, prof_algo_j2) 

    # On initialise les joueurs pour le premier tour (les noirs commencent toujours).
    # À chaque tour, la valeur de joueur et adversaire s'échangent 
    

    while (othellier.cases == 0).any() : # le jeu continue tant qu'il reste au moins une case vide 
        # Il se peut que le joueur ne puisse pas jouer. On le vérifie avec la fontion suivante: 
        if othellier.peut_jouer():
            peut_pas_jouer = 0 # compteur : s'il dépasse 2 c'est que ni J1 ni J2 ne peuvent jouer --> la partie doit s'arreter 
            #print(othellier.cases) # on donne un aperçu de l'othellier 
            if othellier.joueur[1] == True: # Si le joueur est une vraie personne et non un ordinateur, on le laisse faire son choix 
                othellier.tour(othellier.Choix())
            
            else : # si le joueur est un ordinateur 

                
                if othellier.joueur[2] == 'minmax': # Si l'ordinateur joue selon l'algorithme MinMax
                    minmax = MinMax(othellier, othellier.joueur[3], othellier.joueur[0], gains = [], chemin = [], profondeurs = [])
                    # La fonction nous retourne l'arbre minmax avec les valeurs (définies selon l'algo minmax) pour chaque noeud 
                    # L'arbre est sous forme de 3 listes : 
                    gains = minmax[1]
                    chemin = minmax[2]
                    profondeurs = minmax[3]
                    # On veut savoir quelle case jouer --> on prend le meilleur gain au niveau juste après l'othellier racine : 
                    indices = []
                    for i in range(len(profondeurs)):
                        if profondeurs[i] == max(profondeurs): # les indices où le noeud est juste en dessous de la racine 
                            indices.append(i)
                    gains_filtres = [ gains[i] for i in indices] # les gains de l'étage juste en dessous de l'othellier racine 
                    chemin_filtres = [ chemin[i] for i in indices] # les cases associées 
                    # on veut jouer la case qui présente le gain maximal :
                    indice_top_gain = rd.choice(np.argwhere( gains_filtres == np.max(gains_filtres)).flatten())
                    # NB : on ne fait pas juste np.argmax(gains_filtres) car on obtiendrait toujours l'argument 
                    # du premier item maximal. Or, notre liste est ordonnée --> on jouerait alors plus souvent des 
                    # cases du haut de l'othellier --> on efface ce biais en faisant "rd.choice(np.argwhere( gains_filtres = np.max(gains_filtres)))"
                    meilleure_case = chemin_filtres[indice_top_gain] # on choisit la case qui a la meilleure promesse de gain selon minmax 
                    othellier.tour(meilleure_case) # on joue la case 

                elif othellier.joueur[2] == 'ref': # Si l'ordinateur joue selon l'algorithme qui nous sert de référence 
                    # --> le joueur va jouer la case qui donne le plus de points pour ce tour sans considérer plus loin --> un minmax à un seul étage (ie prof = 1 )
                    minmax = MinMax(othellier, 1, othellier.joueur[0], gains = [], chemin = [], profondeurs = [])
                    gains = minmax[1]
                    chemin = minmax[2]
                    profondeurs = minmax[3]
                    indices = []
                    for i in range(len(profondeurs)):
                        if profondeurs[i] == max(profondeurs):
                            indices.append(i)
                    gains_filtres = [ gains[i] for i in indices] # les gains de l'étage juste en dessous de l'othellier racine 
                    chemin_filtres = [ chemin[i] for i in indices] # les cases associées 
                    # on veut jouer la case qui présente le gain maximal :
                    indice_top_gain = rd.choice(np.argwhere( gains_filtres == np.max(gains_filtres)).flatten())
                    meilleure_case = chemin_filtres[indice_top_gain] # on choisit la case qui a la meilleure promesse de gain selon minmax 
                    othellier.tour(meilleure_case) # on joue la case 

                elif othellier.joueur[2] == 'alphaBeta': # Si l'ordinateur joue selon l'algorithme alphaBeta
                    ab = alphaBeta(othellier, othellier.joueur[3], othellier.joueur[0], -1000, 1000, gains = [], chemin = [], profondeurs = [])
                    gains = ab[1]
                    chemin = ab[2]
                    profondeurs = ab[3]
                    indices = []
                    
                    for i in range(len(profondeurs)):
                        if profondeurs[i] == othellier.joueur[3]:
                            indices.append(i)
                    
                    gains_filtres = [ gains[i] for i in indices] # les gains de l'étage juste en dessous de l'othellier racine 
                    chemin_filtres = [ chemin[i] for i in indices] # les cases associées 
                    # on veut jouer la case qui présente le gain maximal :
                    indice_top_gain = rd.choice(np.argwhere( gains_filtres == np.max(gains_filtres)).flatten())
                    meilleure_case = chemin_filtres[indice_top_gain] # on choisit la case qui a la meilleure promesse de gain selon minmax 
                    othellier.tour(meilleure_case) # on joue la case 
                
                elif othellier.joueur[2] == 'MCTS': # Si l'ordinateur joue selon l'algorithme MCTS
                    meilleur_noeud = MCTS(othellier, othellier.joueur[3], valeur_c, nb_play_out)
                    othellier.tour(meilleur_noeud.case) # on joue la case renvoyée par MCTS


                elif othellier.joueur[2] == None: # Si l'ordinateur ne joue selon aucun algorithme (= référence par rapport au hasard)
                    choix = rd.choice(list(othellier.promesses_de_gain().keys())) # on choisit au hasard une case jouable 
                    othellier.tour(choix) # on joue la case 

                else : # En cas de problème : 
                    print("Vous n'avez pas bien renseigné l'algorithme que l'ordinateur doit utiliser. ")
                    print("Il ne peut donc pas jouer, veuillez recommencer.")
                    print("Redonnez un algorithme à l'ordinateur parmi les suivants : None, 'minmax', 'alphaBeta', 'MCTS' ou 'ref'")
                    print("Attention à respecter la casse !! ")
                    exit()

            # au tour de l'autre joueur de jouer --> on inverse les rôles 
            othellier.joueur, othellier.adversaire = othellier.adversaire, othellier.joueur
            #print("C'est au tour de joueur {joueur}".format(joueur = othellier.joueur[0]))

             
        else : # joueur ne peut pas jouer car aucune case possible pour lui 
            #print("Joueur {joueur} tu ne peux pas jouer, passe ton tour ... ".format(joueur = othellier.joueur[0]))
            peut_pas_jouer +=1 
            othellier.joueur, othellier.adversaire = othellier.adversaire, othellier.joueur
            
            if peut_pas_jouer == 2: # Si l'adversaire ne peut pas jouer non plus, alors personne ne peut jouer et la partie se finit. 
                #print("Joueur {joueur} tu ne peux pas jouer non plus !! ".format(joueur = othellier.joueur[0]))
                #print("Plus personne ne peux jouer ...   :'(    La partie est finie")
                return othellier.qui_gagne()

            #print(" C'est au tour de joueur {joueur}".format(joueur = othellier.joueur[0]))

    #print("C'est la fin de la partie!")
    #print(othellier.cases)
    gagnant = othellier.qui_gagne()
    #print("Félicitation, joueur {gagnant}, tu as gagné! ".format(gagnant = gagnant))
    return gagnant
