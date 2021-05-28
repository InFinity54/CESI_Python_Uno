import random
from uno.assets.colors.fore import ForeColor
from uno.assets.font import FontStyle
from uno.game.game import Game
from uno.game.pages.rules import rules
from uno.system.console import clear_console


game_data: Game


# Menu principal du Uno
def main_menu():
    print("MENU PRINCIPAL")
    print("Pour valider votre saisie, utilisez la touche \"Entrer\".")
    print("Choix possibles :")
    print(" - \"Nouvelle partie\"")
    print(" - \"Règles du jeu\"")
    print(" - \"Quitter le jeu\"")

    user_choice = input("Que souhaitez-vous faire ? ")

    if user_choice == "Nouvelle partie":
        clear_console()
        game()
        clear_console()
        main_menu()
    elif user_choice == "Règles du jeu":
        clear_console()
        rules()
        input("Appuyez sur une touche pour continuer...")
        clear_console()
        main_menu()
    elif user_choice == "Quitter le jeu":
        clear_console()
        print("Fermeture de Uno...")
        return
    else:
        clear_console()
        print("Choix non reconnu.")
        main_menu()


# Déroulement de la partie
def game():
    global game_data
    game_data = Game()
    print(FontStyle.Bold + "Début de la partie." + FontStyle.Normal)

    while game_data.get_player("irl").get_points() < 500 and game_data.get_player("ia").get_points() < 500:
        game_manche()
        clear_console()

    if game_data.get_player("irl").get_points() >= 500:
        print(ForeColor.Green + FontStyle.Bold + "Vous avez gagné la partie avec",
              str(game_data.get_player("irl").get_points()), "!" + FontStyle.Normal)

    if game_data.get_player("ia").get_points() >= 500:
        print(ForeColor.Red + FontStyle.Bold + "L'ordinateur a gagné la partie !" + FontStyle.Normal)

    input("Appuyez sur une touche pour revenir au menu principal...")
    return


# Déroulement d'une manche de la partie
def game_manche():
    global game_data
    game_data.new_manche()  # Passage à la nouvelle manche

    print(FontStyle.Bold + "Début de la manche " + str(game_data.get_manche()) + "." + FontStyle.Normal)
    print("Score actuel : Vous " + str(game_data.get_player("irl").get_points()) + " - "
          + str(game_data.get_player("ia").get_points()) + " Ordinateur")

    is_manche_finished = False

    while is_manche_finished is False:
        game_turn_player(False)
        clear_console()

        if len(game_data.get_player("irl").get_hand()) == 0:
            is_manche_finished = True
        else:
            game_turn_ia(False)
            input("Appuyez sur une touche pour continuer la partie...")
            clear_console()

            if len(game_data.get_player("ia").get_hand()) == 0:
                is_manche_finished = True

    if len(game_data.get_player("irl").get_hand()) == 0:
        print(ForeColor.Green + FontStyle.Bold + "Vous avez gagné cette manche !" + FontStyle.Normal)
        points_of_manche = game_manche_calc_points()
        game_data.get_player("irl").add_points(points_of_manche)
        print(ForeColor.Green + FontStyle.Bold + "Vous avez gagné", str(points_of_manche),
              "points pour cette manche !" + FontStyle.Normal)

    if len(game_data.get_player("ia").get_hand()) == 0:
        input(ForeColor.Red + FontStyle.Bold + "Vous avez perdu cette manche..." + FontStyle.Normal)
        points_of_manche = game_manche_calc_points()
        game_data.get_player("ia").add_points(points_of_manche)
        print(ForeColor.Red + FontStyle.Bold + "L'ordinateur a gagné", str(points_of_manche),
              "points pour cette manche." + FontStyle.Normal)

    print(FontStyle.Bold + "Fin de la manche " + str(game_data.get_manche()) + "." + FontStyle.Normal)
    input("Appuyez sur une touche pour continuer la partie...")


