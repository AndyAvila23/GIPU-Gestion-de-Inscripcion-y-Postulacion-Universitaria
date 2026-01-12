import tkinter as tk
from tkinter import PhotoImage, messagebox, ttk
from tkinter import *
from views.Iniciar_Sesion import inicio_sesion
import os

class menu_inicio(tk.Tk):
    def __init__(self, iconos=None):
        super().__init__()
        self.logo = None
        self._crear_contenido()
        self.title("GIPU - Gestión de Inscripción y Postulación Universitaria")

        # Dimensiones centradas en pantalla
        self.ancho = 900
        self.alto = 600
        self._centrar_ventana()

        # Fondo y estilos generales
        self.config(bg="#f0f0f0")
        self._configurar_estilos()

    # ─────────────────────────────
    # Posicionar ventana
    # ─────────────────────────────
    def _centrar_ventana(self):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho - self.ancho) // 2
        y = (pantalla_alto - self.alto) // 2
        self.geometry(f"{self.ancho}x{self.alto}+{x}+{y}")

    # ─────────────────────────────
    # Configuracion de estilos base
    # ─────────────────────────────
    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TButton", font=("Arial", 11), padding=5, background="#cca14c")
        estilo.configure("TLabel", font=("Arial", 11), background = "#ffffff")
        estilo.configure("TFrame", background="#ffffff")
        self.attributes("-fullscreen", False)
        self.attributes("-topmost", False)
        self.resizable(False, False)

    def _crear_contenido(self):
        # Frame principal
        frame = ttk.Frame(self, padding=30)
        frame.pack(expand=True, fill="both")

        # ─────────────────────────────
        # ENCABEZADO
        # ─────────────────────────────
        header = ttk.Frame(frame)
        header.pack(fill="x", pady=10)

        # Cargar logo
        logo_path = os.path.join("assets", "img", "Logo_GIPU.png")
        if os.path.exists(logo_path):
            self.logo = PhotoImage(file=logo_path)
            self.logo = self.logo.subsample(7, 7)
            logo_label = ttk.Label(header, image=self.logo)
        logo_label.pack(side="left", padx=(10, 15))

        # Título del sistema
        titulo_frame = ttk.Frame(header)
        titulo_frame.pack(side="left", anchor="center", pady=10)
        ttk.Label(titulo_frame, text="GIPU", font=("Arial", 18, "bold"), foreground="#2a4f80").pack(anchor="w")
        ttk.Label(titulo_frame, text="Gestión de Inscripción y Postulación Universitaria", font=("Arial", 11), foreground="#2a4f80").pack(anchor="w")

        # Botones de acción (Registrarse / Iniciar Sesión)
        botones_frame = ttk.Frame(header)
        botones_frame.pack(side="right", padx=10)
        ttk.Button(botones_frame, text="Iniciar Sesión", width=15, command=self._iniciar_sesion).pack(side="left", padx=15)
        # ─────────────────────────────
        # CUERPO PRINCIPAL
        # ─────────────────────────────
        contenido = ttk.Frame(frame, padding=(30, 40))
        contenido.pack(expand=True, fill="both")

        # Sección de bienvenida
        ttk.Label(contenido, text="Bienvenido!!", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
        ttk.Label(
            contenido,
            text=("Te damos la bienvenida al sistema de Gestión de Inscripción y Postulación Universitaria.\n"
                  "Ingresa en nuestro sitio para que puedas hacer tus respectivos pasos\n"
                  "para sostener tu cupo universitario."),
            font=("Arial", 11), justify="left", wraplength=700
        ).pack(anchor="w", pady=(0, 30))

        # Sección de “Acerca de”
        ttk.Label(contenido, text="Acerca de:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))
        ttk.Label(
            contenido,
            text=("Este sistema tiene como fin ayudar a las universidades a gestionar de manera eficiente\n"
                  "sus inscripciones y postulaciones de manera correcta."),
            font=("Arial", 11), justify="left", wraplength=700
        ).pack(anchor="w", pady=(0, 20))

    # ─────────────────────────────
    # MÉTODOS DE ACCIÓN
    # ─────────────────────────────

    def _iniciar_sesion(self):
        inicio_sesion(self)

    # ─────────────────────────────
    # Abrir la ventana
    # ─────────────────────────────
    def run(self):
        #Inicia el loop principal.
        self.mainloop()
