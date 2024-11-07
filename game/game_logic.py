import random
import requests


class Player:
    def __init__(self, name: str, color: str):
        self.name = name
        self.position = 0
        self.score = 0
        self.color = color

    def move(self, steps: int):

        self.position += steps

    def apply_punishment(self, penalty):

        if penalty == "reset":
            self.position = 0
        else:
            self.position = max(0, self.position + penalty)

    def increment_score(self):

        self.score += 1


class Game:
    def __init__(self):

        self.players = [Player("Jugador 1", "red"), Player("Jugador 2", "blue")]
        self.current_player = 0
        self.game_over = False
        self.questions = []
        self.punishments = [("Retrocede 3 casillas", -3), ("Retrocede 2 casillas", -2), ("Vuelve a la casilla 1", "reset")]

    @staticmethod
    def obtener_pregunta(dificultad="easy"):

        url = f"https://opentdb.com/api.php?amount=1&type=multiple&difficulty={dificultad}"
        try:
            response = requests.get(url)
            data = response.json()

            if data['response_code'] == 0:
                pregunta_data = data['results'][0]
                texto = pregunta_data['question']
                opciones = pregunta_data['incorrect_answers'] + [pregunta_data['correct_answer']]
                respuesta_correcta = pregunta_data['correct_answer']
                random.shuffle(opciones)
                return texto, opciones, respuesta_correcta
            else:
                print("No se pudieron obtener preguntas.")
                return None, None, None
        except requests.RequestException:
            print("Error de conexión con la API de preguntas.")
            return None, None, None

    @staticmethod
    def roll_dice():

        return random.randint(1, 6)

    def move_player(self, steps):

        player = self.players[self.current_player]
        new_position = min(player.position + steps, 19)
        player.position = new_position

    def apply_penalty(self):

        player = self.players[self.current_player]
        penalty, movement = random.choice(self.punishments)
        player.apply_punishment(movement)
        return penalty

    def check_answer(self, seleccion, respuesta_correcta):
        player = self.players[self.current_player]
        if seleccion == respuesta_correcta:
            player.increment_score()
            return True
        return False

    def switch_player(self):

        self.current_player = 1 - self.current_player

    def get_winner(self):

        scores = [player.score for player in self.players]
        if scores[0] > scores[1]:
            return 0
        elif scores[1] > scores[0]:
            return 1
        return None
