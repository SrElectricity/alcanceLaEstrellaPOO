import tkinter as tk
from tkinter import messagebox, colorchooser
from game.game_logic import Game
import random


class GraphicInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Alcanza la Estrella")
        self.game = Game()

        self.jugador1 = self.game.players[0]
        self.jugador2 = self.game.players[1]

        self.tablero_labels = []
        self.puntaje_label = None
        self.dado_label = None
        self.tablero_frame = None
        self.dado = 0

        self.crear_interfaz()
        self.actualizar_tablero()

    def crear_interfaz(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        self.tablero_frame = tk.Frame(main_frame)
        self.tablero_frame.grid(row=0, column=1, padx=10)

        self.tablero_labels = []
        for i in range(20):
            label = tk.Label(self.tablero_frame, text=f"{i + 1}", borderwidth=1, relief="solid", width=3, height=2)
            label.grid(row=i // 5, column=i % 5)
            self.tablero_labels.append(label)

        self.puntaje_label = tk.Label(self.root,
                                      text=f"Puntajes: Jugador 1 - {self.jugador1.score} | Jugador 2 - {self.jugador2.score}")
        self.puntaje_label.pack()

        self.dado_label = tk.Label(self.root, text="🎲", font=("Helvetica", 32))
        self.dado_label.pack(pady=10)
        self.dado_label.bind("<Button-1>", lambda e: self.iniciar_animacion_dado())

        tk.Button(self.root, text="Elegir color Jugador 1", command=self.elegir_color_jugador1).pack(pady=5)
        tk.Button(self.root, text="Elegir color Jugador 2", command=self.elegir_color_jugador2).pack(pady=5)

    def elegir_color_jugador1(self):
        color = colorchooser.askcolor(title="Elige el color para Jugador 1")[1]
        if color:
            self.jugador1.color = color
            self.actualizar_tablero()

    def elegir_color_jugador2(self):
        color = colorchooser.askcolor(title="Elige el color para Jugador 2")[1]
        if color:
            self.jugador2.color = color
            self.actualizar_tablero()

    def mostrar_pregunta(self):
        if self.game.game_over:
            return

        pregunta_texto, opciones, respuesta_correcta = self.game.obtener_pregunta()

        if pregunta_texto is None:
            messagebox.showinfo("Error", "No se pudo obtener una pregunta.")
            return

        pregunta_window = tk.Toplevel(self.root)
        pregunta_window.title("Pregunta de Trivia")

        tk.Label(pregunta_window, text=pregunta_texto).pack(pady=10)

        def verificar_respuesta(seleccion):
            correcta = (seleccion == respuesta_correcta)
            pregunta_window.destroy()
            if correcta:
                messagebox.showinfo("Correcto", "¡Respuesta correcta!")
                self.game.check_answer(seleccion, respuesta_correcta)
                self.actualizar_puntaje()
                self.game.move_player(self.dado)
                self.verificar_victoria()
            else:
                castigo = self.game.apply_penalty()
                messagebox.showinfo("Incorrecto", f"Respuesta incorrecta. {castigo}")
            self.actualizar_tablero()
            self.actualizar_puntaje()
            self.game.switch_player()

        for opcion in opciones:
            tk.Button(pregunta_window, text=opcion, command=lambda opt=opcion: verificar_respuesta(opt)).pack(pady=5)

    def iniciar_animacion_dado(self):
        if self.game.game_over:
            return
        self.dado = random.randint(1, 6)
        messagebox.showinfo("Dado", f"Lanzaste un {self.dado}")
        self.mostrar_pregunta()

    def actualizar_tablero(self):
        for i, label in enumerate(self.tablero_labels):
            label.config(bg="SystemButtonFace", text=str(i + 1))

        pos_jug1 = self.jugador1.position
        pos_jug2 = self.jugador2.position

        if pos_jug1 == pos_jug2 and pos_jug1 < 20:
            self.tablero_labels[pos_jug1].config(bg="purple", text="1 & 2")
        else:
            if pos_jug1 < 20:
                self.tablero_labels[pos_jug1].config(bg=self.jugador1.color, text="1")
            if pos_jug2 < 20:
                self.tablero_labels[pos_jug2].config(bg=self.jugador2.color, text="2")

    def verificar_victoria(self):
        if self.jugador1.position == 19:
            self.cambiar_color_tablero(self.jugador1.color)
            messagebox.showinfo("Victoria", "¡Jugador 1 ha llegado a la meta y ganó el juego!")
            self.game.game_over = True
        elif self.jugador2.position == 19:
            self.cambiar_color_tablero(self.jugador2.color)
            messagebox.showinfo("Victoria", "¡Jugador 2 ha llegado a la meta y ganó el juego!")
            self.game.game_over = True

    def cambiar_color_tablero(self, color):
        for label in self.tablero_labels:
            label.config(bg=color)

    def actualizar_puntaje(self):
        self.puntaje_label.config(
            text=f"Puntajes: Jugador 1 - {self.jugador1.score} | Jugador 2 - {self.jugador2.score}"
        )
