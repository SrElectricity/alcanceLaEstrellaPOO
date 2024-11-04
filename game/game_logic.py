class Game:
    def __init__(self):
        self.board = list(range(1, 21))
        self.player_positions = [0, 0]  # Posiciones de los jugadores 1 y 2
        self.player_scores = [0, 0]  # Puntuaciones de los jugadores 1 y 2
        self.current_player = 0  # Jugador actual (0 para jugador 1, 1 para jugador 2)

    def roll_dice(self):
        import random
        return random.randint(1, 6)

    def move_player(self, steps):
        new_position = self.player_positions[self.current_player] + steps
        if new_position >= len(self.board):
            new_position = len(self.board) - 1
        self.player_positions[self.current_player] = new_position
        return new_position

    def check_answer(self, answer, correct_answer):
        if answer == correct_answer:
            self.player_scores[self.current_player] += 1
            return True
        return False

    def switch_player(self):
        self.current_player = 1 - self.current_player  # Cambia de jugador
