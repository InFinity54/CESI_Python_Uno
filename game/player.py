class Player:
    # Initialisation du joueur
    def __init__(self, name, ai):
        self.__name = name
        self.__is_ai = ai
        self.__points = 0
        self.__hand = []
        self.__has_said_uno = False

        return

    # Renvoi le nom du joueur
    def get_name(self):
        return self.__name

    # Renvoi le nombre de points actuel du joueur
    def get_points(self):
        return self.__points

    # Ajoute des points au joueur
    def add_points(self, points_to_add):
        self.__points = self.__points + points_to_add
        return

    # Renvoi la main actuelle du joueur
    def get_hand(self):
        return self.__hand

    # Renvoi la main actuelle du joueur, triée par couleur et valeur
    def get_sorted_hand(self):
        order_colors = ["SPECIAL", "ROUGE", "JAUNE", "VERT", "BLEU"]
        order_value = ["+4", "JOKER", "INVERSION", "PASSE", "+2", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0"]

        # Code du tri trouvé sur https://stackoverflow.com/a/33900835 puis adapté
        sorted_hand = sorted(self.__hand,
                             key=lambda x: (order_colors.index(x.split("_")[0]), order_value.index(x.split("_")[1])))
        return sorted_hand

    # Ajoute une carte à la main du joueur
    def draw_card(self, card):
        self.__hand.append(card)
        return

    # Retire une carte de la main du joueur
    def play_card(self, card):
        if card in self.__hand:
            self.__hand.remove(card)
        return

    # Renvoi False si le joueur n'a pas dit Uno, True s'il l'a dit
    def get_has_said_uno(self):
        return self.__has_said_uno

    # Défini si le joueur a dit Uno ou non
    def set_has_said_uno(self, state):
        self.__has_said_uno = state