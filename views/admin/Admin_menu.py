import tkinter as tk
from tkinter import PhotoImage, messagebox, ttk
from tkinter import *
from abc import ABCMeta, abstractmethod
import os, json, csv

class AdminVentana(tk.Tk):
    def __init__(self, parent= None, iconos=None):
        super().__init__()
        self.logo = None
        self._crear_contenido()
        self.title("GIPU - Panel de Administración")

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
        ttk.Label(titulo_frame, text="Panel de Administracion", font=("Arial", 11), foreground="#2a4f80").pack(anchor="w")

        boton = tk.Button(frame, text="Abrir herramientas", font=("Arial", 12))
        boton.pack(pady=20)

class Admin_menu(metaclass=ABCMeta):
    #Idea esto se usara para cuando se inicie por primera vez el administrador tendra que colocar la universidad
    """if not os.path.exists("config\settings.json"):
            Instituto = {
                "Universidad": "Universidad Laica Eloy Alfaro de Manabi"
            }
            with open("settings.json", "w", encoding="utf-8") as archivo:
                json.dump(Instituto, archivo, indent=4)"""
    def Gestionar_inscripciones(self):
        print("Gestionar inscripciones")
        print("Ingrese un periodo: ")
        print("Oferta academica: ")
        print()
    
    def Gestionar_postulaciones(self):
        print("Gestionar postulaciones")
        print("Periodo(ya se puso en las inscripciones): ")
        print("modificar porcentaje de abanderados: ")
        print()
    
    def Gestionar_usuarios(self):
        print("Gestionar usuarios")
        print("Buscar: ")
        print("Suspender cuenta: ")
        print("Eliminar cuenta: ")
        print("Modificar cuenta: ")
        print()
    
    def Gestionar_administradores(self):
        print("Gestionar administradores")
        print("Buscar: ")
        print("Crear administrador: ")
        print("Suspender cuenta: ")
        print("Eliminar cuenta: ")
        print("Modificar cuenta: ")
        print()

menu = Admin_menu()
menu.Gestionar_inscripciones()
menu.Gestionar_postulaciones()
menu.Gestionar_usuarios()
menu.Gestionar_administradores()