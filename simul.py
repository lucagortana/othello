import time
import numpy as np 
from partie import partie 
from MinMax import MinMax
from alphaBeta import alphaBeta
from MCTS import MCTS
import pandas as pd



#-------------------------------------- FIGHTS DES ALGOS -----------------------------
start_time = time.time()

# on va faire affronter 2 ordinateurs au cours de 10 parties. 
# Un avec Minmax, l'autre en choix random.
# on va voir qui gagne le plus de parties. 

def position(element, liste):
    i = -1
    for elem in liste:
        i += 1
        if elem == element:
            return i
    

def simul():
    type_algo = input("quel algo souhaitez-vous tester parmi minmax, alphaBeta, MCTS? ")
    if type_algo == "MCTS":
        combine_ = input("Voulez-vous faire varier la profondeur et la valeur C en même temps? [y/n]: ")
        choix_c = []
        if combine_ == "y":
            print("Donnez différentes valeurs de C:\n")
            while True:
                d = input("--> ").strip()
                if d == '':
                    break
                else:
                    try:
                        choix_c.append(int(d))
                    except ValueError:
                        try:
                            choix_c.append(float(d))
                        except ValueError:
                            choix_c.append(d)
            profondeur = int(input("Jusqu'à quelle profondeur souhaitez-vous aller? "))
        else:
            choix_var = input("Ok pas de galère, que faisons-nous varier? [c/p]: ")
            if choix_var == "c":
                print("Donnez différentes valeurs de C:\n")
                while True:
                    d = input("--> ").strip()
                    if d == '':
                        break
                    else:
                        try:
                            choix_c.append(int(d))
                        except ValueError:
                            try:
                                choix_c.append(float(d))
                            except ValueError:
                                choix_c.append(d)
                profondeur = int(input("Quelle profondeur souhaitez-vous? "))
            else:
                profondeur = int(input("Jusqu'à quelle profondeur souhaitez-vous aller? "))
    
    else:
        profondeur = int(input("Jusqu'à quelle profondeur souhaitez-vous aller? "))
    
    nombre_partie = int(input("Combien de parties souhaitez-vous réaliser? "))
    
    if type_algo == "MCTS":
        if combine_ == "n":
            if choix_var == "p":
                prof_test=np.zeros([profondeur, 3])

                for p in range(1, profondeur+1):
                    print('nous en sommes à la profondeur {p}'.format(p=p))
                    gain_A = 0
                    gain_B = 0
                    egalite = 0

                    #for c in range(len(choix_c)):
                        
                    for nb_partie in range(nombre_partie):
                        print('nb_partie=', nb_partie)
                        joueur_A = None
                        joueur_B = type_algo
                        if nb_partie%2 ==0: # une partie sur 2 c'est le joueur A qui commence 
                            print('Joueur_A commence')
                            #gagnant = partie(False, None, 1, False, joueur_B, p) 
                            gagnant = partie(joueur1 = False , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = joueur_B, prof_algo_j2 = p)
                            # rappel des paramètres : partie(joueur1 = True , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = None, prof_algo_j2 = 3)
                            
                            if gagnant == 1:
                                gain_A += 1
                            elif gagnant == 2:
                                gain_B += 1
                            else:
                                egalite += 1 
                        if nb_partie%2 !=0: # une partie sur 2 c'est le joueur B qui commence 
                            print('Joueur_B commence')
                            gagnant = partie(False, joueur_B,p, False, None, 1)
                            
                            if gagnant == 1:
                                gain_B += 1
                            elif gagnant == 2:
                                gain_A += 1
                            else:
                                egalite += 1 

                    prof_test[p-1, 0] = gain_B  / nombre_partie #pourcentage partie gagnée
                    prof_test[p-1, 1] = gain_A  / nombre_partie #pourcentage partie perdue
                    prof_test[p-1, 2] = egalite  / nombre_partie #pourcentage partie égalité
            
                list1 = [i for i in range(1, profondeur+1)]
                list2 = prof_test[:,0]
                list3 = prof_test[:,1]
                list4 = prof_test[:,2]
                
                col1 = "Profondeur"
                col2 = "Gain Algo"
                col3 = "Perte Algo"
                col4 = "Egalité"
                data = pd.DataFrame({col1:list1,col2:list2, col3:list3, col4:list4})
                data.to_excel('resultats_simulations/resultat_othello_{algo}_nbp_{nb}.xlsx'.format(algo=type_algo, nb=nombre_partie), sheet_name='sheet1', index=False)

            else:
                prof_test=np.zeros([len(choix_c), 3])
                for c in choix_c:
                    print('nous en sommes à la valeur C = {c}'.format(c=c))
                    gain_A = 0
                    gain_B = 0
                    egalite = 0
                        
                    for nb_partie in range(nombre_partie):
                        print('nb_partie=', nb_partie)
                        joueur_A = None
                        joueur_B = type_algo
                        if nb_partie%2 ==0: # une partie sur 2 c'est le joueur A qui commence 
                            print('Joueur_A commence')
                            #gagnant = partie(False, None, 1, False, joueur_B, p) 
                            gagnant = partie(joueur1 = False , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = joueur_B, prof_algo_j2 = profondeur, valeur_c = c)
                            # rappel des paramètres : partie(joueur1 = True , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = None, prof_algo_j2 = 3)
                            
                            if gagnant == 1:
                                gain_A += 1
                            elif gagnant == 2:
                                gain_B += 1
                            else:
                                egalite += 1 
                        if nb_partie%2 !=0: # une partie sur 2 c'est le joueur B qui commence 
                            print('Joueur_B commence')
                            gagnant = partie(joueur1 = False , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = joueur_B, prof_algo_j2 = profondeur, valeur_c = c)
                            
                            if gagnant == 1:
                                gain_B += 1
                            elif gagnant == 2:
                                gain_A += 1
                            else:
                                egalite += 1 

                    prof_test[position(c, choix_c), 0] = gain_B  / nombre_partie #pourcentage partie gagnée
                    prof_test[position(c, choix_c), 1] = gain_A  / nombre_partie #pourcentage partie perdue
                    prof_test[position(c, choix_c), 2] = egalite  / nombre_partie #pourcentage partie égalité

                list2 = prof_test[:,0]
                list3 = prof_test[:,1]
                list4 = prof_test[:,2]
                list5 = [profondeur] + (len(choix_c)-1)*["-"]
                
                col1 = "Valeur C"
                col2 = "Gain Algo"
                col3 = "Perte Algo"
                col4 = "Egalité"
                col5 = "Profondeur"

                data = pd.DataFrame({col1:choix_c,col2:list2, col3:list3, col4:list4, col5:list5})
                data.to_excel('resultats_simulations/resultat_othello_{algo}_nbp_{nb}.xlsx'.format(algo=type_algo, nb=nombre_partie), sheet_name='sheet1', index=False)

        else:
            prof_test=np.zeros([profondeur, len(choix_c)])

            for p in range(1, profondeur+1):
                print('nous en sommes à la profondeur {p}'.format(p=p))

                for c in choix_c:
                    print('Nous en sommes à la valeur c = ', c)
                    gain_A = 0
                    gain_B = 0
                    egalite = 0

                    for nb_partie in range(nombre_partie):
                        print('nb_partie=', nb_partie)
                        joueur_A = None
                        joueur_B = type_algo
                        if nb_partie%2 ==0: # une partie sur 2 c'est le joueur A qui commence 
                            print('Joueur_A commence')
                            #gagnant = partie(False, None, 1, False, joueur_B, p) 
                            gagnant = partie(joueur1 = False , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = joueur_B, prof_algo_j2 = p, valeur_c = c)
                            # rappel des paramètres : partie(joueur1 = True , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = None, prof_algo_j2 = 3)
                            
                            if gagnant == 1:
                                gain_A += 1
                            elif gagnant == 2:
                                gain_B += 1
                            else:
                                egalite += 1 
                        if nb_partie%2 !=0: # une partie sur 2 c'est le joueur B qui commence 
                            print('Joueur_B commence')
                            gagnant = partie(joueur1 = False , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = joueur_B, prof_algo_j2 = p, valeur_c = c)
                            
                            if gagnant == 1:
                                gain_B += 1
                            elif gagnant == 2:
                                gain_A += 1
                            else:
                                egalite += 1 

                    prof_test[p-1, position(c, choix_c)] = gain_B  / nombre_partie #pourcentage partie gagnée

            col1 = "Profondeur"
            dico_results = {col1:[i for i in range(1, profondeur+1)]}
            for i in range(len(choix_c)):
                list_ = prof_test[:, i]
                col_ = "{c}".format(c=choix_c[i])
                dico_results[col_] = list_

            data = pd.DataFrame(dico_results)
            data.to_excel('resultats_simulations/resultat_othello_{algo}_nbp_{nb}.xlsx'.format(algo=type_algo, nb=nombre_partie), sheet_name='sheet1', index=False)

    else:
        prof_test=np.zeros([profondeur, 3])

        for p in range(1, profondeur+1):
            print('nous en sommes à la profondeur {p}'.format(p=p))
            gain_A = 0
            gain_B = 0
            egalite = 0
                
            for nb_partie in range(nombre_partie):
                print('nb_partie=', nb_partie)
                joueur_A = None
                joueur_B = type_algo
                if nb_partie%2 ==0: # une partie sur 2 c'est le joueur A qui commence 
                    print('Joueur_A commence')
                    #gagnant = partie(False, None, 1, False, joueur_B, p) 
                    gagnant = partie(joueur1 = False , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = joueur_B, prof_algo_j2 = p)
                    # rappel des paramètres : partie(joueur1 = True , algo_j1 = None, prof_algo_j1 = 3, joueur2 = False, algo_j2 = None, prof_algo_j2 = 3)
                    
                    if gagnant == 1:
                        gain_A += 1
                    elif gagnant == 2:
                        gain_B += 1
                    else:
                        egalite += 1 
                if nb_partie%2 !=0: # une partie sur 2 c'est le joueur B qui commence 
                    print('Joueur_B commence')
                    gagnant = partie(False, joueur_B,p, False, None, 1)
                    
                    if gagnant == 1:
                        gain_B += 1
                    elif gagnant == 2:
                        gain_A += 1
                    else:
                        egalite += 1 

            prof_test[p-1, 0] = gain_B  / nombre_partie #pourcentage partie gagnée
            prof_test[p-1, 1] = gain_A  / nombre_partie #pourcentage partie perdue
            prof_test[p-1, 2] = egalite  / nombre_partie #pourcentage partie égalité

        list1 = [i for i in range(1, profondeur+1)]
        list2 = prof_test[:,0]
        list3 = prof_test[:,1]
        list4 = prof_test[:,2]
        
        col1 = "Profondeur"
        col2 = "Gain Algo"
        col3 = "Perte Algo"
        col4 = "Egalité"


        data = pd.DataFrame({col1:list1,col2:list2, col3:list3, col4:list4})
        data.to_excel('resultats_simulations/resultat_othello_{algo}_nbp_{nb}.xlsx'.format(algo=type_algo, nb=nombre_partie), sheet_name='sheet1', index=False)

    # faire un histogramme à partir du dictionnaire prof_test : en abscisse les profondeurs 
    # pour chaque profondeur 2 barres : une pour "parties gagnées par A et l'autre parties gagnées par B 
    # # ou alors : une seule barre avec la difference gain A - B"
    print("--- %s seconds ---" % (time.time() - start_time))

simul()