# Calcul des points de la manche
def game_manche_calc_points():
    global game_data
    total_points = 0

    # Quelque soit le joueur qui gagne, on récupère la main de son adversaire, et on calcul le nombre de points.
    # Les cartes numérotées définissent le nombre de points qu'elles donnent (entre 0 et 9 points).
    # Les +2, cartes d'inversion et cartes "Passe" donnent chacune 20 points.
    # Les cartes spéciales (+4 et Joker) donnent 50 points chacune.

    if len(game_data.get_player("irl").get_hand()) == 0:
        for card in game_data.get_player("ia").get_hand():
            card_data = card.split("_")
            if card_data[0] != "SPECIAL":
                if card_data[1] in ["+2", "INVERSION", "PASSE"]:
                    total_points = total_points + 20
                else:
                    total_points = total_points + int(card_data[1])
            else:
                total_points: total_points + 50

    if len(game_data.get_player("ia").get_hand()) == 0:
        for card in game_data.get_player("irl").get_hand():
            card_data = card.split("_")
            if card_data[0] != "SPECIAL":
                if card_data[1] in ["+2", "INVERSION", "PASSE"]:
                    total_points = total_points + 20
                else:
                    total_points = total_points + int(card_data[1])
            else:
                total_points: total_points + 50

    return total_points


# Traitement de la dernière carte jouée
# Renvoi True si le joueur peut jouer, False s'il doit passer son tour
def game_process_last_played_card(player_id):
    global game_data

    if game_data.get_deck().get_last_played_card().split("_")[1] == "+2" \
            and game_data.get_deck().get_last_played_card_executed() is False:
        if player_id == "irl":
            print(ForeColor.Red + "Vous devez piocher deux cartes." + FontStyle.Normal)
        else:
            print(ForeColor.Red + "L'ordinateur doit piocher deux cartes." + FontStyle.Normal)
        drawn_cards = 0

        while drawn_cards < 2:
            game_draw_card(player_id)
            drawn_cards = drawn_cards + 1

        game_data.get_deck().set_last_played_card_executed(True)
        return False
    elif game_data.get_deck().get_last_played_card().split("_")[1] == "+4" \
            and game_data.get_deck().get_last_played_card_executed() is False:
        if player_id == "irl":
            print(ForeColor.Red + "Vous devez piocher quatre cartes." + FontStyle.Normal)
        else:
            print(ForeColor.Red + "L'ordinateur doit piocher quatre cartes." + FontStyle.Normal)
        drawn_cards = 0

        while drawn_cards < 4:
            game_draw_card(player_id)
            drawn_cards = drawn_cards + 1

        game_data.get_deck().set_last_played_card_executed(True)
        return False
    elif game_data.get_deck().get_last_played_card().split("_")[1] == "PASSE" \
            and game_data.get_deck().get_last_played_card_executed() is False:
        game_data.get_deck().set_last_played_card_executed(True)
        return False
    else:
        game_data.get_deck().set_last_played_card_executed(True)
        return True


# Piocher une carte
def game_draw_card(player):
    global game_data
    selected_card = random.choice(game_data.get_deck().available_cards())
    game_data.get_player(player).draw_card(selected_card)
    game_data.get_player(player).set_has_said_uno(False)
    game_data.get_deck().remove_card(selected_card)

    if player == "irl":
        print("Vous avez pioché :", game_data.get_deck().get_displayable_card_name(selected_card, False))

    return selected_card


