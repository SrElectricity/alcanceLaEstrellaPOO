class UserInterface:
    @staticmethod
    def display_welcome_message():
        print("¡Bienvenido al juego Alcance la estrella!")

    @staticmethod
    def display_board(players):
        print("\nTablero:")
        for row in range(4):
            line = ""
            for col in range(5):
                pos = row * 5 + col
                if pos == players[0].position and pos == players[1].position:
                    marker = "J1/J2"
                elif pos == players[0].position:
                    marker = "J1"
                elif pos == players[1].position:
                    marker = "J2"
                else:
                    marker = f"{pos + 1:2}"
                line += f"{marker} | "
            print(line.rstrip(" | "))
            print("-" * len(line.rstrip(" | ")))
        print(f"Aciertos Jugador 1: {players[0].score} | Aciertos Jugador 2: {players[1].score}\n")

    @staticmethod
    def display_dice_roll(player_name, roll):
        print(f"{player_name} lanzó un {roll}")

    @staticmethod
    def display_question(text, options):
        print("\n" + text)
        for option in options:
            print(option)

    @staticmethod
    def get_user_input(prompt):
        return input(prompt)

    @staticmethod
    def display_correct_answer():
        print("¡Respuesta correcta!")

    @staticmethod
    def display_incorrect_answer(punishment):
        print(f"Respuesta incorrecta. Castigo: {punishment}")

    @staticmethod
    def display_next_turn(next_player_name):
        print(f"Es turno del {next_player_name}")

    @staticmethod
    def display_no_questions_message():
        print("No quedan preguntas disponibles.")

    @staticmethod
    def display_tie_message():
        print("--------¡Empate! Reiniciando el juego...--------")

    @staticmethod
    def display_winner_message(winner):
        print(f"--------¡Jugador {winner} ha ganado!--------")

    @staticmethod
    def display_score_winner_message(winner):
        print(f"--------¡Jugador {winner} ha ganado por aciertos!--------")

    @staticmethod
    def display_game_reset():
        print("Juego reiniciado.")
