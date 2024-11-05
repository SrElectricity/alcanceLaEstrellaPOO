import tkinter as tk
from tkinter import messagebox, colorchooser
from game.game_logic import Game
import random



class GraphicInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Alcanza la Estrella")

        # Lógica del juego
        self.game = Game()
        self.dado = 0
        self.dado_rolling = False
        self.jugador1_nombre = "Jugador 1"
        self.jugador2_nombre = "Jugador 2"
        self.jugador1_color = "red"  # Color predeterminado para Jugador 1
        self.jugador2_color = "blue"  # Color predeterminado para Jugador 2
        self.pregunta_ventana = None
        self.iniciar_btn = None
        self.dado_label = None
        self.tablero_labels = []  # Lista de etiquetas del tablero
        self.puntaje_label = None
        self.jugador1_label = None
        self.jugador2_label = None
        self.jugador1_frame = None
        self.jugador2_frame = None
        self.tablero_frame = None  # Inicializa tablero_frame
        self.temporizador_dado = None  # Inicializa temporizador_dado

        # Crear la interfaz gráfica
        self.crear_interfaz()
        self.actualizar_tablero(inicial=True)  # Colocar ambos jugadores en la casilla inicial solo al inicio

    def crear_interfaz(self):
        # Crear marco principal para contener tablero y barra lateral
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        # Crear barra lateral para instrucciones
        sidebar = tk.Frame(main_frame, width=200, bg="lightgray", padx=10, pady=10)
        sidebar.grid(row=0, column=0, sticky="ns")

        # Mensaje de bienvenida e instrucciones en la barra lateral
        instrucciones = (
            "Bienvenidos a Alcanza la Estrella\n\n"
            "1. Inician en la primera casilla.\n"
            "2. Haz clic en 'Iniciar Juego'.\n"
            "3. Selecciona tu nombre y color.\n"
            "4. Haz clic en 'Guardar'.\n"
            "5. Haz clic en el dado para lanzar.\n\n"
            "Objetivo:\n"
            "Responde bien para avanzar y llegar a la estrella.\n\n"
            "Oh no! Si respondes mal, podrías recibir uno de estos castigos:\n"
            "- Retrocede 2 o 3 casillas.\n"
            "- Vuelve a la casilla 1."
        )
        instrucciones_label = tk.Label(sidebar, text=instrucciones, justify="left", bg="lightgray",
                                       font=("Helvetica", 10))
        instrucciones_label.pack(anchor="nw")

        # Crear tablero visual dentro del marco principal
        self.tablero_frame = tk.Frame(main_frame)
        self.tablero_frame.grid(row=0, column=1, padx=10)

        self.tablero_labels = []
        for i in range(20):
            # Crear casillas numeradas
            label = tk.Label(
                self.tablero_frame,
                text=f"{i + 1}",
                borderwidth=1,
                relief="solid",
                width=3,
                height=2,
                font=("Helvetica", 12)
            )
            label.grid(row=i // 5, column=i % 5)
            self.tablero_labels.append(label)

        # Agregar la estrella justo a la derecha de la última casilla (20) en la misma fila
        estrella_label = tk.Label(self.tablero_frame, text="⭐", font=("Helvetica", 16), fg="gold")
        estrella_label.grid(row=3, column=5)  # Columna 5 es justo después de la columna de la casilla 20

        # Botón para iniciar el juego
        self.iniciar_btn = tk.Button(self.root, text="Iniciar Juego", command=self.iniciar_juego)
        self.iniciar_btn.pack(pady=10)

        # Dado
        self.dado_label = tk.Label(self.root, text="🎲", font=("Helvetica", 32))
        self.dado_label.pack(pady=10)
        # Desactivar el clic en el dado hasta que se haga clic en "Iniciar Juego"
        self.dado_label.bind("<Button-1>", lambda event: None)  # Desactiva el clic en el dado temporalmente

        # Mostrar cuadro de color para Jugador 1 sin modificar el color del texto
        self.jugador1_frame = tk.Frame(self.root, bg=self.jugador1_color, width=20, height=20)
        self.jugador1_frame.pack(pady=5, padx=5, side=tk.LEFT)
        self.jugador1_label = tk.Label(self.root, text=self.jugador1_nombre, fg="black")  # Color negro para el texto
        self.jugador1_label.pack(side=tk.LEFT)

        # Mostrar cuadro de color para Jugador 2 sin modificar el color del texto
        self.jugador2_frame = tk.Frame(self.root, bg=self.jugador2_color, width=20, height=20)
        self.jugador2_frame.pack(pady=5, padx=5, side=tk.LEFT)
        self.jugador2_label = tk.Label(self.root, text=self.jugador2_nombre, fg="black")  # Color negro para el texto
        self.jugador2_label.pack(side=tk.LEFT)

        # Puntaje
        self.puntaje_label = tk.Label(self.root,
                                      text=f"Puntajes: {self.jugador1_nombre} - 0 | {self.jugador2_nombre} - 0")
        self.puntaje_label.pack()

    def iniciar_juego(self):
        # Activar el clic en el dado una vez iniciado el juego
        self.dado_label.bind("<Button-1>", self.iniciar_animacion_dado)

        # Crear una ventana de diálogo personalizada para solicitar ambos nombres y colores
        dialog = tk.Toplevel(self.root)
        dialog.title("Nombres y Colores de los Jugadores")

        # Nombre y color del Jugador 1
        tk.Label(dialog, text="Nombre del Jugador 1:").grid(row=0, column=0, padx=10, pady=5)
        jugador1_entry = tk.Entry(dialog)
        jugador1_entry.grid(row=0, column=1, padx=10, pady=5)

        # Botón para seleccionar color del Jugador 1
        def seleccionar_color_jugador1():
            color = colorchooser.askcolor(title="Seleccione el color del Jugador 1")[1]
            if color:
                self.jugador1_color = color  # Guardamos el color seleccionado
                jugador1_color_btn.config(bg=color)

        jugador1_color_btn = tk.Button(dialog, text="Color", command=seleccionar_color_jugador1)
        jugador1_color_btn.grid(row=0, column=2, padx=5)

        # Nombre y color del Jugador 2
        tk.Label(dialog, text="Nombre del Jugador 2:").grid(row=1, column=0, padx=10, pady=5)
        jugador2_entry = tk.Entry(dialog)
        jugador2_entry.grid(row=1, column=1, padx=10, pady=5)

        # Botón para seleccionar color del Jugador 2
        def seleccionar_color_jugador2():
            color = colorchooser.askcolor(title="Seleccione el color del Jugador 2")[1]
            if color:
                self.jugador2_color = color  # Guardamos el color seleccionado
                jugador2_color_btn.config(bg=color)

        jugador2_color_btn = tk.Button(dialog, text="Color", command=seleccionar_color_jugador2)
        jugador2_color_btn.grid(row=1, column=2, padx=5)

        # Función para guardar nombres y colores seleccionados
        def guardar_nombres_y_colores():
            # Asigna los nombres seleccionados o usa valores por defecto
            self.jugador1_nombre = jugador1_entry.get() or "Jugador 1"
            self.jugador2_nombre = jugador2_entry.get() or "Jugador 2"
            self.jugador1_color = getattr(self, 'jugador1_color', 'red')  # Color por defecto: rojo
            self.jugador2_color = getattr(self, 'jugador2_color', 'blue')  # Color por defecto: azul
            dialog.destroy()

            # Actualizar el texto y color de los cuadros junto a los nombres
            self.jugador1_frame.config(bg=self.jugador1_color)
            self.jugador1_label.config(text=self.jugador1_nombre, fg="black")

            self.jugador2_frame.config(bg=self.jugador2_color)
            self.jugador2_label.config(text=self.jugador2_nombre, fg="black")

            # Actualizar la etiqueta del puntaje con los nombres ingresados
            self.actualizar_puntaje()

            # Desactivar el botón de inicio una vez comenzado el juego
            self.iniciar_btn.config(state=tk.DISABLED)
            self.actualizar_tablero()

        # Botón para guardar los nombres y colores
        guardar_btn = tk.Button(dialog, text="Guardar", command=guardar_nombres_y_colores)
        guardar_btn.grid(row=2, column=0, columnspan=3, pady=10)

        dialog.grab_set()
        self.root.wait_window(dialog)

    def iniciar_animacion_dado(self, event=None):
        print("iniciar_animacion_dado fue llamado")  # Mensaje de depuración

        if not self.dado_rolling and not self.game.game_over:
            self.dado_rolling = True
            self.temporizador_dado = 1500  # Duración de la animación en milisegundos
            print("Animación de dado comenzada")  # Mensaje de depuración
            self.animar_dado()

    def animar_dado(self):
        if self.dado_rolling and self.temporizador_dado > 0:
            self.dado = random.randint(1, 6)
            self.dado_label.config(text=str(self.dado))
            self.temporizador_dado -= 100
            self.root.after(100, self.animar_dado)
        else:
            self.detener_animacion_dado()

    def detener_animacion_dado(self):
        self.dado_rolling = False
        jugador_actual = self.jugador1_nombre if self.game.current_player == 0 else self.jugador2_nombre
        messagebox.showinfo("Dado", f"{jugador_actual} lanzó un {self.dado}")
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        # Llama a obtener_pregunta en Game para obtener una pregunta dinámica
        pregunta_texto, opciones, respuesta_correcta = self.game.obtener_pregunta(
            dificultad="easy")  # o "medium", "hard" según se desee

        # Verifica si se obtuvo una pregunta válida
        if not pregunta_texto:
            messagebox.showinfo("Juego terminado", "No hay más preguntas disponibles.")
            self.declarar_ganador_por_puntaje()
            return

        # Abre una ventana para mostrar la pregunta y las opciones
        self.pregunta_ventana = tk.Toplevel(self.root)
        self.pregunta_ventana.title("Pregunta")

        # Mostrar la pregunta
        tk.Label(self.pregunta_ventana, text=pregunta_texto).pack(pady=10)

        # Crear botones para cada opción
        for opcion in opciones:
            tk.Button(
                self.pregunta_ventana,
                text=opcion,
                command=lambda seleccion=opcion: self.verificar_respuesta(seleccion, respuesta_correcta)
            ).pack(pady=2)

    def verificar_respuesta(self, seleccion, respuesta_correcta):
        # Cierra la ventana de la pregunta
        self.pregunta_ventana.destroy()

        # Llamada a check_answer en Game
        correcta = self.game.check_answer(seleccion, respuesta_correcta)
        print(f"Respuesta seleccionada: {seleccion}, Respuesta correcta: {respuesta_correcta}")  # Depuración

        # Muestra el resultado al jugador
        messagebox.showinfo("Resultado", "¡Respuesta correcta!" if correcta else "Respuesta incorrecta.")

        if correcta:
            self.game.move_player(self.dado)
            self.actualizar_puntaje()  # Actualiza el puntaje en la interfaz
        else:
            castigo = self.game.apply_penalty()
            messagebox.showinfo("Castigo", castigo)

        self.actualizar_tablero()

        if self.game.player_positions[self.game.current_player] == 19:
            self.game.game_over = True
            ganador = self.jugador1_nombre if self.game.current_player == 0 else self.jugador2_nombre
            messagebox.showinfo("Juego terminado", f"¡{ganador} ha ganado!")
        else:
            self.game.switch_player()

    def actualizar_tablero(self, inicial=False):
        for i, label in enumerate(self.tablero_labels):
            label.config(bg="SystemButtonFace", text=str(i + 1))  # Resetea el color y el texto de cada casilla

        # Establecer las posiciones solo al inicio
        if inicial:
            self.game.player_positions = [0, 0]

        pos_jug1 = self.game.player_positions[0]
        pos_jug2 = self.game.player_positions[1]

        # Mostrar las iniciales de los jugadores con sus colores respectivos
        inicial_jug1 = self.jugador1_nombre[0].upper() if self.jugador1_nombre else "1"
        inicial_jug2 = self.jugador2_nombre[0].upper() if self.jugador2_nombre else "2"

        if pos_jug1 == pos_jug2 and pos_jug1 < 20:
            # Si ambos jugadores están en la misma casilla
            self.tablero_labels[pos_jug1].config(bg="purple", text=f"{inicial_jug1}&{inicial_jug2}")
        else:
            # Casilla para el jugador 1
            if pos_jug1 < 20:
                self.tablero_labels[pos_jug1].config(bg=self.jugador1_color, text=inicial_jug1)
            # Casilla para el jugador 2
            if pos_jug2 < 20:
                self.tablero_labels[pos_jug2].config(bg=self.jugador2_color, text=inicial_jug2)

    def actualizar_puntaje(self):
        # Actualiza la etiqueta de puntaje para reflejar los puntajes actuales de ambos jugadores
        self.puntaje_label.config(
            text=f"Puntajes: {self.jugador1_nombre} - {self.game.player_scores[0]} | {self.jugador2_nombre} - {self.game.player_scores[1]}"
        )

    def declarar_ganador_por_puntaje(self):
        ganador_index = self.game.get_winner()
        if ganador_index is None:
            messagebox.showinfo("Juego terminado", "¡Es un empate!")
        else:
            ganador = self.jugador1_nombre if ganador_index == 0 else self.jugador2_nombre
            color = "red" if ganador_index == 0 else "blue"
            for label in self.tablero_labels:
                label.config(bg=color)
            messagebox.showinfo("Juego terminado", f"¡{ganador} ha ganado por puntaje!")
        self.game.game_over = True