# Déroulement d'un tour pour le joueur
def game_turn_player(replay):
    global game_data
    if replay is False:
        print(FontStyle.Bold + "Début de votre tour." + FontStyle.Normal)
        print("Dernière carte jouée :",
              game_data.get_deck().get_displayable_card_name(game_data.get_deck().get_last_played_card(), True))

    # Traitement de la dernière carte jouée
    if game_process_last_played_card("irl"):
        # Si la dernière carte jouée n'empêche par le joueur d'effectuer son tour...
        # ..., on regarde ce qu'il a en main, et on lui propose de jouer (s'il le peut) ou de piocher
        cards_in_hand = ""

        for card in game_data.get_player("irl").get_sorted_hand():
            cards_in_hand = cards_in_hand + str(game_data.get_deck().get_displayable_card_name(card, False)) + " "

        print("Votre main actuelle :", cards_in_hand)

        selected_action = game_turn_player_menu()

        while selected_action is None:
            print(ForeColor.Red + "Une erreur est survenue durant la reconnaissance de l'action demandée.",
                  "Merci de réessayer." + FontStyle.Normal)
            selected_action = game_turn_player_menu()

        if selected_action == "PIOCHE":
            # Le joueur a choisi de piocher
            drawed_card = game_draw_card("irl")
            game_data.get_player("irl").set_has_said_uno(False)

            if is_card_can_be_played(drawed_card):
                if input("La carte piochée est jouable. Voulez-vous la jouer ? (Oui / Non) ") == "Oui":
                    if drawed_card.split("_")[0] == "SPECIAL":
                        selected_color = ""

                        while selected_color == "":
                            selected_color = input(
                                "Veuillez choisir la nouvelle couleur qui sera jouée (ROUGE / JAUNE / VERT / BLEU) : ")

                            if selected_color in ["ROUGE", "JAUNE", "VERT", "BLEU"]:
                                game_data.get_player("irl").play_card(drawed_card)
                                game_data.get_deck().set_last_played_card(drawed_card, selected_color)
                            else:
                                selected_color = ""
                                print(ForeColor.Red + "Cette couleur n'a pas été reconnue." + FontStyle.Normal)
                    else:
                        game_data.get_player("irl").play_card(drawed_card)
                        game_data.get_deck().set_last_played_card(drawed_card, drawed_card.split("_")[0])

                    if len(game_data.get_player("irl").get_hand()) == 1:
                        if input("Il ne vous reste plus qu'une carte. Voulez-vous dire UNO ? (Oui / Non) ") == "Oui":
                            print(ForeColor.Green + "UNO ! Il ne vous reste plus qu'une carte !" + FontStyle.Normal)
                            game_data.get_player("irl").set_has_said_uno(True)

                if drawed_card.split("_")[1] == "INVERSION":
                    print(ForeColor.Green + "Vous pouvez rejouer immédiatement." + FontStyle.Normal)
                    game_data.get_deck().set_last_played_card_executed(True)
                    game_turn_player(True)
            else:
                print(ForeColor.Red + "La carte piochée ne peut pas être jouée." + FontStyle.Normal)
                input("Appuyez sur une touche pour continuer la partie...")
        else:
            # Le joueur a choisi de jouer une carte
            if selected_action.split("_")[0] == "SPECIAL":
                selected_color = ""

                while selected_color == "":
                    selected_color = input(
                        "Veuillez choisir la nouvelle couleur qui sera jouée (ROUGE / JAUNE / VERT / BLEU) : ")

                    if selected_color in ["ROUGE", "JAUNE", "VERT", "BLEU"]:
                        game_data.get_player("irl").play_card(selected_action)
                        game_data.get_deck().set_last_played_card(selected_action, selected_color)
                    else:
                        selected_color = ""
                        print(ForeColor.Red + "Cette couleur n'a pas été reconnue." + FontStyle.Normal)
            else:
                game_data.get_player("irl").play_card(selected_action)
                game_data.get_deck().set_last_played_card(selected_action, selected_action.split("_")[0])

                if selected_action.split("_")[1] == "INVERSION":
                    print(ForeColor.Green + "Vous pouvez rejouer immédiatement." + FontStyle.Normal)
                    game_data.get_deck().set_last_played_card_executed(True)
                    game_turn_player(True)
    else:
        print(ForeColor.Red + "Vous passez votre tour." + FontStyle.Normal)
        input("Appuyez sur une touche pour continuer la partie...")

    if replay is False:
        print(FontStyle.Bold + "Fin de votre tour." + FontStyle.Normal)


