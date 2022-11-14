import numpy as np
from othellier import Othellier
from MinMax import MinMax


def partie(joueur1 = True, joueur2 = False, prof = 3):

    # On crée un othellier :
    # en début de partie, l'othellier est tel que : 
    debut_partie = np.zeros([8,8]) 
    debut_partie[4,3] = 1   # pion noir 
    debut_partie[3,4] = 1   # pion noir 
    debut_partie[3,3] = 2   # pion blanc 
    debut_partie[4,4] = 2   # pion blanc 

    # On initialise l'othellier 
    othellier = Othellier(debut_partie, joueur1, joueur2) 

    # On initialise les joueurs pour le premier tour (les noirs commencent toujours)
    # à chaque tour, la valeur de joueur et adversaire s'échangent 
    #joueur = 1, joueur1 ---> on en a plus besoin, c'est un attribut au sein de othellier !!! 
    #adversaire = 2 , joueur2 ---> on en a plus besoin, c'est un attribut au sein de othellier !!! 

    # le jeu continue tant qu'il reste au moins une case vide 

    while (othellier.cases == 0).any():

        # Il se peut que le joueur ne puisse pas jouer. 
        # On vérifie avec cette fontion : 
        if othellier.peut_jouer() :
            # on donne un aperçu de l'othellier 
            print(othellier.cases)
            if othellier.joueur[1] == True: 
                # Si le joueur est une vraie personne, on la laisse faire son choix 
                othellier.tour(othellier.Choix())
            else : 
                minmax = MinMax(othellier, prof, 1, gains = [], chemin = [], profondeurs = [])
                # La fonction nous retourne l'arbre minmax avec les valeurs (définies selon l'algo minmax) pour chaque noeud 
                # L'oarbre est sous forme de 3 listes : 
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
                indice_top_gain = np.argmax(gains_filtres)
                meilleure_case = chemin_filtres[indice_top_gain] # on choisit la case qui a la meilleure promesse de gain selon minmax 
                #print("meilleure case, gain")
                #print(meilleure_case, gains_filtres[indice_top_gain])
                othellier.tour(meilleure_case) # on joue la case 

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
    return "Félicitation, joueur {gagnant}, tu as gagné! ".format(gagnant = gagnant)
