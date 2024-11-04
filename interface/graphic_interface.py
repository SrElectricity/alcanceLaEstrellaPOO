import tkinter as tk
from tkinter import messagebox


class AlcanzaLaEstrella:
    def __init__(self, root):
        self.root = root
        self.root.title("Alcanza la Estrella")

        # Configuración del tablero y posiciones
        self.tablero = [" "] * 20
        self.posiciones_jugadores = [0, 0]
        self.puntajes = [0, 0]
        self.turno = 0

        # Crear interfaz gráfica
        self.crear_interfaz()

    def crear_interfaz(self):
        # Crear tablero visual
        self.tablero_frame = tk.Frame(self.root)
        self.tablero_frame.pack(pady=10)

        self.tablero_labels = []
        for i in range(20):
            label = tk.Label(self.tablero_frame, text=f"{i + 1}", borderwidth=1, relief="solid", width=3, height=2)
            label.grid(row=i // 5, column=i % 5)
            self.tablero_labels.append(label)

        # Botón para lanzar dado
        self.lanzar_btn = tk.Button(self.root, text="Lanzar Dado", command=self.lanzar_dado)
        self.lanzar_btn.pack(pady=10)

        # Mostrar puntaje
        self.puntaje_label = tk.Label(self.root, text="Puntajes: Jugador 1 - 0 | Jugador 2 - 0")
        self.puntaje_label.pack()

    def lanzar_dado(self):
        import random
        dado = random.randint(1, 6)
        jugador = self.turno + 1
        messagebox.showinfo("Dado", f"Jugador {jugador} lanzó un {dado}")

        # Actualizar posición del jugador
        self.posiciones_jugadores[self.turno] += dado
        if self.posiciones_jugadores[self.turno] >= 20:
            self.posiciones_jugadores[self.turno] = 19  # Limitar al final del tablero

        # Pregunta de trivia
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        pregunta, opciones, respuesta_correcta = self.obtener_pregunta()
        self.pregunta_ventana = tk.Toplevel(self.root)
        self.pregunta_ventana.title("Pregunta")

        pregunta_label = tk.Label(self.pregunta_ventana, text=pregunta)
        pregunta_label.pack(pady=10)

        # Crear botones para opciones
        for idx, opcion in enumerate(opciones):
            boton_opcion = tk.Button(self.pregunta_ventana, text=opcion,
                                     command=lambda idx=idx: self.verificar_respuesta(idx, respuesta_correcta))
            boton_opcion.pack(pady=2)

    def verificar_respuesta(self, seleccion, respuesta_correcta):
        self.pregunta_ventana.destroy()

        if seleccion == respuesta_correcta:
            self.puntajes[self.turno] += 1
            messagebox.showinfo("Resultado", "¡Respuesta correcta!")
        else:
            messagebox.showinfo("Resultado", "Respuesta incorrecta.")

        # Actualizar tablero visual y puntajes
        self.actualizar_tablero()

        # Cambiar turno
        self.turno = 1 - self.turno  # Alternar entre 0 y 1
        self.puntaje_label.config(text=f"Puntajes: Jugador 1 - {self.puntajes[0]} | Jugador 2 - {self.puntajes[1]}")

    def actualizar_tablero(self):
        # Actualizar las posiciones de los jugadores en el tablero visual
        for i, label in enumerate(self.tablero_labels):
            label.config(text=str(i + 1), bg="SystemButtonFace")  # Resetear color

        for i, pos in enumerate(self.posiciones_jugadores):
            self.tablero_labels[pos].config(bg="red" if i == 0 else "blue")  # Colorear posiciones de jugadores

    def obtener_pregunta(self):
        # Ejemplo de pregunta, podrías modificarlo para obtener aleatorias
        pregunta = "¿Qué es H2O?"
        opciones = ["a) Agua", "b) Oxígeno", "c) Hidrógeno"]
        respuesta_correcta = 0  # Índice de la respuesta correcta
        return pregunta, opciones, respuesta_correcta


# Ejecutar la interfaz gráfica
root = tk.Tk()
app = AlcanzaLaEstrella(root)
root.mainloop()