# Menu de sélection de l'action pendant le tour du joueur
def game_turn_player_menu():
    global game_data

    # On vérifie si le joueur possède au moins une carte en main qui peut être jouée pendant ce tour.
    if is_player_can_play_a_card("irl"):
        # Si c'est le cas, on lui donne le choix entre jouer une carte ou piocher.
        print("Pour valider votre saisie, utilisez la touche \"Entrer\".")
        print("Choix possibles :")
        print(" - \"Jouer une carte\"")
        print(" - \"Piocher une carte\"")

        if is_player_can_say_uno("irl") is True and is_player_has_say_uno("irl") is False:
            print(" - \"Dire UNO\"")

        user_choice = input("Que souhaitez-vous faire ? ")

        if user_choice == "Piocher une carte":
            # Le joueur a choisi de piocher une carte.
            return "PIOCHE"
        elif user_choice == "Jouer une carte":
            # Le joueur souhaite jouer une carte. On lui demande donc de choisir laquelle.
            selected_card = ""

            while selected_card not in game_data.get_player("irl").get_hand():
                cards_in_hand = ""

                for card in game_data.get_player("irl").get_sorted_hand():
                    cards_in_hand = cards_in_hand + card + " "

                if selected_card != "":
                    # Si la carte sélectionné n'a pas été réinitialisée, cela signifie qu'il ne la possède pas.
                    # On prévient donc le joueur de son erreur.
                    print(ForeColor.Red + "Vous ne possédez pas cette carte dans votre main." + FontStyle.Normal)

                print("Pour valider votre saisie, utilisez la touche \"Entrer\".")
                print("Pour jouer une carte, veuillez saisir le nom de la carte que vous souhaitez jouer.")
                print("Cartes de votre main :", cards_in_hand)

                selected_card = input("Quelle carte souhaitez-vous jouer ? ")

                if not is_card_can_be_played(selected_card):
                    # Si la carte sélectionnée n'est pas jouable, on prévient l'utilisateur.
                    print(ForeColor.Red + "Vous ne pouvez pas jouer cette carte actuellement." + FontStyle.Normal)
                    selected_card = ""

            return selected_card
        elif user_choice == "Dire UNO":
            if len(game_data.get_player("irl").get_hand()) == 2:
                if game_data.get_player("irl").get_has_said_uno() is False:
                    print(ForeColor.Green + "UNO ! Il ne vous reste plus qu'une carte !" + FontStyle.Normal)
                    game_data.get_player("irl").set_has_said_uno(True)
                    return game_turn_player_menu()
                else:
                    print(ForeColor.Red + "Vous avez déjà dit UNO." + FontStyle.Normal)
                    return game_turn_player_menu()
            else:
                print(ForeColor.Red + "Vous ne pouvez pas dire UNO si vous avez plus de 2 cartes." + FontStyle.Normal)
                return game_turn_player_menu()
        else:
            print("Choix non reconnu.")
            game_turn_player_menu()
    else:
        # Si le joueur ne possède aucun carte jouable, on lui fait piocher une carte.
        print(ForeColor.Red + "Aucune carte de votre main ne peut être jouée actuellement." + FontStyle.Normal)
        print(ForeColor.Yellow + "Vous allez piocher une carte automatiquement." + FontStyle.Normal)
        return "PIOCHE"


# Vérifie si le joueur a dit Uno
def is_player_has_say_uno(player):
    global game_data

    if len(game_data.get_player(player).get_hand()) > 2:
        return True

    if len(game_data.get_player(player).get_hand()) == 2 and game_data.get_player(player).get_has_said_uno() is True:
        return True

    return False


# Vérifie si le joueur peut dire Uno
def is_player_can_say_uno(player):
    global game_data

    if len(game_data.get_player(player).get_hand()) == 2 and game_data.get_player(player).get_has_said_uno() is False:
        return True

    return False

