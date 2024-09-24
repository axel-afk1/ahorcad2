import tkinter as tk
from tkinter import messagebox
import random

# Lista de palabras para el juego, organizadas por dificultad
palabras = {
    "FACIL": [
        "PYTHON", "JUEGO", "VIDA", "SER", "NACIMIENTO", "CASA", "PERRO", "GATO", 
        "SOL", "LUNA", "AGUA", "FUEGO", "TIERRA", "AIRE", "FLOR", "ARBOL", 
        "LIBRO", "MESA", "SILLA", "CAMA", "COCHE", "BICI", "TREN", "AVION", 
        "BARCO", "PLAYA", "MONTE", "RIO", "MAR", "LAGO", "BOSQUE", "CIUDAD"
    ],
    "NORMAL": [
        "PROGRAMACION", "COMPUTADORA", "AHORCADO", "ESPECIE", "REPRODUCCION",
        "TELEFONO", "INTERNET", "TELEVISION", "BIBLIOTECA", "UNIVERSIDAD",
        "RESTAURANTE", "SUPERMERCADO", "GIMNASIO", "HOSPITAL", "AEROPUERTO",
        "ESTACION", "CONCIERTO", "PELICULA", "TEATRO", "MUSEO", "JARDIN",
        "ACUARIO", "ZOOLOGICO", "CASCADA", "VOLCAN", "DESIERTO",
        "SELVA", "PRADERA", "GLACIAR", "OCEANO", "CONTINENTE"
    ],
    "DIFICIL": [
        "ELECTROENCEFALOGRAFISTA", "OTORRINOLARINGOLOGO", "INTERDISCIPLINARIO",
        "INCONMENSURABLE", "EXTRAORDINARIAMENTE", "LEPIDOPTEROFOBIA",
        "ANTIHISTAMINICO", "ARTERIOESCLEROSIS", "DESENHEBRAR", "CIRCUNSCRIPCION",
        "ALEBRESTARSE", "PROCRASTINACION", "ENDOMETRIO", "POLIMETILMETACRILATO",
        "TORTICOLIS", "PARAFRASTICO", "FOTOSINTESIS", "BIOLUMINISCENCIA",
        "PALEONTOLOGIA", "ARQUEOLOGIA", "NANOTECNOLOGIA", "BIOTECNOLOGIA",
        "CRIPTOGRAFIA", "TERMODINAMICA", "EPISTEMOLOGIA", "METAFISICA",
        "ONTOLOGIA", "FENOMENOLOGIA", "HERMENEUTICA", "AXIOLOGIA",
        "PARADIGMA", "IDIOSINCRASIA"
    ]
}

def elegir_palabra(lista_palabras):
    return random.choice(lista_palabras).upper()

