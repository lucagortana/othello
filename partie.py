import numpy as np
from othellier import Othellier
from MinMax import MinMax
import random as rd 
from random import randint 


def partie(joueur1 = True , algo_j1 = None , joueur2 = False, algo_j2 = None, prof = 3):

    # On crée un othellier :
    # en début de partie, l'othellier est tel que : 
    debut_partie = np.zeros([8,8]) 
    debut_partie[4,3] = 1   # pion noir 
    debut_partie[3,4] = 1   # pion noir 
    debut_partie[3,3] = 2   # pion blanc 
    debut_partie[4,4] = 2   # pion blanc 

    # On initialise l'othellier 
    othellier = Othellier(debut_partie, joueur1, algo_j1, joueur2, algo_j2) 

    # On initialise les joueurs pour le premier tour (les noirs commencent toujours)
    # à chaque tour, la valeur de joueur et adversaire s'échangent 
    #joueur = 1, joueur1 ---> on en a plus besoin, c'est un attribut au sein de othellier !!! 
    #adversaire = 2 , joueur2 ---> on en a plus besoin, c'est un attribut au sein de othellier !!! 

    # le jeu continue tant qu'il reste au moins une case vide 

    while (othellier.cases == 0).any():
        print(othellier.joueur)
        # Il se peut que le joueur ne puisse pas jouer. 
        # On vérifie avec cette fontion : 
        if othellier.peut_jouer() :
            # on donne un aperçu de l'othellier 
            print(othellier.cases)
            if othellier.joueur[1] == True: 
                # Si le joueur est une vraie personne, on la laisse faire son choix 
                othellier.tour(othellier.Choix())
            else : 
                if othellier.joueur[2] == 'minmax': 
                    print('je suis un ordinateur et je joue avec minmax')
                    minmax = MinMax(othellier, prof, othellier.joueur[0], gains = [], chemin = [], profondeurs = [])
                    # La fonction nous retourne l'arbre minmax avec les valeurs (définies selon l'algo minmax) pour chaque noeud 
                    # L'arbre est sous forme de 3 listes : 
                    gains = minmax[1]
                    chemin = minmax[2]
                    profondeurs = minmax[3]
                    # On veut savoir quelle case jouer --> on prend le meilleur gain au niveau juste après l'othellier root : 
                    indices = []
                    for i in range(len(profondeurs)):
                        if profondeurs[i] == 3:
                            indices.append(i)
                    gains_filtres = [ gains[i] for i in indices] # les gains de l'étage juste en dessous de l'othellier racine 
                    chemin_filtres = [ chemin[i] for i in indices] # les cases associées 
                    # on veut jouer la case qui présente le gain maximal :
                    indice_top_gain = rd.choice(np.argwhere( gains_filtres == np.max(gains_filtres)).flatten())
                    # NB : on ne fait pas juste np.argmax(gains_filtres) car on n'obtiendrait toujours l'argument 
                    # du premier item maximal. Or, notre liste est ordonnée --> on jouerait alors plus souvent des 
                    # cases du haut de l'othellier --> on efface ce biais en faisant "rd.choice(np.argwhere( gains_filtres = np.max(gains_filtres)))"
                    meilleure_case = chemin_filtres[indice_top_gain] # on choisit la case qui a la meilleure promesse de gain selon minmax 
                    othellier.tour(meilleure_case) # on joue la case 
                elif othellier.joueur[2] == None: # choix de la case à jouer au hasard 
                    print("je suis un ordianteur et j'ai choisi au pif")
                    indices_poss = list(othellier.promesses_de_gain().keys())
                    choix = rd.choice(indices_poss)
                    othellier.tour(choix)  # on joue la case 
                elif othellier.joueur[2] == 'alphaBeta':
                    pass
                else : 
                    print("Vous n'avez pas bien renseigné l'algo que l'ordinateur doit utiliser! ")
                    print(" Il ne peut donc pas jouer, veuillez recommencer.")
                    print("Redonnez un algo à l'ordianteur parmi les suivants : None, 'minmax', 'alphaBeta'")
                    print("Gardez la casse !! ")
                    print("quittez avec ctrl + C ")

            # au tour de l'autre joueur de jouer --> on inverse les rôles 
            othellier.joueur, othellier.adversaire = othellier.adversaire, othellier.joueur
            print(" C'est au tour de joueur {joueur}".format(joueur = othellier.joueur[0]))
        else : 
            print("Joueur {joueur} tu ne peux pas jouer, passe ton tour ... ".format(joueur = othellier.joueur[0]))
            othellier.joueur, othellier.adversaire = othellier.adversaire, othellier.joueur
            print(" C'est au tour de joueur {joueur}".format(joueur = othellier.joueur[0]))

    print("C'est la fin de la partie!")
    print(othellier.cases)
    gagnant = othellier.qui_gagne()
    print("Félicitation, joueur {gagnant}, tu as gagné! ".format(gagnant = gagnant))
    return gagnant
