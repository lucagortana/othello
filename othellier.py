import numpy as np 
import random as rd

# ----------------------------------- CLASSE -----------------------------------

class Othellier:
    '''
    Cette classe modélise l'état du jeu à un moment donné :
    - le plateau de jeu (=l'othellier) 
    - à qui est ce de jouer ? 
    - vraie parsonne ou ordinateur ? 
    - si ordinateur : selon quel algorithme ? 
    '''

    def __init__(self, cases, joueur1,algo_j1,prof_algo_j1, joueur2, algo_j2,prof_algo_j2):
        self.cases = cases 
        self.joueur = [1] + [joueur1] + [algo_j1] + [prof_algo_j1]   # Le joueur 1 (=les noirs) commence toujours
        self.adversaire = [2] + [joueur2] + [algo_j2] + [prof_algo_j2] # On passe en liste pour ne pas avoir de tuple, qui ne supporte pas le "item assignment" 

        # [1] et [2] signifient "joueur 1 / pions noirs" et "joueur 2 / pions blancs"
        # les valeurs pour [joueur1] et [joueur2] sont True (si la personne qui joue est réelle) et False (si c'est un ordinateur qui joue)
        # la 3ème valeur est l'algorithme que va utiliser l'ordinateur. Si la deuxième valeur == True, il n'est pas nécéssaire de définir d'algorithme. 
        # La 4ème valeur correspond à la profondeur / nombre d'itération utilisés lors de l'execution des algorithmes. 
    
    def case_libre(self, choix):
        '''
        Cette fonction permet de vérifier, pour un othellier donné, si la case choisie par le joueur est libre. 
        '''
        try : 
            if self.cases[choix[0], choix[1]] != 0 : 
                case_libre = False
            else : 
                case_libre = True 
        except IndexError:
            case_libre = False
            pass

        return case_libre

    def a_des_voisins(self, choix):
        '''
        Cette fonction permet de déterminer si une case choisie par le joueur, 
        pour un othellier donné, est accolée à un pion de l'adversaire 
        '''
        a_des_voisins = False # initialisation 
        indices_voisins = [ 
            [choix[0], choix[1]-1],     # indice du voisin de gauche 
            [choix[0], choix[1]+1],     # ------ -- voisin de droite 
            [choix[0]+1, choix[1]],     # ------ -- voisin du bas 
            [choix[0]-1, choix[1]],     # ------ -- voisin du haut 
            [choix[0]-1, choix[1]-1],   # ------ -- voisin en haut à gauche 
            [choix[0]+1, choix[1]+1],   # ------ -- voisin en bas à droite 
            [choix[0]+1, choix[1]-1],   # ------ -- voisin en bas à gauche 
            [choix[0]-1, choix[1]+1] ]  # ------ -- voisin en haut à droite 

    
        for i in range(len(indices_voisins)) :
            try:
                if 7 >= indices_voisins[i][0] >= 0 and 7 >= indices_voisins[i][1]>=0:
                    if self.cases[indices_voisins[i][0], indices_voisins[i][1]] == self.adversaire[0] :
                        a_des_voisins = True 
                        break
            except IndexError:
                pass # gestion des effets de bord 
                
        return a_des_voisins 


    def a_des_binomes(self, choix):
        '''
        Cette fonction :
        - détermine si le choix de la case permet de capturer des jetons adverses. 
        - renvoie les indices des pions capturés 

        On part du pion et de sa potentielle position. 
        On scanne dans chacune des directions pour aller chercher le prochain pion de la même couleur 
        permettant de capturer les jetons adverses. 
        On appelle le pion trouvé "binome".
        Il faut qu'entre 2 binomes, il y ait en effet des pions adverses (que l'on note "captures") ! 
        '''

        # initialisation 
        a_un_binome = False 
        binomes = []
        captures = []
        sens = ['haut', 'bas', 'gauche', 'droite', 'diag_haut_droite', 'diag_haut_gauche', 'diag_bas_droite', 'diag_bas_gauche']
        
        for sens_ in sens :

            captures_temporaires = []
            for i in range(1,8): # sept pas dans un sens pour essayer de trouver un binome. 
                try : 
                    directions = { 'haut' : (choix[0]-i, choix[1]), 
                        'bas' : (choix[0]+i, choix[1]), 
                        'gauche' : (choix[0], choix[1]-i), 
                        'droite' : (choix[0], choix[1]+i), 
                        'diag_haut_droite' : (choix[0]-i, choix[1]+i), 
                        'diag_haut_gauche' : (choix[0]-i, choix[1]-i), 
                        'diag_bas_droite' : (choix[0]+i, choix[1]+i),                   
                        'diag_bas_gauche' : (choix[0]+i, choix[1]-i)}

                    if 0 <= directions[sens_][0] <=7 and 0 <= directions[sens_][1] <=7: 
                    # NB : cette ligne complète le "try" car si les valeurs sont négatives, il n'y a pas d'exception levée pas le except ... 
                        if self.cases[directions[sens_][0], directions[sens_][1]] == self.adversaire[0]:
                            captures_temporaires.append(directions[sens_]) 

                        elif self.cases[directions[sens_][0], directions[sens_][1]] == 0 :
                            # si on a trouvé une capture mais qu'il y a un trou ensuite, ça ne compte plus! 
                            captures_temporaires = [] # on repart à zéro 
                            break 
                        
                        if self.cases[directions[sens_][0], directions[sens_][1]] == self.joueur[0] and len(captures_temporaires)>0: # and joueur not in captures_temporaires:
                            binomes.append(directions[sens_])
                            for item in captures_temporaires:
                                captures.append(item)
                            break # pas besoin d'aller voir plus loin une fois qu'on a trouvé un binome 
                        if self.cases[directions[sens_][0], directions[sens_][1]] == self.joueur[0] and len(captures_temporaires) == 0:
                            # si on rencontre un pion de le meme couleur que celui du joueur, alors on ne captures rien! --> on arrete 
                            break
                except IndexError:
                    pass

        if len(binomes) != 0:
            a_un_binome = True
        return a_un_binome, binomes, captures 
    
    def mise_a_jour(self, choix, captures):
        '''
        Cette fonction met à jour l'othellier à la suite du choix du joueur 
        ''' 
        try:
            self.cases[choix[0], choix[1]] = self.joueur[0] # on place le pion sur la case choisie par le joueur 
            for capture in captures:
                self.cases[capture[0], capture[1]] = self.joueur[0] # on retourne les pions capturés 
        except IndexError:
            pass


    def peut_jouer(self):
        '''
        On regarde parmi les cases libres restantes si le joueur peut y placer un jeton.
        Si ce n'est pas possible, il doit passer son tour.
        '''
        peut_jouer = False
        cases_libres = list(zip(np.where(self.cases == 0)[0], np.where(self.cases == 0)[1]))
        for case in cases_libres:
            if self.a_des_voisins((case[0],case[1])) and self.a_des_binomes((case[0],case[1]))[0]:
                peut_jouer = True
                break # Si il y a au moins une possibilité pour le jouer de jouer, on arrete ici 
        return peut_jouer

    def qui_gagne(self):
        '''
        Cette fonction renvoie le numéro du joueur gagnant (1 ou 2) ou 0 en cas d'égalité
        '''
        if np.where(self.cases == 1, True, False).sum() > np.where(self.cases == 2, True, False).sum():
            #print("joueur 1 gagne")
            return 1
        elif np.where(self.cases == 1, True, False).sum() < np.where(self.cases == 2, True, False).sum() : 
            #print("joueur 2 gagne")
            return 2
        else : 
            #print("égalité !!")
            return 0 

    def tour(self, choix):
        '''
        Cette fonction représente un tour de jeu. 
        On spécifie dans le paramètre "joueur" à quel joueur est le tour (1 ou 2) 
        Dans un tour : 
        - le joueur choisit la case sur laquelle il souhaite placer son jeton 
        - on compte et retourne les jetons capturés 
        - on met à jour l'othellier 
        '''
        # --------------------- choix de la case ----------------------------
        
        # Il ne peut pas entrer n'importe quelle case : 
        while est_sur_othellier(choix) == False or \
        self.case_libre(choix) == False or \
        self.a_des_voisins(choix) == False or \
        self.a_des_binomes(choix)[0] == False:

            if self.joueur[1] == True : # on ne print que si c'est une personne réelle 

                # 1 - La case doit avoir un sens (ie être sur l'échiquier)
                if est_sur_othellier(choix) == False :
                    print("Merci de choisir des chiffres entre 1 et 8")

                # 2 - La case doit être libre  
                if self.case_libre(choix) == False:
                    print("Tu ne peux pas jouer là, la case est déjà prise")

                # 3 - La case choisie doit être accolée à au moins un pion de son adversaire
                if self.a_des_voisins(choix) == False:
                    print("Tu ne peux pas placer ton pion ici, il doit etre accolé à au moins un pion de l'adversaire ")
                
                #  4 - On vérifie maintenant qu'en plaçant son pion ici, le joueur capture effectivement 
                # des jetons de son adversaire. Sinon, il n'a pas le droit de placer son pion ici.
                if self.a_des_binomes(choix)[0] == False:
                    print("tu ne peux pas placer ton jeton ici, tu ne captures aucun pion!")

            choix = self.Choix()

        # Une fois les 4 conditions vérifiées, on peut renvoyer l'othellier avec les nouvelles valeurs 
        #print("Le joueur ", self.joueur[0], " a choisi la case ", (choix[0] + 1 ,choix[1] + 1 ), '. Son coup lui permet de capturer {n_capture} pion(s)'.format(n_capture = len(self.a_des_binomes(choix)[2])), "en position ", [(self.a_des_binomes(choix)[2][i][0]+1, self.a_des_binomes(choix)[2][i][1]+1) for i in range(len(self.a_des_binomes(choix)[2]))])
        #print('Son coup lui permet de capturer {n_capture} pion(s)'.format(n_capture = len(self.a_des_binomes(choix)[2])))
        #print("en position ", [(self.a_des_binomes(choix)[2][i][0]+1, self.a_des_binomes(choix)[2][i][1]+1) for i in range(len(self.a_des_binomes(choix)[2]))])
        self.mise_a_jour(choix, self.a_des_binomes(choix)[2])

    def fonction_evaluation(self):
        nb = np.where(self.cases == self.joueur[0], True, False).sum() - np.where(self.cases == self.adversaire[0], True, False).sum()
        for i in range(len(self.cases)):
            for j in range(len(self.cases)):

                if (j==0 or j==7) and (i ==0 or i ==7) : # si on est dans les coins : bonus 
                    if self.cases[i,j] == self.joueur[0]:
                        nb += 100
                
                elif (i== 0 or i ==7 ) or (j==0 or j==7):   # si on est sur les bords (hors coins et proches-coins)
                    if self.cases[i,j] == self.joueur[0]:
                        nb += 20 

                elif ((i ==1 or i==0 or i==6 or i ==7) and ( j==0 or j==1 or j==6 or j==7 )) and not ((i== 0 or i ==7 ) and (j==0 or j==7)) : # si on offre à l'adversaire une chance d'aller trouver un bord ou un coin : malus 
                    if self.cases[i,j] == self.joueur[0]:
                        nb -= 30

        return nb , None, None # None et None pour des questions de format 
      

    def promesses_de_gain(self):
        '''
        Cette fonction retourne pour chaque case jouable par le joeur du tour
        le nombre de jeton(s) retourné(s) si le joueur joue sur la case en question. 
        '''
        promesses_de_gain = {}
        for i in range(0,8):
            for j in range(0,8):
                case = [i,j]
                if self.cases[i][j] == 0: 
                    # chaque case jouable est associée à ses captures 
                    if len(self.a_des_binomes(case)[2]) != 0:
                        # on ne rajoute que les cases qui ont un interet 
                        promesses_de_gain[(case[0],case[1])] = self.a_des_binomes(case)[2]
        return promesses_de_gain
            

    def Choix(self):
        '''
        Le joueur chosit la case sur laquelle il veut placer son jeton 
        '''

        if self.joueur[1] == True: 
            choix_ = False # Tant que le choix entré n'est pas sous la bonne forme, on garde choix_ = False
            while choix_ == False:
                choix = input('joueur {joueur}, où veux tu placer ton pion ? '.format(joueur = self.joueur[0]))
                try:
                    choix = [int(item) for item in choix.split(',')] # input fournit un str --> on fait en sorte d'avoir une liste 
                    # On réindexe le choix du joueur pour avoir une indexation à 0 (python-compatible)
                    choix[0] = choix[0] - 1 # Réindexage de la ligne 
                    choix[1] = choix[1] - 1 # Réindexage de la colonne 
                    choix_ = True

                except ValueError:
                    print("Rentre ton choix sous la forme <n°ligne>,<n°colonne> stp :) ")
                except IndexError:
                    print("Merci de choisir des chiffres entre 1 et 8")
        
        else : # OUT-DATED : Maintenant, avec MinMax/AlphaBeta/MCTS, on ne rentre plus jamais dans cette boucle. 
            # Dans le cas où c'est l'ordinateur qui joue, il choisit une case au hasard.
            # Si la case ne permet pas de jouer, il choisira de nouveau jusqu'à ce que ça fonctionne 
            choix = [rd.randint(0,7), rd.randint(0,7)]

        return choix 

# -------------------------------------- FONCTIONS -----------------------------------------

def est_sur_othellier(choix):
    '''
    Vérifier que la case choisie par le joueur est bien sur un othellier 
    '''
    if choix[0]>7 or choix[0]<0 or choix[1]>7 or choix[0]<0 : 
        est_sur_othellier = False
    else : 
        est_sur_othellier = True

    return est_sur_othellier