# Vérification de la main du joueur pour savoir s'il peut jouer une carte ou non
# Renvoi True si le joueur à au moins une carte qu'il peut jouer en main, sinon renvoi False
def is_player_can_play_a_card(player_id):
    global game_data

    for card in game_data.get_player(player_id).get_hand():
        if is_card_can_be_played(card):
            return True

    return False


# Vérifie si une carte peut être jouée actuellement ou non
# Renvoi True si la carte peut être jouée maintenant, sinon renvoi False
def is_card_can_be_played(card):
    global game_data
    card_data = card.split("_")

    # Si la carte est une carte spéciale, elle peut être jouée n'importe quand.
    # On renvoi donc True directement.
    if card_data[0] == "SPECIAL":
        return True

    # Si la couleur de la carte correspond à celle de la dernière carte jouée, elle peut être jouée.
    # On renvoi donc True.
    if card_data[0] == game_data.get_deck().get_expected_color():
        return True

    # Si l'inscription sur la carte correspond à celle de la dernière carte jouée, elle peut être jouée.
    # On renvoi donc True directement.
    if card_data[1] == game_data.get_deck().get_last_played_card().split("_")[1]:
        return True

    # Si aucun des cas précédents n'a fonctionné, cela signifie que la carte ne peut pas être jouée.
    # On renvoi donc False.
    return False


