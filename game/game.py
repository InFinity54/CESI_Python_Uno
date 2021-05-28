from game.deck import Deck
from game.player import Player
import random


class Game:
    # Initialisation de la partie
    def __init__(self):
        self.__game_deck = Deck()
        self.__game_players = {
            "irl": Player("Joueur", False),
            "ia": Player("IA", True)
        }
        self.__game_manche = 0
        return

    # Renvoi la pioche restante de la partie
    def get_deck(self):
        return self.__game_deck

    # Renvoi un joueur en fonction de son identifiant
    def get_player(self, player_id):
        return self.__game_players[player_id]

    # Renvoi le numéro de la manche actuelle
    def get_manche(self):
        return self.__game_manche

    # Prépare la partie à une nouvelle manche
    def new_manche(self):
        self.__game_manche = self.__game_manche + 1  # Augmentation du numéro de manche de 1
        self.__game_deck.reset()  # Réinitialisation de la pioche

        # Réinitialisation des mains des joueurs
        for player in self.__game_players.keys():
            self.__game_players[player].set_has_said_uno(False)

            for card in self.__game_players[player].get_hand():
                self.__game_players[player].get_hand().remove(card)

        # Distribution des cartes aux joueurs
        for player in self.__game_players.keys():
            while len(self.__game_players[player].get_hand()) < 7:
                selected_card = random.choice(self.__game_deck.available_cards())
                self.__game_players[player].draw_card(selected_card)
                self.__game_deck.remove_card(selected_card)

        # Démarrage de la manche sur l'une des cartes restantes dans la pioche
        selected_card = random.choice(self.__game_deck.available_cards())
        self.__game_deck.remove_card(selected_card)
        color = selected_card.split("_")[0]

        if color == "SPECIAL":
            color = random.choice(["ROUGE", "JAUNE", "VERT", "BLEU"])

        self.__game_deck.set_last_played_card(selected_card, color)

        return