class Ahorcado:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Ahorcado")
        self.root.state('zoomed')  # Maximiza la ventana
        self.root.configure(background='#ADD8E6')

        self.custom_font = ('Comic Sans MS', 16)
        self.title_font = ('Comic Sans MS', 32, 'bold')

        self.dificultad = "NORMAL"  # Dificultad por defecto
        self.intentos_por_dificultad = {"FACIL": 8, "NORMAL": 6, "DIFICIL": 4}

        self.pantalla_inicio()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def pantalla_inicio(self):
        self.limpiar_ventana()

        self.main_frame = tk.Frame(self.root, bg='#ADD8E6')
        self.main_frame.pack(expand=True, fill='both')

        titulo_label = tk.Label(self.main_frame, text="Bienvenido al Juego del Ahorcado", font=self.title_font, bg='#ADD8E6')
        titulo_label.pack(pady=40)

        instrucciones = ("Instrucciones:\n"
                         "1. Adivina la palabra letra por letra.\n"
                         "2. Los intentos dependen de la dificultad elegida.\n"
                         "3. Por cada intento fallido, se dibujará una parte del ahorcado.\n"
                         "¡Buena suerte!")

        instrucciones_label = tk.Label(self.main_frame, text=instrucciones, font=self.custom_font, justify=tk.LEFT, bg='#ADD8E6')
        instrucciones_label.pack(pady=40)

        dificultad_frame = tk.Frame(self.main_frame, bg='#ADD8E6')
        dificultad_frame.pack(pady=20)

        tk.Label(dificultad_frame, text="Selecciona la dificultad:", font=self.custom_font, bg='#ADD8E6').pack(side=tk.LEFT, padx=10)

        dificultades = ["FACIL", "NORMAL", "DIFICIL"]
        self.dificultad_var = tk.StringVar(value="NORMAL")
        for dif in dificultades:
            tk.Radiobutton(dificultad_frame, text=dif, variable=self.dificultad_var, value=dif, font=self.custom_font, bg='#ADD8E6').pack(side=tk.LEFT, padx=10)

        comenzar_button = tk.Button(self.main_frame, text="Comenzar", command=self.iniciar_juego, font=self.custom_font, bg="#32CD32", fg="white", padx=20, pady=10)
        comenzar_button.pack(pady=40)

    def iniciar_juego(self):
        self.dificultad = self.dificultad_var.get()
        self.limpiar_ventana()

        self.main_frame = tk.Frame(self.root, bg='#ADD8E6')
        self.main_frame.pack(expand=True, fill='both')

        self.palabra = elegir_palabra(palabras[self.dificultad])
        self.letras_adivinadas = []
        self.intentos = self.intentos_por_dificultad[self.dificultad]
        self.partes_personaje = 0

        game_frame = tk.Frame(self.main_frame, bg='#ADD8E6')
        game_frame.pack(expand=True, fill='both')

        left_frame = tk.Frame(game_frame, bg='#ADD8E6')
        left_frame.pack(side=tk.LEFT, expand=True, fill='both')

        right_frame = tk.Frame(game_frame, bg='#ADD8E6')
        right_frame.pack(side=tk.RIGHT, expand=True, fill='both')

        self.estado_label = tk.Label(left_frame, text=self.mostrar_estado(), font=self.custom_font, bg='#ADD8E6')
        self.estado_label.pack(pady=20)

        self.intento_label = tk.Label(left_frame, text=f"Intentos restantes: {self.intentos}", font=self.custom_font, bg='#ADD8E6')
        self.intento_label.pack(pady=10)

        self.letra_entry = tk.Entry(left_frame, font=self.custom_font)
        self.letra_entry.pack(pady=10)
        self.letra_entry.bind("<Return>", self.verificar_letra)

        self.adivinar_button = tk.Button(left_frame, text="Adivinar", command=self.verificar_letra, font=self.custom_font, bg="#32CD32", fg="white")
        self.adivinar_button.pack(pady=10)

        self.letras_usadas_label = tk.Label(left_frame, text="Letras usadas: ", font=self.custom_font, bg='#ADD8E6')
        self.letras_usadas_label.pack(pady=10)

        self.canvas = tk.Canvas(right_frame, width=400, height=400, bg='#E6E6FA')
        self.canvas.pack(pady=20)
        self.dibujar_estructura()
        self.dibujar_fondo()

        self.crear_teclado_virtual(left_frame)

    def mostrar_estado(self):
        return " ".join([letra if letra in self.letras_adivinadas else "_" for letra in self.palabra])

    def verificar_letra(self, event=None):
        letra = self.letra_entry.get().upper()
        self.letra_entry.delete(0, tk.END)

        if letra in self.letras_adivinadas:
            messagebox.showinfo("Letra repetida", "Ya has intentado con esa letra.")
            return

        self.letras_adivinadas.append(letra)
        self.letras_usadas_label.config(text="Letras usadas: " + " ".join(sorted(self.letras_adivinadas)))

        if letra in self.palabra:
            self.estado_label.config(text=self.mostrar_estado())
            if "_" not in self.mostrar_estado():
                messagebox.showinfo("¡Felicidades!", f"¡Has ganado! La palabra era: {self.palabra}")
                self.reiniciar_juego()
        else:
            self.intentos -= 1
            self.intento_label.config(text=f"Intentos restantes: {self.intentos}")
            self.dibujar_personaje()
            if self.intentos == 0:
                messagebox.showinfo("Fin del juego", f"¡Has perdido! La palabra era: {self.palabra}")
                self.reiniciar_juego()
    def mostrar_mensaje_fin_juego(self, resultado):
        self.limpiar_ventana()
        
        mensaje_frame = tk.Frame(self.root, bg='#ADD8E6')
        mensaje_frame.pack(expand=True, fill='both', pady=50)

        if resultado == "ganado":
            mensaje = "¡Felicidades!"
            submensaje = f"Has adivinado la palabra: {self.palabra}"
            color = "#FFD700"  # Dorado
        else:
            mensaje = "¡Oh no!"
            submensaje = f"Te has quedado sin intentos. La palabra era: {self.palabra}"
            color = "#FF6347"  # Tomate

        tk.Label(mensaje_frame, text=mensaje, font=('Comic Sans MS', 48, 'bold'), bg='#ADD8E6', fg=color).pack(pady=20)
        tk.Label(mensaje_frame, text=submensaje, font=self.custom_font, bg='#ADD8E6').pack(pady=10)

        if resultado == "ganado":
            tk.Label(mensaje_frame, text="🎉🏆🎉", font=('Arial', 72), bg='#ADD8E6').pack(pady=20)

        volver_button = tk.Button(mensaje_frame, text="Volver al Inicio", command=self.pantalla_inicio, font=self.custom_font, bg="#32CD32", fg="white")
        volver_button.pack(pady=20)

    def dibujar_estructura(self):
        self.canvas.create_line(50, 350, 200, 350, width=3)
        self.canvas.create_line(100, 350, 100, 50, width=3)
        self.canvas.create_line(100, 50, 250, 50, width=3)
        self.canvas.create_line(250, 50, 250, 100, width=3)

    def dibujar_fondo(self):
        self.canvas.create_oval(50, 400, 150, 300, fill='green', outline='')
        self.canvas.create_rectangle(0, 350, 400, 400, fill='brown', outline='')

    def dibujar_personaje(self):
        partes = [
            lambda: self.canvas.create_oval(225, 100, 275, 150, width=3),  # Cabeza
            lambda: self.canvas.create_line(250, 150, 250, 250, width=3),  # Cuerpo
            lambda: self.canvas.create_line(250, 180, 220, 220, width=3),  # Brazo izquierdo
            lambda: self.canvas.create_line(250, 180, 280, 220, width=3),  # Brazo derecho
            lambda: self.canvas.create_line(250, 250, 220, 290, width=3),  # Pierna izquierda
            lambda: self.canvas.create_line(250, 250, 280, 290, width=3),  # Pierna derecha
            lambda: self.canvas.create_oval(240, 115, 245, 120, fill='black'),  # Ojo izquierdo
            lambda: self.canvas.create_oval(255, 115, 260, 120, fill='black'),  # Ojo derecho
            lambda: self.canvas.create_arc(235, 125, 265, 145, start=0, extent=-180, width=3)  # Boca triste
        ]
        if self.partes_personaje < len(partes):
            partes[self.partes_personaje]()
            self.partes_personaje += 1

    def crear_teclado_virtual(self, frame):
        teclado_frame = tk.Frame(frame, bg='#ADD8E6')
        teclado_frame.pack(pady=20)

        letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        row = 0
        col = 0
        for letra in letras:
            tk.Button(teclado_frame, text=letra, command=lambda l=letra: self.usar_letra_virtual(l),
                      font=self.custom_font, width=2, height=1).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 9:
                col = 0
                row += 1

    def usar_letra_virtual(self, letra):
        self.letra_entry.delete(0, tk.END)
        self.letra_entry.insert(0, letra)
        self.verificar_letra()

    def reiniciar_juego(self):
        respuesta = messagebox.askyesno("Jugar de nuevo", "¿Quieres jugar otra partida?")
        if respuesta:
            self.pantalla_inicio()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    juego = Ahorcado(root)
    root.mainloop()
    