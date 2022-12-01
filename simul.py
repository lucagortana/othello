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

def simul():
    profondeur = int(input("Quelle profondeur souhaitez-vous? "))
    nombre_partie = int(input("Combien de parties souhaitez-vous réaliser? "))
    type_algo = input("quel algo souhaitez-vous tester parmi minmax, alphaBeta, MCTS? ")
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
    data.to_excel('resultat_othello_{algo}.xlsx'.format(algo=type_algo), sheet_name='sheet1', index=False)

    # faire un histogramme à partir du dictionnaire prof_test : en abscisse les profondeurs 
    # pour chaque profondeur 2 barres : une pour "parties gagnées par A et l'autre parties gagnées par B 
    # # ou alors : une seule barre avec la difference gain A - B"
    print("--- %s seconds ---" % (time.time() - start_time))

simul()