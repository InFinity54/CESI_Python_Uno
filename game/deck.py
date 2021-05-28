from assets.colors.fore import ForeColor
from assets.font import FontStyle


class Deck:
    # Initialisation de la pioche
    def __init__(self):
        # Les valeurs proviennent de la règle du jeu
        self.__card_list = {
            # Cartes rouges
            "ROUGE_0": 1, "ROUGE_1": 2, "ROUGE_2": 2, "ROUGE_3": 2, "ROUGE_4": 2, "ROUGE_5": 2, "ROUGE_6": 2, "ROUGE_7": 2,
            "ROUGE_8": 2, "ROUGE_9": 2, "ROUGE_+2": 2, "ROUGE_INVERSION": 2, "ROUGE_PASSE": 2,
            # Cartes jaunes
            "JAUNE_0": 1, "JAUNE_1": 2, "JAUNE_2": 2, "JAUNE_3": 2, "JAUNE_4": 2, "JAUNE_5": 2, "JAUNE_6": 2,
            "JAUNE_7": 2, "JAUNE_8": 2, "JAUNE_9": 2, "JAUNE_+2": 2, "JAUNE_INVERSION": 2, "JAUNE_PASSE": 2,
            # Cartes vertes
            "VERT_0": 1, "VERT_1": 2, "VERT_2": 2, "VERT_3": 2, "VERT_4": 2, "VERT_5": 2, "VERT_6": 2,
            "VERT_7": 2, "VERT_8": 2, "VERT_9": 2, "VERT_+2": 2, "VERT_INVERSION": 2, "VERT_PASSE": 2,
            # Cartes bleues
            "BLEU_0": 1, "BLEU_1": 2, "BLEU_2": 2, "BLEU_3": 2, "BLEU_4": 2, "BLEU_5": 2, "BLEU_6": 2, "BLEU_7": 2,
            "BLEU_8": 2, "BLEU_9": 2, "BLEU_+2": 2, "BLEU_INVERSION": 2, "BLEU_PASSE": 2,
            # Cartes spéciales
            "SPECIAL_JOKER": 4, "SPECIAL_+4": 4
        }
        self.__last_played_card = ""
        self.__expected_color = ""
        self.__last_played_card_executed = False

    # Récupération de la liste des cartes (debug uniquement)
    def get_card_list(self):
        return self.__card_list

    # Renvoi la couleur attendue pour la prochaine carte
    def get_expected_color(self):
        return self.__expected_color

    # Défini la couleur attendue pour la prochaine carte
    def set_expected_color(self, color):
        self.__expected_color = color

    # Renvoi la dernière carte jouée
    def get_last_played_card(self):
        return self.__last_played_card

    # Détermine la dernière carte jouée
    def set_last_played_card(self, card, color):
        self.__last_played_card = card
        self.__expected_color = color
        self.__last_played_card_executed = False

    # Renvoi True si la dernière carte posée a été traitée, False dans le cas inverse
    def get_last_played_card_executed(self):
        return self.__last_played_card_executed

    # Change l'état du traitement de la dernière carte jouée
    def set_last_played_card_executed(self, state):
        self.__last_played_card_executed = state

    # Renvoi de la liste des cartes encore disponibles dans la pioche
    def available_cards(self):
        cards = []
        for card in self.__card_list.keys():
            if self.__card_list[card] > 0:
                cards.append(card)
        return cards

    # Retire un exemplaire d'une carte de la pioche
    def remove_card(self, card):
        self.__card_list[card] = self.__card_list[card] - 1
        return

    # Renvoi un nom de carte mis en forme pour affichage
    def get_displayable_card_name(self, card, is_last_played_card):
        card_data = card.split("_")

        if is_last_played_card:
            if card_data[0] == "ROUGE":
                return ForeColor.Red + card_data[1] + FontStyle.Normal
            elif card_data[0] == "JAUNE":
                return ForeColor.Yellow + card_data[1] + FontStyle.Normal
            elif card_data[0] == "VERT":
                return ForeColor.Green + card_data[1] + FontStyle.Normal
            elif card_data[0] == "BLEU":
                return ForeColor.Blue + card_data[1] + FontStyle.Normal
            else:
                if self.__expected_color == "ROUGE" and self.__last_played_card.split("_")[0] == "SPECIAL":
                    return ForeColor.Red + card_data[1] + FontStyle.Normal
                elif self.__expected_color == "JAUNE" and self.__last_played_card.split("_")[0] == "SPECIAL":
                    return ForeColor.Yellow + card_data[1] + FontStyle.Normal
                elif self.__expected_color == "VERT" and self.__last_played_card.split("_")[0] == "SPECIAL":
                    return ForeColor.Green + card_data[1] + FontStyle.Normal
                elif self.__expected_color == "BLEU" and self.__last_played_card.split("_")[0] == "SPECIAL":
                    return ForeColor.Blue + card_data[1] + FontStyle.Normal
        else:
            if card_data[0] == "ROUGE":
                return ForeColor.Red + card_data[1] + FontStyle.Normal
            elif card_data[0] == "JAUNE":
                return ForeColor.Yellow + card_data[1] + FontStyle.Normal
            elif card_data[0] == "VERT":
                return ForeColor.Green + card_data[1] + FontStyle.Normal
            elif card_data[0] == "BLEU":
                return ForeColor.Blue + card_data[1] + FontStyle.Normal
            else:
                return card_data[1]

    # Réinitialise la pioche pour une nouvelle manche
    def reset(self):
        self.__init__()
        return