# Déroulement d'un tour pour l'ordinateur
def game_turn_ia(replay):
    global game_data

    if replay is False:
        print(FontStyle.Bold + "Début du tour de l'ordinateur." + FontStyle.Normal)
        print("Dernière carte jouée :",
              game_data.get_deck().get_displayable_card_name(game_data.get_deck().get_last_played_card(), True))

    if len(game_data.get_player("irl").get_hand()) == 1 and game_data.get_player("irl").get_has_said_uno() is False:
        print(ForeColor.Red + "CONTRE-UNO ! Vous piochez deux cartes." + FontStyle.Normal)
        game_draw_card("irl")
        game_draw_card("irl")

    # Traitement de la dernière carte jouée
    if game_process_last_played_card("ia"):
        # Si la dernière carte jouée n'empêche par le joueur d'effectuer son tour, on regarde ce qu'il peut faire
        if is_player_can_play_a_card("ia"):
            # Le joueur peut visiblement jouer une carte, on regarde donc quelle est la meilleure carte jouable
            # Dans l'ordre, on vérifie et joue, si c'est possible, un +4, une carte de la couleur actuelle ou une carte
            # ayant la même description d'une couleur différente
            playable_card = ""

            if "SPECIAL_+4" in game_data.get_player("ia").get_hand():
                playable_card = "SPECIAL_+4"
            else:
                for card in game_data.get_player("ia").get_hand():
                    if card.startswith(game_data.get_deck().get_expected_color()):
                        playable_card = card
                        break

                if playable_card == "":
                    for card in game_data.get_player("ia").get_hand():
                        if card.split("_")[1] == game_data.get_deck().get_last_played_card().split("_")[1]:
                            playable_card = card
                            break

            if playable_card != "" and is_card_can_be_played(playable_card) \
                    and playable_card in game_data.get_player("ia").get_hand():
                playable_card_data = playable_card.split("_")
                # On a trouvé une carte jouable par l'IA
                if playable_card_data[0] == "SPECIAL":
                    selected_color = random.choice(["ROUGE", "JAUNE", "VERT", "BLEU"])
                    game_data.get_player("ia").play_card(playable_card)
                    game_data.get_deck().set_last_played_card(playable_card, selected_color)
                    print("L'ordinateur a joué :", game_data.get_deck().get_displayable_card_name(playable_card, False))
                else:
                    game_data.get_player("ia").play_card(playable_card)
                    game_data.get_deck().set_last_played_card(playable_card, playable_card.split("_")[0])
                    print("L'ordinateur a joué :", game_data.get_deck().get_displayable_card_name(playable_card, False))

                    if playable_card_data[1] == "INVERSION":
                        game_data.get_deck().set_last_played_card_executed(True)
                        print(ForeColor.Red + "L'ordinateur peut rejouer immédiatement." + FontStyle.Normal)
                        game_turn_ia(True)

                if len(game_data.get_player("ia").get_hand()) == 1:
                    print(ForeColor.Red + "UNO ! Il ne reste plus qu'une carte à l'ordinateur." + FontStyle.Normal)
                    game_data.get_player("ia").set_has_said_uno(True)
            else:
                # On n'a trouvé aucune carte jouable par l'IA, on lui fait donc piocher une carte
                drawed_card = game_draw_card("ia")
                game_data.get_player("ia").set_has_said_uno(False)

                if is_card_can_be_played(drawed_card):
                    # Si la carte peut être jouée par le joueur, elle est jouée automatiquement.
                    drawed_card_data = drawed_card.split("_")

                    if drawed_card_data[0] == "SPECIAL":
                        selected_color = random.choice(["ROUGE", "JAUNE", "VERT", "BLEU"])
                        game_data.get_player("ia").play_card(drawed_card)
                        game_data.get_deck().set_last_played_card(drawed_card, selected_color)
                        print("L'ordinateur a joué :",
                              game_data.get_deck().get_displayable_card_name(drawed_card, False))

                        if len(game_data.get_player("ia").get_hand()) == 1:
                            print(
                                ForeColor.Red + "UNO ! Il ne reste plus qu'une carte à l'ordinateur.", FontStyle.Normal)
                            game_data.get_player("ia").set_has_said_uno(True)
                    else:
                        game_data.get_player("ia").play_card(drawed_card)
                        game_data.get_deck().set_last_played_card(drawed_card, drawed_card.split("_")[0])
                        print("L'ordinateur a joué :",
                              game_data.get_deck().get_displayable_card_name(playable_card, False))

                        if len(game_data.get_player("ia").get_hand()) == 1:
                            print(
                                ForeColor.Red + "UNO ! Il ne reste plus qu'une carte à l'ordinateur.", FontStyle.Normal)
                            game_data.get_player("ia").set_has_said_uno(True)

                        if drawed_card_data[1] == "INVERSION":
                            game_data.get_deck().set_last_played_card_executed(True)
                            print(ForeColor.Red + "L'ordinateur peut rejouer immédiatement." + FontStyle.Normal)
                            game_turn_ia(True)

                else:
                    # Sinon, il passe son tour.
                    print(
                        ForeColor.Red + "La carte piochée par l'ordinateur ne peut pas être jouée." + FontStyle.Normal)
        else:
            # Le joueur ne possède aucune carte jouable, il pioche donc une carte.
            drawed_card = game_draw_card("ia")

            if is_card_can_be_played(drawed_card) and drawed_card in game_data.get_player("ia").get_hand():
                # Si la carte peut être jouée par le joueur, elle est jouée automatiquement.
                game_data.get_player("ia").play_card(drawed_card)
                game_data.get_deck().set_last_played_card(drawed_card, drawed_card.split("_")[0])

                if drawed_card.split("_")[0] == "SPECIAL":
                    selected_color = random.choice(["ROUGE", "JAUNE", "VERT", "BLEU"])
                    game_data.get_player("ia").play_card(drawed_card)
                    game_data.get_deck().set_last_played_card(drawed_card, selected_color)
                else:
                    game_data.get_player("ia").play_card(drawed_card)
                    game_data.get_deck().set_last_played_card(drawed_card, drawed_card.split("_")[0])

                print("L'ordinateur a joué :", game_data.get_deck().get_displayable_card_name(drawed_card, False))
            else:
                # Sinon, il passe son tour.
                print(ForeColor.Red + "La carte piochée par l'ordinateur ne peut pas être jouée." + FontStyle.Normal)
    else:
        print(ForeColor.Red + "L'ordinateur passe son tour." + FontStyle.Normal)

    if replay is False:
        print(FontStyle.Bold + "Fin du tour de l'ordinateur." + FontStyle.Normal)


# Programme principal
print("=========================================")
print("==                 UNO                 ==")
print("=========================================")
main_menu()
