# Règles du jeu
# Règles complètes disponibles sur https://fr.wikipedia.org/wiki/Uno#R%C3%A8gles_du_jeu
def rules():
    print("RÈGLES DU JEU")
    print("Le but du jeu est d'être le premier joueur à ne plus avoir de cartes en main.")
    print("A la fin de chaque manche, les cartes restantes aux autres joueurs sont cumulées au score du gagnant de la"
          "manche.")
    print("Les manches s'enchaînent jusqu'à ce que l'un des joueurs atteigne 500 points.",
          "Dans ce cas, le joueur gagne la partie.")
    print("Les points donnés par les cartes sont calculés de cette manière :")
    print(" - Les cartes numérotées de 0 à 9 donnent le même nombre de points que le nombre qu'elles représentent.")
    print(" - Les cartes \"+2\" donnent chacune 20 points.")
    print(" - Les cartes \"Inversion\" donnent chacune 20 points.")
    print(" - Les cartes \"Joker\" donnent chacune 50 points.")
    print(" - Les cartes \"+4\" donnent chacune 50 points.")