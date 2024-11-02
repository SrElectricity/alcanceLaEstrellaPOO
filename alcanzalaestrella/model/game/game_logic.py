import random

from alcanzalaestrella.model.game.interface.user_interface import UserInterface


class Question:
    def __init__(self, text, options, correct_answer):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer

    def ask(self):
        UserInterface.display_question(self.text, self.options)

    def check_answer(self, chosen):
        return chosen == self.correct_answer


class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.score = 0

    def move(self, spaces):
        self.position += spaces

    def apply_punishment(self, punishment):
        if "retrocede 3" in punishment:
            self.position = max(0, self.position - 3)
        elif "retrocede 2" in punishment:
            self.position = max(0, self.position - 2)
        elif "vuelve al inicio" in punishment:
            self.position = 0

    def increment_score(self):
        self.score += 1


class Game:
    def __init__(self):
        self.questions = [
            Question("¿Capital de Francia?", ["a) Madrid", "b) Berlín", "c) París"], "c"),
            Question("¿2 + 2 es igual a?", ["a) 3", "b) 4", "c) 5"], "b"),
            Question("¿Color del cielo?", ["a) Verde", "b) Azul", "c) Rojo"], "b"),
            Question("¿Capital de España?", ["a) Madrid", "b) Lisboa", "c) París"], "a"),
            Question("¿Planeta más cercano al Sol?", ["a) Venus", "b) Marte", "c) Mercurio"], "c"),
            Question("¿Animal más rápido del mundo?", ["a) Tigre", "b) Guepardo", "c) Halcón"], "b"),
            Question("¿País con más habitantes?", ["a) China", "b) India", "c) EE.UU."], "a"),
            Question("¿Qué es H2O?", ["a) Agua", "b) Oxígeno", "c) Hidrógeno"], "a"),
            Question("¿Cuántos continentes hay?", ["a) 6", "b) 7", "c) 8"], "b"),
            Question("¿Qué es el Everest?", ["a) Río", "b) Montaña", "c) Valle"], "b"),
            Question("¿Capital de Italia?", ["a) Roma", "b) Atenas", "c) Lisboa"], "a"),
            Question("¿Cuál es el océano más grande?", ["a) Atlántico", "b) Índico", "c) Pacífico"], "c"),
        ]
        self.punishments = ["Puente: retrocede 3 casillas", "Resbalón: retrocede 2 casillas", "Calavera: vuelve al inicio"]
        self.players = [Player("Jugador 1"), Player("Jugador 2")]
        self.current_player_index = 0
        self.used_questions = []
        self.casilla_punishment = {i: random.choice(self.punishments) for i in range(1, 20)}
        random.shuffle(self.questions)

    def start(self):
        UserInterface.display_welcome_message()
        self.print_board()
        while True:
            self.roll_dice()

    def print_board(self):
        UserInterface.display_board(self.players)

    def roll_dice(self):
        dice_roll = random.randint(1, 6)
        current_player = self.players[self.current_player_index]
        UserInterface.display_dice_roll(current_player.name, dice_roll)
        self.move_player(dice_roll)

    def move_player(self, spaces):
        current_player = self.players[self.current_player_index]
        new_position = current_player.position + spaces

        if new_position >= 19:
            current_player.position = 19
            self.check_game_over()
        else:
            current_player.move(spaces)
            self.ask_question()

    def ask_question(self):
        available_questions = [q for q in self.questions if q not in self.used_questions]

        if not available_questions:
            UserInterface.display_no_questions_message()
            self.check_game_over()
            return

        question = random.choice(available_questions)
        self.used_questions.append(question)
        question.ask()

        answer = UserInterface.get_user_input("Tu respuesta (a/b/c): ").strip().lower()
        self.check_answer(answer, question)

    def check_answer(self, chosen, question):
        current_player = self.players[self.current_player_index]
        if question.check_answer(chosen):
            current_player.increment_score()
            UserInterface.display_correct_answer()
        else:
            punishment = self.casilla_punishment[current_player.position]
            UserInterface.display_incorrect_answer(punishment)
            current_player.apply_punishment(punishment)

        self.print_board()
        self.current_player_index = (self.current_player_index + 1) % 2
        UserInterface.display_next_turn(self.players[self.current_player_index].name)

    def check_game_over(self):
        self.print_board()
        if self.players[0].position == 19 and self.players[1].position == 19:
            UserInterface.display_tie_message()
            self.reset_game()
        elif self.players[0].position == 19:
            UserInterface.display_winner_message(1)
            UserInterface.get_user_input("Presiona Enter para reiniciar el juego.")
            self.reset_game()
        elif self.players[1].position == 19:
            UserInterface.display_winner_message(2)
            UserInterface.get_user_input("Presiona Enter para reiniciar el juego.")
            self.reset_game()
        elif len(self.used_questions) == len(self.questions):
            if self.players[0].score == self.players[1].score:
                UserInterface.display_tie_message()
                self.reset_game()
            else:
                winner = 1 if self.players[0].score > self.players[1].score else 2
                UserInterface.display_score_winner_message(winner)
                UserInterface.get_user_input("Presiona Enter para reiniciar el juego.")
                self.reset_game()

    def reset_game(self):
        for player in self.players:
            player.position = 0
            player.score = 0
        self.current_player_index = 0
        self.used_questions = []
        self.casilla_punishment = {i: random.choice(self.punishments) for i in range(1, 20)}

        UserInterface.display_game_reset()
        self.print_board()


# Inicialización del juego
game = Game()
game.start()
