import numpy as np
from othellier import Othellier


def partie(joueur1=False, joueur2=True):

    # On crée un othellier :
    # en début de partie, l'othellier est tel que : 
    debut_partie = np.zeros([8,8]) 
    debut_partie[4,3] = 1   # pion noir 
    debut_partie[3,4] = 1   # pion noir 
    debut_partie[3,3] = 2   # pion blanc 
    debut_partie[4,4] = 2   # pion blanc 

    # On initialise l'othellier 
    othellier = Othellier(debut_partie, True, False) 

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
            othellier.tour(othellier.Choix())
            # au tour de l'autre joueur de jouer : 
            othellier.joueur[0], othellier.adversaire[0] = othellier.adversaire[0], othellier.joueur[0]
            othellier.joueur[1], othellier.adversaire[1] = othellier.adversaire[1], othellier.joueur[1]
            print(" C'est au tour de joueur {joueur}".format(joueur = othellier.joueur[0]))
        else : 
            print("Joueur {joueur} tu ne peux pas jouer, passe ton tour ... ".format(joueur = othellier.joueur[0]))
            othellier.joueur[0], othellier.adversaire[0] = othellier.adversaire[0], othellier.joueur[0]
            print(" C'est au tour de joueur {joueur}".format(joueur = othellier.joueur[0]))

    print("C'est la fin de la partie!")
    print(othellier.cases)
    gagnant = othellier.qui_gagne()
    return "Félicitation, joueur {gagnant}, tu as gagné! ".format(gagnant = gagnant)
